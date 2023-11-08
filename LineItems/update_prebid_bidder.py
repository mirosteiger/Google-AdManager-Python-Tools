"""Initializes a AdManagerClient using a Service Account."""

# Import necessary libraries
from datetime import datetime
from datetime import timedelta
import sys

import pytz

sys.path.append("../")
import locale
from googleads import ad_manager, errors
import config
from pick import pick
from Utils.json_tools import read_from_json, get_field
from data.targeting_keys import targeting_keys

locale.getdefaultlocale = lambda *args: ["de_DE", "UTF-8"]


option_title = (
    "Please choose an action: \n(Use Arrow-Keys to choose and confirm with ENTER):"
)
OPTION = pick(["add", "remove"], option_title, min_selection_count=1)


safeframe_title = "Select which Line Items to update: \n(Use Arrow-Keys to choose and confirm with ENTER):"
SEARCH_KEY = pick(
    ["Safeframe", "Non-Safeframe"], safeframe_title, min_selection_count=1
)


# SEARCH_KEY = input("Safeframe? 'j' or 'n' or 'c' (Custom): ")

# TODO: Liste aller hb_bidder values pullen und als selection verfügbar machen
# TODO: CommonError.CONCURRENT_MODIFICATION -> Retry-Logik implementieren


# all bidders (name + id)
bidder_data = read_from_json("../data/hb_bidders.json")

# extract bidder names to array
bidder_codes = get_field(bidder_data, "name")

# terminal prompt
bidder_text = "Please select the hb_bidder you want to " + str(OPTION)
BIDDER_ID = pick(bidder_codes, bidder_text, min_selection_count=1)
print(BIDDER_ID[0])

# get the specific id
BIDDER_ID = get_field(bidder_data, "id", filterBy=BIDDER_ID[0])


def main(client, option, search_key, bidder_id):
    # Initialize Line Item Service
    print("Initializing LineItemService")
    print("option: ", option)
    print("key: ", search_key)
    service = client.GetService("LineItemService", version=config.API_VERSION)

    if search_key == "Safeframe":
        search_key = config.SAFEFRAME
        print(search_key)
    if search_key == "Non-Safeframe":
        search_key = config.NON_SAFEFRAME
        print(search_key)

    print(option)
    if option == "add":
        print("add bidderID: ", bidder_id)

        # Get List of all Line Items as an array
        line_item_ids = get_line_items(service, search_key)
        print(line_item_ids)

        # TEST
        # add_hb_bidder(service, ["6163684505"], "448734789836")

        # update selected Line Item hb_bidder:
        add_hb_bidder(service, line_item_ids, bidder_id)
    else:
        print(option)

    if option == "remove":
        print("remove bidderID: ", bidder_id)
        line_item_ids = get_line_items(service, search_key)

        delete = input(
            "do you want to remove the Bidder from these line Items? ('y' or 'n'): "
        )
        if delete == "y":
            remove_hb_bidder(service, line_item_ids, bidder_id)
        else:
            return

    else:
        return


# Returns an array of Line Item Ids
def get_line_items(line_item_service, search_key):
    print("gracias, retrieving line items now...")

    last_modified = datetime.now(tz=pytz.timezone("Europe/Berlin")) - timedelta(hours=8)

    statement = (
        ad_manager.StatementBuilder(version=config.API_VERSION)
        .Where(
            (
                "name LIKE :name"
                # AND lastModifiedDateTime >= :lastModifiedDateTime "
            )
        )
        .WithBindVariable("name", search_key)
        # .WithBindVariable("lastModifiedDateTime", last_modified)
        .Limit(100)
    )

    found_line_items = []
    # counter = 0
    while True:
        response = line_item_service.getLineItemsByStatement(statement.ToStatement())
        if "results" in response and len(response["results"]):
            for line_item in response["results"]:
                # Print out some information for each line item.
                print(
                    'Line item with ID "%d" and name "%s" was found.\n'
                    % (line_item["id"], line_item["name"])
                )

                found_line_items.append(line_item["id"])
            statement.offset += statement.limit

        else:
            break

    print("\nNumber of results found: %s" % response["totalResultSetSize"])
    return found_line_items


# Adds value to hb_bidder-targeting
def add_hb_bidder(line_item_service, line_item_ids, bidder_id):
    items_left = len(line_item_ids)
    print("updating Line Items, please wait...")

    for id in line_item_ids:
        statement = (
            ad_manager.StatementBuilder(version=config.API_VERSION)
            .Where("id = :id")
            .WithBindVariable("id", int(id))
        )

        response = line_item_service.getLineItemsByStatement(statement.ToStatement())
        if "results" in response and len(response["results"]):
            # Update each local line item by changing its delivery rate type.
            updated_line_items = []

            for line_item in response["results"]:
                if not line_item["isArchived"]:
                    targeting = (
                        line_item["targeting"]
                        .customTargeting.children[0]
                        .children[1]
                        .valueIds
                    )
                    if int(bidder_id) not in targeting:
                        print("updating: ", line_item["id"])
                        # save values
                        hb_bidders = (
                            line_item["targeting"]
                            .customTargeting.children[0]
                            .children[1]
                            .valueIds
                        )
                        # append new bidder-id
                        hb_bidders.append(bidder_id)

                        # overwrite old id-list
                        line_item["targeting"].customTargeting.children[0].children[
                            1
                        ].valueIds = hb_bidders

                        updated_line_items.append(line_item)
                    else:
                        print("already existing - skip")
                    items_left -= 1
                    print("items left %s" % items_left)

            # update Line Item
            try:
                line_item_service.updateLineItems(updated_line_items)
                items_left -= 1
            except errors.GoogleAdsError as error:
                print("An error occurred: ", error)
                print("line item: ", updated_line_items["id"])

        else:
            print("No line items found to update.")


# Removes value from hb_bidder-targeting
def remove_hb_bidder(line_item_service, line_item_ids, bidder_id):
    print("--- ____ --- REMOVE --- ___ ---")
    items_left = len(line_item_ids)
    for id in line_item_ids:
        statement = (
            ad_manager.StatementBuilder(version=config.API_VERSION)
            .Where("id = :id")
            .WithBindVariable("id", int(id))
        )

        response = line_item_service.getLineItemsByStatement(statement.ToStatement())

        if "results" in response and len(response["results"]):
            # Update each local line item by changing its delivery rate type.
            updated_line_items = []
            updated_ids = []

            for line_item in response["results"]:
                # if not line_item["isArchived"]:
                # save values
                hb_bidders = (
                    line_item["targeting"]
                    .customTargeting.children[0]
                    .children[1]
                    .valueIds
                )

                if int(bidder_id) not in hb_bidders:
                    print("skip")
                else:
                    # remove selected bidder-id from list
                    for id in hb_bidders:
                        if int(id) == int(bidder_id):
                            print("removed id ", bidder_id, " from list of bidders")
                        else:
                            updated_ids.append(id)

                    # overwrite old id-list
                    line_item["targeting"].customTargeting.children[0].children[
                        1
                    ].valueIds = updated_ids

                    updated_line_items.append(line_item)

            # update Line Item
            try:
                line_item_service.updateLineItems(updated_line_items)
                items_left -= 1
            except errors.GoogleAdsError as error:
                print("An error occurred: ", error)
                print("line item: ", updated_line_items["id"])

            print("items left %s" % items_left)
        else:
            print("No line items found to update.")


if __name__ == "__main__":
    client = ad_manager.AdManagerClient.LoadFromStorage()
    main(client, OPTION[0], SEARCH_KEY[0], BIDDER_ID)
