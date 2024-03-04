from CPQ_SF_IntegrationSettings import CL_SalesforceAccountObjects
from CPQ_SF_FunctionModules import strip_html_tags


###############################################################################################
# Class CL_InboundCustomerMapping:
#       Class to store customer mapping for Salesforce -> CPQ (Quote Creation/Update from CRM)
###############################################################################################
class CL_InboundCustomerMapping:
    # Map to CL_SalesforceAccountObjects
    BILL_TO = None
    SHIP_TO = None
    END_CUSTOMER = None

#####################
# BILL TO           #
###############################################################################################
# Function for Customer Bill To mappings on Quote Create (Salesforce -> CPQ)
###############################################################################################
    def on_quote_create_bill_to_mapping(self, cpqCustomer, salesforceCustomer):

        return cpqCustomer

###############################################################################################
# Function for Customer Bill To mappings on Quote Update (Salesforce -> CPQ)
###############################################################################################
    def on_quote_update_bill_to_mapping(self, cpqCustomer, salesforceCustomer):

        return cpqCustomer

###############################################################################################
# Function for Customer Bill To mappings on Quote Create & Update (Salesforce -> CPQ)
###############################################################################################
    def on_quote_createupdate_bill_to_mapping(self, cpqCustomer, salesforceCustomer):

        # cpqCustomer.CompanyName = str(salesforceCustomer["Name"])
        # cpqCustomer.City = str(salesforceCustomer["BillingCity"])
        # cpqCustomer.Address1 = str(salesforceCustomer["BillingStreet"])
        # cpqCustomer.CountryAbbreviation = str(salesforceCustomer["BillingCountry"])
        # cpqCustomer.ZipCode = str(salesforceCustomer["BillingPostalCode"])

        return cpqCustomer

#####################
# SHIP TO           #
###############################################################################################
# Function for Customer Ship To mappings on Quote Create (Salesforce -> CPQ)
###############################################################################################
    def on_quote_create_ship_to_mapping(self, cpqCustomer, salesforceCustomer):

        return cpqCustomer

###############################################################################################
# Function for Customer Ship To mappings on Quote Update (Salesforce -> CPQ)
###############################################################################################
    def on_quote_update_ship_to_mapping(self, cpqCustomer, salesforceCustomer):

        return cpqCustomer

###############################################################################################
# Function for Customer Ship To mappings on Quote Create & Update (Salesforce -> CPQ)
###############################################################################################
    def on_quote_createupdate_ship_to_mapping(self, cpqCustomer, salesforceCustomer):

        # cpqCustomer.CompanyName = str(salesforceCustomer["Name"])
        # cpqCustomer.City = str(salesforceCustomer["BillingCity"])
        # cpqCustomer.Address1 = str(salesforceCustomer["BillingStreet"])
        # cpqCustomer.CountryAbbreviation = str(salesforceCustomer["BillingCountry"])
        # cpqCustomer.ZipCode = str(salesforceCustomer["BillingPostalCode"])

        return cpqCustomer

#####################
# END CUSTOMER      #
###############################################################################################
# Function for Customer End Customer mappings on Quote Create (Salesforce -> CPQ)
###############################################################################################
    def on_quote_create_end_customer_mapping(self, cpqCustomer, salesforceCustomer):

        return cpqCustomer

###############################################################################################
# Function for Customer End Customer mappings on Quote Update (Salesforce -> CPQ)
###############################################################################################
    def on_quote_update_end_customer_mapping(self, cpqCustomer, salesforceCustomer):

        return cpqCustomer

###############################################################################################
# Function for Customer End Customer mappings on Quote Create & Update (Salesforce -> CPQ)
###############################################################################################
    def on_quote_createupdate_end_customer_mapping(self, cpqCustomer, salesforceCustomer):

        # cpqCustomer.CompanyName = str(salesforceCustomer["Name"])
        # cpqCustomer.City = str(salesforceCustomer["BillingCity"])
        # cpqCustomer.Address1 = str(salesforceCustomer["BillingStreet"])
        # cpqCustomer.CountryAbbreviation = str(salesforceCustomer["BillingCountry"])
        # cpqCustomer.ZipCode = str(salesforceCustomer["BillingPostalCode"])

        return cpqCustomer


###############################################################################################
# Class CL_OutboundCustomerMapping:
#       Class to store customer mapping for CPQ -> Salesforce (Opportunity Creation/Update from CRM)
###############################################################################################
class CL_OutboundCustomerMapping:
    # Map to CL_SalesforceAccountObjects
    BILL_TO = None
    SHIP_TO = None
    END_CUSTOMER = None

#####################
# BILL TO           #
###############################################################################################
# Function for Customer Bill To mappings on Quote Create (CPQ -> Salesforce)
###############################################################################################
    def on_opportunity_create_bill_to_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceCustomer = dict()

        return salesforceCustomer

###############################################################################################
# Function for Customer Bill To mappings on Quote Update (CPQ -> Salesforce)
###############################################################################################
    def on_opportunity_update_bill_to_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceCustomer = dict()

        return salesforceCustomer

###############################################################################################
# Function for Customer Bill To mappings on Quote Create & Update (CPQ -> Salesforce)
###############################################################################################
    def on_opportunity_createupdate_bill_to_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceCustomer = dict()

        # salesforceCustomer["Name"] = cpqCustomer.CompanyName
        # salesforceCustomer["BillingStreet"] = cpqCustomer.Address1
        # salesforceCustomer["CurrencyIsoCode"] = TagParserQuote.ParseString("<*CTX( Market.CurrencyCode )*>")

        return salesforceCustomer

#####################
# SHIP TO           #
###############################################################################################
# Function for Customer Ship To mappings on Quote Create (CPQ -> Salesforce)
###############################################################################################
    def on_opportunity_create_ship_to_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceCustomer = dict()

        return salesforceCustomer

###############################################################################################
# Function for Customer Ship To mappings on Quote Update (CPQ -> Salesforce)
###############################################################################################
    def on_opportunity_update_ship_to_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceCustomer = dict()

        return salesforceCustomer

###############################################################################################
# Function for Customer Ship To mappings on Quote Create & Update (CPQ -> Salesforce)
###############################################################################################
    def on_opportunity_createupdate_ship_to_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceCustomer = dict()

        # salesforceCustomer["Name"] = cpqCustomer.CompanyName
        # salesforceCustomer["BillingStreet"] = cpqCustomer.Address1
        # salesforceCustomer["CurrencyIsoCode"] = TagParserQuote.ParseString("<*CTX( Market.CurrencyCode )*>")

        return salesforceCustomer

#####################
# END CUSTOMER      #
###############################################################################################
# Function for Customer End Customer mappings on Quote Create (CPQ -> Salesforce)
###############################################################################################
    def on_opportunity_create_end_customer_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceCustomer = dict()

        return salesforceCustomer

###############################################################################################
# Function for Customer End Customer mappings on Quote Update (CPQ -> Salesforce)
###############################################################################################
    def on_opportunity_update_end_customer_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceCustomer = dict()

        return salesforceCustomer

###############################################################################################
# Function for Customer End Customer mappings on Quote Create & Update (CPQ -> Salesforce)
###############################################################################################
    def on_opportunity_createupdate_end_customer_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceCustomer = dict()

        # salesforceCustomer["Name"] = cpqCustomer.CompanyName
        # salesforceCustomer["BillingStreet"] = cpqCustomer.Address1
        # salesforceCustomer["CurrencyIsoCode"] = TagParserQuote.ParseString("<*CTX( Market.CurrencyCode )*>")

        return salesforceCustomer
