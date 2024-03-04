from CPQ_SF_Configuration import CL_SalesforceSettings
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_IntegrationSettings import CL_SalesforceAccountObjects, CL_SalesforceContactObjects, CL_SalesforceIntegrationParams
from CPQ_SF_CpqHelper import CPQ_BILL_TO, CPQ_SHIP_TO, CPQ_END_USER, EVENT_CREATE, EVENT_UPDATE
from CPQ_SF_IntegrationReferences import CL_SalesforceApis as API, CL_CompositeRequestReferences as REF, CL_SalesforceCustomerRoles as SFROLES, CL_IntegrationReferences as INT_REF
from CPQ_SF_CustomerMapping import CL_OutboundCustomerMapping, CL_InboundCustomerMapping
from CPQ_SF_ContactMapping import CL_InboundContactMapping
from CPQ_SF_FunctionModules import get_customer_crm_account_id, get_quote_customer, set_customer_on_quote, set_empty_customer_on_quote


###############################################################################################
# Class CL_CustomerModules:
#       Class to store integration functions related to Customers(Accounts)
###############################################################################################
class CL_CustomerModules(CL_SalesforceIntegrationModules):
    ###############################################################################################
    # Function to get the compositeRequest of a GET Account request
    ###############################################################################################
    def build_cr_sobject_get_account(self, accountId, cpqRole):
        url = API.CR_GET_ACCOUNT_API.format(version=str(CL_SalesforceSettings.SALESFORCE_VERSION), accountId=str(accountId))
        compositeRequest = self.build_cr_sobject_request(url, API.GET, None, cpqRole)
        return compositeRequest

    ###############################################################################################
    # Function to get the compositeRequest of a PATCH Account request
    ###############################################################################################
    def build_cr_sobject_patch_account(self, accountId, cpqRole, record):
        url = API.CR_GET_ACCOUNT_API.format(version=str(CL_SalesforceSettings.SALESFORCE_VERSION), accountId=str(accountId))
        compositeRequest = self.build_cr_sobject_request(url, API.PATCH, record, cpqRole)
        return compositeRequest

    ###############################################################################################
    # Function to build Customer Role sObject POST API body
    ###############################################################################################
    def build_account_sobject_create_record(self, cpqRole, event):
        body = dict()
        if cpqRole == CPQ_BILL_TO:
            if event == EVENT_CREATE:
                body = CL_OutboundCustomerMapping().on_opportunity_create_bill_to_mapping(self.Quote, self.TagParserQuote, self.Quote.BillToCustomer)
            elif event == EVENT_UPDATE:
                body = CL_OutboundCustomerMapping().on_opportunity_update_bill_to_mapping(self.Quote, self.TagParserQuote, self.Quote.BillToCustomer)
            body.update(CL_OutboundCustomerMapping().on_opportunity_createupdate_bill_to_mapping(self.Quote, self.TagParserQuote, self.Quote.BillToCustomer))

        elif cpqRole == CPQ_SHIP_TO:
            if event == EVENT_CREATE:
                body = CL_OutboundCustomerMapping().on_opportunity_create_ship_to_mapping(self.Quote, self.TagParserQuote, self.Quote.ShipToCustomer)
            elif event == EVENT_UPDATE:
                body.update(CL_OutboundCustomerMapping().on_opportunity_update_ship_to_mapping(self.Quote, self.TagParserQuote, self.Quote.ShipToCustomer))
            body.update(CL_OutboundCustomerMapping().on_opportunity_createupdate_ship_to_mapping(self.Quote, self.TagParserQuote, self.Quote.ShipToCustomer))

        elif cpqRole == CPQ_END_USER:
            if event == EVENT_CREATE:
                body = CL_OutboundCustomerMapping().on_opportunity_create_end_customer_mapping(self.Quote, self.TagParserQuote, self.Quote.EndUserCustomer)
            elif event == EVENT_UPDATE:
                body.update(CL_OutboundCustomerMapping().on_opportunity_update_end_customer_mapping(self.Quote, self.TagParserQuote, self.Quote.EndUserCustomer))
            body.update(CL_OutboundCustomerMapping().on_opportunity_createupdate_end_customer_mapping(self.Quote, self.TagParserQuote, self.Quote.EndUserCustomer))
        return body

    ###############################################################################################
    # Function to get Create/Update Account Composite Payload
    ###############################################################################################
    def get_create_update_account_composite_payload(self, event):
        compositePayload = list()
        customerMappings = [{"CpqRole": CPQ_BILL_TO, "Mapping": CL_OutboundCustomerMapping.BILL_TO, "CreateReference": REF.CREATE_BILL_TO_ACC, "UpdateReference": REF.UPDATE_BILL_TO_ACC},
                            {"CpqRole": CPQ_SHIP_TO, "Mapping": CL_OutboundCustomerMapping.SHIP_TO, "CreateReference": REF.CREATE_SHIP_TO_ACC, "UpdateReference": REF.UPDATE_SHIP_TO_ACC},
                            {"CpqRole": CPQ_END_USER, "Mapping": CL_OutboundCustomerMapping.END_CUSTOMER, "CreateReference": REF.CREATE_END_USER_ACC, "UpdateReference": REF.UPDATE_END_USER_ACC}]

        for customerMapping in customerMappings:
            if customerMapping["Mapping"]:
                customer = get_quote_customer(self.Quote, customerMapping["CpqRole"])
                if customer:
                    # Create account
                    if customer.CrmAccountId == "" and customer.Active and customer.CompanyName != "":
                        customerRecord = self.build_account_sobject_create_record(customerMapping["CpqRole"], event)
                        compositeRequest = self.get_sobject_post_payload_header(CL_SalesforceIntegrationParams.SF_ACCOUNT_OBJECT, customerMapping["CreateReference"])
                        compositeRequest["body"] = customerRecord
                        compositePayload.append(compositeRequest)
                    # Update account
                    elif customer.CrmAccountId != "" and customer.Active:
                        customerRecord = self.build_account_sobject_create_record(customerMapping["CpqRole"], event)
                        compositeRequest = self.build_cr_sobject_patch_account(customer.CrmAccountId, customerMapping["UpdateReference"], customerRecord)
                        compositePayload.append(compositeRequest)

        return compositePayload

    ###############################################################################################
    # Function to get accountId of customers (Accounts & Partners)
    ###############################################################################################
    def get_opportunity_customers_accountid(self, bearerToken, customerType, opportunityResponse, opportunityPartnersResp):
        accountId = None
        # Opportunity Main Account
        oppMainAccount = str(opportunityResponse["body"]["AccountId"])
        if customerType == CL_SalesforceAccountObjects.SF_OPPORTUNITY_ACC:
            accountId = oppMainAccount
        # OpportunityAccountPartnerRoleAccount
        elif customerType == CL_SalesforceAccountObjects.SF_OPPORTUNITY_ACC_PARTNER_ROLE_ACC:
            compositePayload = list()
            compositeRequest = self.build_cr_get_opp_acc_partner_role(oppMainAccount, REF.GET_OPP_ACC_PARTNER_ROLE_ACC)
            compositePayload.append(compositeRequest)
            if compositePayload:
                response = self.post_composite_request(bearerToken, compositePayload, INT_REF.REF_GET_OPP_ACC_PARTNER_ROLE_ACC)
                if response:
                    partnerResp = next((resp["body"] for resp in response["compositeResponse"] if resp["referenceId"] == REF.GET_OPP_ACC_PARTNER_ROLE_ACC), None)
                    if partnerResp:
                        accountId = next((str(resp["AccountFromId"]) for resp in partnerResp["body"]["records"]), None)
        else:
            # Opportunity Partners
            if opportunityPartnersResp:
                # OpportunityPartnerRoleAccountBillTo
                if customerType == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ACC_BILL_TO:
                    partnerResp = next((resp for resp in opportunityPartnersResp["body"]["records"] if resp["Role"] == SFROLES.SF_BILL_TO and resp["AccountToId"] != oppMainAccount), None)
                    if partnerResp:
                        accountId = str(partnerResp["AccountToId"])
                # OpportunityPartnerRoleAccountShipTo
                elif customerType == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ACC_SHIP_TO:
                    partnerResp = next((resp for resp in opportunityPartnersResp["body"]["records"] if resp["Role"] == SFROLES.SF_SHIP_TO and resp["AccountToId"] != oppMainAccount), None)
                    if partnerResp:
                        accountId = str(partnerResp["AccountToId"])
                # OpportunityPartnerRoleAccountEndUser
                elif customerType == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ACC_END_USER:
                    partnerResp = next((resp for resp in opportunityPartnersResp["body"]["records"] if resp["Role"] == SFROLES.SF_END_USER and resp["AccountToId"] != oppMainAccount), None)
                    if partnerResp:
                        accountId = str(partnerResp["AccountToId"])
                # OpportunityPartnerRoleAccount
                elif customerType == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ROLE_ACC:
                    partnerResp = next((resp for resp in opportunityPartnersResp["body"]["records"] if resp["AccountToId"] != oppMainAccount), None)
                    if partnerResp:
                        accountId = str(partnerResp["AccountToId"])
        return accountId

    ###############################################################################################
    # Function to build create Opportunity Partner compositeRequest
    ###############################################################################################
    def build_opportunitypartners_sobjectcollection_create_record(self, opportunityId, cpqRole, partnerRole):
        records = list()
        rec = dict()
        # Check if customer is present on Quote
        customer = get_quote_customer(self.Quote, cpqRole)
        if customer and customer.CrmAccountId and partnerRole:
            # Opportunity ID
            rec["OpportunityId"] = opportunityId
            # Account ID
            rec["AccountToId"] = customer.CrmAccountId
            # Role
            if partnerRole == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ACC_BILL_TO:
                rec["Role"] = SFROLES.SF_BILL_TO
            elif partnerRole == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ACC_SHIP_TO:
                rec["Role"] = SFROLES.SF_SHIP_TO
            elif partnerRole == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ACC_END_USER:
                rec["Role"] = SFROLES.SF_END_USER
            rec["attributes"] = {"type": CL_SalesforceIntegrationParams.SF_OPPORTUNITY_PARTNER_OBJECT}
            records.append(rec)
        return records

    ###############################################################################################
    # Function to build composite request record to create Opportunity Partners
    ###############################################################################################
    def build_cr_record_create_opp_partners(self, opportunityId, oppPartnerRolesResponse):
        # Build composite request to create opportunity partners
        records = list()
        for outboundCustomerMapping in [{"Role": CPQ_BILL_TO, "Mapping": CL_OutboundCustomerMapping().BILL_TO}, {"Role": CPQ_SHIP_TO, "Mapping": CL_OutboundCustomerMapping().SHIP_TO}, {"Role": CPQ_END_USER, "Mapping": CL_OutboundCustomerMapping().END_CUSTOMER}]:
            if outboundCustomerMapping["Mapping"] in CL_SalesforceAccountObjects.SF_OPP_PARTNERS:
                if oppPartnerRolesResponse:
                    # Get CPQ Account Id
                    cpqAccountId = get_customer_crm_account_id(self.Quote, outboundCustomerMapping["Role"])
                    if cpqAccountId:
                        # Role
                        sfRole = None
                        if outboundCustomerMapping["Mapping"] == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ACC_BILL_TO:
                            sfRole = SFROLES.SF_BILL_TO
                        elif outboundCustomerMapping["Mapping"] == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ACC_SHIP_TO:
                            sfRole = SFROLES.SF_SHIP_TO
                        elif outboundCustomerMapping["Mapping"] == CL_SalesforceAccountObjects.SF_OPPORTUNITY_PARTNER_ACC_END_USER:
                            sfRole = SFROLES.SF_END_USER
                        # Check if partner is already assigned. Create Partner if it is not already assigned
                        if not next((resp for resp in oppPartnerRolesResponse["body"]["records"]if resp["Role"] == sfRole and resp["AccountToId"] == cpqAccountId), None):
                            records += self.build_opportunitypartners_sobjectcollection_create_record(opportunityId, outboundCustomerMapping["Role"], outboundCustomerMapping["Mapping"])
                else:
                    records += self.build_opportunitypartners_sobjectcollection_create_record(opportunityId, outboundCustomerMapping["Role"], outboundCustomerMapping["Mapping"])
        return records

    ###############################################################################################
    # Function to build composite request to Get Opportunity Account Partner Role
    ###############################################################################################
    def build_cr_get_opp_acc_partner_role(self, opportunityAccountId, referenceId):
        compositeRequest = None
        condition = "AccountToId='{opportunityAccountId}'".format(opportunityAccountId=str(opportunityAccountId))
        soql = self.build_soql_query(selectedFields="AccountFromId",
                                        table="Partner",
                                        condition=condition)
        compositeRequest = self.build_soql_query_composite_payload(soql, referenceId)
        return compositeRequest

    ###############################################################################################
    # Function to build composite payload to create Opportunity Account Partner Role
    ###############################################################################################
    def build_cp_create_update_opp_acc_partner_role(self, bearerToken, opportunityResponse):
        compositePayload = list()
        customerMappings = [{"OuboundCustomerMapping": CL_OutboundCustomerMapping().BILL_TO, "CpqRole": CPQ_BILL_TO, "Ref": REF.OPP_PARTNER_ROLE_ACC_BILL_TO},
                            {"OuboundCustomerMapping": CL_OutboundCustomerMapping().SHIP_TO, "CpqRole": CPQ_SHIP_TO, "Ref": REF.OPP_PARTNER_ROLE_ACC_SHIP_TO},
                            {"OuboundCustomerMapping": CL_OutboundCustomerMapping().END_CUSTOMER, "CpqRole": CPQ_END_USER, "Ref": REF.OPP_PARTNER_ROLE_ACC_END_USER}]
        # Get Opportunity Account Id
        opportunityAccountId = str(opportunityResponse["body"]["AccountId"])
        if opportunityAccountId:
            for customerMapping in customerMappings:
                if customerMapping["OuboundCustomerMapping"] == CL_SalesforceAccountObjects.SF_OPPORTUNITY_ACC_PARTNER_ROLE_ACC:
                    compositeRequest = self.build_cr_get_opp_acc_partner_role(opportunityAccountId, customerMapping["Ref"])
                    compositePayload.append(compositeRequest)
            if compositePayload:
                # Call SOQL
                response = self.post_composite_request(bearerToken, compositePayload, INT_REF.REF_GET_OPP_ACC_PARTNER_ROLE_ACC)
                if response:
                    compositePayload = list()
                    url = API.SOBJECT_API.format(sObject=str(CL_SalesforceIntegrationParams.SF_PARTNER))
                    # Assign Opportunity Account Partner
                    for customerMapping in customerMappings:
                        oppAccResponse = next((resp for resp in response["compositeResponse"] if resp["referenceId"] == customerMapping["Ref"]), None)
                        if oppAccResponse:
                            crmAccountId = get_customer_crm_account_id(self.Quote, customerMapping["CpqRole"])
                            if crmAccountId:
                                # Chect if Opportunity Account Partner is already assigned
                                if not next((account for account in oppAccResponse["body"]["records"] if account["AccountFromId"] == crmAccountId), None):
                                    record = dict()
                                    record["AccountToId"] = opportunityAccountId
                                    record["AccountFromId"] = crmAccountId
                                    compositeRequest = self.build_cr_sobject_request(url, API.POST, record, customerMapping["Ref"])
                                    compositePayload.append(compositeRequest)
                    if compositePayload:
                        return compositePayload
        return None

    ###############################################################################################
    # Function to get Account and Contact Information from Salesforce
    ###############################################################################################
    def get_customer_details(self, bearerToken, class_contact_modules, opportunityId, opportunityResponse, opportunityPartnersResp):
        response = None
        compositePayload = list()
        # CUSTOMERS
        for customerMapping in [{"InboundCustomerMapping": CL_InboundCustomerMapping().BILL_TO, "InboundContactMapping": CL_InboundContactMapping().BILL_TO_CONTACT, "CpqRole": CPQ_BILL_TO, "ContactIdRef": REF.BILL_TO_CONTACT_ID_REFID, "ContactRef": REF.BILL_TO_CONTACT},
                                {"InboundCustomerMapping": CL_InboundCustomerMapping().SHIP_TO, "InboundContactMapping": CL_InboundContactMapping().SHIP_TO_CONTACT, "CpqRole": CPQ_SHIP_TO, "ContactIdRef": REF.SHIP_TO_CONTACT_ID_REFID, "ContactRef": REF.SHIP_TO_CONTACT},
                                {"InboundCustomerMapping": CL_InboundCustomerMapping().END_CUSTOMER, "InboundContactMapping": CL_InboundContactMapping().END_CUSTOMER_CONTACT, "CpqRole": CPQ_END_USER, "ContactIdRef": REF.END_USER_CONTACT_ID_REFID, "ContactRef": REF.END_USER_CONTACT}]:
            # Inbound Customer Mapping
            if customerMapping["InboundCustomerMapping"]:
                accountId = self.get_opportunity_customers_accountid(bearerToken, customerMapping["InboundCustomerMapping"], opportunityResponse, opportunityPartnersResp)
                if accountId:
                    # Account
                    compositeRequest = self.build_cr_sobject_get_account(accountId, customerMapping["CpqRole"])
                    compositePayload.append(compositeRequest)
            # Inbound Contact Mapping
            if customerMapping["InboundContactMapping"]:
                # Get Contact Id
                compositePayload = class_contact_modules.get_contact_composite_payload(compositePayload, customerMapping["InboundContactMapping"], opportunityId, opportunityResponse, customerMapping["ContactIdRef"])
                # Get Contact Details
                if (customerMapping["InboundContactMapping"] in [CL_SalesforceContactObjects.SF_OPPORTUNITY_FIRST_ROLE,
                                                                    CL_SalesforceContactObjects.SF_OPPORTUNITY_BILL_TO_ROLE,
                                                                    CL_SalesforceContactObjects.SF_OPPORTUNITY_SHIP_TO_ROLE,
                                                                    CL_SalesforceContactObjects.SF_OPPORTUNITY_PRIMARY_ROLE,
                                                                    CL_SalesforceContactObjects.SF_OPPORTUNIY_ACC_BILL_TO_ROLE,
                                                                    CL_SalesforceContactObjects.SF_OPPORTUNITY_ACC_SHIP_TO_ROLE,
                                                                    CL_SalesforceContactObjects.SF_OPPORTUNIY_ACC_PRIMARY_CONTACT,
                                                                    CL_SalesforceContactObjects.SF_OPPORTUNITY_PARTNER_ROLE_ACC_PRIMARY_CONTACT]):
                    compositeRequest = class_contact_modules.build_cr_sobject_get_contact("@{"+customerMapping["ContactIdRef"]+".records[0].ContactId}", customerMapping["ContactRef"])
                else:
                    compositeRequest = class_contact_modules.build_cr_sobject_get_contact("@{"+customerMapping["ContactIdRef"]+".records[0].Id}", customerMapping["ContactRef"])
                if compositeRequest is not None:
                    compositePayload.append(compositeRequest)
        if compositePayload:
            response = self.post_composite_request(bearerToken, compositePayload, INT_REF.REF_GET_ACC)
        return response

    ###############################################################################################
    # Function to process Accounts and Contacts Information from Salesforce
    ###############################################################################################
    def process_customers_contacts(self, response, CustomerHelper, event):
        # Process Customers and Contacts
        for inboundCustomerProc in [{"InboundCustomerMapping": CL_InboundCustomerMapping().BILL_TO, "CpqRole": CPQ_BILL_TO, "ContactRef": REF.BILL_TO_CONTACT, "CreateCustomer": "on_quote_create_bill_to_mapping", "UpdateCustomer": "on_quote_update_bill_to_mapping", "CreateUpdateCustomer": "on_quote_createupdate_bill_to_mapping", "CreateContact": "on_quote_create_bill_to_contact_mapping", "UpdateContact": "on_quote_update_bill_to_contact_mapping", "CreateUpdateContact": "on_quote_createupdate_bill_to_contact_mapping"},
                                    {"InboundCustomerMapping": CL_InboundCustomerMapping().SHIP_TO, "CpqRole": CPQ_SHIP_TO, "ContactRef": REF.SHIP_TO_CONTACT, "CreateCustomer": "on_quote_create_ship_to_mapping", "UpdateCustomer": "on_quote_update_ship_to_mapping", "CreateUpdateCustomer": "on_quote_createupdate_ship_to_mapping", "CreateContact": "on_quote_create_ship_to_contact_mapping", "UpdateContact": "on_quote_update_ship_to_contact_mapping", "CreateUpdateContact": "on_quote_createupdate_ship_to_contact_mapping"},
                                    {"InboundCustomerMapping": CL_InboundCustomerMapping().END_CUSTOMER, "CpqRole": CPQ_END_USER, "ContactRef": REF.END_USER_CONTACT, "CreateCustomer": "on_quote_create_end_customer_mapping", "UpdateCustomer": "on_quote_update_end_customer_mapping", "CreateUpdateCustomer": "on_quote_createupdate_end_customer_mapping", "CreateContact": "on_quote_create_end_customer_contact_mapping", "UpdateContact": "on_quote_update_end_customer_contact_mapping", "CreateUpdateContact": "on_quote_createupdate_end_customer_contact_mapping"}]:
            if inboundCustomerProc["InboundCustomerMapping"]:
                compositeResponse = next((resp for resp in response["compositeResponse"] if str(resp["referenceId"]) == inboundCustomerProc["CpqRole"] and resp["httpStatusCode"] == 200), None)
                if compositeResponse:
                    # Get crmAccountId
                    crmAccountId = str(compositeResponse["body"]["Id"])
                    # Get crmContactId
                    crmContactId = str()
                    contactResponse = next((resp for resp in response["compositeResponse"] if str(resp["referenceId"]) == inboundCustomerProc["ContactRef"] and resp["httpStatusCode"] == 200), None)
                    if contactResponse:
                        crmContactId = str(contactResponse["body"]["Id"])
                    customer = None
                    # Check if customer exists in CPQ
                    customer = CustomerHelper.GetCustomer(crmAccountId, crmContactId, inboundCustomerProc["CpqRole"])

                    # Create customer
                    if customer is None:

                        customer = self.Quote.NewCustomer(inboundCustomerProc["CpqRole"], crmAccountId, crmContactId)
                    # Set customer in Quote
                    set_customer_on_quote(self.Quote, inboundCustomerProc["CpqRole"], customer)
                    # Check if customer is present on Quote
                    customer = get_quote_customer(self.Quote, inboundCustomerProc["CpqRole"])

                    # Update customer
                    if event == EVENT_CREATE:

                        customer = getattr(CL_InboundCustomerMapping(), inboundCustomerProc["CreateCustomer"])(customer, compositeResponse["body"])
                    elif event == EVENT_UPDATE:
                        customer = getattr(CL_InboundCustomerMapping(), inboundCustomerProc["UpdateCustomer"])(customer, compositeResponse["body"])
                    customer = getattr(CL_InboundCustomerMapping(), inboundCustomerProc["CreateUpdateCustomer"])(customer, compositeResponse["body"])
                    if contactResponse:
                        if event == EVENT_CREATE:
                            customer = getattr(CL_InboundContactMapping(), inboundCustomerProc["CreateContact"])(customer, contactResponse["body"])
                        elif event == EVENT_UPDATE:
                            customer = getattr(CL_InboundContactMapping(), inboundCustomerProc["UpdateContact"])(customer, contactResponse["body"])
                        customer = getattr(CL_InboundContactMapping(), inboundCustomerProc["CreateUpdateContact"])(customer, contactResponse["body"])
                    # Set customer in Quote
                    set_customer_on_quote(self.Quote, inboundCustomerProc["CpqRole"], customer)
                else:
                    set_empty_customer_on_quote(self.Quote, inboundCustomerProc["CpqRole"])