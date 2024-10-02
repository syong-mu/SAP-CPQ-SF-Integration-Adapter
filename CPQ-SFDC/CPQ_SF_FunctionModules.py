from CPQ_SF_IntegrationSettings import CL_CpqIntegrationParams, CL_GeneralIntegrationSettings
from CPQ_SF_OpportunityStatusMapping import opportunity_status_mapping
from CPQ_SF_CpqHelper import CPQ_BILL_TO, CPQ_SHIP_TO, CPQ_END_USER


###############################################################################################
# Function to retrieve CPQ Customer (QUOTE 1.0 ONLY)
###############################################################################################
def get_quote_customer(Quote, cpqRole):
    customer = None
    if cpqRole == CPQ_BILL_TO:
        customer = Quote.BillToCustomer
    elif cpqRole == CPQ_SHIP_TO:
        customer = Quote.ShipToCustomer
    elif cpqRole == CPQ_END_USER:
        customer = Quote.EndUserCustomer
    return customer


###############################################################################################
# Function to set Customer on Quote
# ERROR when Quote.SaveCustomer is applied for ShipTo
###############################################################################################
def set_customer_on_quote(Quote, cpqRole, customer):
    if cpqRole == CPQ_BILL_TO:
        Quote.CopyToBillToCustomer(customer)
        Quote.SaveCustomer(customer)
    elif cpqRole == CPQ_SHIP_TO:
        Quote.CopyToShipToCustomer(customer)
        Quote.SaveCustomer(Quote.ShipToCustomer)
    elif cpqRole == CPQ_END_USER:
        Quote.CopyToEndUserCustomer(customer)
        Quote.SaveCustomer(customer)


###############################################################################################
# Function to set empty Customer on Quote
# ERROR when Quote.SaveCustomer is applied for ShipTo
###############################################################################################
def set_empty_customer_on_quote(Quote, cpqRole):
    customer = Quote.NewCustomer(cpqRole)
    customer.Active = False
    if cpqRole == CPQ_BILL_TO:
        Quote.CopyToBillToCustomer(customer)
        Quote.SaveCustomer(customer)
    elif cpqRole == CPQ_SHIP_TO:
        Quote.CopyToShipToCustomer(customer)
    elif cpqRole == CPQ_END_USER:
        Quote.CopyToEndUserCustomer(customer)
        Quote.SaveCustomer(customer)


###############################################################################################
# Function to retrieve Opportunity Id attached to Quote
###############################################################################################
def get_quote_opportunity_id(Quote):
    value = None
    if Quote:
        customField = Quote.GetCustomField(CL_CpqIntegrationParams.OPPORTUNITY_ID_FIELD)
        if customField:
            value = customField.Content
    return value


###############################################################################################
# Function to attach opportunity id to Quote
###############################################################################################
def set_quote_opportunity_id(Quote, opportunityId):
    customField = Quote.GetCustomField(CL_CpqIntegrationParams.OPPORTUNITY_ID_FIELD)
    if customField:
        customField.Content = opportunityId


###############################################################################################
# Function to get Opportunity Name
###############################################################################################
def get_quote_opportunity_name(Quote):
    value = str()
    customField = Quote.GetCustomField(CL_CpqIntegrationParams.OPPORTUNITY_NAME_FIELD)
    if customField:
        value = customField.Content
    return value


###############################################################################################
# Function to set Opportunity Name
###############################################################################################
def set_quote_opportunity_name(Quote, opportunityName):
    customField = Quote.GetCustomField(CL_CpqIntegrationParams.OPPORTUNITY_NAME_FIELD)
    if customField:
        customField.Content = opportunityName


###############################################################################################
# Function to get Salesforce Opportunity Status to be mapped
###############################################################################################
def get_opportunity_mapping_status(Quote):
    oppStatus = str()
    cpqStatus = Quote.OrderStatus.Name
    statusMappings = opportunity_status_mapping()
    mappings = next((x for x in statusMappings if x["CPQ_STATUS"] == cpqStatus), None)
    if mappings:
        oppStatus = mappings["SF_STATUS"]
    return oppStatus


###############################################################################################
# Function to get CPQ Quote Market Id
###############################################################################################
def get_quote_market_id(Quote):
    marketId = str()
    quoteId = Quote.QuoteId
    ownerId = Quote.UserId
    sql = """SELECT market_id FROM CART
    WHERE USERID = '{ownerId}'
    AND CART_ID = '{quoteId}'""".format(ownerId=ownerId, quoteId=quoteId)
    sqlRecord = SqlHelper.GetFirst(sql)
    if sqlRecord:
        marketId = sqlRecord.market_id
    return marketId


