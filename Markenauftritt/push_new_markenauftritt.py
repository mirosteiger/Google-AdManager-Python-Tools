from googleads import ad_manager
import create_new_advertiser
import create_new_order
import create_new_line_items
import delete_order
# import copy_creatives_from_templates
# import assign_creative_to_lineItem
class color:
   BOLD = '\033[1m'
   END = '\033[0m'

CHOICE = input ("type 'd' to delete an existing order or press Enter to create a new Markenauftritt: ")

def main(client, choice):
    if choice == "d":
      print(color.BOLD + "Hinweis: Es lassen sich nur Aufträge mit dem Status 'Entwurf/Draft' löschen!" + color.END)
      DELETE_ORDER_ID = input("ID des zu löschenden Auftrags: ")
      delete_order.main(client, DELETE_ORDER_ID)

    else: 
      ADVERTISER_NAME = input("Name des Werbetreibenden (Falls schon vorhanden, wird der neue Auftrag dem existierenden Werbetreibenden zugeordnet) : ")
      # ORDER_NAME = input("Name des zu erstellenden Auftrags: ")

      # 1. Create a new Advertiser or get existing Advertisers ID
      advertiser_id = create_new_advertiser.main(client, ADVERTISER_NAME)

      # 2. Create a new order based on the advertiser ID and the user-entered order name and returns the order_id
      order_id = create_new_order.main(client, advertiser_id, ADVERTISER_NAME)

      # 3. Create new Line Items inside the order with the provided ID
      line_item_ids = create_new_line_items.main( client, order_id, ADVERTISER_NAME )

      print(color.BOLD + "HINWEIS: Derzeit können die Creatives noch nicht zuverlässig in die neuen Werbebuchungen kopiert werden!", color.END)
      # 4. Copy Image Creatives from "Mustervorlage | Markenauftritt" 
      #creative_ids = copy_creatives_from_templates.main( client, ADVERTISER_NAME, advertiser_id)

      # 5. Assign new Creatives to new LineItems
      #result = assign_creative_to_lineItem.main(client, line_item_ids, creative_ids)
      #print("Assigned the Creatives: ", result)

      print("...... Completed!")
      



if __name__ == '__main__':
  # Initialize client object.
  ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
  main(ad_manager_client, CHOICE)