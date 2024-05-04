"""Script to clear salesforce item fields"""
from CPQ_SF_CustomObjectLineItemMapping import CL_CustomObjectLineItemMapping
from CPQ_SF_OpportunityLineItemMapping import CL_OpportunityLineItemMapping
from CPQ_SF_IntegrationSettings import CL_GeneralIntegrationSettings

object_mappings = sorted(CL_CustomObjectLineItemMapping.mappings, key=lambda x: x["Rank"])
opplineItem_mapping = CL_OpportunityLineItemMapping.mapping

# either feature to update opportunity product or update custom object are enabled
if CL_GeneralIntegrationSettings.UPDATE_OPP_LINE_ITEM\
or CL_GeneralIntegrationSettings.UPDATE_CUSTOM_ITEM_OBJECT:
    # clear mapped SF custom object Ids from copied items
    for item in Quote.Items:
        # feature to update opportunity product is enabled
        if CL_GeneralIntegrationSettings.UPDATE_OPP_LINE_ITEM:
            item[opplineItem_mapping["CPQ_ITEM_FIELD_NAME"]].Value  = ""
        # feature to update custom object line item is enabled
        if CL_GeneralIntegrationSettings.UPDATE_CUSTOM_ITEM_OBJECT:
            for mapping in object_mappings:
                item[mapping["CPQ_ITEM_FIELD_NAME"]].Value = ""
