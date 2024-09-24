OUTBOUND = "OUTBOUND"
INBOUND = "INBOUND"
EVENT_CREATE = "Create"
EVENT_UPDATE = "Update"
EVENT_CREATE_UPDATE = "CreateUpdate"
CPQ_CUSTOM_FIELD = "QuoteCustomField"
CPQ_STANDARD_FIELD = "QuoteStandardField"
CPQ_STANDARD_DATE_FIELD = "QuoteStandardDateField"
CPQ_TAGS = "QuoteTags"
CPQ_ITEM_STANDARD_FIELD = "QuoteItemStandardField"
CPQ_ITEM_CUSTOM_FIELD = "QuoteItemCustomField"
CUSTOM = "Custom"
CPQ_CUSTOMER_FIELD = "CustomerField"
CPQ_CUSTOMER_CUSTOM_FIELD = "CustomerCustomField"
CPQ_BILL_TO = "BillTo"
CPQ_SHIP_TO = "ShipTo"
CPQ_END_USER = "EndUser"


###############################################################################################
# Class CL_CpqHelper:
#       Class to instantiate CPQ Quote and TagparserQuote
###############################################################################################
class CL_CpqHelper:
    # Data Types for SOQL Lookups
    TYPE_STRING = "String"
    TYPE_FLOAT = "Float"
    TYPE_BOOL = "Boolean"

    def __init__(self, Quote, TagParserQuote, WorkflowContext, Session):
        self.Quote = Quote
        self.TagParserQuote = TagParserQuote
        self.WorkflowContext = WorkflowContext
        self.Session = Session

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
