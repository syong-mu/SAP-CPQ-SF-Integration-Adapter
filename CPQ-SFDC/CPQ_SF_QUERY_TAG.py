from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_IntegrationReferences import CL_IntegrationReferences as INT_REF
from CPQ_SF_IntegrationSettings import CL_GeneralIntegrationSettings
import re

###############################################################################################
# Function to replace special characters in string
###############################################################################################
def replace_special_char(text):
    special_chars = [{"symbol": "&", "code": "%26"}, {"symbol": "#", "code": "%23"}, {"symbol": "%", "code": "%25"}]
    for special_char in special_chars:
        text = text.replace(special_char["symbol"], special_char["code"])

    return text

def execute():
    #########################################
    # 1. INIT
    #########################################
    result = str()
    query = "?q=" + re.sub('\++', '+', str(Param.QUERY))
    query = str.replace(query, "[", "(")
    query = str.replace(query, "]", ")")
    #escaping special characters in query
    query = replace_special_char(query)
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)

    try:
        caching = Param.CACHING
    except: 
        caching = CL_GeneralIntegrationSettings.TAG_CACHING # default value
    #########################################
    # 2. SESSION CHECK
    #########################################
    # Implement Caching for Salesforce Object Definitions
    if caching:
        session_query = Session['Query']
        if str(session_query) != 'None':
            if query in session_query.keys():
                return session_query[query]
        else:
            Session['Query'] = {}
    else:
        Session['Query'] = {query: ""}
    #########################################
    # 3. AUTHORIZATION
    #########################################
    bearerToken = class_sf_integration_modules.get_auth2_token()
    headers = class_sf_integration_modules.get_authorization_header(bearerToken)
    #########################################
    # 4. RETURN SELECTED PROPERTY TO TAG
    #########################################
    response = class_sf_integration_modules.call_soql_api(headers, query, INT_REF.REF_QUERY_TAG)
    if response:
        for record in response.records:
            for attr in record:
                if attr.Name != 'attributes':
                    try:
                        result = unicode(getattr(record, attr.Name))
                    except Exception as e:
                        #Trace.Write("CPQ-SFDC: QUERY_TAG Error -->"+str(e))
                        pass
                    break
            break
    Session['Query'][query] = result
    return result


Result = ''
Result = unicode(execute())
