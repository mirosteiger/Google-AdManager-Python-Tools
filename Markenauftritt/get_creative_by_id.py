
from googleads import ad_manager


def main(client):
  # Initialize appropriate service.
  creative_service = client.GetService('CreativeService', version='v202211')
  # Create a statement to select creatives.
  statement = (ad_manager.StatementBuilder(version='v202211')
               .Where('creativeId = :creativeId')
               .WithBindVariable('creativeId', '138420836913'))

  # Retrieve a small amount of creatives at a time, paging
  # through until all creatives have been retrieved.
  while True:
    response = creative_service.getCreativesByStatement(statement.ToStatement())
    if 'results' in response and len(response['results']):
      for creative in response['results']:
        # Print out some information for each creative.
        print('Creative with ID "%d" and name "%s" was found.\n' %
              (creative['id'], creative['name']))
      statement.offset += statement.limit
    else:
      break

    print(response['results'])


if __name__ == '__main__':
  # Initialize client object.
  ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
  main(ad_manager_client)
