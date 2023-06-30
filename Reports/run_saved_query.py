
"""This script runs a report from a saved query."""

# Import appropriate modules from the client library.
import tempfile
from googleads import ad_manager
from googleads import errors
import pandas as pd
from datetime import datetime
from datetime import timedelta

import config
import util

API_VERSION = config.API_VERSION

def main(client, saved_query_id):
  print("Initialize ReportService")
  # Initialize appropriate service.
  report_service = client.GetService('ReportService', version=API_VERSION)

  # Initialize a DataDownloader.
  report_downloader = client.GetDataDownloader(version=API_VERSION)

  print("Generate statement with the following ID: " + saved_query_id)
  # Create statement object to filter for an order.
  statement = (ad_manager.StatementBuilder(version=API_VERSION)
               .Where('id = :id')
               .WithBindVariable('id', int(saved_query_id))
               .Limit(1))

  response = report_service.getSavedQueriesByStatement(
      statement.ToStatement())
  
  end_date = datetime.now().date() - timedelta(days=1)
  if 'results' in response and len(response['results']):
    saved_query = response['results'][0]

    if saved_query['isCompatibleWithApiVersion']:
      report_job = {}

      # Set report query and optionally modify it.
      report_job['reportQuery'] = saved_query['reportQuery']
      #modify Date to work with API
      report_job['reportQuery']['dateRangeType']='CUSTOM_DATE'
      report_job['reportQuery']['startDate']= config.START_DATE
      report_job['reportQuery']['endDate']= end_date

      print("Pulling data via ReportService...")
      try:
        # Run the report and wait for it to finish.
        report_job_id = report_downloader.WaitForReport(report_job)
      except errors.AdManagerReportError as e:
        print('Failed to generate report. Error was: %s' % e)

      # Change to your preferred export format.
      export_format = 'CSV_DUMP'

      with tempfile.NamedTemporaryFile(
                prefix="report-", suffix=".csv", mode="wb", dir="../data", delete=False
            ) as report_file:
            # Download report data.
            report_downloader.DownloadReportToFile(
            report_job_id,
            export_format,
            report_file,
            use_gzip_compression=False,
            )
      report_file.close()
      
      print("Formatting CSV-Columns...")

      util.format_csv_columns(report_file.name)
      

      # Display results.
      print('Report job with id "%s" downloaded to:\n%s' % (
          report_job_id, report_file.name))
    else:
      print('The query specified is not compatible with the API version.')
