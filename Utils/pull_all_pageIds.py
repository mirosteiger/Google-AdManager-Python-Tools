"""Updates name of custom targeting values belonging to a custom targeting key.

To determine which custom targeting keys exist, run
get_all_custom_targeting_keys_and_values.py.
"""


# Import appropriate modules from the client library.
from googleads import ad_manager
import numpy as np

CUSTOM_TARGETING_KEY_ID = '679141'


def main(client, key_id):
  # Initialize appropriate service.
    custom_targeting_service = client.GetService(
      'CustomTargetingService', version='v202211')

    statement = (ad_manager.StatementBuilder(version='v202211')
               .Where('customTargetingKeyId = :keyId')
               .WithBindVariable('keyId', int(key_id)))

    values = []
    while True:
        # Get custom targeting values by statement.
        response = custom_targeting_service.getCustomTargetingValuesByStatement(
            statement.ToStatement())

        if 'results' in response and len(response['results']):
            for value in response['results']:
                values.append(value['name'])

        # Display results.
            for value in values:
                print(value)
            statement.offset += statement.limit
        else:
            break
    np.savetxt("../data/gam_page_ids.txt", values, delimiter=" ", newline = "\n", fmt="%s")

    if response['totalResultSetSize'] == 0:
        print('No custom targeting values were updated.')


if __name__ == '__main__':
  # Initialize client object.
  ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
  main(ad_manager_client, CUSTOM_TARGETING_KEY_ID)
