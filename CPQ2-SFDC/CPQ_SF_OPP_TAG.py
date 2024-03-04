from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_FunctionModules import get_quote_opportunity_id
from CPQ_SF_IntegrationSettings import CL_SalesforceIntegrationParams, CL_GeneralIntegrationSettings


def execute():
    #########################################
    # 1. INIT
    #########################################
    result = str()
    Quote = context.Quote
    key = Param.PROPERTY
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, Session)
    opportunityId = get_quote_opportunity_id(Quote)
    # Get from Session if empty on Quote
    if not opportunityId:
        opportunityId = Session["OpportunityId"]
    # Get Caching param
    try:
        caching = Param.CACHING
    except:
        caching = CL_GeneralIntegrationSettings.TAG_CACHING # default value

    if opportunityId:
        #########################################
        # 2. SESSION CHECK
        #########################################
        # Implement Caching for Salesforce Object Definitions
        if caching:
            session_opp = Session[opportunityId]
            if str(session_opp) != 'None':
                if key in session_opp.keys():
                    return session_opp[key]
            else:
                Session[opportunityId] = {}
        else:
            Session[opportunityId] = {key: ""}
        #########################################
        # 3. AUTHORIZATION
        #########################################
        bearerToken = class_sf_integration_modules.get_auth2_token()
        #########################################
        # 4. RETURN SELECTED PROPERTY TO TAG
        #########################################
        response = class_sf_integration_modules.get_sobject(bearerToken, CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT, opportunityId)
        if response:
            try:
                result = unicode(getattr(response, key))
                Session[opportunityId][key] = result
            except Exception as e:
                #Trace.Write("CPQ-SFDC: OPP_TAG Error -->"+str(e))
                pass
    return result


Result = ''
Result = unicode(execute())