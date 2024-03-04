from CPQ_SF_FunctionModules import strip_html_tags


###############################################################################################
# OUTBOUND (CPQ -> Salesforce)
###############################################################################################
###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_opp_create_outbound_opportunity_integration_mapping(Quote):
    opportunity = dict()

    opportunity["CloseDate"] = Quote.EffectiveDate.ToString("yyyy-MM-dd")

    return opportunity


###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_opp_update_outbound_opportunity_integration_mapping(Quote):
    opportunity = dict()

    return opportunity


###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_opp_createupdate_outbound_opportunity_integration_mapping(Quote):
    opportunity = dict()

    opportunity["Name"] = Quote.GetCustomField("CPQ_SF_OPPORTUNITY_NAME").Value

    return opportunity


###############################################################################################
# INBOUND (Salesforce -> CPQ)
###############################################################################################
###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_quote_create_inbound_opportunity_integration_mapping(Quote, opportunity):

    pass


###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_quote_update_inbound_opportunity_integration_mapping(Quote, opportunity):

    pass


###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_quote_createupdate_inbound_opportunity_integration_mapping(Quote, opportunity):

    Quote.GetCustomField("CPQ_SF_OPPORTUNITY_NAME").Value = str(opportunity["Name"])
