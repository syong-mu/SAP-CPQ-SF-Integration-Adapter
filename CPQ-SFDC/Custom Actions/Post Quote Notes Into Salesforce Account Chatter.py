from CPQ_SF_IntegrationMessages import CL_IntegrationMessages
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_IntegrationSettings import CL_SalesforceIntegrationParams
from CPQ_SF_FunctionModules import get_quote_opportunity_id

# Check if Opportunity is attached
opportunityId = get_quote_opportunity_id(Quote)
if opportunityId:
    if Quote.Total.QuoteComment:
        postComment = False
        if Session["accountComment"]:
            if Session["accountComment"]["QuoteId"] != Quote.QuoteId or Session["accountComment"]["UserId"] != Quote.UserId or Session["accountComment"]["Comment"] != Quote.Total.QuoteComment:
                postComment = True
        else:
            postComment = True
        if postComment:
            class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
            bearerToken = class_sf_integration_modules.get_auth2_token()
            response = class_sf_integration_modules.get_sobject(bearerToken, CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT, opportunityId)
            if response:
                # Get Opportunity Account Id
                accountId = str(response["AccountId"])
                if accountId != "":
                    text = "QuoteId #{quoteNumber}: {text}".format(quoteNumber=str(Quote.CompositeNumber), text=unicode(Quote.Total.QuoteComment))
                    response = class_sf_integration_modules.post_notes_into_chatter(bearerToken, accountId, text)
                    Session["accountComment"] = {"QuoteId": Quote.QuoteId, "UserId": Quote.UserId, "Comment": Quote.Total.QuoteComment}
else:
    Quote.Messages.Add(CL_IntegrationMessages.NO_OPPORTUNITY_ATTACHED)
