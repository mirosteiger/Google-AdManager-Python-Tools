import config
import pandas as pd

def get_reportId_by_name( name ):
    ids = []
    print("Getting GAM report ids")
    for n in name: 
        n = n[0]
        if n == "AdX": ids.append(config.ADX)
        if n == "EBDA": ids.append(config.EBDA)
        if n == "PMPs": 
            ids.append(config.PMP_ADM)
            ids.append(config.PMP_ADX)
        if n == "Direct": ids.append(config.DIRECT)
        if n == "JobAds": ids.append(config.JOBADS)
        if n == "ImmoAds": ids.append(config.IMMOADS)
        if n == "Everything": ids.append(config.EVERYTHING)
    return ids    
            
def format_csv_columns(filename):

    report_df = pd.read_csv(filename)
    report_df_prep = report_df[
        [
            "Dimension.DATE",
            "Dimension.DEVICE_CATEGORY_NAME",
            "Column.AD_EXCHANGE_LINE_ITEM_LEVEL_REVENUE",
        ]
    ].rename(
        columns={
            "Dimension.DATE": "Datum",
            "Dimension.DEVICE_CATEGORY_NAME": "Device",
            "Column.AD_EXCHANGE_LINE_ITEM_LEVEL_REVENUE": "Revenue",
        }
    )

    report_df_prep["Column.AD_EXCHANGE_LINE_ITEM_LEVEL_REVENUE"] = round(
        report_df["Column.AD_EXCHANGE_LINE_ITEM_LEVEL_REVENUE"] / 1000000, 2
    )

    report_df_prep.to_csv(
        "../data/admanager_reporting.csv", decimal=".", sep=",", index=False
    )
