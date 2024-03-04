from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_CustomObjectLineItemModules import CL_CustomObjectLineItemModules

class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
class_cust_obj_item_modules = CL_CustomObjectLineItemModules(Quote, TagParserQuote, None, Session)
#############################################
# 1. AUTHORIZATION
#############################################
bearerToken = class_sf_integration_modules.get_auth2_token()
#############################################
# 2. ITEM INTEGRATION
#############################################
# Send Quote Items to Custom Objects
class_cust_obj_item_modules.process_custom_object_line_item_mappings(bearerToken)