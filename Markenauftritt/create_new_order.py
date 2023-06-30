from googleads import ad_manager
import constants


def main(client, advertiser_id, advertiser_name ) :
  order_service = client.GetService('OrderService', version=constants.API_VERSION)
  
  
  # Create order objects.
  order = {
        'name': advertiser_name + ' | Markenauftritt'  ,
        'advertiserId': advertiser_id,
        'traffickerId': constants.TRAFFICKER_ID,
        'secondaryTraffickerIds': constants.SECONDARY_TRAFFICKERS
    }

  # Add orders.
  order = order_service.createOrders(order)
  print('successfully created an order with the id: ')
  print(order[0]['id'])
  print('and name: ')
  print(order[0]['name'])
  
  return(order[0]['id'])


