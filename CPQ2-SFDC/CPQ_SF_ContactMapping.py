from CPQ_SF_IntegrationSettings import CL_SalesforceContactObjects
from CPQ_SF_FunctionModules import strip_html_tags, get_country_code_from_abrev3


###############################################################################################
# Class CL_InboundContactMapping:
#       Class to store contact mapping for Salesforce -> CPQ (Quote Creation/Update from CRM)
###############################################################################################
class CL_InboundContactMapping:

    inboundContactMappings = list()
    
    # mapping = dict()
    # mapping["CpqPartnerFunction"] = "CP"
    # mapping["SalesforceContact"] = CL_SalesforceContactObjects.SF_OPPORTUNITY_SHIP_TO_ROLE
    # inboundContactMappings.append(mapping)
    
    # mapping = dict()
    # mapping["CpqPartnerFunction"] = "PY"
    # mapping["SalesforceContact"] = CL_SalesforceContactObjects.SF_OPPORTUNITY_BILL_TO_ROLE
    # inboundContactMappings.append(mapping)

    ###############################################################################################
    # Function for Contact Bill To mappings on Quote Create (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_create_contact_mapping(self, cpqPartnerFunction, cpqBusinessPartner, salesforceContact):

        return cpqBusinessPartner

    ###############################################################################################
    # Function for Contact Bill To mappings on Quote Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_update_contact_mapping(self, cpqPartnerFunction, cpqBusinessPartner, salesforceContact):

        return cpqBusinessPartner

    ###############################################################################################
    # Function for Contact Bill To mappings on Quote Create & Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_createupdate_contact_mapping(self, cpqPartnerFunction, cpqBusinessPartner, salesforceContact):

        # if cpqPartnerFunction == "CP" or cpqPartnerFunction == "PY":
        #     cpqBusinessPartner.FirstName = str(salesforceContact["FirstName"])
        #     cpqBusinessPartner.LastName = str(salesforceContact["LastName"])
        #     cpqBusinessPartner.Name = str(salesforceContact["Name"])
        #     cpqBusinessPartner.CityName = str(salesforceContact["BillingCity"])
        #     if str(salesforceContact["BillingStreet"]) != "None":
        #         cpqBusinessPartner.AddressName = str(salesforceContact["BillingStreet"])
        #     else:
        #         cpqBusinessPartner.AddressName = str()
        #     # Set country using get_country_code_from_abrev3()
        #     cpqBusinessPartner.Country = get_country_code_from_abrev3(str(salesforceContact["BillingCountry"]))
        #     cpqBusinessPartner.PostalCode = str(salesforceContact["BillingPostalCode"])

        return cpqBusinessPartner

###############################################################################################
# Class CL_OutboundContactMapping:
#       Class to store contact mapping for Salesforce -> CPQ (Opportunity Creation/Update from CRM)
###############################################################################################
class CL_OutboundContactMapping:

    outboundContactMappings = list()
    
    # mapping = dict()
    # mapping["CpqPartnerFunction"] = "CP"
    # mapping["SalesforceContact"] = CL_SalesforceContactObjects.SF_OPPORTUNITY_SHIP_TO_ROLE
    # outboundContactMappings.append(mapping)
    
    # mapping = dict()
    # mapping["CpqPartnerFunction"] = "PY"
    # mapping["SalesforceContact"] = CL_SalesforceContactObjects.SF_OPPORTUNITY_BILL_TO_ROLE
    # outboundContactMappings.append(mapping)

    ###############################################################################################
    # Function for Contact mappings on Quote Create (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_create_contact_mapping(self, Quote, cpqBusinessPartner):
        salesforceContact = dict()

        return salesforceContact

    ###############################################################################################
    # Function for Contact mappings on Quote Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_update_contact_mapping(self, Quote, cpqBusinessPartner):
        salesforceContact = dict()

        return salesforceContact

    ###############################################################################################
    # Function for Contact mappings on Quote Create & Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opportunity_createupdate_contact_mapping(self, Quote, cpqBusinessPartner):
        salesforceContact = dict()

        # salesforceContact["FirstName"] = cpqBusinessPartner.FirstName
        # salesforceContact["LastName"] = cpqBusinessPartner.LastName
        # salesforceContact["CurrencyIsoCode"] = Quote.SelectedMarket.CurrencyCode

        return salesforceContact
