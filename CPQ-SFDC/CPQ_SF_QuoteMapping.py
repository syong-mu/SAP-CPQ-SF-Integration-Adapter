from CPQ_SF_FunctionModules import strip_html_tags


###############################################################################################
# Function for Quote integration mapping
###############################################################################################
def quote_integration_mapping(Quote, TagParserQuote):
    salesforceQuote = dict()

    # Revision Number
    #salesforceQuote["Revision_Number__c"] = TagParserQuote.ParseString("<*CTX( Quote.Revision.RevisionNumber )*>")
    # Discount Percent
    #salesforceQuote["Discount_Percent__c"] = TagParserQuote.ParseString("<*CTX( Quote.Total.OverallDiscountPercent.MarketDecimal )*>")
    # Total List Price
    #salesforceQuote["Total_List_Price__c"] = TagParserQuote.ParseString("<*CTX( Quote.Total.TotalListPrice.DefaultDecimal )*>")
    # Total Net Price
    #salesforceQuote["Total_Net_Price__c"] = Quote.Total.TotalNetPrice

    return salesforceQuote
