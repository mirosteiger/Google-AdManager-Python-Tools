# Import appropriate modules from the client library.
from googleads import ad_manager


def main(client):
  # Initialize appropriate service.
  ad_unit_service = client.GetService('InventoryService', version='v202211')

  # Create a statement to select ad units.
  statement = (
        ad_manager.StatementBuilder(version=constants.API_VERSION)
        .Where(("name LIKE :name"))
        .WithBindVariable("name", search_key)
        #.Limit(100)
    )

  # Retrieve a small amount of ad units at a time, paging
  # through until all ad units have been retrieved.
  while True:
    response = ad_unit_service.getAdUnitsByStatement(statement.ToStatement())
    if 'results' in response and len(response['results']):
      for ad_unit in response['results']:
        # Print out some information for each ad unit.
        print('Ad unit with ID "%s" and name "%s" was found.\n' %
              (ad_unit['id'], ad_unit['name']))
      statement.offset += statement.limit
    else:
      break

  print('\nNumber of results found: %s' % response['totalResultSetSize'])


if __name__ == '__main__':
  # Initialize client object.
  ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
  main(ad_manager_client)
