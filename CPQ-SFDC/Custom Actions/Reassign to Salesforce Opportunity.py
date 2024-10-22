from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_FunctionModules import get_quote_opportunity_id, set_quote_opportunity_id
from CPQ_SF_IntegrationReferences import CL_IntegrationReferences as INT_REF
from CPQ_SF_IntegrationSettings import CL_SalesforceQuoteParams



# Main execution process logic
def main(Quote):
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
    #############################################
    # 1. AUTHORIZATION
    #############################################
    bearerToken = class_sf_integration_modules.get_auth2_token()
    #############################################
    # 2. DETACH
    #############################################
    # Check if Quote is attached to an Opportunity
    opportunityId = get_quote_opportunity_id(Quote)
    if opportunityId:
        # Delete Quote from Salesforce
        class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
        # Call REST API
        response = class_sf_integration_modules.get_quote_by_number(bearerToken, opportunityId, INT_REF.REF_GET_SF_QUOTE)
        if response:
            if response["totalSize"] > 0:
                # Collect Quote Id records
                quoteIdRecords = [str(record["Id"]) for record in response["records"]]
                url = class_sf_integration_modules.get_salesforce_api_url(class_sf_integration_modules.build_delete_sobj_collection_url(quoteIdRecords))
                # Check Delete Quote Permissions
                permissionList = [class_sf_integration_modules.build_permission_checklist(CL_SalesforceQuoteParams.SF_QUOTE_OBJECT, False, False, True)]
                # Call REST API
                response = class_sf_integration_modules.call_sobject_delete_api(bearerToken, url, INT_REF.REF_DETACH_QUOTE, permissionList)
                if response:
                    # set opportunity Id where quote should be reassigned to
                    if Session["OpportunityId"]:
                        set_quote_opportunity_id(Quote, Session["OpportunityId"])
                    #############################################
                    # 3. REATTACH (OUTBOUND MAPPINGS)
                    #############################################
                    ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')
Quote = QuoteHelper.Edit(Quote.UserId, Quote.QuoteId)
# Execute main
main(Quote)