###############################################################################################
# Function to get Market Code based on Market Id
###############################################################################################
def get_market_code(marketId):
    marketCode = None
    sql = """SELECT market_code FROM market_defn
    WHERE market_id = '{marketId}'""".format(marketId=str(marketId))
    sqlRecord = SqlHelper.GetFirst(sql)
    if sqlRecord:
        marketCode = sqlRecord.market_code
    return marketCode


###############################################################################################
# Function to set Customer CrmAccountId
###############################################################################################
def set_customer_crm_account_id(Quote, cpqRole, crmAccountId):
    if cpqRole == CPQ_BILL_TO:
        customer = Quote.BillToCustomer
    elif cpqRole == CPQ_SHIP_TO:
        customer = Quote.ShipToCustomer
    elif cpqRole == CPQ_END_USER:
        customer = Quote.EndUserCustomer

    if customer is not None:
        customer.CrmAccountId = crmAccountId
        Quote.SaveCustomer(customer)


###############################################################################################
# Function to get Customer CrmAccountId
###############################################################################################
def get_customer_crm_account_id(Quote, cpqRole):
    crmAccountId = None
    if cpqRole == CPQ_BILL_TO:
        customer = Quote.BillToCustomer
    elif cpqRole == CPQ_SHIP_TO:
        customer = Quote.ShipToCustomer
    elif cpqRole == CPQ_END_USER:
        customer = Quote.EndUserCustomer

    if customer is not None:
        crmAccountId = customer.CrmAccountId
    return crmAccountId


###############################################################################################
# Function to set Customer CrmContactId
###############################################################################################
def set_customer_crm_contact_id(Quote, cpqRole, CrmContactId):
    if cpqRole == CPQ_BILL_TO:
        customer = Quote.BillToCustomer
    elif cpqRole == CPQ_SHIP_TO:
        customer = Quote.ShipToCustomer
    elif cpqRole == CPQ_END_USER:
        customer = Quote.EndUserCustomer

    if customer is not None:
        customer.CrmContactId = CrmContactId
        Quote.SaveCustomer(customer)


###############################################################################################
# Function to strip HTML Tags
###############################################################################################
def strip_html_tags(text):
    tag = False
    quote = False
    out = ""
    for letter in text:
        if letter == '<' and not quote:
            tag = True
        elif letter == '>' and not quote:
            tag = False
        elif (letter == '"' or letter == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + letter
    return out


###############################################################################################
# Function to get number of users types which have workflow permission on an action
###############################################################################################
def get_usergroup_count(User, actionId):
    user_type_code = SqlHelper.GetFirst("""
    SELECT COUNT(1) AS count
    FROM actions_usergroups
    WHERE action_id = {actionId}
    AND user_type_code={userTypeCode}
    """.format(actionId=actionId, userTypeCode=User.UserType.Id))

    return user_type_code.count


###############################################################################################
# Function block to get tab id
# The Tab Id value e.g. 1 for My Quotes, 2 for Waiting For Approval and 3 for Other Quotes.
###############################################################################################
def get_tabid(User, ownerId):
    # My Quotes
    if User.Id == ownerId: tabId = 1
    # Other Quotes
    else: tabId = 3

    return tabId


###############################################################################################
# Function to get number of actions which have been assigned to workflow
###############################################################################################
def get_actionid_count(tabId, Quote, actionId):
    action_id = SqlHelper.GetFirst("""
        SELECT COUNT(1) AS count
        FROM actions AS actions
        JOIN actions_status AS actions_status
        ON actions.action_id = actions_status.action_id
        WHERE actions.action_id = {actionId}
        AND actions_status.start_order_status_id={statusId}
        AND actions_status.tab_id={tabId}
    """.format(actionId=actionId, statusId=Quote.OrderStatus.Id, tabId=tabId))

    return action_id.count


###############################################################################################
# Function to check if user is allowed to trigger this action
###############################################################################################
def is_action_allowed(Quote, User, externalParameters, actionId):
    ownerId = externalParameters["ownerId"]

    # get tab Id, whether user is on My Quote, Other Quotes
    tabId = get_tabid(User, ownerId)
    # action count = 0 when this action is not assigned on worflow
    actionCount = get_actionid_count(tabId, Quote, actionId)
    # user type count = 0 when user type does not have permission on this action
    userTypeCount = get_usergroup_count(User, actionId)

    if actionCount > 0 and userTypeCount > 0:
        return True
    else:
        return False
