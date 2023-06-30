# Google AdManager Python Tools
 
A collection of custom python scripts to perform specific bulk actions on the google adserver via the Google AdManager Python API.
These actions have to be done more or less frequently and need an additional `googleads.yaml` file for authentication.

---

For the moment, the following actions are possible:

### Line Items:
- Update targetings for all Line Items in an order. 
- Add or remove a bidder for Prebid (Non-)/Safeframe line items

### Markenauftritt (A specific advertising product):
- Start by executing `python3 push_new_markenauftritt.py`
- Create a new advertiser
- Create a new order for the advertiser
- Dynamically create new line items based on the previous informations and template data
- Create and assign new creatives (*currently not working*)
- Delete an order by id

### Reportings:
- Select a presaved query by its name and save a csv locally
- Push data via API to google spreadsheets (*TODO*) 

### Random:
- Pull a list of all pageIds existing in the adserver
