from CPQ_SF_IntegrationMessages import CL_IntegrationMessages
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_FunctionModules import get_quote_opportunity_id

# Check if Opportunity is attached
opportunityId = get_quote_opportunity_id(Quote)
if opportunityId:
    if Quote.Total.QuoteComment:
        postComment = False
        if Session["opportunityComment"]:
            if Session["opportunityComment"]["QuoteId"] != Quote.QuoteId or Session["opportunityComment"]["UserId"] != Quote.UserId or Session["opportunityComment"]["Comment"] != Quote.Total.QuoteComment:
                postComment = True
        else:
            postComment = True
        if postComment:
            class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, WorkflowContext, Session)
            bearerToken = class_sf_integration_modules.get_auth2_token()
            text = "QuoteId #{quoteNumber}: {text}".format(quoteNumber=str(Quote.CompositeNumber), text=unicode(Quote.Total.QuoteComment))
            response = class_sf_integration_modules.post_notes_into_chatter(bearerToken, opportunityId, text)
            Session["opportunityComment"] = {"QuoteId": Quote.QuoteId, "UserId": Quote.UserId, "Comment": Quote.Total.QuoteComment}
else:
    Quote.Messages.Add(CL_IntegrationMessages.NO_OPPORTUNITY_ATTACHED)
