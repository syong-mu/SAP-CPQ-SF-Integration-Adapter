from CPQ_SF_CustomObjectLineItemMapping import CL_CustomObjectLineItemMapping
from CPQ_SF_OpportunityLineItemMapping import CL_OpportunityLineItemMapping

object_mappings = sorted(CL_CustomObjectLineItemMapping.mappings, key=lambda x: x["Rank"])
opplineItem_mapping = CL_OpportunityLineItemMapping.mapping

# clear mapped SF custom object Ids from copied items
for item in CopiedItems:
    item[opplineItem_mapping["CPQ_ITEM_FIELD_NAME"]].Value  = ""
    for mapping in object_mappings:
        item[mapping["CPQ_ITEM_FIELD_NAME"]].Value = ""