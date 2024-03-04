from CPQ_SF_CpqHelper import CL_CpqHelper


###############################################################################################
# Class CL_MessageHandler:
#       Class to handle messages
###############################################################################################
class CL_MessageHandler(CL_CpqHelper):

    messages = list()

    def __init__(self, Quote, TagParserQuote, WorkflowContext, Session):
        self.messages = list()
        self.Quote = Quote
        self.TagParserQuote = TagParserQuote
        self.WorkflowContext = WorkflowContext
        self.Session = Session

###############################################################################################
# Function to add messages
###############################################################################################
    def add_message(self, msg):
        self.messages.append(msg)

###############################################################################################
# Function to display messages on Quote
###############################################################################################
    def show_messages(self):
        if self.messages:
            self.Quote.Messages.Clear()
            self.Quote.Messages.Add("\n".join(self.messages))

###############################################################################################
# Function to append to Quote messages
###############################################################################################
    def add_to_quote_msgs(self, msg):
        self.Quote.Messages.Add(msg)


###############################################################################################
# Class CL_IntegrationMessages:
#       Class to store messages
###############################################################################################
class CL_IntegrationMessages:

    ONLY_ONE_QUOTE_E_MSG = "Only one quote can be linked to an opportunity. Please contact your CPQ Admin."
    NO_OPPORTUNITY_NAME = "Opportunity name is missing. To Create/Update an Opportunity please add the Opportunity Name."
    CANNOT_ATTACH_QUOTE = "Quote is already attached to an Opportunity. Please detach Quote from Opportunity before reattaching with another Opportunity."
    CANNOT_DETACH_QUOTE = "Quote cannot be detached as it is not linked to any Opportunity."
    NO_OPPORTUNITY_ATTACHED = "Quote is not attached to any Opportunity."