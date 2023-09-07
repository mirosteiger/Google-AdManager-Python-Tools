"""Initializes a AdManagerClient using a Service Account."""

# Import necessary libraries
import sys
import locale
from googleads import ad_manager
import config
import m9_ids

locale.getdefaultlocale = lambda *args: ["de_DE", "UTF-8"]

# Initialize Targeting service
print("Initializing LineItem-Service")

ORDER_ID = 2603779404
#ORDER_ID = input("Please enter orderID: ")
# Amazon | 320x480: 2603779404



def main(client, order_id):
    # Initialize Line Item Service
    service = client.GetService("LineItemService", version=config.API_VERSION)
    get_line_items(service, order_id)

# Returns an array of Line Item Ids
def get_line_items(service, order_id):

#    statement = (
 #       ad_manager.StatementBuilder(version=config.API_VERSION)
  #      .Where(("orderId = :order_id"))
   #     .WithBindVariable("order_id", order_id)
    #    .Limit(1)
    #)
    statement = (
        ad_manager.StatementBuilder(version=config.API_VERSION)
        .Where(("orderId = :id"))
        .WithBindVariable("id", order_id)
        .Limit(100)
    )
    # Get line items by statement.
    response = service.getLineItemsByStatement(
      statement.ToStatement())
    
    if 'results' in response and len(response['results']):
        # Update each local line item by excluding a list of adUnits
        updated_line_items = []
        for line_item in response['results']:
            if not line_item['isArchived']:
                line_item['targeting']['inventoryTargeting']['excludedAdUnits'] = m9_ids.M9_IDS
                updated_line_items.append(line_item)

        # Push line items with updated targeting to the adserver.
        line_items = service.updateLineItems(updated_line_items)

        # Display results.
        if line_items:
            for line_item in line_items:
                print('Line item with id "%s", belonging to order id "%s", named '
                    '"%s" was updated.'
                    % (line_item['id'], line_item['orderId'], line_item['name']))
        else:
            print('No line items were updated.')
    else:
        print('No line items found to update.')


if __name__ == "__main__":
    client = ad_manager.AdManagerClient.LoadFromStorage()
    main(client, ORDER_ID)