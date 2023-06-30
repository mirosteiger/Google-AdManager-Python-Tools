"""This code example creates new line item creative associations (LICAs) for an
existing line item and a set of creative ids.

To determine which LICAs exist, run get_all_licas.py.
"""


# Import appropriate modules from the client library.
from googleads import ad_manager

# Set the line item ID and creative IDs to associate.

def main(client, line_item_id, creative_ids):
  print(creative_ids)
  # Initialize appropriate service.
  lica_service = client.GetService(
      'LineItemCreativeAssociationService', version='v202211')

  licas = []
  for creative_id in creative_ids:
    licas.append({'creativeId': creative_id,
                  'lineItemId': line_item_id})

    print(licas)
  # Create the LICAs remotely.
    licas = lica_service.createLineItemCreativeAssociations(licas)

  # Display results.
  if licas:
    for lica in licas:
      print('LICA with line item id "%s", creative id "%s", and '
            'status "%s" was created.' %
            (lica['lineItemId'], lica['creativeId'], lica['status']))
  else:
    print('No LICAs created.')

  return licas

