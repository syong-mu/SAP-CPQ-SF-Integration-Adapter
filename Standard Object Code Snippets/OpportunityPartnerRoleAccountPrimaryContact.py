from CPQ_SF_FunctionModules import get_quote_opportunity_id
def custom_object_mappings(self):
    mappings = list()

    # OBJECT DEFINITION FOR OPPORTUNITY PARTNER ROLE ACCOUNT PRIMARY CONTACT (CONTACT)
    # Get Opportunity Id
    oppId = get_quote_opportunity_id(self.Quote)
    # Get Opportunity Account Id
    oppAccountId = ScriptExecutor.Execute("CPQ_SF_ACCOUNT_TAG", {"PROPERTY": "Id"})
    if oppId and oppAccountId:
        # Get Opportunity Partner Account
        condition = "OpportunityId='{opportunityId}' AND AccountToId !='{oppAccountId}'".format(opportunityId=str(oppId), oppAccountId=str(oppAccountId))
        soql = self.build_soql_query("AccountToId", "Partner", condition)
        oppPartnerAccountId = ScriptExecutor.Execute("CPQ_SF_QUERY_TAG", {"QUERY": soql})
        if oppPartnerAccountId:
            # Get Contact
            condition = "AccountId='{oppPartnerAccountId}' AND IsPrimary=true".format(oppPartnerAccountId=str(oppPartnerAccountId))
            soql = self.build_soql_query("ContactId", "AccountContactRole", condition)
            mapping = dict()
            mapping["Name"] = "Opportunity_Partner_Role_Account_Primary_Contact"
            mapping["Type"] = "Contact"
            mapping["Query"] = soql
            mapping["Linked_To_Quote"] = False
            mapping["Inbound"] = True
            mapping["Outbound"] = True
            mapping["Create"] = False
            mappings.append(mapping)

    return mappings