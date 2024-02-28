from CPQ_SF_IntegrationSettings import CL_SalesforceContactObjects
from CPQ_SF_FunctionModules import strip_html_tags


###############################################################################################
# Class CL_InboundContactMapping:
#       Class to store contact mapping for Salesforce -> CPQ (Quote Creation/Update from CRM)
###############################################################################################
class CL_InboundContactMapping:
    # Map to CL_SalesforceContactObjects
    BILL_TO_CONTACT = None
    SHIP_TO_CONTACT = None
    END_CUSTOMER_CONTACT = None

    #####################
    # BILL TO           #
    ###############################################################################################
    # Function for Contact Bill To mappings on Quote Create (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_create_bill_to_contact_mapping(self, cpqCustomer, salesforceContact):

        return cpqCustomer

    ###############################################################################################
    # Function for Contact Bill To mappings on Quote Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_update_bill_to_contact_mapping(self, cpqCustomer, salesforceContact):

        return cpqCustomer

    ###############################################################################################
    # Function for Contact Bill To mappings on Quote Create & Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_createupdate_bill_to_contact_mapping(self, cpqCustomer, salesforceContact):

        # cpqCustomer.FirstName = str(salesforceContact["FirstName"])
        # cpqCustomer.LastName = str(salesforceContact["LastName"])

        return cpqCustomer

    #####################
    # SHIP TO           #
    ###############################################################################################
    # Function for Contact Ship To mappings on Quote Create (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_create_ship_to_contact_mapping(self, cpqCustomer, salesforceContact):

        return cpqCustomer

    ###############################################################################################
    # Function for Contact Ship To mappings on Quote Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_update_ship_to_contact_mapping(self, cpqCustomer, salesforceContact):

        return cpqCustomer

    ###############################################################################################
    # Function for Contact Ship To mappings on Quote Create & Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_createupdate_ship_to_contact_mapping(self, cpqCustomer, salesforceContact):

        # cpqCustomer.FirstName = str(salesforceContact["FirstName"])
        # cpqCustomer.LastName = str(salesforceContact["LastName"])

        return cpqCustomer

    #####################
    # END CUSTOMER      #
    ###############################################################################################
    # Function for Contact End Customer mappings on Quote Create (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_create_end_customer_contact_mapping(self, cpqCustomer, salesforceContact):

        return cpqCustomer

    ###############################################################################################
    # Function for Contact End Customer mappings on Quote Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_update_end_customer_contact_mapping(self, cpqCustomer, salesforceContact):

        return cpqCustomer

    ###############################################################################################
    # Function for Contact End Customer mappings on Quote Create & Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_createupdate_end_customer_contact_mapping(self, cpqCustomer, salesforceContact):

        # cpqCustomer.FirstName = str(salesforceContact["FirstName"])
        # cpqCustomer.LastName = str(salesforceContact["LastName"])

        return cpqCustomer


###############################################################################################
# Class CL_OutboundContactMapping:
#       Class to store contact mapping for Salesforce -> CPQ (Opportunity Creation/Update from CRM)
###############################################################################################
class CL_OutboundContactMapping:
    # Map to CL_SalesforceContactObjects
    BILL_TO_CONTACT = None
    SHIP_TO_CONTACT = None
    END_CUSTOMER_CONTACT = None

    #####################
    # BILL TO           #
    ###############################################################################################
    # Function for Contact Bill To mappings on Quote Create (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_create_bill_to_contact_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceContact = dict()

        return salesforceContact

    ###############################################################################################
    # Function for Contact Bill To mappings on Quote Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_update_bill_to_contact_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceContact = dict()

        return salesforceContact

    ###############################################################################################
    # Function for Contact Bill To mappings on Quote Create & Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_createupdate_bill_to_contact_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceContact = dict()

        # salesforceContact["FirstName"] = cpqCustomer.FirstName
        # salesforceContact["LastName"] = cpqCustomer.LastName
        # salesforceContact["CurrencyIsoCode"] = TagParserQuote.ParseString("<*CTX( Market.CurrencyCode )*>")

        return salesforceContact

    #####################
    # SHIP TO           #
    ###############################################################################################
    # Function for Contact Ship To mappings on Quote Create (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_create_ship_to_contact_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceContact = dict()

        return salesforceContact

    ###############################################################################################
    # Function for Contact Ship To mappings on Quote Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_update_ship_to_contact_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceContact = dict()

        return salesforceContact

    ###############################################################################################
    # Function for Contact Ship To mappings on Quote Create & Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_createupdate_ship_to_contact_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceContact = dict()

        # salesforceContact["FirstName"] = cpqCustomer.FirstName
        # salesforceContact["LastName"] = cpqCustomer.LastName
        # salesforceContact["CurrencyIsoCode"] = TagParserQuote.ParseString("<*CTX( Market.CurrencyCode )*>")

        return salesforceContact

    #####################
    # END CUSTOMER      #
    ###############################################################################################
    # Function for Contact End Customer mappings on Quote Create (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_create_end_customer_contact_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceContact = dict()

        return salesforceContact

    ###############################################################################################
    # Function for Contact End Customer mappings on Quote Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_update_end_customer_contact_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceContact = dict()

        return salesforceContact

    ###############################################################################################
    # Function for Contact End Customer mappings on Quote Create & Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_createupdate_end_customer_contact_mapping(self, Quote, TagParserQuote, cpqCustomer):
        salesforceContact = dict()

        # salesforceContact["FirstName"] = cpqCustomer.FirstName
        # salesforceContact["LastName"] = cpqCustomer.LastName
        # salesforceContact["CurrencyIsoCode"] = TagParserQuote.ParseString("<*CTX( Market.CurrencyCode )*>")

        return salesforceContact
