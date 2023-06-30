

# Import appropriate modules from the client library.
from googleads import ad_manager
import constants


WP_IMAGE_CREATIVE_IDS = constants.WALLPAPER_IMAGE_CREATIVE_TEMPLATE_IDS
WP_CUSTOM_CREATIVE_IDS = constants.WALLPAPER_IMAGE_CREATIVE_TEMPLATE_IDS

MOBILE_IMAGE_CREATIVE_IDS = constants.MOBILE_IMAGE_CREATIVE_TEMPLATE_IDS
DESKTOP_IMAGE_CREATIVE_IDS = constants.DESKTOP_IMAGE_CREATIVE_TEMPLATE_IDS

IMAGE_CREATIVE_IDS = [
  *constants.WALLPAPER_IMAGE_CREATIVE_TEMPLATE_IDS,
  *constants.MOBILE_IMAGE_CREATIVE_TEMPLATE_IDS,
  *constants.DESKTOP_IMAGE_CREATIVE_TEMPLATE_IDS
]

def main(client, advertiser_name, advertiser_id):
  
  # COPY IMAGE CREATIVES:
  copy_image_creatives(client, advertiser_name, WP_IMAGE_CREATIVE_IDS, advertiser_id)

  # COPY_CUSTOM_CREATIVES:
  #create_custom_creatives(client, advertiser_name, IMAGE_CREATIVE_IDS, advertiser_id)


def copy_image_creatives(client, advertiser_name, creative_ids, advertiser_id):
  # Initialize appropriate service.
  print("Copying Template Creatives...")
  creative_service = client.GetService('CreativeService', version=constants.API_VERSION)
  new_creatives = []
  creative_ids = []

  for cid in creative_ids:
    # Create a statement to get the image creative.
    statement = (ad_manager.StatementBuilder(version=constants.API_VERSION)
                .Where('id = :id')
                .OrderBy('id', ascending=True)
                .WithBindVariable('id', cid))

    # Get the creative.
    query_result = creative_service.getCreativesByStatement(
        statement.ToStatement())

    
    image_creative = query_result['results'][0]


    # Build the new creative, set id to None to create a copy.
    image_creative['id'] = None
    image_creative['name'] = advertiser_name + image_creative['name'][13:]
    image_creative['advertiserId'] = advertiser_id


    new_creatives.append(image_creative)

    print(  image_creative['name'])

  creatives = creative_service.createCreatives(new_creatives)

  print (creatives)
    #creative_ids.append(i['id'])

  #return creative_ids

