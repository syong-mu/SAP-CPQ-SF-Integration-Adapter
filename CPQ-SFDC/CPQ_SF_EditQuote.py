from CPQ_SF_Configuration import CL_CPQSettings
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_IntegrationSettings import CL_GeneralIntegrationSettings, CL_SalesforceIntegrationParams
from CPQ_SF_FunctionModules import set_quote_opportunity_id
from CPQ_SF_CpqHelper import EVENT_UPDATE
from CPQ_SF_IntegrationReferences import CL_CompositeRequestReferences as REF, CL_IntegrationReferences as INT_REF
import CPQ_SF_OpportunityMapping as OpportunityMapping
from CPQ_SF_CustomerModules import CL_CustomerModules
from CPQ_SF_ContactModules import CL_ContactIntegrationModules
from CPQ_SF_CustomObjectModules import CL_CustomObjectModules

if Param is not None:
    externalParameters = Param.externalParameters
    redirectionUrl = CL_CPQSettings.CPQ_URL
    # Get Opportunity Id
    opportunityId = externalParameters["opportunityid"].strip()
    quoteNumber = externalParameters["quotenumber"]
    quoteId = externalParameters["quoteId"]
    ownerId = externalParameters["ownerId"]
    if opportunityId and quoteId and ownerId:
        # Open active revision
        if CL_GeneralIntegrationSettings.ALL_REV_ATTACHED_TO_SAME_OPPORTUNITY:
            editQuoteURl = "/cart/edit?cartcompositenumber={quoteNumber}".format(quoteNumber=str(quoteNumber))
            Quote = QuoteHelper.Edit(quoteNumber)
        # Open chosen revision
        else:
            editQuoteURl = "/cart/edit?ownerId={ownerId}&quoteId={quoteId}".format(ownerId=str(ownerId), quoteId=str(quoteId))
            Quote = QuoteHelper.Edit(float(ownerId), float(quoteId))
        if Quote:
            # Attach Opportunity Id to Quote
            set_quote_opportunity_id(Quote, opportunityId)
            class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
            class_customer_modules = CL_CustomerModules(Quote, TagParserQuote, None, Session)
            class_contact_modules = CL_ContactIntegrationModules(Quote, TagParserQuote, None, Session)
            class_custom_object_modules = CL_CustomObjectModules(Quote, TagParserQuote, None, Session)
            #############################################
            # 1. AUTHORIZATION
            #############################################
            bearerToken = class_sf_integration_modules.get_auth2_token()
            ######################################################
            # 2. COLLECT OPPORTUNITY INFORMATION & CREATE QUOTE
            ######################################################
            compositePayload = list()
            # Opportunity
            compositeRequest = dict()
            compositeRequest = class_sf_integration_modules.build_cr_sobject_get_opportunity(opportunityId)
            compositePayload.append(compositeRequest)

            # Opportunity Partners
            compositeRequest = dict()
            compositeRequest = class_sf_integration_modules.build_cr_sobject_get_opportunity_partners(opportunityId)
            compositePayload.append(compositeRequest)

            # Call API
            response = class_sf_integration_modules.post_composite_request(bearerToken, compositePayload, INT_REF.REF_GET_OPP)
            if response:
                # Set opportunity fields in Quote
                # Get Opportunity info
                opportunityResponse = next((resp for resp in response["compositeResponse"] if str(resp["referenceId"]) == CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT), None)
                if opportunityResponse:
                    OpportunityMapping.on_quote_update_inbound_opportunity_integration_mapping(Quote, opportunityResponse["body"])
                    OpportunityMapping.on_quote_createupdate_inbound_opportunity_integration_mapping(Quote, opportunityResponse["body"])

                # Get Opportunity Partners info
                opportunityPartnersResp = next((resp for resp in response["compositeResponse"] if str(resp["referenceId"]) == REF.GET_OPP_PARTNERS_REFID), None)

                if opportunityResponse:
                    # Set Market on quote
                    class_sf_integration_modules.set_market_on_quote(opportunityResponse)
                    ######################################################
                    # 3. COLLECT ADDITIONAL INFORMATION
                    ######################################################
                    response = class_customer_modules.get_customer_details(bearerToken, class_contact_modules, opportunityId, opportunityResponse, opportunityPartnersResp)
                    if response:
                        # Process Customers and Contacts
                        class_customer_modules.process_customers_contacts(response, CustomerHelper, EVENT_UPDATE)
            #############################################
            # 4. CUSTOM OBJECTS
            #############################################
            class_custom_object_modules.process_inbound_custom_object_mappings(bearerToken, EVENT_UPDATE)
        Quote.Save(False)
        # Return redirect URL
        redirectionUrl = CL_CPQSettings.CPQ_URL + editQuoteURl
    Result = str(redirectionUrl)
