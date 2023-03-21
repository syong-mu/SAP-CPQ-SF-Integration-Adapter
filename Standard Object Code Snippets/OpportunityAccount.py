def custom_object_mappings(self):
    mappings = list()
    # OBJECT DEFINITION FOR OPPORTUNITY ACCOUNT (ACCOUNT)
    mapping = dict()
    mapping["Name"] = "Opportunity_Account"
    mapping["Type"] = "Account"
    mapping["Query"] = self.build_soql_query(selectedFields="AccountId",
                                                    table="Opportunity",
                                                    condition="Id='"+self.Quote.GetCustomField("CPQ_SF_OPPORTUNITY_ID").Content+"'")
    mapping["Linked_To_Quote"] = False
    mapping["Inbound"] = True
    mapping["Outbound"] = True
    mapping["Create"] = False
    mappings.append(mapping)

    return mappings