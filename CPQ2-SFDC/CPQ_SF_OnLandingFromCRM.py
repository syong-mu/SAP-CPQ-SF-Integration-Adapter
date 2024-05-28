from CPQ_SF_FunctionModules import is_action_allowed

CREATE = "create"
EDIT = "edit"
NEW = "new"
VIEW = "view"
# Get paramters
externalParameters = context.ExternalParameters
# Create Quote or Edit Quote
action = externalParameters["action"]
# Clear Session OnLandingFromCRM
opportunityId = externalParameters["opportunityid"].strip()
Session[opportunityId] = None
Session["Query"] = None
# Set SF User Session Token
Session["apiSessionID"] = externalParameters["apiSessionID"]
# Set Opportunity Id in Session
Session["OpportunityId"] = opportunityId

if action == CREATE:
    redirectionUrl = ScriptExecutor.Execute("CPQ_SF_CreateQuote", {"externalParameters": externalParameters, "createQuote": True})
elif action == EDIT:
    # action Edit -> Id = 13
    actionId = 13
    if is_action_allowed(QuoteHelper, User, externalParameters, actionId) == True:
        redirectionUrl = ScriptExecutor.Execute("CPQ_SF_EditQuote", {"externalParameters": externalParameters})
    else:
        redirectionUrl = ScriptExecutor.Execute("CPQ_SF_ViewQuote", {"externalParameters": externalParameters})
elif action == NEW:
    redirectionUrl = ScriptExecutor.Execute("CPQ_SF_LandingOnCatalogue")
elif action == VIEW:
    redirectionUrl = ScriptExecutor.Execute("CPQ_SF_ViewQuote", {"externalParameters": externalParameters})