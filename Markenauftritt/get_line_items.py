
from googleads import ad_manager

LINE_ITEM_ID = "5178197038"

def main(client, line_item_id):
  # Initialize appropriate service.
  line_item_service = client.GetService('LineItemService', version='v202211')
  # Create a statement to select line items.
  statement = (ad_manager.StatementBuilder(version='v202211')
               .Where('id = :lineItem_id')
               .WithBindVariable('lineItem_id', line_item_id))

  # Retrieve a small amount of line items at a time, paging
  # through until all line items have been retrieved.
  while True:
    response = line_item_service.getLineItemsByStatement(statement.ToStatement(
    ))
    if 'results' in response and len(response['results']):
      for line_item in response['results']:
        # Print out some information for each line item.
        print(line_item)
      statement.offset += statement.limit
    else:
      break

  print('\nNumber of results found: %s' % response['totalResultSetSize'])




if __name__ == '__main__':
  # Initialize client object.
  ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
  main(ad_manager_client, LINE_ITEM_ID)
