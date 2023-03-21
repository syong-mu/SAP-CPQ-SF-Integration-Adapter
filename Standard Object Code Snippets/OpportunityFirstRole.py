from CPQ_SF_FunctionModules import get_quote_opportunity_id
def custom_object_mappings(self):
    mappings = list()

    # OBJECT DEFINITION FOR OPPORTUNITY FIRST ROLE (CONTACT)
    # Get Opportunity Id
    oppId = get_quote_opportunity_id(self.Quote)
    if oppId:
        mapping = dict()
        condition = "OpportunityId='{opportunityId}'".format(opportunityId=str(oppId))
        soql = self.build_soql_query("ContactId", "OpportunityContactRole", condition)
        mapping["Name"] = "Opportunity_First_Role"
        mapping["Type"] = "Contact"
        mapping["Query"] = soql
        mapping["Linked_To_Quote"] = False
        mapping["Inbound"] = True
        mapping["Outbound"] = True
        mapping["Create"] = False
        mappings.append(mapping)

    return mappings