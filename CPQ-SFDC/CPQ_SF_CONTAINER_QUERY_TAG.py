from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
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
    def update_container_row(row, col_prop_map, prop_values):
        for key, prop in col_prop_map.items():
            for p_key in prop_values.keys():
                if str(p_key).lower() == prop.lower():
                    row.SetColumnValue(key, str(prop_values[str(p_key)]))
                    break

    query = "?q=" + re.sub('\++', '+', str(Param.QUERY))
    query = str.replace(query, "[", "(")
    query = str.replace(query, "]", ")")
    #escaping special characters in query
    query = replace_special_char(query)
    #Get id as 1st property in request (after "select")
    query_with_id = query[:9] + "+Id," + query[9:] if not re.search("(?i)(?<![\w\d])id(?![\w\d])", query.lower().split("where")[0]) else query

    #Replace ||| with space in container name
    container_name = Param.CONTAINER.replace("|||", " ")
    container = Product.GetContainerByName(container_name)
    column_proprty_mapping = {}

    #properies in order based on query
    counter = 2 #[0] q, [1] select
    props = re.findall("\w+", query)
    for val in Param.COLUMNS:
        column_proprty_mapping[val.replace("|||", " ")] = props[counter]
        counter = counter + 1

    session_stored = ""
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)

    try:
        caching = Param.CACHING
    except: 
        caching = CL_GeneralIntegrationSettings.TAG_CACHING # default value

    try: groupBy = Param.GROUP_BY
    except: groupBy = [] # default value

    #########################################
    # 2. SESSION CHECK
    #########################################
    # Implement Caching for Salesforce Object Definitions
    if caching:
        session_query=Session['Query']
        if str(session_query) != 'None':
            if query_with_id in session_query.keys():
                session_stored = session_query[query_with_id]
        else:
            Session['Query'] = {}
    else:
            Session['Query'] = {query_with_id: ""}
    #########################################
    # 3. AUTHORIZATION
    #########################################
    bearerToken = class_sf_integration_modules.get_auth2_token()
    headers = class_sf_integration_modules.get_authorization_header(bearerToken)
    #########################################
    # 4. RESOLVE QUERY
    #########################################
    if not session_stored:
        distinctList = []

        response = class_sf_integration_modules.call_soql_api(headers, query_with_id, None)
        response_dict = {}
        for record in response.records:
            response_dict[str(record.Id)] = {}
            for attr in record:
               # get attribute value from response
               attrValue = getattr(record,attr.Name)
               if str(attr.Name) in groupBy:
                # add unique attribute value
                if attrValue not in distinctList:
                    response_dict[str(record.Id)][attr.Name] = attrValue
                # flag that attribute value had been added to the list
                distinctList.append(attrValue)
               else: response_dict[str(record.Id)][attr.Name] = attrValue


        Session['Query'][query_with_id] = response_dict
        session_stored = response_dict
    #########################################
    # 5. REMOVE EXCESS ROWS
    #########################################
    def crmid_not_in_response(row):
        return row.CrmId not in session_stored.keys()
    def get_row_index(row):
        return row.RowIndex

    #get indexes of rows that need to be removed, sorted to avoid index change of lower rows
    remove_rows_indexes = sorted(map(get_row_index, filter(crmid_not_in_response, container.Rows)), reverse=True)
    for index in remove_rows_indexes:
        container.DeleteRow(index)
    #########################################
    # 6. UPDATE EXISTING ROWS
    #########################################
    for row in container.Rows:
        update_container_row(row, column_proprty_mapping, session_stored[row.CrmId])
    #########################################
    # 7. ADD MISSING ROWS
    #########################################
    rows_to_add = [crmid for crmid in session_stored.keys() if crmid not in [row.CrmId for row in container.Rows]]
    for crmid in rows_to_add:
        row = container.AddNewRow(False)
        row.CrmId = crmid
        update_container_row(row, column_proprty_mapping, session_stored[crmid])
    #########################################
    # 8. CALCULATE CONTAINER
    #########################################
    container.Calculate()

Result = 'NOK'
execute()
Result = 'OK'
