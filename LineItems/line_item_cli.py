from Utils.get_custom_targeting import get_values_by_id
from Utils.json_tools import get_field, read_from_json
from pick import pick

prebid_title = "Do you want to edit the viewability-targetings on all Prebid Line Items (Including Safeframe and Non-Safeframe)?"
search_string = pick(["Yes", "No", "test"], prebid_title)


options_title = "Do you want to add or remove targeting-values?"
OPTION = pick(["Add", "Remove"], options_title)

operator_title = "Do you want to include or exclude the seleted targeting-keys?"
OPERATOR = pick(["Include", "Exclude"], operator_title)


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

VALUES = get_values_by_id(client, key_id=key_selection)
# value_names = get_field(VALUES, "name")
value_selection_title = (
    "Which values to " + str(OPTION[0]) + "\n (select values with your SPACE-KEY)"
)
VALUE_SELECTION = pick(
    VALUES, value_selection_title, multiselect=True, min_selection_count=1
)