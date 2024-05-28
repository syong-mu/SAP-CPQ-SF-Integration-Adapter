CPQ_BP_STANDARD_FIELD = "BpStandardField"
CPQ_BP_CUSTOM_FIELD = "BpCustomField"
OUTBOUND = "OUTBOUND"
INBOUND = "INBOUND"
EVENT_CREATE = "Create"
EVENT_UPDATE = "Update"
###############################################################################################
# Class CL_CpqHelper:
#       Class to instantiate CPQ Quote
###############################################################################################
class CL_CpqHelper:

    TYPE_STRING = "String"
    TYPE_FLOAT = "Float"
    TYPE_BOOL = "Boolean"

    def __init__(self, Quote, Session, BusinessPartnerRepository=None):
        self.Quote = Quote
        self.Session = Session
        self.BusinessPartnerRepository = BusinessPartnerRepository

    ###############################################################################################
    # Function to build SOQL query to be used in API Calls
    ###############################################################################################
    def build_soql_query(self, selectedFields, table, condition):
        soql = None
        if selectedFields != "" and table != "":
            if condition == "":
                soql = "?q=SELECT {selectedFields} FROM {table}".format(selectedFields=str(selectedFields), table=str(table))
            else:
                # Replace special characters (&, #, +) 
                condition = self.replace_special_char(str(condition))
                soql = "?q=SELECT {selectedFields} FROM {table} WHERE {condition}".format(selectedFields=str(selectedFields), table=str(table), condition=str(condition))
        if soql is not None:
            soql = soql.replace(" ", "+")
        return soql
    
    ###############################################################################################
    # Function to replace special characters in string (Used in SOQL API calls)
    ###############################################################################################
    def replace_special_char(self, text):
        special_chars = [{"symbol": "&", "code": "%26"}, {"symbol": "#", "code": "%23"}, {"symbol": "+", "code": "%2B"}]
        for special_char in special_chars:
            text = text.replace(special_char["symbol"], special_char["code"])

        return text