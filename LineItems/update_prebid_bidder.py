"""Initializes a AdManagerClient using a Service Account."""

# Import necessary libraries
import sys
import locale
from googleads import ad_manager, errors
import constants
from pick import pick

locale.getdefaultlocale = lambda *args: ["de_DE", "UTF-8"]


option_title = 'Please choose an action: \n(Use Arrow-Keys to choose and confirm with ENTER):'
OPTION = pick(['add', 'remove'], option_title, min_selection_count=1)


safeframe_title = 'Select which Line Items to update: \n(Use Arrow-Keys to choose and confirm with ENTER):'
SEARCH_KEY = pick(['Safeframe', 'Non-Safeframe'], safeframe_title, min_selection_count=1)


#SEARCH_KEY = input("Safeframe? 'j' or 'n' or 'c' (Custom): ")

# TODO: Liste aller hb_bidder values pullen und als selection verfügbar machen
# TODO: CommonError.CONCURRENT_MODIFICATION -> Retry-Logik implementieren



BIDDER_ID = input('Please insert the value-id for the hb_bidder:')
# stroeerCore   448734789836
# triplelift    448925755227
# connectad     448934363496
# adnuntius     448560253337



def main(client, option, search_key, bidder_id):

    # Initialize Line Item Service
    print("Initializing LineItemService")
    print("option: ", option)
    print("key: ", search_key)
    service = client.GetService("LineItemService", version=constants.API_VERSION)
       
    if search_key == "Safeframe":
        print("Safe :)")
        search_key = constants.SAFEFRAME
    if search_key == "Non-Safeframe":
        print("No Safe :(")
        search_key = constants.NON_SAFEFRAME

    
    print(option)
    if option == 'add':
        print("add bidderID: ", bidder_id)
        
        # Get List of all Line Items as an array
        line_item_ids = get_line_items(service, search_key)
        print (line_item_ids)

        # TEST
        #add_hb_bidder(service, ["6163684505"], "448734789836")

        # update selected Line Item hb_bidder:
        add_hb_bidder(service, line_item_ids, bidder_id)
    else: 
        print(option)



    if option == "remove":
        print("delete")
        print("remove bidderID: ", bidder_id)
        line_item_ids = get_line_items(service, search_key)

        delete = input("do you want to remove the Bidder from these line Items? ('y' or 'n'): ")
        if (delete == "y"):
            remove_hb_bidder(service, line_item_ids, bidder_id)
        else: 
            return

    else:
        return



# Returns an array of Line Item Ids
def get_line_items(line_item_service, search_key):
    print("gracias, retrieving line items now...")
    statement = (
        ad_manager.StatementBuilder(version=constants.API_VERSION)
        .Where(("name LIKE :name"))
        .WithBindVariable("name", search_key)
        #.Limit(100)
    )

    found_line_items = []
    #counter = 0
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
                #counter += 1
                #if counter % statement.limit == 0:
                #    print("#", counter)
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
            ad_manager.StatementBuilder(version=constants.API_VERSION)
            .Where("id = :id")
            .WithBindVariable("id", int(id))
        )

        response = line_item_service.getLineItemsByStatement(statement.ToStatement())
        if "results" in response and len(response["results"]):
            # Update each local line item by changing its delivery rate type.
            updated_line_items = []

            for line_item in response["results"]:
                if not line_item["isArchived"]:

                    targeting = line_item["targeting"].customTargeting.children[0].children[1].valueIds
                    if int(bidder_id) not in targeting:
                        print("updating: ", line_item['id'])
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
                        line_item["targeting"].customTargeting.children[0].children[1].valueIds = hb_bidders

                        updated_line_items.append(line_item)
                    else:
                        print("already existing - skip")
                    items_left -= 1
                    print("items left %s" % items_left)

            # update Line Item
            result = line_item_service.updateLineItems(updated_line_items)

        else:
            print("No line items found to update.")


# Removes value from hb_bidder-targeting
def remove_hb_bidder(line_item_service, line_item_ids, bidder_id):
    print("--- ____ --- REMOVE --- ___ ---")
    items_left = len(line_item_ids)
    for id in line_item_ids:
        statement = (
            ad_manager.StatementBuilder(version=constants.API_VERSION)
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
                hb_bidders = (  line_item["targeting"].customTargeting.children[0].children[1].valueIds)

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
                    line_item["targeting"].customTargeting.children[0].children[1].valueIds = updated_ids

                    updated_line_items.append(line_item)

            # update Line Item
            try:
                line_item_service.updateLineItems(updated_line_items)
                items_left -= 1
            except errors.GoogleAdsError as error:
                print("An error occurred: ", error)
            
            print("items left %s" % items_left)
        else:
            print("No line items found to update.")


if __name__ == "__main__":
    client = ad_manager.AdManagerClient.LoadFromStorage()
    main(client, OPTION[0], SEARCH_KEY[0], BIDDER_ID)
