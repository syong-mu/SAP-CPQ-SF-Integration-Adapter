###############################################################################################
# Class CL_CPQSettings:
#       Class to store general CPQ properties (TENANT SPECIFIC)
###############################################################################################
class CL_CPQSettings:
    # https://xxx.webcomcpq.com
    CPQ_URL = ""


###############################################################################################
# Class CL_SalesforceSettings:
#       Class to store general Salesforce properties (TENANT SPECIFIC)
###############################################################################################
class CL_SalesforceSettings:

    SALESFORCE_VERSION = "55.0"
    # https://xxx.my.salesforce.com
    SALESFORCE_URL = ""

    # Credential Management Keys for Integration User
    SALESFORCE_PWD = "CPQ_SFDC_PWD"
    SALESFORCE_SECRET = "CPQ_SFDC_SECRET"
