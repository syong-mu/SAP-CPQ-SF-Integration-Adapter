from CPQ_SF_FunctionModules import strip_html_tags


###############################################################################################
# Function for Quote integration mapping
###############################################################################################
def quote_integration_mapping(Quote):
    salesforceQuote = dict()

    # # Total List Price
    # salesforceQuote["Total_List_Price__c"] = Quote.Totals.ListPrice

    return salesforceQuote
