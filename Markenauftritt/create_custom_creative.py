import os
import uuid

# Import appropriate modules from the client library.
from googleads import ad_manager
import constants

# Set id of the advertiser (company) that the creative will be assigned to.
ADVERTISER_ID = 'INSERT_ADVERTISER_COMPANY_ID_HERE'


def main(client, advertiser_id, advertiser_name, position, width, height):
    # Initialize appropriate service.
    creative_service = client.GetService('CreativeService', version=constants.API_VERSION)

    # Get the image data for the creative.
    image_data = open(os.path.join(os.path.split(__file__)[0], '..', 'images',
                                    position + '.png'), 'r').read()

    html_snippet = ""
    # Create the HTML snippet used in the custom creative.
    if (position == "p2"):
        html_snippet = (constants.P2_RIGHT_HTML_SNIPPET) % ('%%CLICK_URL_UNESC%%', '%%DEST_URL%%',
                                        '%%FILE:IMAGE_ASSET%%')

    # Create custom creative.
    creative = {
        'xsi_type': 'CustomCreative',
        'name': advertiser_name +' | Markenauftritt | Wallpaper | '+ position + ' - Rechtsbündig',
        'advertiserId': advertiser_id,
        'size': {'width': width, 'height': height},
        'destinationUrl': 'https://www.meinestadt.de/koeln/immobilien',
        'customCreativeAssets': [
            {
                'xsi_type': 'CustomCreativeAsset',
                'macroName': 'IMAGE_ASSET',
                'asset': {
                    'assetByteArray': image_data,
                    'fileName': 'image%s.jpg' % uuid.uuid4()
                }
            }
        ],
        'htmlSnippet': html_snippet
    }

    # Call service to create the creative.
    creatives = creative_service.createCreatives([creative])

    # Display results.
    if creatives:
        creative = creatives[0]
        print('Template creative with id "%s", name "%s", and type "%s" was '
            'created and can be previewed at %s.'
            % (creative['id'], creative['name'],
                ad_manager.AdManagerClassType(creative), creative['previewUrl']))

if __name__ == '__main__':
  # Initialize client object.
  ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
  main(ad_manager_client, ADVERTISER_ID)
