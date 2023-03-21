from CPQ_SF_FunctionModules import get_quote_opportunity_id
def custom_object_mappings(self):
    mappings = list()

    # OBJECT DEFINITION FOR OPPORTUNITY PARTNER ROLE ACCOUNT (ACCOUNT)
    # Get Opportunity Id
    oppId = get_quote_opportunity_id(self.Quote)
    # Get Opportunity Account Id
    oppAccountId = ScriptExecutor.Execute("CPQ_SF_ACCOUNT_TAG", {"PROPERTY": "Id"})
    if oppId and oppAccountId:
        mapping = dict()
        condition = "OpportunityId='{oppId}' AND AccountToId <>'{oppAccountId}'".format(oppId=str(oppId), oppAccountId=str(oppAccountId))
        soql = self.build_soql_query(selectedFields="AccountToId",
                                        table="Partner",
                                        condition=condition)
        mapping["Name"] = "Opportunity_Partner_Role_Account"
        mapping["Type"] = "Account"
        mapping["Query"] = soql
        mapping["Linked_To_Quote"] = False
        mapping["Inbound"] = True
        mapping["Outbound"] = True
        mapping["Create"] = False
        mappings.append(mapping)

    return mappings