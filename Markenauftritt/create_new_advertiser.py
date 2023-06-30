import constants
from googleads import ad_manager

def main(client, advertiser_name):

  # Initialize appropriate service.
  company_service = client.GetService('CompanyService', version=constants.API_VERSION)
  advertiser_check = check_if_advertiser_exists(company_service, advertiser_name)
  advertiser_id = 0

  if advertiser_check:
    print("Advertiser already existing!")
    advertiser_id = advertiser_check
  else:
    print("Advertiser not found. Creating a new one?")
    choice = input("Type y or n ")
    if choice == "y":
      new_id = create_new_advertiser(company_service, advertiser_name)
      advertiser_id = new_id
    else:
      print("Stopped") 
      return
    
  return advertiser_id

def check_if_advertiser_exists(company_service, advertiser_name):
  result = 0
  statement = (ad_manager.StatementBuilder(version='v202211')
               .Where('type = :type')
               .Where('name = :name')
               .WithBindVariable('type', 'ADVERTISER')
               .WithBindVariable('name', advertiser_name))

  response = company_service.getCompaniesByStatement(statement.ToStatement())
  if 'results' in response and len(response['results']):
    for company in response['results']:
      # Print out some information for each company.
      print('Company with ID "%d", name "%s", and type "%s" was found.\n' %
            (company['id'], company['name'], company['type']))
      result = company['id']

  return result

def create_new_advertiser(company_service, advertiser_name):
  # Create company objects.
  company = [
      {
          'name': advertiser_name,
          'type': 'ADVERTISER'
      }
  ]

  # Add companies.
  company = company_service.createCompanies(company)

  # Display results.
  for company in company:
    print('Company with ID "%s", name "%s", and type "%s" was created.'
          % (company['id'], company['name'], company['type']))
  return company['id']
