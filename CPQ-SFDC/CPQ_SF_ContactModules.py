from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_ContactMapping import CL_OutboundContactMapping
from CPQ_SF_IntegrationReferences import CL_SalesforceApis as API, CL_CompositeRequestReferences as REF, CL_SalesforceCustomerRoles as SFROLES, CL_IntegrationReferences as INT_REF
from CPQ_SF_IntegrationSettings import CL_SalesforceContactObjects, CL_SalesforceIntegrationParams
from CPQ_SF_CpqHelper import CPQ_BILL_TO, CPQ_SHIP_TO, CPQ_END_USER, EVENT_CREATE, EVENT_UPDATE
from CPQ_SF_FunctionModules import get_quote_customer, get_customer_crm_account_id


###############################################################################################
# Class CL_ContactIntegrationModules:
#       Class to store integration functions related to contacts
###############################################################################################
class CL_ContactIntegrationModules(CL_SalesforceIntegrationModules):
    ###############################################################################################
    # Function to get the compositeRequest of a GET Contact request
    ###############################################################################################
    def build_cr_sobject_get_contact(self, contactId, cpqRoleContact):
        url = API.CR_GET_CONTACT_API.format(contactId=str(contactId))
        compositeRequest = self.build_cr_sobject_request(url, API.GET, None, cpqRoleContact)
        return compositeRequest

    ###############################################################################################
    # Function to get the compositeRequest of a PATCH Contact request
    ###############################################################################################
    def build_cr_sobject_patch_contact(self, contactId, cpqRoleContact, record):
        url = API.CR_GET_CONTACT_API.format(contactId=str(contactId))
        compositeRequest = self.build_cr_sobject_request(url, API.PATCH, record, cpqRoleContact)
        return compositeRequest

    ###############################################################################################
    # Function to get the compositeRequest to GET Opportunity Contacts
    ###############################################################################################
    def build_cr_sobject_get_opportunity_contacts(self, opportunityId):
        url = API.CR_GET_OPP_CONTACTS_API.format(opportunityId=str(opportunityId))
        compositeRequest = self.build_cr_sobject_request(url, API.GET, None, REF.GET_OPP_CONTACTS_REFID)
        return compositeRequest

    ###############################################################################################
    # Function to build Create Contact sObject POST API body
    ###############################################################################################
    def build_contact_sobject_create_record(self, cpqRole, event):
        body = dict()
        # Build records with values to send to Salesforce
        body["AccountId"] = get_customer_crm_account_id(self.Quote, cpqRole)
        if cpqRole == CPQ_BILL_TO:
            if event == EVENT_CREATE:
                body = CL_OutboundContactMapping().on_opportunity_create_bill_to_contact_mapping(self.Quote, self.TagParserQuote, self.Quote.BillToCustomer)
            elif event == EVENT_UPDATE:
                body.update(CL_OutboundContactMapping().on_opportunity_update_bill_to_contact_mapping(self.Quote, self.TagParserQuote, self.Quote.BillToCustomer))
            body.update(CL_OutboundContactMapping().on_opportunity_createupdate_bill_to_contact_mapping(self.Quote, self.TagParserQuote, self.Quote.BillToCustomer))

        elif cpqRole == CPQ_SHIP_TO:
            if event == EVENT_CREATE:
                body = CL_OutboundContactMapping().on_opportunity_create_ship_to_contact_mapping(self.Quote, self.TagParserQuote, self.Quote.ShipToCustomer)
            elif event == EVENT_UPDATE:
                body.update(CL_OutboundContactMapping().on_opportunity_update_ship_to_contact_mapping(self.Quote, self.TagParserQuote, self.Quote.ShipToCustomer))
            body.update(CL_OutboundContactMapping().on_opportunity_createupdate_ship_to_contact_mapping(self.Quote, self.TagParserQuote, self.Quote.ShipToCustomer))

        elif cpqRole == CPQ_END_USER:
            if event == EVENT_CREATE:
                body = CL_OutboundContactMapping().on_opportunity_create_end_customer_contact_mapping(self.Quote, self.TagParserQuote, self.Quote.EndUserCustomer)
            elif event == EVENT_UPDATE:
                body.update(CL_OutboundContactMapping().on_opportunity_update_end_customer_contact_mapping(self.Quote, self.TagParserQuote, self.Quote.EndUserCustomer))
            body.update(CL_OutboundContactMapping().on_opportunity_createupdate_end_customer_contact_mapping(self.Quote, self.TagParserQuote, self.Quote.EndUserCustomer))
        return body

    ###############################################################################################
    # Function to get create/update Contact Composite Payload
    ###############################################################################################
    def get_create_update_contact_composite_payload(self, event):
        compositePayload = list()
        contactMappings = [{"CpqRole": CPQ_BILL_TO, "Mapping": CL_OutboundContactMapping().BILL_TO_CONTACT, "CreateReference": REF.CREATE_BILL_TO_CONTACT, "UpdateReference": REF.UPDATE_BILL_TO_CONTACT},
                           {"CpqRole": CPQ_SHIP_TO, "Mapping": CL_OutboundContactMapping().SHIP_TO_CONTACT, "CreateReference": REF.CREATE_SHIP_TO_CONTACT, "UpdateReference": REF.UPDATE_SHIP_TO_CONTACT},
                           {"CpqRole": CPQ_END_USER, "Mapping": CL_OutboundContactMapping().END_CUSTOMER_CONTACT, "CreateReference": REF.CREATE_END_USER_CONTACT, "UpdateReference": REF.UPDATE_END_USER_CONTACT}]
        
        for contactMapping in contactMappings:
            if contactMapping["Mapping"] and contactMapping["Mapping"] != "":
                customer = get_quote_customer(self.Quote, contactMapping["CpqRole"])
                if customer:
                    if customer.CrmContactId == "" and customer.Active and customer.CompanyName != "":
                        customerRecord = self.build_contact_sobject_create_record(contactMapping["CpqRole"], event)
                        compositeRequest = self.get_sobject_post_payload_header(CL_SalesforceIntegrationParams.SF_CONTACT_OBJECT, contactMapping["CreateReference"])
                        compositeRequest["body"] = customerRecord
                        compositePayload.append(compositeRequest)
                    # Update contact
                    elif customer.CrmContactId != "" and customer.Active:
                        customerRecord = self.build_contact_sobject_create_record(contactMapping["CpqRole"], event)
                        compositeRequest = self.build_cr_sobject_patch_contact(customer.CrmContactId, contactMapping["UpdateReference"], customerRecord)
                        compositePayload.append(compositeRequest)

        return compositePayload

    ###############################################################################################
    # Function to get Contact Composite Payload
    ###############################################################################################
    def get_contact_composite_payload(self, compositePayload, contactType, opportunityId, opportunityResponse, referenceId):
        # OpportunityAccountFirstContact
        if contactType == CL_SalesforceContactObjects.SF_OPPORTUNITY_ACC_FIRST_CONTACT:
            if str(opportunityResponse["body"]["AccountId"]) != "":
                condition = "AccountId='{oppAccountId}'".format(oppAccountId=str(str(opportunityResponse["body"]["AccountId"])))
                soql = self.build_soql_query("Id", "Contact", condition)
                compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
                compositePayload.append(compositeRequest)
        # OpportunityFirstRole
        elif contactType == CL_SalesforceContactObjects.SF_OPPORTUNITY_FIRST_ROLE:
            condition = "OpportunityId='{opportunityId}'".format(opportunityId=str(opportunityId))
            soql = self.build_soql_query("ContactId", "OpportunityContactRole", condition)
            compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
            compositePayload.append(compositeRequest)
        # OpportunityBillToRole
        elif contactType == CL_SalesforceContactObjects.SF_OPPORTUNITY_BILL_TO_ROLE:
            condition = "OpportunityId='{opportunityId}' AND Role='Bill To'".format(opportunityId=str(opportunityId))
            soql = self.build_soql_query("ContactId", "OpportunityContactRole", condition)
            compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
            compositePayload.append(compositeRequest)
        # OpportunityShipToRole
        elif contactType == CL_SalesforceContactObjects.SF_OPPORTUNITY_SHIP_TO_ROLE:
            condition = "OpportunityId='{opportunityId}' AND Role = 'Ship To'".format(opportunityId=str(opportunityId))
            soql = self.build_soql_query("ContactId", "OpportunityContactRole", condition)
            compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
            compositePayload.append(compositeRequest)
        # OpportunityPrimaryRole
        elif contactType == CL_SalesforceContactObjects.SF_OPPORTUNITY_PRIMARY_ROLE:
            condition = "OpportunityId='{opportunityId}' AND IsPrimary=true".format(opportunityId=str(opportunityId))
            soql = self.build_soql_query("ContactId", "OpportunityContactRole", condition)
            compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
            compositePayload.append(compositeRequest)
        # OpportunityAccountBillToRole
        elif contactType == CL_SalesforceContactObjects.SF_OPPORTUNIY_ACC_BILL_TO_ROLE:
            if str(opportunityResponse["body"]["AccountId"]) != "":
                condition = "AccountId='{oppAccountId}' AND Role='Bill To'".format(oppAccountId=str(str(opportunityResponse["body"]["AccountId"])))
                soql = self.build_soql_query("ContactId", "AccountContactRole", condition)
                compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
                compositePayload.append(compositeRequest)
        # OpportunityAccountShipToRole
        elif contactType == CL_SalesforceContactObjects.SF_OPPORTUNITY_ACC_SHIP_TO_ROLE:
            if str(opportunityResponse["body"]["AccountId"]) != "":
                condition = "AccountId='{oppAccountId}' AND Role='Ship To'".format(oppAccountId=str(str(opportunityResponse["body"]["AccountId"])))
                soql = self.build_soql_query("ContactId", "AccountContactRole", condition)
                compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
                compositePayload.append(compositeRequest)
        # OpportunityAccountPrimaryContact
        elif contactType == CL_SalesforceContactObjects.SF_OPPORTUNIY_ACC_PRIMARY_CONTACT:
            if str(opportunityResponse["body"]["AccountId"]) != "":
                condition = "AccountId='{oppAccountId}' AND IsPrimary=true".format(oppAccountId=str(str(opportunityResponse["body"]["AccountId"])))
                soql = self.build_soql_query("ContactId", "AccountContactRole", condition)
                compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
                compositePayload.append(compositeRequest)
        # OpportunityPartnerAccountFirstContact
        elif contactType == CL_SalesforceContactObjects.SF_OPPORTUNITY_PARTNER_ACC_FIRST_CONTACT:
            if str(opportunityResponse["body"]["AccountId"]) != "":
                # Get Opportunity Partner Account
                condition = "OpportunityId='{opportunityId}'+AND+AccountToId!='{oppAccountId}'".format(opportunityId=str(opportunityId), oppAccountId=str(opportunityResponse["body"]["AccountId"]))
                soql = "SELECT+{field}+FROM+{table}+WHERE+{condition}".format(field="AccountToId", table="Partner", condition=str(condition))
                oppPartnerAccountId = ScriptExecutor.Execute("CPQ_SF_QUERY_TAG", {"QUERY": soql, "CACHING": False})
                # Get Contact
                condition = "AccountId='"+oppPartnerAccountId+"'"
                soql = self.build_soql_query("Id", "Contact", condition)
                compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
                compositePayload.append(compositeRequest)
        # OpportunityPartnerRoleAccountPrimaryContact
        elif contactType == CL_SalesforceContactObjects.SF_OPPORTUNITY_PARTNER_ROLE_ACC_PRIMARY_CONTACT:
            if str(opportunityResponse["body"]["AccountId"]) != "":
                # Get Opportunity Partner Account
                condition = "OpportunityId='{opportunityId}'+AND+AccountToId!='{oppAccountId}'".format(opportunityId=str(opportunityId), oppAccountId=str(opportunityResponse["body"]["AccountId"]))
                soql = "SELECT+{field}+FROM+{table}+WHERE+{condition}".format(field="AccountToId", table="Partner", condition=str(condition))
                oppPartnerAccountId = ScriptExecutor.Execute("CPQ_SF_QUERY_TAG", {"QUERY": soql, "CACHING": False})
                # Get Contact Id
                condition = "AccountId='{oppPartnerAccountId}' AND IsPrimary=true".format(oppPartnerAccountId=str(oppPartnerAccountId))
                soql = self.build_soql_query("ContactId", "AccountContactRole", condition)
                compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
                compositePayload.append(compositeRequest)
                # Get Contact
                # condition = "AccountId='@{"+REF.GET_OPP_PARTNER_ACC+".records[0].ContactId}'"
                # soql = self.build_soql_query("Id", "Contact", condition)
                # compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
                # compositePayload.append(compositeRequest)
        return compositePayload

    ###############################################################################################
    # Functions to build composite payload to assign contacts
    ###############################################################################################
    def build_composite_payload_assign_contacts(self, opportunityId, recordType, cpqRole, compositePayload):
        customer = get_quote_customer(self.Quote, cpqRole)
        # Get reference
        if cpqRole == CPQ_BILL_TO:
            referenceId = REF.ASSIGN_BILL_TO_CONTACT_REFID
        elif cpqRole == CPQ_SHIP_TO:
            referenceId = REF.ASSIGN_SHIP_TO_CONTACT_REFID
        elif cpqRole == CPQ_END_USER:
            referenceId = REF.ASSIGN_END_USER_CONTACT_REFID
        # Build payload
        if customer is not None:
            if customer.Active and customer.CrmContactId != "":
                # Get Opportunity to get AccountId
                if (recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_ACC_FIRST_CONTACT
                   or recordType == CL_SalesforceContactObjects.SF_OPPORTUNIY_ACC_BILL_TO_ROLE
                   or recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_ACC_SHIP_TO_ROLE
                   or recordType == CL_SalesforceContactObjects.SF_OPPORTUNIY_ACC_PRIMARY_CONTACT):
                    if next((req for req in compositePayload if req["referenceId"] == CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT), None) is None:
                        compositeRequest = self.build_cr_sobject_get_opportunity(opportunityId)
                        compositePayload.append(compositeRequest)
                # AccountId field variable
                refAccIdField = ".AccountId}"
                # OpportunityAccountFirstContact
                if recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_ACC_FIRST_CONTACT:
                    # Update Contact assignment
                    url = API.CR_GET_CONTACT_API.format(contactId=str(customer.CrmContactId))
                    record = dict()
                    record["AccountId"] = "@{" + CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT + refAccIdField
                    compositeRequest = self.build_cr_sobject_request(url, API.PATCH, record, referenceId)
                    compositePayload.append(compositeRequest)
                # OpportunityFirstRole
                elif recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_FIRST_ROLE:
                    # Update Contact assignment
                    record = dict()
                    record["OpportunityId"] = opportunityId
                    record["ContactId"] = customer.CrmContactId
                    compositeRequest = self.get_sobject_post_payload_header(CL_SalesforceIntegrationParams.SF_OPPORTUNITY_CONTACT_OBJECT, referenceId)
                    compositeRequest["body"] = record
                    compositePayload.append(compositeRequest)
                # OpportunityBillToRole
                elif recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_BILL_TO_ROLE:
                    # Update Contact assignment
                    record = dict()
                    record["OpportunityId"] = opportunityId
                    record["Role"] = SFROLES.SF_BILL_TO
                    record["ContactId"] = customer.CrmContactId
                    compositeRequest = self.get_sobject_post_payload_header(CL_SalesforceIntegrationParams.SF_OPPORTUNITY_CONTACT_OBJECT, referenceId)
                    compositeRequest["body"] = record
                    compositePayload.append(compositeRequest)
                # OpportunityShipToRole
                elif recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_SHIP_TO_ROLE:
                    # Update Contact assignment
                    record = dict()
                    record["OpportunityId"] = opportunityId
                    record["Role"] = SFROLES.SF_SHIP_TO
                    record["ContactId"] = customer.CrmContactId
                    compositeRequest = self.get_sobject_post_payload_header(CL_SalesforceIntegrationParams.SF_OPPORTUNITY_CONTACT_OBJECT, referenceId)
                    compositeRequest["body"] = record
                    compositePayload.append(compositeRequest)
                # OpportunityPrimaryRole
                elif recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_PRIMARY_ROLE:
                    # Update Contact assignment
                    record = dict()
                    record["OpportunityId"] = opportunityId
                    record["ContactId"] = customer.CrmContactId
                    record["IsPrimary"] = True
                    compositeRequest = self.get_sobject_post_payload_header(CL_SalesforceIntegrationParams.SF_OPPORTUNITY_CONTACT_OBJECT, referenceId)
                    compositeRequest["body"] = record
                    compositePayload.append(compositeRequest)
                # OpportunityAccountBillToRole & OpportunityAccountShipToRole
                elif recordType == CL_SalesforceContactObjects.SF_OPPORTUNIY_ACC_BILL_TO_ROLE or recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_ACC_SHIP_TO_ROLE:
                    record = dict()
                    # OpportunityAccountBillToRole
                    if recordType == CL_SalesforceContactObjects.SF_OPPORTUNIY_ACC_BILL_TO_ROLE:
                        # Update Contact assignment
                        record["Role"] = SFROLES.SF_BILL_TO
                    # OpportunityAccountShipToRole
                    elif recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_ACC_SHIP_TO_ROLE:
                        # Update Contact assignment
                        record["Role"] = SFROLES.SF_SHIP_TO
                    # Update Contact assignment
                    record["AccountId"] = "@{" + CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT + refAccIdField
                    record["ContactId"] = customer.CrmContactId
                    compositeRequest = self.get_sobject_post_payload_header(CL_SalesforceIntegrationParams.SF_ACCOUNT_CONTACT_ROLE, referenceId)
                    compositeRequest["body"] = record
                    compositePayload.append(compositeRequest)
                # OpportunityAccountPrimaryContact
                elif recordType == CL_SalesforceContactObjects.SF_OPPORTUNIY_ACC_PRIMARY_CONTACT:
                    # Update Contact assignment
                    record = dict()
                    record["AccountId"] = "@{" + CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT + refAccIdField
                    record["ContactId"] = customer.CrmContactId
                    record["IsPrimary"] = True
                    compositeRequest = self.get_sobject_post_payload_header(CL_SalesforceIntegrationParams.SF_ACCOUNT_CONTACT_ROLE, referenceId)
                    compositeRequest["body"] = record
                    compositePayload.append(compositeRequest)
                # OpportunityPartnerAccountFirstContact
                elif recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_PARTNER_ACC_FIRST_CONTACT:
                    # Get Opportunity Partner Account
                    compositeRequest = self.build_cr_sobject_get_opportunity_partners(opportunityId)
                    compositePayload.append(compositeRequest)
                    # Update Contact assignment
                    record = dict()
                    record["AccountId"] = "@{"+REF.GET_OPP_PARTNERS_REFID+".records[0].AccountToId}"
                    url = API.CR_GET_CONTACT_API.format(contactId=str(customer.CrmContactId))
                    compositeRequest = self.build_cr_sobject_request(url, API.PATCH, record, REF.UPDATE_CONTACT)
                    compositePayload.append(compositeRequest)
                # OpportunityPartnerRoleAccountPrimaryContact
                elif recordType == CL_SalesforceContactObjects.SF_OPPORTUNITY_PARTNER_ROLE_ACC_PRIMARY_CONTACT:
                    # Get Opportunity Partner Account
                    compositeRequest = self.build_cr_sobject_get_opportunity_partners(opportunityId)
                    compositePayload.append(compositeRequest)
                    # Update Contact assignment
                    record = dict()
                    record["AccountId"] = "@{"+REF.GET_OPP_PARTNERS_REFID+".records[0].AccountToId}"
                    record["ContactId"] = customer.CrmContactId
                    record["IsPrimary"] = True
                    compositeRequest = self.get_sobject_post_payload_header(CL_SalesforceIntegrationParams.SF_ACCOUNT_CONTACT_ROLE, referenceId)
                    compositeRequest["body"] = record
                    compositePayload.append(compositeRequest)
        return compositePayload
    ###############################################################################################
    # Function to get contact ids from Contacts response
    ###############################################################################################
    def get_contact_ids_from_response(self, contactsResponse, cpqRole):
        contactIds = list()
        # Get reference
        if cpqRole == CPQ_BILL_TO:
            referenceId = REF.BILL_TO_CONTACT_ID_REFID
        elif cpqRole == CPQ_SHIP_TO:
            referenceId = REF.SHIP_TO_CONTACT_ID_REFID
        elif cpqRole == CPQ_END_USER:
            referenceId = REF.END_USER_CONTACT_ID_REFID
        # Get contact Id
        contactsResponse = next((resp["body"]["records"] for resp in contactsResponse["compositeResponse"] if resp["referenceId"]==referenceId and resp["body"]["totalSize"]>0), None)
        if contactsResponse:
            for contact in contactsResponse:
                contactId = None
                for attr in contact:
                    if attr.Name != "attributes":
                        contactId = str(getattr(contact, attr.Name))
                        if contactId:
                            contactIds.append(contactId)
                        break
        return contactIds
    ###############################################################################################
    # Functions to assign Contacts
    ###############################################################################################
    def assign_contacts(self, bearerToken, opportunityId, opportunityResponse):
        response = None
        if opportunityResponse:
            # Check if contacts need to be assigned
            compositePayload = list()
            contactMappings = [{"CpqRole": CPQ_BILL_TO, "Mapping": CL_OutboundContactMapping().BILL_TO_CONTACT, "ContactIdReference": REF.BILL_TO_CONTACT_ID_REFID},
                                {"CpqRole": CPQ_SHIP_TO, "Mapping": CL_OutboundContactMapping().SHIP_TO_CONTACT, "ContactIdReference": REF.SHIP_TO_CONTACT_ID_REFID},
                                {"CpqRole": CPQ_END_USER, "Mapping": CL_OutboundContactMapping().END_CUSTOMER_CONTACT, "ContactIdReference": REF.END_USER_CONTACT_ID_REFID}]
            
            for contactMapping in contactMappings:
                if contactMapping["Mapping"] and contactMapping["Mapping"] != "":
                    # Get Contact Id
                    compositePayload = self.get_contact_composite_payload(compositePayload, contactMapping["Mapping"], opportunityId, opportunityResponse, contactMapping["ContactIdReference"])
            
            if compositePayload:
                contactsResponse = self.post_composite_request(bearerToken, compositePayload, INT_REF.REF_GET_CONTACTS)
                if contactsResponse:
                    # Assign Contacts
                    compositePayload = list()
                    for contactMapping in contactMappings:
                        if contactMapping["Mapping"] and contactMapping["Mapping"] != "":
                            customer = get_quote_customer(self.Quote, contactMapping["CpqRole"])
                            if customer:
                                if customer.Active and customer.CrmContactId != "":
                                    # Get contact Ids
                                    contactIds = self.get_contact_ids_from_response(contactsResponse, contactMapping["CpqRole"])
                                    # Assign Contact if it is different
                                    if customer.CrmContactId not in contactIds:
                                        compositePayload = self.build_composite_payload_assign_contacts(opportunityId, contactMapping["Mapping"], contactMapping["CpqRole"], compositePayload)
                    # Call API to Assign Contacts
                    if compositePayload:
                        # Check Assign Contact Permissions
                        permissionList = [  self.build_permission_checklist(CL_SalesforceIntegrationParams.SF_CONTACT_OBJECT, True, True),
                                            self.build_permission_checklist(CL_SalesforceIntegrationParams.SF_ACCOUNT_CONTACT_ROLE, True, True),
                                            self.build_permission_checklist(CL_SalesforceIntegrationParams.SF_OPPORTUNITY_CONTACT_OBJECT, True, True)]
                        response = self.post_composite_request(bearerToken, compositePayload, INT_REF.REF_ASSIGN_CONTACTS, permissionList)
        return response