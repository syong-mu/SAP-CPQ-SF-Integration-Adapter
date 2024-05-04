from CPQ_SF_Configuration import CL_SalesforceSettings
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_IntegrationReferences import CL_IntegrationReferences as INT_REF, CL_SalesforceApiLimits as API_LIMIT
from CPQ_SF_CustomObjectLineItemMapping import CL_CustomObjectLineItemMapping
from CPQ_SF_IntegrationSettings import CL_GeneralIntegrationSettings


###############################################################################################
# Class CL_CustomObjectLineItemModules:
#       Class to store integration functions related to quote items to custom objects
###############################################################################################
class CL_CustomObjectLineItemModules(CL_SalesforceIntegrationModules, CL_CustomObjectLineItemMapping):

    ###############################################################################################
    # Function process quote items to custom objects mappings (CPQ -> Salesforce)
    ###############################################################################################
    def process_custom_object_line_item_mappings(self, bearerToken):
        # Get Mappings sorted by rank
        mappings = sorted(self.mappings, key=lambda x: x["Rank"])
        headers = self.get_authorization_header(bearerToken)
        # Process for each Custom Object
        for mapping in mappings:
            # Initialize list of quote items to be sent
            quoteItems = [{"item": item, "recordId": ""} for item in self.Quote.Items]
            # Remove items that should not be sent depending on condition
            quoteItems = filter(lambda item,mapping=mapping: self.custom_object_item_condition(self.Quote, self.TagParserQuote, item["item"], mapping["ObjectType"]), quoteItems)
            # Get lookups
            lookUps = self.custom_object_item_lookups(self.Quote, self.TagParserQuote, mapping["ObjectType"])
            # Get existing record ids
            recordIds = self.get_custom_object_item_record_ids(headers, lookUps, mapping["ObjectType"])

            # do not update line items from opportunity whenever flag is set to false
            if not CL_GeneralIntegrationSettings.UPDATE_CUSTOM_ITEM_OBJECT:
                # Delete all Salesforce records id
                if recordIds:
                    if recordIds["totalSize"] > 0:
                        recordsToDelete = [str(record["Id"]) for record in recordIds["records"]]
                        permissionList = [self.build_permission_checklist(mapping["ObjectType"], False, False, True)]
                        self.delete_cust_obj_items(bearerToken, recordsToDelete, permissionList)
                if quoteItems:
                    permissionList = [self.build_permission_checklist(mapping["ObjectType"], True)]
                    # Create records
                    for batch in range(0, len(quoteItems), API_LIMIT.CREATE_API_RECORD_LIMIT):
                        self.recreate_cust_obj_items(bearerToken, lookUps, mapping["ObjectType"], quoteItems[batch:batch+API_LIMIT.CREATE_API_RECORD_LIMIT], permissionList)
            else:
                if quoteItems:
                    recordsToUpdate, recordsToDelete = self.build_records(recordIds, quoteItems, mapping)

                    if recordsToUpdate:
                        # Update Salesforce records id not found in quote items
                        permissionList = [self.build_permission_checklist(mapping["ObjectType"], False, True)]
                        # Update records
                        for batch in range(0, len(recordsToUpdate), API_LIMIT.CREATE_API_RECORD_LIMIT):
                            self.update_cust_obj_items(bearerToken, lookUps, mapping["ObjectType"], recordsToUpdate[batch:batch+API_LIMIT.CREATE_API_RECORD_LIMIT], mapping["CPQ_ITEM_FIELD_NAME"], permissionList)

                    if recordsToDelete:
                        # Delete Salesforce records id not found in quote items
                        permissionList = [self.build_permission_checklist(mapping["ObjectType"], False, False, True)]
                        self.delete_cust_obj_items(bearerToken, recordsToDelete, permissionList)

                    self.create_record(bearerToken, headers, lookUps, quoteItems, mapping)
                # handle the deletion of the last item on a quote
                else:
                    if recordIds:
                        if recordIds["totalSize"] > 0:
                            recordsToDelete = [str(record["Id"]) for record in recordIds["records"]]
                            permissionList = [self.build_permission_checklist(mapping["ObjectType"], False, False, True)]
                            self.delete_cust_obj_items(bearerToken, recordsToDelete, permissionList)

    ###############################################################################################
    # Function to delete custom object item records in Salesforce
    ###############################################################################################
    def delete_cust_obj_items(self, bearerToken, recordsToDelete, permissionList = None):
        # Delete in batches of API_LIMIT.DELETE_API_RECORD_LIMIT (Currently 200)
        for batch in range(0, len(recordsToDelete), API_LIMIT.DELETE_API_RECORD_LIMIT):
            url = CL_SalesforceSettings.SALESFORCE_URL + self.build_delete_sobj_collection_url(recordsToDelete[batch:batch+API_LIMIT.DELETE_API_RECORD_LIMIT])
            self.call_sobject_delete_api(bearerToken, url, INT_REF.REF_CR_UP_CUST_OBJ_ITEM, permissionList)

    ###############################################################################################
    # Function to recreate quote items to custom objects mapping
    ###############################################################################################
    def recreate_cust_obj_items(self, bearerToken, lookUps, customObjectName, quoteItems, permissionList = None):
        # Create in batches of API_LIMIT.CREATE_API_RECORD_LIMIT (Currently 200)
        for batch in range(0, len(quoteItems), API_LIMIT.CREATE_API_RECORD_LIMIT):
            records = list()
            for item in quoteItems[batch:batch+API_LIMIT.CREATE_API_RECORD_LIMIT]:
                record = self.create_outbound_custom_object_item_mapping(self.Quote, self.TagParserQuote, item["item"], customObjectName)
                record = self.fill_cust_obj_lookup_record(lookUps, record)
                record["attributes"] = {"type": customObjectName}
                records.append(record)
            if records:
                body = dict()
                body["records"] = records
                headers = self.get_authorization_header(bearerToken)
                self.post_sobjectcollection_request(headers, body, INT_REF.REF_CR_UP_CUST_OBJ_ITEM, permissionList)

    ###############################################################################################
    # Function to get record ids of the custom objects on Salesforce
    ###############################################################################################
    def get_custom_object_item_record_ids(self, headers, lookUps, customObjectName, itemId=""):
        response = None
        if lookUps:
            # Get Salesforce LookUp Fields
            lookUpFields = str([key["SalesforceField"] for key in lookUps])[1:-1].replace("'", "").replace(" ", "")
            # Build Condition
            condition = str()
            for indx, lookUp in enumerate(lookUps):
                lookUpValue = str()
                if lookUp["FieldType"] == self.TYPE_STRING:
                    lookUpValue = "'{lookUpValue}'".format(lookUpValue=str(lookUp["CpqLookUpValue"]))
                elif lookUp["FieldType"] == self.TYPE_FLOAT or lookUp["FieldType"] == self.TYPE_BOOL:
                    lookUpValue = "{lookUpValue}".format(lookUpValue=str(lookUp["CpqLookUpValue"]))
                condition += "{lookUpField}={lookUpValue}".format(lookUpField=str(lookUp["SalesforceField"]), lookUpValue=str(lookUpValue))
                if indx+1 != len(lookUps):
                    condition += " AND "
            soql = self.build_soql_query(selectedFields="Id,"+itemId+lookUpFields,
                                        table= customObjectName,
                                        condition=condition)
            # Call API
            response = self.call_soql_api(headers, soql, INT_REF.REF_GET_CUST_ITEM_IDS)
        return response

    ###############################################################################################
    # Function to fill Custom Object look up fields in a record payload (Composite Request)
    ###############################################################################################
    def fill_cust_obj_lookup_record(self, lookUps, record):
        for lookUp in lookUps:
            record[lookUp["SalesforceField"]] = lookUp["CpqLookUpValue"]
        return record

    ###############################################################################################
    # Function to get object line items ID matching Item IDs on SF
    ###############################################################################################
    def get_recordId_by_items(self, items, record, fieldName):
        item = [item for item in items if str(record["Id"]) == str(item[fieldName].Value)]
        if not item: return str(record["Id"])
        else: return None

    ###############################################################################################
    # Function to get list of object line items IDs matching object IDs
    ###############################################################################################
    def get_recordId_by_objId(self, records, objectId):
        recordIds = [str(record["Id"]) for record in records if objectId == str(record["Id"])]
        return recordIds

    ###############################################################################################
    # Function to build list of items to be updated and deleted on Salesforce
    ###############################################################################################
    def build_records(self, recordIds, quoteItems, mapping):
        recordsToUpdate = []
        recordsToDelete = []

        if recordIds:
            # Build list of Salesforce records id found in quote items
            for item in quoteItems:
                if self.get_recordId_by_objId(recordIds["records"], item["item"][mapping["CPQ_ITEM_FIELD_NAME"]].Value):
                    recordsToUpdate.append(item)

            # Build list of Salesforce records id which does not exist in quote items
            for record in recordIds["records"]:
                recordId = self.get_recordId_by_items(self.Quote.Items, record, mapping["CPQ_ITEM_FIELD_NAME"])
                if recordId: recordsToDelete.append(recordId)

        return recordsToUpdate, recordsToDelete

    ###############################################################################################
    # Function to update custom object item records in Salesforce
    ###############################################################################################
    def update_cust_obj_items(self, bearerToken, lookUps, customObjectName, quoteItems, customObjectId, permissionList = None):
        # Update in batches of API_LIMIT.CREATE_API_RECORD_LIMIT (Currently 200)
        for batch in range(0, len(quoteItems), API_LIMIT.CREATE_API_RECORD_LIMIT):
            records = list()
            for item in quoteItems[batch:batch+API_LIMIT.CREATE_API_RECORD_LIMIT]:
                record = self.update_outbound_custom_object_item_mapping(self.Quote, self.TagParserQuote, item["item"], customObjectName)
                record = self.fill_cust_obj_lookup_record(lookUps, record)
                record["attributes"] = {"type": customObjectName}
                record["Id"] = item["item"][customObjectId].Value
                records.append(record)
            if records:
                body = dict()
                body["records"] = records
                headers = self.get_authorization_header(bearerToken)
                self.patch_sobjectcollection_request(headers, body, INT_REF.REF_CR_UP_CUST_OBJ_ITEM, permissionList)

    ###############################################################################################
    # Function to bulk create new records from quote line items
    ###############################################################################################
    def create_record(self, bearerToken, headers, lookUps, quoteItems, mapping):
        recordsToCreate = [item for item in quoteItems if not item["item"][mapping["CPQ_ITEM_FIELD_NAME"]].Value]
        if recordsToCreate:
            permissionList = [self.build_permission_checklist(mapping["ObjectType"], True)]
            # Create records
            for batch in range(0, len(recordsToCreate), API_LIMIT.CREATE_API_RECORD_LIMIT):
                self.recreate_cust_obj_items(bearerToken, lookUps, mapping["ObjectType"], recordsToCreate[batch:batch+API_LIMIT.CREATE_API_RECORD_LIMIT], permissionList)

            # get Salesforce field which reference CPQ line items identifier
            itemId = "{},".format(mapping["SALESFORCE_FIELD_NAME"])
            # Get existing record ids
            recordIds = self.get_custom_object_item_record_ids(headers, lookUps, mapping["ObjectType"], itemId)
            if recordIds:
                if recordIds["totalSize"] > 0:
                    for item in self.Quote.Items:
                        guid = [str(record["Id"]) for record in recordIds["records"] if str(record[mapping["SALESFORCE_FIELD_NAME"]]) == str(item.QuoteItemGuid)]
                        if guid: item[mapping["CPQ_ITEM_FIELD_NAME"]].Value = str(guid[0])
