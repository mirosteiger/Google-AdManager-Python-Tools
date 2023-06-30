'''
    Doku zur GAM_API:
    Werbetreibender:    https://developers.google.com/ad-manager/api/reference/v202211/CompanyService
    Auftrag:            https://developers.google.com/ad-manager/api/reference/v202211/OrderService

'''

API_VERSION = "v202211"         # API Version der Google API. Sollte nur geändert werden, wenn nicht mehr supported, da Google gerne Features ändert und damit einige Funktionen kaputt gehen könnten.

''' Default-Werte um Auftrag zu erstellen '''

TRAFFICKER_ID = 245927227       # User ID des Traffick  ers als Integer, bzw. des Erstellers des Auftrags (Bens ID als Default). 
                                # WICHTIG: Der Haupt-Trafficker darf nicht in der Liste der Sekundären stehen!
SECONDARY_TRAFFICKERS = [       # User IDs der sekundären Trafficker
    245533491,                  # Miro
    248265948                   # Minh
    ]
DEFAULT_STATUS= "DRAFT"   # Auftrag wird zur Überprüfung per default als Entwurf erstellt. Muss im GAM nach Überprüfung manuell gestartet werden. 

WALLPAPER_IMAGE_CREATIVE_TEMPLATE_IDS = [
    138421467088,
    138420836169,
]
WALLPAPER_CUSTOM_CREATIVE_TEMPLATE_IDS = [
    138420836913,
    138420819101,
    138421467664,
    138420819119
]

MOBILE_IMAGE_CREATIVE_TEMPLATE_IDS = [
    138420835410,
    138420835383,
    138420835368,
    138420818819,
    138421466704
]

DESKTOP_IMAGE_CREATIVE_TEMPLATE_IDS = [
    138421465363,
    138421466059,
    138421466020
]

### Funktioniert noch nicht ###
P2_RIGHT_HTML_SNIPPET = '<a href="%%CLICK_URL_UNESC%%%%DEST_URL%%" target="_blank">\n<img src="%%FILE:PNG1%%" alt="banner">\n</a>\n<script>\nvar p2 = parent.document.getElementsByClassName("-p2");\nparent.window.onscroll = function() {\n\n    if (parent.window.pageYOffset > 210) {\n\n \n        p2[0].style.top = \'10px\';\n    } else {\n\n        p2[0].style.top = -10 + \'px\';\n    }\n\n}\n</script>'