import pandas as pd
import ssl
from urllib.request import urlopen

import io
import requests


def format_csv_columns(filename):

    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

    res = requests.get(filename)
    pd.read_csv(io.BytesIO(res.content), sep=';')
    # workaround for ssl-problem
    # https://stackoverflow.com/questions/71102229/pandas-read-csv-from-web-acting-different-between-python-3-8-and-3-10
    # based on this issue: https://bugs.python.org/issue43998

    
    context = ssl.create_default_context()
    context.set_ciphers("DEFAULT")
    result = urlopen(filename, context=context)  


    report_df = pd.read_csv(result)
    # report_df_prep = report_df[
    #     [
    #         "Dimension.DATE",
    #         "Dimension.DEVICE_CATEGORY_NAME",
    #         "Column.TOTAL_LINE_ITEM_LEVEL_ALL_REVENUE",
    #     ]
    # ].rename(
    #     columns={
    #         "Dimension.DATE": "Datum",
    #         "Dimension.DEVICE_CATEGORY_NAME": "Device",
    #         "Column.TOTAL_LINE_ITEM_LEVEL_ALL_REVENUE": "Revenue",
    #     }
    # )

    report_df["Column.AD_EXCHANGE_LINE_ITEM_LEVEL_REVENUE"] = round(
        report_df["Column.AD_EXCHANGE_LINE_ITEM_LEVEL_REVENUE"] / 1000000, 2
    )

    report_df.to_csv(
        "./data/admanager_reporting.csv", decimal=".", sep=",", index=False
    )