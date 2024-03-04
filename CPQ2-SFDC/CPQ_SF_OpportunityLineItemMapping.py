from CPQ_SF_FunctionModules import strip_html_tags
from CPQ_SF_CpqHelper import CL_CpqHelper

###############################################################################################
# Class CL_OpportunityLineItemMapping:
#       Class to store Opportunity Line Item Mappings
###############################################################################################
class CL_OpportunityLineItemMapping(CL_CpqHelper):
    ############################################################################
    # mapping is REQUIRED when --> CL_GeneralIntegrationSettings.UPDATE_OPP_LINE_ITEM = True
    ############################################################################
    mapping = dict()
    # INSERT API name of SObject field API used to store CPQ Item ID
    mapping["SALESFORCE_FIELD_NAME"] = "CPQ_Item_Id__c"
    # INSERT reserved name for Quote Item Custom Field used to store CRM ID
    mapping["CPQ_ITEM_FIELD_NAME"] = "CPQ_SF_OPP_LINE_ITEM"

    ###############################################################################################
    # Function for Opportunity Line Item Mapping
    ###############################################################################################
    def create_outbound_opplineitem_integration_mapping(self, Quote, cpqItem):
        salesforceLineItem = dict()
        # MANDATORY* mapping
        salesforceLineItem[self.mapping["SALESFORCE_FIELD_NAME"]] = cpqItem.Id

        salesforceLineItem["Description"] = cpqItem.Description
        salesforceLineItem["Quantity"] = cpqItem.Quantity
        salesforceLineItem["UnitPrice"] = cpqItem.ListPrice

        return salesforceLineItem

    ###############################################################################################
    # Function for Opportunity Line Item Mapping
    ###############################################################################################
    def update_outbound_opplineitem_integration_mapping(self, Quote, cpqItem):
        salesforceLineItem = dict()

        salesforceLineItem["Description"] = cpqItem.Description
        salesforceLineItem["Quantity"] = cpqItem.Quantity
        salesforceLineItem["UnitPrice"] = cpqItem.ListPrice

        return salesforceLineItem

    ###############################################################################################
    # Function for Product Master Mapping
    ###############################################################################################
    def product_integration_mapping(self, Quote, cpqItem):
        salesforceLineItem = dict()

        salesforceLineItem["Name"] = cpqItem.PartNumber
        #salesforceLineItem["CurrencyIsoCode"] = Quote.SelectedMarket.CurrencyCode

        return salesforceLineItem

    ###############################################################################################
    # Function for Product lookup Salesforce
    ###############################################################################################
    def get_product_lookups(self, Quote, cpqItem):
        productlookUps = list()

        lookUp = dict()
        lookUp["SalesforceField"] = "Name"
        lookUp["CpqLookUpValue"] = cpqItem.PartNumber
        lookUp["FieldType"] = self.TYPE_STRING
        productlookUps.append(lookUp)

        return productlookUps