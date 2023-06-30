from pick import pick
import config, util
from googleads import ad_manager
import run_saved_query
import config

def main(client):
    title = 'Please choose the Reportings you want to run: \n(Use Arrow-Keys to choose and SPACE to select. Confirm with ENTER):'
    selected = pick(config.REPORT_OPTIONS, title, multiselect=True, min_selection_count=1)
    print(selected)

    report_ids = util.get_reportId_by_name(selected)
    print("selected report Ids: " + str(report_ids))
    for rID in report_ids:
        run_saved_query.main(client, str(rID))

if __name__ == '__main__':
  # Initialize client object.
    ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()
    main(ad_manager_client)