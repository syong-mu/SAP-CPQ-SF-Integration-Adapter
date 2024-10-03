from CPQ_SF_FunctionModules import is_action_allowed
from CPQ_SF_IntegrationSettings import CL_GeneralIntegrationSettings

# Constants
CREATE = "create"
EDIT = "edit"
NEW = "new"
VIEW = "view"
# action Edit -> Id = 13
EDIT_ACTION_ID = 13

# Get parameters
externalParameters = context.ExternalParameters
# Create Quote or Edit Quote
action = externalParameters["action"]
# Clear Session OnLandingFromCRM
opportunityId = externalParameters["opportunityid"].strip()

# Clear Session OnLandingFromCRM
Session[opportunityId] = None
Session["Query"] = None

# Set SF User Session Token
Session["apiSessionID"] = externalParameters["apiSessionID"]
# Set Opportunity Id in Session
Session["OpportunityId"] = opportunityId

if action == CREATE:
    redirectionUrl = ScriptExecutor.Execute("CPQ_SF_CreateQuote", {"externalParameters": externalParameters, "createQuote": True})
elif action == EDIT:
    # Open active revision
    if CL_GeneralIntegrationSettings.ALL_REV_ATTACHED_TO_SAME_OPPORTUNITY:
        quoteNumber = externalParameters["quotenumber"]
        Quote = QuoteHelper.Get(quoteNumber)
    else:
        quoteId = externalParameters["quoteId"]
        Quote = QuoteHelper.Get(float(quoteId))

    if is_action_allowed(Quote, User, externalParameters, EDIT_ACTION_ID) == True:
        redirectionUrl = ScriptExecutor.Execute("CPQ_SF_EditQuote", {"externalParameters": externalParameters, "quote": Quote})
    else:
        redirectionUrl = ScriptExecutor.Execute("CPQ_SF_ViewQuote", {"externalParameters": externalParameters})
elif action == NEW:
    redirectionUrl = ScriptExecutor.Execute("CPQ_SF_LandingOnCatalogue")
elif action == VIEW:
    redirectionUrl = ScriptExecutor.Execute("CPQ_SF_ViewQuote", {"externalParameters": externalParameters})
