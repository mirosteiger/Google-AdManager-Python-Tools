"""Initializes a AdManagerClient using a Service Account."""

# Import necessary libraries
from datetime import datetime, timedelta
import sys

sys.path.append("../")
from googleads import ad_manager, errors
import config
from pick import pick
from Utils.json_tools import read_from_json, get_field
from Utils.get_custom_targeting import get_values_by_id, get_values_by_key

prebid_title = "Do you want to edit the viewability-targetings on all Prebid Line Items (Including Safeframe and Non-Safeframe)?"
search_string = pick(["Yes", "No", "test"], prebid_title)

options_title = "Do you want to add or remove targeting-values?"
OPTION = pick(["Add", "Remove"], options_title)

operator_title = "Do you want to include or exclude the seleted targeting-keys?"
OPERATOR = pick(["Include", "Exclude"], operator_title)

print(OPERATOR)
if OPERATOR[1] == 0:
    OPERATOR = "IS"
if OPERATOR[1] == 1:
    OPERATOR = "IS_NOT"

# all targeting-keys (name + id)
targeting_data = read_from_json("../data/targeting_keys.json")
# extract key name to array
targeting_names = get_field(targeting_data, "name")

key_seletion_title = "Which custom key-value targeting would you like to " + str(
    OPTION[0]
)
KEY_SELECTION = pick(targeting_names, key_seletion_title, min_selection_count=1)

KEY_ID = get_field(targeting_data, "id")[KEY_SELECTION[1]]


def main(client, search_string, key_selection, operator):
    print("\n -----------")
    VALUES = get_values_by_id(client, key_id=key_selection)
    # value_names = get_field(VALUES, "name")
    value_selection_title = (
        "Which values to " + str(OPTION[0]) + "\n (select values with your SPACE-KEY)"
    )
    VALUE_SELECTION = pick(
        VALUES, value_selection_title, multiselect=True, min_selection_count=1
    )

    # Initialize Line Item Service
    print("Initializing LineItemService")
    service = client.GetService("LineItemService", version=config.API_VERSION)

    t = create_custom_targeting(
        keyId=key_selection, valueIds=VALUE_SELECTION, operator=operator
    )

    line_item_ids = []

    if search_string == "Yes":
        KEY = config.PREBID_ALL
        get_line_items(service, KEY)

    if search_string == "test":
        KEY = "Miro_Prebid Test"
        line_item_ids = get_line_items(service, KEY)

    if search_string == "No":
        search_string = ""
        return

    confirm_text = (
        "Do you want to add the following targeting to all eligible line items? \n"
        + str(t)
    )
    CONFIRM = pick(["continue", "abort"], confirm_text)

    if CONFIRM[1] == 0:
        update_custom_targeting(service, line_item_ids, t)
    else:
        return


def create_custom_targeting(keyId="", valueIds=[], operator=""):
    print("\n ----------- \n ")
    values = []
    for entry in valueIds:
        values.append(int(entry[0]["id"]))


    print("creating a new targeting object with the following IDs:")
    print(values)

    t = {"keyId": int(keyId), "valueIds": values, "operator": operator}

    print("new targeting object: ")
    print(t)
    return t


# Returns an array of Line Item Ids
def get_line_items(line_item_service, search_string):
    print("\n -----------")
    print("collecting line items...")
    # last_modified = datetime.now(tz=pytz.timezone("Europe/Berlin")) - timedelta(hours=8)
    statement = (
        ad_manager.StatementBuilder(version=config.API_VERSION)
        .Where(
            (
                "name LIKE :name"
                #   AND lastModifiedDateTime >= :lastModifiedDateTime "
            )
        )
        .WithBindVariable("name", search_string)
        # .WithBindVariable("lastModifiedDateTime", last_modified)
        .Limit(1)
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
                # print(
                #     "The line item has the following custom targeting: %s"
                #     % (
                #         line_item["targeting"]["customTargeting"]["children"][0][
                #             "children"
                #         ]
                #     )
                # )

                found_line_items.append(line_item["id"])
            statement.offset += statement.limit

        else:
            break

    print("\nNumber of results found: %s" % response["totalResultSetSize"])
    return found_line_items


def update_custom_targeting(line_item_service, line_item_ids, new_targeting):
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
            updated_line_items = []

            for line_item in response["results"]:
                targeting_index = -1

                if not line_item["isArchived"]:
                    current_targeting = line_item["targeting"]["customTargeting"][
                        "children"
                    ][0]["children"]
                    print("current targeting: ")
                    print(current_targeting)

                    # check if key already exists in line item targeting:
                    targeting_index = key_exists(
                        new_targeting["keyId"],
                        current_targeting=current_targeting,
                        new_targeting=new_targeting,
                    )

                    print("index: " + str(targeting_index))

                    # adding values to existing key at index i
                    if targeting_index > -1:
                        print("Adding missing values to array.")
                        for id in new_targeting["valueIds"]:
                            if id not in current_targeting[targeting_index]:
                                current_targeting[targeting_index]["valueIds"].append(
                                    id
                                )

                    # adding key and values to targeting      
                    if targeting_index < 0:
                        print("Adding new targeting key with values to targeting")
   
   
                        # Adding 'logicalOperator': 'AND'
                        line_item["targeting"]["customTargeting"]["children"][0][
                            "logicalOperator"
                        ] = "AND"

                        #Adding key-values
                        current_targeting.append(new_targeting)



                    # TODO: original targeting updaten.
                    line_item["targeting"]["customTargeting"]["children"][0][
                        "children"
                    ] = current_targeting



                    # TODO: line item mit neuem targeting zu array hinzufügen
                    updated_line_items.append(line_item)

                    print(line_item["targeting"]["customTargeting"])

            # update Line Item
            try:
                line_item_service.updateLineItems(updated_line_items)
                items_left -= 1
            except errors.GoogleAdsError as error:
                print("An error occurred: ", error)
                print("line item: ", updated_line_items["id"])

        else:
            print("No line items found to update.")


def key_exists(key, current_targeting, new_targeting):
    targeting_index = -1
    for i, key in enumerate(current_targeting):
        if key["keyId"] == new_targeting["keyId"]:
            print(key["keyId"])
            print(new_targeting["keyId"])
            print("targeting key already existing in line item.")
            targeting_index = i

    return targeting_index


if __name__ == "__main__":
    client = ad_manager.AdManagerClient.LoadFromStorage()
    main(client, search_string[0], KEY_ID, OPERATOR)
