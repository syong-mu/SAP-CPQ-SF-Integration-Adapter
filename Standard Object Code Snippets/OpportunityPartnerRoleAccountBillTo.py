from CPQ_SF_FunctionModules import get_quote_opportunity_id
def custom_object_mappings(self):
    mappings = list()

    # OBJECT DEFINITION FOR OPPORTUNITY PARTNER ROLE ACCOUNT BILL TO (ACCOUNT)
    # Get Opportunity Id
    oppId = get_quote_opportunity_id(self.Quote)
    if oppId:
        mapping = dict()
        condition = "OpportunityId='{oppId}' AND And Role = 'Bill To'".format(oppId=str(oppId))
        soql = self.build_soql_query(selectedFields="AccountToId",
                                        table="Partner",
                                        condition=condition)
        mapping["Name"] = "Opportunity_Partner_Role_Account_Bill_To"
        mapping["Type"] = "Account"
        mapping["Query"] = soql
        mapping["Linked_To_Quote"] = False
        mapping["Inbound"] = True
        mapping["Outbound"] = True
        mapping["Create"] = False
        mappings.append(mapping)

    return mappings