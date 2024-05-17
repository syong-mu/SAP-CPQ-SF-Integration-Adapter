from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_FunctionModules import get_quote_opportunity_id
from CPQ_SF_IntegrationSettings import CL_SalesforceIntegrationParams, CL_GeneralIntegrationSettings
from CPQ_SF_IntegrationReferences import CL_CompositeRequestReferences as REF, CL_IntegrationReferences as INT_REF
from CPQ_SF_CustomerModules import CL_CustomerModules


def execute():
    #########################################
    # 1. INIT
    #########################################
    result = str()
    key = Param.PROPERTY
    session_key = 'account_' + key
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
    class_customer_modules = CL_CustomerModules(Quote, TagParserQuote, None, Session)
    opportunityId = get_quote_opportunity_id(Quote)

    try:
        caching = Param.CACHING
    except: 
        caching = CL_GeneralIntegrationSettings.TAG_CACHING # default value
    # Get from Session if empty on Quote
    if not opportunityId:
        opportunityId = Session["OpportunityId"]
    if opportunityId:
        compositePayload = list()
        #########################################
        # 2. SESSION CHECK
        #########################################
        # Implement Caching for Salesforce Object Definitions
        if caching:
            session_opp = Session[opportunityId]
            if str(session_opp) != 'None':
                if session_key in session_opp.keys():
                    return session_opp[session_key]
            else:
                Session[opportunityId] = {}
        else:
            Session[opportunityId] = {session_key: ""}
        #########################################
        # 3. AUTHORIZATION
        #########################################
        bearerToken = class_sf_integration_modules.get_auth2_token()
        #########################################
        # 4. RETURN SELECTED PROPERTY TO TAG
        #########################################
        oppRequest = class_sf_integration_modules.build_cr_sobject_get_opportunity(opportunityId)
        compositePayload.append(oppRequest)
        oppAccountRequest = class_customer_modules.build_cr_sobject_get_account("@{"+CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT+".AccountId}", REF.GET_OPP_ACC)
        compositePayload.append(oppAccountRequest)
        response = class_sf_integration_modules.post_composite_request(bearerToken, compositePayload, INT_REF.REF_GET_ACC)
        for resp in response['compositeResponse']:
            if resp:
                try:
                    if str(resp['body']['attributes']['type']) == CL_SalesforceIntegrationParams.SF_ACCOUNT_OBJECT:
                        result = unicode(getattr(resp['body'], key))
                        Session[opportunityId][session_key] = result
                        return result
                except Exception as e:
                    #Trace.Write("CPQ-SFDC: ACCOUNT_TAG Error -->"+str(e))
                    pass
        return result


Result = ''
Result = unicode(execute())
