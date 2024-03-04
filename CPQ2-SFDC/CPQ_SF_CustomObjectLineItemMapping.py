from CPQ_SF_CpqHelper import CL_CpqHelper
from CPQ_SF_FunctionModules import strip_html_tags

###############################################################################################
# Class CL_CustomObjectLineItemMapping:
#       Class to store Quote Items to Custom Object Mappings
###############################################################################################
class CL_CustomObjectLineItemMapping(CL_CpqHelper):
    mappings = list()

    # mapping = dict()
    # INSERT API name of SObject field which refer to CPQ Item ID
    # mapping["SALESFORCE_FIELD_NAME"] = "CPQ_Item_Id__c"
    # INSERT reserved name for Quote Item Custom Field used to store CRM ID
    # mapping["CPQ_ITEM_FIELD_NAME"] = "CPQ_SF_ASSET_CRM_ID"

    # mapping["ObjectType"] = "Asset"
    # mapping["Rank"] = 1
    # mappings.append(mapping)

    ###############################################################################################
    # Function that stores condition on whether line item should be created/updated
    ###############################################################################################
    def custom_object_item_condition(self, Quote, cpqItem, customObjectName):
        condition = False
        # An If condition for each object
        # if customObjectName == "Asset":
        #     # Condition
        #     if cpqItem.ProductTypeName == "Service":
        #         condition = True

        return condition

    ###############################################################################################
    # Function that stores the Look up mapping of the custom objects
    ###############################################################################################
    def custom_object_item_lookups(self, Quote, customObjectName):
        customlookUps = list()

        # if customObjectName == "Asset":
        #     lookUp = dict()
        #     lookUp["SalesforceField"] = "Quote_ID__c"
        #     lookUp["CpqLookUpValue"] = Quote.Id
        #     lookUp["FieldType"] = self.TYPE_FLOAT
        #     customlookUps.append(lookUp)

        #     lookUp = dict()
        #     lookUp["SalesforceField"] = "Owner_ID__c"
        #     lookUp["CpqLookUpValue"] = Quote.OwnerId
        #     lookUp["FieldType"] = self.TYPE_FLOAT
        #     customlookUps.append(lookUp)

        return customlookUps

    ###############################################################################################
    # Function that stores the line item mappings per object
    ###############################################################################################
    def create_outbound_custom_object_item_mapping(self, Quote, cpqItem, customObjectName):
        customObjectLineItem = dict()

        # An If condition for each object
        # if customObjectName == "Asset":
        #     # MANDATORY* mapping
        #     customObjectLineItem[self.mapping["SALESFORCE_FIELD_NAME"]] = cpqItem.Id

        #     customObjectLineItem["CurrencyIsoCode"] = Quote.SelectedMarket.CurrencyCode
        return customObjectLineItem

    ###############################################################################################
    # Function that stores the line item mappings per object
    ###############################################################################################
    def update_outbound_custom_object_item_mapping(self, Quote, cpqItem, customObjectName):
        customObjectLineItem = dict()

        # An If condition for each object
        # if customObjectName == "Asset":
        #     customObjectLineItem["CurrencyIsoCode"] = Quote.SelectedMarket.CurrencyCode

        return customObjectLineItem