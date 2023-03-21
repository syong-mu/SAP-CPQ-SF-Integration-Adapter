def custom_object_mappings(self):
    mappings = list()

    # OBJECT DEFINITION FOR OPPORTUNITY ACCOUNT PRIMARY CONTACT (CONTACT)
    # Get Opportunity Account Id
    oppAccountId = ScriptExecutor.Execute("CPQ_SF_ACCOUNT_TAG", {"PROPERTY": "Id"})
    if oppAccountId:
        mapping = dict()
        condition = "AccountId='{oppAccountId}' AND IsPrimary=true'".format(oppAccountId=str(oppAccountId))
        soql = self.build_soql_query("ContactId", "AccountContactRole", condition)
        mapping["Name"] = "Opportunity_Account_Primary_Contact"
        mapping["Type"] = "Contact"
        mapping["Query"] = soql
        mapping["Linked_To_Quote"] = False
        mapping["Inbound"] = True
        mapping["Outbound"] = True
        mapping["Create"] = False
        mappings.append(mapping)

    return mappings