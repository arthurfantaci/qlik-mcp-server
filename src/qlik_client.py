"""Simplified Qlik WebSocket client for measure retrieval"""

import json
import ssl
import os
from typing import Dict, Any, Optional, List
import websocket
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class QlikClient:
    """Lightweight Qlik Engine API client focused on measure retrieval"""
    
    def __init__(self):
        """Initialize client with configuration from environment"""
        self.server_url = os.getenv("QLIK_SERVER_URL")
        self.server_port = os.getenv("QLIK_SERVER_PORT", "4747")
        self.user_directory = os.getenv("QLIK_USER_DIRECTORY", "INTERNAL")
        self.user_id = os.getenv("QLIK_USER_ID", "sa_engine")
        
        # Certificate paths
        self.cert_root = os.getenv("QLIK_CERT_ROOT", "certs/root.pem")
        self.cert_client = os.getenv("QLIK_CERT_CLIENT", "certs/client.pem")
        self.cert_key = os.getenv("QLIK_CERT_KEY", "certs/client_key.pem")
        
        # Timeout settings
        self.timeout = int(os.getenv("WEBSOCKET_TIMEOUT", "30"))
        self.recv_timeout = int(os.getenv("WEBSOCKET_RECV_TIMEOUT", "60"))
        
        # Connection state
        self.ws: Optional[websocket.WebSocket] = None
        self.request_id = 0
        self.app_handle: Optional[int] = None
        
    def connect(self, app_id: str) -> bool:
        """Connect to Qlik Engine and open specified app"""
        try:
            # First try connecting to global context and using OpenDoc
            url = f"wss://{self.server_url}:{self.server_port}/app/"
            print(f"Connecting to: {url}")
            
            # Setup SSL context with certificates
            sslopt = {
                "cert_reqs": ssl.CERT_REQUIRED,
                "ca_certs": self.cert_root,
                "certfile": self.cert_client,
                "keyfile": self.cert_key,
                "check_hostname": False,
                "ssl_version": ssl.PROTOCOL_TLS
            }
            
            # Setup headers
            headers = {
                "X-Qlik-User": f"UserDirectory={self.user_directory}; UserId={self.user_id}"
            }
            
            # Create WebSocket connection
            self.ws = websocket.create_connection(
                url,
                sslopt=sslopt,
                header=headers,
                timeout=self.timeout
            )
            
            print("Connected to Qlik Engine")
            
            # Open the app using OpenDoc
            print(f"Opening app: {app_id}")
            result = self._send_request(
                "OpenDoc",
                -1,  # Global handle
                {"qDocName": app_id}
            )
            
            if result and "qReturn" in result and "qHandle" in result["qReturn"]:
                self.app_handle = result["qReturn"]["qHandle"]
                print(f"App opened with handle: {self.app_handle}")
                
                # Verify by getting app layout
                layout = self._send_request("GetAppLayout", self.app_handle)
                if layout:
                    app_title = layout.get("qTitle", app_id)
                    print(f"Successfully opened app: {app_title}")
                    return True
            
            print("Failed to open app")
            return False
            
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close WebSocket connection"""
        if self.ws:
            self.ws.close()
            self.ws = None
            self.app_handle = None
            print("Disconnected from Qlik Engine")
    
    def connect_global(self) -> bool:
        """Connect to Qlik Engine global context (for listing apps)"""
        try:
            # Connect to global context (no specific app)
            url = f"wss://{self.server_url}:{self.server_port}/app/"
            print(f"Connecting to global context: {url}")
            
            # Setup SSL context with certificates
            sslopt = {
                "cert_reqs": ssl.CERT_REQUIRED,
                "ca_certs": self.cert_root,
                "certfile": self.cert_client,
                "keyfile": self.cert_key,
                "check_hostname": False,
                "ssl_version": ssl.PROTOCOL_TLS
            }
            
            # Setup headers
            headers = {
                "X-Qlik-User": f"UserDirectory={self.user_directory}; UserId={self.user_id}"
            }
            
            # Create WebSocket connection
            self.ws = websocket.create_connection(
                url,
                sslopt=sslopt,
                header=headers,
                timeout=self.timeout
            )
            
            print("Connected to Qlik Engine global context")
            return True
            
        except Exception as e:
            print(f"Global connection failed: {e}")
            return False
    
    def get_doc_list(self) -> Dict[str, Any]:
        """Get list of all available applications"""
        if not self.ws:
            raise ConnectionError("Not connected to Qlik Engine")
        
        try:
            print("Fetching application list...")
            
            # Get document list using global handle (-1)
            result = self._send_request("GetDocList", -1)
            
            apps = []
            if result and "qDocList" in result:
                doc_list = result["qDocList"]
                print(f"Found {len(doc_list)} applications")
                
                for app in doc_list:
                    app_info = {
                        "app_id": app.get("qDocId", ""),
                        "name": app.get("qTitle", "Untitled"),
                        "last_reload_time": app.get("qLastReloadTime", ""),
                        "meta": app.get("qMeta", {}),
                        "doc_type": app.get("qDocType", "")
                    }
                    apps.append(app_info)
            
            return {
                "applications": apps,
                "count": len(apps)
            }
            
        except Exception as e:
            print(f"Error fetching application list: {e}")
            raise
    
    def get_measures(self, include_expression: bool = True, include_tags: bool = True) -> Dict[str, Any]:
        """Retrieve all measures from the current app"""
        if not self.ws or not self.app_handle:
            raise ConnectionError("Not connected to Qlik Engine")
        
        try:
            # Create MeasureList session object
            print("Creating MeasureList session object...")
            
            # Build qData paths based on options
            q_data = {
                "title": "/qMetaDef/title",
                "description": "/qMetaDef/description",
                "id": "/qInfo/qId"
            }
            
            if include_expression:
                q_data["expression"] = "/qMeasure/qDef"
                q_data["label"] = "/qMeasure/qLabel"
            
            if include_tags:
                q_data["tags"] = "/qMetaDef/tags"
            
            create_params = [
                {
                    "qInfo": {
                        "qType": "MeasureList"
                    },
                    "qMeasureListDef": {
                        "qType": "measure",
                        "qData": q_data
                    }
                }
            ]
            
            create_result = self._send_request(
                "CreateSessionObject",
                self.app_handle,
                create_params
            )
            
            if not create_result or "qReturn" not in create_result:
                raise ValueError("Failed to create MeasureList object")
            
            measure_list_handle = create_result["qReturn"]["qHandle"]
            print(f"Created MeasureList with handle: {measure_list_handle}")
            
            # Get layout containing measure data
            layout = self._send_request("GetLayout", measure_list_handle)
            # The actual data is nested under qLayout
            actual_layout = layout.get("qLayout", layout) if layout else {}
            
            # Extract measures from layout
            measures = []
            if actual_layout and "qMeasureList" in actual_layout:
                items = actual_layout["qMeasureList"].get("qItems", [])
                print(f"Processing {len(items)} measures...")
                for item in items:
                    # Parse both qData (custom paths) and standard qInfo/qMeta
                    q_data = item.get("qData", {})
                    q_info = item.get("qInfo", {})
                    q_meta = item.get("qMeta", {})
                    
                    measure = {
                        "id": q_data.get("id", q_info.get("qId", "")),
                        "title": q_data.get("title", q_meta.get("title", "")),
                        "description": q_data.get("description", q_meta.get("description", ""))
                    }
                    
                    if include_expression:
                        # Try to get expression from qData first, then fall back to qMeasure
                        expression_data = q_data.get("expression", {})
                        if isinstance(expression_data, dict):
                            measure["expression"] = expression_data.get("qDef", "") or expression_data.get("qExpr", "")
                        else:
                            # Fallback to standard qMeasure structure
                            q_measure = item.get("qMeasure", {})
                            measure["expression"] = q_measure.get("qDef", "") or str(expression_data) if expression_data else ""
                        
                        # Try to get label
                        label_data = q_data.get("label", {})
                        if isinstance(label_data, dict):
                            measure["label"] = label_data.get("qExpr", "")
                        else:
                            measure["label"] = item.get("qMeasure", {}).get("qLabel", "") or str(label_data) if label_data else ""
                    
                    if include_tags:
                        measure["tags"] = q_data.get("tags", [])
                    
                    measures.append(measure)
            
            # Clean up session object (skip for now to avoid errors)
            # Note: In production, should properly destroy session objects
            print(f"Found {len(measures)} measures")
            
            return {
                "measures": measures,
                "count": len(measures)
            }
            
        except Exception as e:
            print(f"Error retrieving measures: {e}")
            raise
    
    def get_variables(
        self, 
        include_definition: bool = True, 
        include_tags: bool = True,
        show_reserved: bool = True,
        show_config: bool = True
    ) -> Dict[str, Any]:
        """Retrieve all variables from the current app"""
        if not self.ws or not self.app_handle:
            raise ConnectionError("Not connected to Qlik Engine")
        
        try:
            # Create VariableList session object
            print("Creating VariableList session object...")
            
            # Build qData paths based on options
            q_data = {
                "name": "/qName"
            }
            
            if include_definition:
                q_data["definition"] = "/qDefinition"
            
            if include_tags:
                q_data["tags"] = "/tags"
            
            create_params = [
                {
                    "qInfo": {
                        "qType": "VariableList"
                    },
                    "qVariableListDef": {
                        "qType": "variable",
                        "qShowReserved": show_reserved,
                        "qShowConfig": show_config,
                        "qData": q_data
                    }
                }
            ]
            
            create_result = self._send_request(
                "CreateSessionObject",
                self.app_handle,
                create_params
            )
            
            if not create_result or "qReturn" not in create_result:
                raise ValueError("Failed to create VariableList object")
            
            variable_list_handle = create_result["qReturn"]["qHandle"]
            print(f"Created VariableList with handle: {variable_list_handle}")
            
            # Get layout containing variable data
            layout = self._send_request("GetLayout", variable_list_handle)
            # The actual data is nested under qLayout
            actual_layout = layout.get("qLayout", layout) if layout else {}
            
            # Extract variables from layout
            variables = []
            if actual_layout and "qVariableList" in actual_layout:
                items = actual_layout["qVariableList"].get("qItems", [])
                print(f"Processing {len(items)} variables...")
                for item in items:
                    # Parse both qData (custom paths) and standard qInfo
                    q_data = item.get("qData", {})
                    q_info = item.get("qInfo", {})
                    
                    variable = {
                        "name": q_data.get("name", q_info.get("qId", ""))
                    }
                    
                    if include_definition:
                        variable["definition"] = q_data.get("definition", "")
                    
                    if include_tags:
                        variable["tags"] = q_data.get("tags", [])
                    
                    # Add additional metadata if available
                    if "qMeta" in item:
                        q_meta = item["qMeta"]
                        variable["is_reserved"] = q_meta.get("qIsReserved", False)
                        variable["is_config"] = q_meta.get("qIsConfig", False)
                    
                    variables.append(variable)
            
            # Clean up session object (skip for now to avoid errors)
            # Note: In production, should properly destroy session objects
            print(f"Found {len(variables)} variables")
            
            return {
                "variables": variables,
                "count": len(variables)
            }
            
        except Exception as e:
            print(f"Error retrieving variables: {e}")
            raise
    
    def get_fields(
        self,
        show_system: bool = True,
        show_hidden: bool = True,
        show_derived_fields: bool = True,
        show_semantic: bool = True,
        show_src_tables: bool = True,
        show_implicit: bool = True
    ) -> Dict[str, Any]:
        """Retrieve all fields from the current app"""
        if not self.ws or not self.app_handle:
            raise ConnectionError("Not connected to Qlik Engine")
        
        try:
            # Create FieldList session object
            print("Creating FieldList session object...")
            
            create_params = [
                {
                    "qInfo": {
                        "qType": "FieldList"
                    },
                    "qFieldListDef": {
                        "qShowSystem": show_system,
                        "qShowHidden": show_hidden,
                        "qShowDerivedFields": show_derived_fields,
                        "qShowSemantic": show_semantic,
                        "qShowSrcTables": show_src_tables,
                        "qShowImplicit": show_implicit
                    }
                }
            ]
            
            create_result = self._send_request(
                "CreateSessionObject",
                self.app_handle,
                create_params
            )
            
            if not create_result or "qReturn" not in create_result:
                raise ValueError("Failed to create FieldList object")
            
            field_list_handle = create_result["qReturn"]["qHandle"]
            print(f"Created FieldList with handle: {field_list_handle}")
            
            # Get layout containing field data
            layout = self._send_request("GetLayout", field_list_handle)
            # The actual data is nested under qLayout
            actual_layout = layout.get("qLayout", layout) if layout else {}
            
            # Extract fields from layout
            fields = []
            tables = set()
            
            if actual_layout and "qFieldList" in actual_layout:
                items = actual_layout["qFieldList"].get("qItems", [])
                print(f"Processing {len(items)} fields...")
                
                for item in items:
                    field_name = item.get("qName", "")
                    
                    field_info = {
                        "name": field_name,
                        "is_system": item.get("qIsSystem", False),
                        "is_hidden": item.get("qIsHidden", False),
                        "is_semantic": item.get("qIsSemantic", False),
                        "is_numeric": item.get("qIsNumeric", False),
                        "cardinal": item.get("qCardinal", 0)
                    }
                    
                    # Add source table information if available
                    src_tables = item.get("qSrcTables", [])
                    if src_tables:
                        field_info["source_tables"] = src_tables
                        # Add tables to our set for summary
                        tables.update(src_tables)
                    
                    # Add tags if available
                    tags = item.get("qTags", [])
                    if tags:
                        field_info["tags"] = tags
                    
                    # Add field type information
                    if "qAndMode" in item:
                        field_info["and_mode"] = item["qAndMode"]
                    
                    fields.append(field_info)
            
            # Convert tables set to sorted list for consistent output
            tables_list = sorted(list(tables))
            
            # Clean up session object (skip for now to avoid errors)
            # Note: In production, should properly destroy session objects
            print(f"Found {len(fields)} fields across {len(tables_list)} tables")
            
            return {
                "fields": fields,
                "field_count": len(fields),
                "tables": tables_list,
                "table_count": len(tables_list)
            }
            
        except Exception as e:
            print(f"Error retrieving fields: {e}")
            raise
    
    def get_sheets(
        self,
        include_thumbnail: bool = False,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """Retrieve all sheets from the current app"""
        if not self.ws or not self.app_handle:
            raise ConnectionError("Not connected to Qlik Engine")
        
        try:
            print("Getting sheets using GetAllInfos...")
            
            # Get all objects in the app
            all_infos_result = self._send_request("GetAllInfos", self.app_handle)
            
            if not all_infos_result or "qInfos" not in all_infos_result:
                raise ValueError("Failed to get app objects")
            
            # Filter for sheets
            all_objects = all_infos_result["qInfos"]
            sheet_infos = [obj for obj in all_objects if obj.get("qType") == "sheet"]
            print(f"Found {len(sheet_infos)} sheets")
            
            sheets = []
            
            # Get detailed information for each sheet
            for sheet_info in sheet_infos:
                sheet_id = sheet_info.get("qId", "")
                if not sheet_id:
                    continue
                
                try:
                    # Get the sheet object to retrieve metadata
                    sheet_obj_result = self._send_request("GetObject", self.app_handle, [sheet_id])
                    
                    if sheet_obj_result and "qReturn" in sheet_obj_result:
                        # Get the handle for the sheet object
                        sheet_handle = sheet_obj_result["qReturn"]["qHandle"]
                        
                        # Get the layout from the sheet handle
                        layout_result = self._send_request("GetLayout", sheet_handle)
                        
                        if layout_result and "qLayout" in layout_result:
                            layout = layout_result["qLayout"]
                            q_meta = layout.get("qMeta", {})
                            
                            sheet_data = {
                                "sheet_id": sheet_id,
                                "title": q_meta.get("title", ""),
                                "description": q_meta.get("description", ""),
                                "rank": layout.get("rank", 0)
                            }
                            
                            if include_thumbnail:
                                sheet_data["thumbnail"] = q_meta.get("thumbnail", "")
                            
                            if include_metadata:
                                sheet_data["created"] = q_meta.get("createdDate", "")
                                sheet_data["modified"] = q_meta.get("modifiedDate", "")
                                sheet_data["published"] = q_meta.get("published", False)
                                sheet_data["approved"] = q_meta.get("approved", False)
                            
                            sheets.append(sheet_data)
                        else:
                            raise ValueError("No layout data returned")
                    else:
                        raise ValueError("GetObject failed")
                        
                except Exception as e:
                    print(f"Warning: Could not get metadata for sheet {sheet_id}: {e}")
                    # Add basic sheet info even if metadata retrieval fails
                    sheets.append({
                        "sheet_id": sheet_id,
                        "title": sheet_id,  # Use sheet_id as title fallback
                        "description": "",
                        "rank": 0
                    })
            
            # Sort sheets by rank
            sheets.sort(key=lambda x: x.get("rank", 0))
            
            print(f"Successfully retrieved {len(sheets)} sheets")
            
            return {
                "sheets": sheets,
                "sheet_count": len(sheets)
            }
            
        except Exception as e:
            print(f"Error retrieving sheets: {e}")
            raise
    
    def get_sheet_objects(
        self,
        sheet_id: str,
        include_properties: bool = True,
        include_layout: bool = True,
        include_data_definition: bool = True
    ) -> Dict[str, Any]:
        """Retrieve all visualization objects from a specific sheet"""
        if not self.ws or not self.app_handle:
            raise ConnectionError("Not connected to Qlik Engine")
        
        try:
            # First get the sheet object itself
            print(f"Getting sheet object: {sheet_id}")
            sheet_result = self._send_request(
                "GetObject",
                self.app_handle,
                [sheet_id]
            )
            
            if not sheet_result or "qReturn" not in sheet_result:
                raise ValueError(f"Failed to get sheet object: {sheet_id}")
            
            sheet_handle = sheet_result["qReturn"]["qHandle"]
            print(f"Got sheet with handle: {sheet_handle}")
            
            # Get sheet layout
            sheet_layout = self._send_request("GetLayout", sheet_handle)
            sheet_data = sheet_layout.get("qLayout", sheet_layout) if sheet_layout else {}
            
            sheet_title = ""
            if "qMeta" in sheet_data:
                sheet_title = sheet_data["qMeta"].get("title", "")
            
            # Get child objects (visualizations)
            child_infos = []
            if "qChildList" in sheet_data:
                child_list = sheet_data["qChildList"]
                if "qItems" in child_list:
                    child_infos = child_list["qItems"]
            
            print(f"Found {len(child_infos)} child objects")
            
            # Process each visualization object
            objects = []
            for child_info in child_infos:
                obj_id = child_info.get("qInfo", {}).get("qId", "")
                obj_type = child_info.get("qInfo", {}).get("qType", "")
                
                obj_data = {
                    "object_id": obj_id,
                    "object_type": obj_type
                }
                
                # Get detailed object information if it's not a container
                if obj_type not in ["container", "filterpane"]:
                    try:
                        # Get the object
                        obj_result = self._send_request(
                            "GetObject",
                            self.app_handle,
                            [obj_id]
                        )
                        
                        if obj_result and "qReturn" in obj_result:
                            obj_handle = obj_result["qReturn"]["qHandle"]
                            
                            # Get object layout for detailed info
                            obj_layout = self._send_request("GetLayout", obj_handle)
                            obj_layout_data = obj_layout.get("qLayout", obj_layout) if obj_layout else {}
                            
                            # Extract title and subtitle
                            if "title" in obj_layout_data:
                                obj_data["title"] = obj_layout_data["title"]
                            if "subtitle" in obj_layout_data:
                                obj_data["subtitle"] = obj_layout_data["subtitle"]
                            
                            # Extract layout information
                            if include_layout and "qInfo" in obj_layout_data:
                                obj_data["layout"] = {
                                    "x": child_info.get("qData", {}).get("col", 0),
                                    "y": child_info.get("qData", {}).get("row", 0),
                                    "width": child_info.get("qData", {}).get("colspan", 0),
                                    "height": child_info.get("qData", {}).get("rowspan", 0)
                                }
                            
                            # Extract measures and dimensions
                            if include_data_definition:
                                measures = []
                                dimensions = []
                                
                                # Get measures from HyperCubeDef
                                if "qHyperCubeDef" in obj_layout_data:
                                    hc_def = obj_layout_data["qHyperCubeDef"]
                                    
                                    # Extract measures
                                    if "qMeasures" in hc_def:
                                        for measure in hc_def["qMeasures"]:
                                            measure_def = measure.get("qDef", {})
                                            measures.append({
                                                "label": measure_def.get("qLabel", ""),
                                                "expression": measure_def.get("qDef", "")
                                            })
                                    
                                    # Extract dimensions
                                    if "qDimensions" in hc_def:
                                        for dimension in hc_def["qDimensions"]:
                                            dim_def = dimension.get("qDef", {})
                                            dimensions.append({
                                                "label": dim_def.get("qLabel", ""),
                                                "field": dim_def.get("qFieldDefs", [""])[0] if dim_def.get("qFieldDefs") else ""
                                            })
                                
                                if measures:
                                    obj_data["measures"] = measures
                                if dimensions:
                                    obj_data["dimensions"] = dimensions
                            
                            # Extract properties if requested
                            if include_properties:
                                properties = {}
                                
                                # Extract color settings
                                if "color" in obj_layout_data:
                                    properties["color"] = obj_layout_data["color"]
                                
                                # Extract other visualization-specific properties
                                if "qHyperCubeDef" in obj_layout_data:
                                    hc_def = obj_layout_data["qHyperCubeDef"]
                                    if "qInterColumnSortOrder" in hc_def:
                                        properties["sortOrder"] = hc_def["qInterColumnSortOrder"]
                                
                                if properties:
                                    obj_data["properties"] = properties
                    
                    except Exception as e:
                        print(f"Warning: Could not get details for object {obj_id}: {e}")
                        # Continue with basic info
                
                objects.append(obj_data)
            
            # Clean up session object (skip for now to avoid errors)
            # Note: In production, should properly destroy session objects
            
            return {
                "sheet_title": sheet_title,
                "objects": objects,
                "object_count": len(objects)
            }
            
        except Exception as e:
            print(f"Error retrieving sheet objects: {e}")
            raise
    
    def get_dimensions(
        self,
        include_title: bool = True,
        include_tags: bool = True,
        include_grouping: bool = True,
        include_info: bool = True
    ) -> Dict[str, Any]:
        """Retrieve all dimensions from the current app"""
        if not self.ws or not self.app_handle:
            raise ConnectionError("Not connected to Qlik Engine")
        
        try:
            print("Creating DimensionList session object...")
            
            # Build qData paths based on options
            q_data = {}
            
            if include_title:
                q_data["title"] = "/title"
            
            if include_tags:
                q_data["tags"] = "/tags"
            
            if include_grouping:
                q_data["grouping"] = "/qDim/qGrouping"
            
            if include_info:
                q_data["info"] = "/qDimInfos"
            
            create_params = [
                {
                    "qInfo": {
                        "qType": "DimensionList"
                    },
                    "qDimensionListDef": {
                        "qType": "dimension",
                        "qData": q_data
                    }
                }
            ]
            
            create_result = self._send_request(
                "CreateSessionObject",
                self.app_handle,
                create_params
            )
            
            if not create_result or "qReturn" not in create_result:
                raise ValueError("Failed to create DimensionList object")
            
            dimension_list_handle = create_result["qReturn"]["qHandle"]
            print(f"Created DimensionList with handle: {dimension_list_handle}")
            
            # Get layout containing dimension data
            layout = self._send_request("GetLayout", dimension_list_handle)
            # The actual data is nested under qLayout
            actual_layout = layout.get("qLayout", layout) if layout else {}
            
            # Extract dimensions from layout
            dimensions = []
            if actual_layout and "qDimensionList" in actual_layout:
                items = actual_layout["qDimensionList"].get("qItems", [])
                print(f"Processing {len(items)} dimensions...")
                for item in items:
                    # Parse both qData (custom paths) and standard qInfo
                    q_data = item.get("qData", {})
                    q_info = item.get("qInfo", {})
                    q_meta = item.get("qMeta", {})
                    
                    dimension = {
                        "dimension_id": q_info.get("qId", ""),
                        "name": q_meta.get("title", q_info.get("qId", ""))
                    }
                    
                    if include_title:
                        dimension["title"] = q_data.get("title", q_meta.get("title", ""))
                    
                    if include_tags:
                        dimension["tags"] = q_data.get("tags", [])
                    
                    if include_grouping:
                        dimension["grouping"] = q_data.get("grouping", "N")
                    
                    if include_info:
                        dimension["info"] = q_data.get("info", [])
                    
                    # Add additional metadata from qMeta
                    dimension["description"] = q_meta.get("description", "")
                    dimension["created"] = q_meta.get("createdDate", "")
                    dimension["modified"] = q_meta.get("modifiedDate", "")
                    dimension["published"] = q_meta.get("published", False)
                    dimension["approved"] = q_meta.get("approved", False)
                    
                    dimensions.append(dimension)
            
            # Clean up session object (skip for now to avoid errors)
            # Note: In production, should properly destroy session objects
            print(f"Found {len(dimensions)} dimensions")
            
            return {
                "dimensions": dimensions,
                "dimension_count": len(dimensions)
            }
            
        except Exception as e:
            print(f"Error retrieving dimensions: {e}")
            raise
    
    def get_script(self) -> Dict[str, Any]:
        """Retrieve the script from the current app"""
        if not self.ws or not self.app_handle:
            raise ConnectionError("Not connected to Qlik Engine")
        
        try:
            print("Getting app script...")
            
            # Call GetScript method on the app handle
            script_result = self._send_request("GetScript", self.app_handle)
            
            if not script_result:
                raise ValueError("Failed to get app script")
            
            print("Successfully retrieved app script")
            
            # The script content is typically in qScript
            script_content = script_result.get("qScript", "")
            
            return {
                "script": script_content,
                "script_length": len(script_content)
            }
            
        except Exception as e:
            print(f"Error retrieving script: {e}")
            raise
    
    def get_lineage(
        self,
        include_resident: bool = True,
        include_file_sources: bool = True,
        include_binary_sources: bool = True,
        include_inline_sources: bool = True
    ) -> Dict[str, Any]:
        """Retrieve data sources lineage from the current app"""
        if not self.ws or not self.app_handle:
            raise ConnectionError("Not connected to Qlik Engine")
        
        try:
            print("Getting app data sources lineage...")
            
            # Call GetLineage method on the app handle (no parameters needed)
            lineage_result = self._send_request("GetLineage", self.app_handle)
            
            if not lineage_result:
                raise ValueError("Failed to get app lineage")
            
            print("Successfully retrieved app lineage")
            
            # The lineage data is in qLineage
            lineage_data = lineage_result.get("qLineage", [])
            
            # Process and categorize the data sources
            data_sources = []
            categories = {
                "binary": [],
                "resident": [],
                "file": [],
                "inline": [],
                "other": []
            }
            
            for item in lineage_data:
                discriminator = item.get("qDiscriminator", "")
                statement = item.get("qStatement", "")
                
                # Create data source object
                source = {
                    "discriminator": discriminator,
                    "statement": statement if statement else None,
                    "type": self._categorize_data_source(discriminator, statement)
                }
                
                # Apply filters based on include options
                source_type = source["type"]
                if (source_type == "binary" and include_binary_sources) or \
                   (source_type == "resident" and include_resident) or \
                   (source_type == "file" and include_file_sources) or \
                   (source_type == "inline" and include_inline_sources) or \
                   (source_type == "other"):
                    
                    data_sources.append(source)
                    categories[source_type].append(source)
            
            print(f"Found {len(data_sources)} data sources")
            
            return {
                "data_sources": data_sources,
                "source_count": len(data_sources),
                "categories": {
                    "binary_count": len(categories["binary"]),
                    "resident_count": len(categories["resident"]),
                    "file_count": len(categories["file"]),
                    "inline_count": len(categories["inline"]),
                    "other_count": len(categories["other"])
                },
                "by_category": categories
            }
            
        except Exception as e:
            print(f"Error retrieving lineage: {e}")
            raise
    
    def _categorize_data_source(self, discriminator: str, statement: str = None) -> str:
        """Categorize data source based on discriminator and statement"""
        discriminator_lower = discriminator.lower()
        
        # Check for binary sources
        if statement and statement.lower() == "binary":
            return "binary"
        
        # Check for resident sources
        if discriminator_lower.startswith("resident "):
            return "resident"
        
        # Check for inline sources
        if discriminator_lower.startswith("inline"):
            return "inline"
        
        # Check for file sources (paths, URLs, etc.)
        if any(indicator in discriminator_lower for indicator in [
            "\\", "/", ".", "lib://", "http://", "https://", "ftp://", ".txt", ".csv", ".xlsx", ".qvd"
        ]):
            return "file"
        
        # Everything else
        return "other"
    
    def _send_request(self, method: str, handle: int = -1, params: Optional[Any] = None) -> Dict[str, Any]:
        """Send JSON-RPC request and wait for response"""
        if not self.ws:
            raise ConnectionError("WebSocket is not connected")
        
        self.request_id += 1
        
        # Handle params based on method type
        if method == "CreateSessionObject" and isinstance(params, list):
            # CreateSessionObject expects array params
            request = {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "method": method,
                "handle": handle,
                "params": params
            }
        elif method == "OpenDoc" and isinstance(params, dict) and "qDocName" in params:
            # OpenDoc expects array with just the doc name
            request = {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "method": method,
                "handle": handle,
                "params": [params["qDocName"]]
            }
        else:
            request = {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "method": method,
                "handle": handle,
                "params": params if params is not None else {}
            }
        
        # Send request
        self.ws.send(json.dumps(request))
        
        # Set receive timeout
        if hasattr(self.ws, 'sock') and self.ws.sock:
            self.ws.sock.settimeout(self.recv_timeout)
        
        # Wait for response
        while True:
            response_str = self.ws.recv()
            response = json.loads(response_str)
            
            # Skip connection messages
            if response.get("method") == "OnConnected":
                continue
            
            # Check for errors
            if "error" in response:
                error = response["error"]
                raise Exception(f"Engine API Error: {error.get('message', 'Unknown error')}")
            
            # Check if this is our response
            if response.get("id") == self.request_id:
                return response.get("result", {})


def test_connection():
    """Test function to verify Qlik connection and measure retrieval"""
    client = QlikClient()
    
    # Test with a sample app ID (replace with actual app ID)
    test_app_id = "12345678-abcd-1234-efgh-123456789abc"
    
    try:
        if client.connect(test_app_id):
            print("\n✅ Connection successful!")
            
            # Get measures
            result = client.get_measures(include_expression=True, include_tags=True)
            
            print(f"\n📊 Found {result['count']} measures:")
            for measure in result['measures'][:5]:  # Show first 5
                print(f"  - {measure['title']} (ID: {measure['id']})")
                if measure.get('expression'):
                    print(f"    Expression: {measure['expression'][:50]}...")
            
            client.disconnect()
            return True
        else:
            print("❌ Connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        client.disconnect()
        return False


if __name__ == "__main__":
    # Run test when module is executed directly
    test_connection()