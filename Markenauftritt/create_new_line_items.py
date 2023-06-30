import datetime
import uuid
# Import appropriate modules from the client library.
from googleads import ad_manager
import pytz
import constants
import line_item_templates

ORDER_ID = '3147880498'

def main(client, order_id, advertiser_name):
  # Initialize appropriate service.
  line_item_service = client.GetService('LineItemService', version='v202211')

  # Create line item objects.
  templates = [line_item_templates.WALLPAPER, line_item_templates.GALERIE, line_item_templates.MOBILE]
  line_items = []
  line_item_ids = []

  for i in range(3):
    name = advertiser_name + templates[i]['name']
    
    templates[i]['orderId'] = order_id
    templates[i]['status'] = constants.DEFAULT_STATUS
    templates[i]['name'] = name
    line_items.append(templates[i])


  # Add line items.
  line_items = line_item_service.createLineItems(line_items)
  for i in line_items:
    line_item_ids.append(i['id'])

  print("created new LineItems using Markenauftritt Templates")
  return line_item_ids


if __name__ == '__main__':
  # Initialize client object.
  ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
  main(ad_manager_client, ORDER_ID, ADVERTISER_NAME)