def custom_object_mappings(self):
    mappings = list()

    # OBJECT DEFINITION FOR OPPORTUNITY ACCOUNT PARTNER ROLE ACCOUNT (ACCOUNT)
    # Get Opportunity Account Id
    oppAccountId = ScriptExecutor.Execute("CPQ_SF_ACCOUNT_TAG", {"PROPERTY": "Id"})
    if oppAccountId:
        mapping = dict()
        condition = "AccountToId='{opportunityAccountId}'".format(opportunityAccountId=str(oppAccountId))
        soql = self.build_soql_query(   selectedFields="AccountFromId",
                                        table="Partner",
                                        condition=condition)
        mapping["Name"] = "Opportunity_Account_Partner_Role_Account"
        mapping["Type"] = "Account"
        mapping["Query"] = soql
        mapping["Linked_To_Quote"] = False
        mapping["Inbound"] = True
        mapping["Outbound"] = True
        mapping["Create"] = False
        mappings.append(mapping)

    return mappings