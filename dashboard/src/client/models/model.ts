import { MatterNode } from "./node";

export interface APICommands {
  start_listening: {
    requestArgs: {};
    response: Array<MatterNode>;
  };
  diagnostics: {
    requestArgs: {};
    response: {};
  };
  server_info: {
    requestArgs: {};
    response: {};
  };
  get_nodes: {
    requestArgs: {};
    response: {};
  };
  get_node: {
    requestArgs: {};
    response: {};
  };
  commission_with_code: {
    requestArgs: {};
    response: {};
  };
  commission_on_network: {
    requestArgs: {};
    response: {};
  };
  set_wifi_credentials: {
    requestArgs: {};
    response: {};
  };
  set_thread_dataset: {
    requestArgs: {};
    response: {};
  };
  open_commissioning_window: {
    requestArgs: {};
    response: {};
  };
  discover: {
    requestArgs: {};
    response: {};
  };
  interview_node: {
    requestArgs: {};
    response: {};
  };
  device_command: {
    requestArgs: {};
    response: {};
  };
  remove_node: {
    requestArgs: {};
    response: {};
  };
  get_vendor_names: {
    requestArgs: {};
    response: {};
  };
  subscribe_attribute: {
    requestArgs: {};
    response: {};
  };
  read_attribute: {
    requestArgs: {};
    response: {};
  };
  write_attribute: {
    requestArgs: {};
    response: {};
  };
  ping_node: {
    requestArgs: {};
    response: {};
  };
  import_test_node: {
    requestArgs: {};
    response: null;
  };
  get_node_ip_addresses: {
    requestArgs: {};
    response: {};
  };
  check_node_update: {
    requestArgs: {};
    response: MatterSoftwareVersion | null;
  };
  update_node: {
    requestArgs: {};
    response: MatterSoftwareVersion | null;
  };
  discover_commissionable_nodes: {
    requestArgs: {};
    response: {};
  };
  get_matter_fabrics: {
    requestArgs: {};
    response: {};
  };
  remove_matter_fabric: {
    requestArgs: {};
    response: {};
  };
  set_acl_entry: {
    requestArgs: {};
    response: {};
  };
  set_node_binding: {
    requestArgs: {};
    response: {};
  };
}

export interface CommandMessage {
  message_id: string;
  command: string;
  args?: { [key: string]: any };
}

export interface ServerInfoMessage {
  fabric_id: number;
  compressed_fabric_id: number;
  schema_version: number;
  min_supported_schema_version: number;
  sdk_version: string;
  wifi_credentials_set: boolean;
  thread_credentials_set: boolean;
  bluetooth_enabled: boolean;
}

interface ServerEventNodeAdded {
  event: "node_added";
  data: MatterNode;
}
interface ServerEventNodeUpdated {
  event: "node_updated";
  data: MatterNode;
}
interface ServerEventNodeRemoved {
  event: "node_removed";
  data: number;
}
interface ServerEventNodeEvent {
  event: "node_event";
  data: {};
}
interface ServerEventAttributeUpdated {
  event: "attribute_updated";
  data: [number, string, any];
}
interface ServerEventServerShutdown {
  event: "server_shutdown";
  data: {};
}
interface ServerEventEndpointAdded {
  event: "endpoint_added";
  data: {};
}
interface ServerEventEndpointRemoved {
  event: "endpoint_removed";
  data: {};
}
interface ServerEvenInfoUpdated {
  event: "server_info_updated";
  data: ServerInfoMessage;
}

export type EventMessage = ServerEventNodeAdded | ServerEventNodeUpdated | ServerEventNodeRemoved | ServerEventNodeEvent | ServerEventAttributeUpdated | ServerEventServerShutdown | ServerEventEndpointAdded | ServerEventEndpointRemoved | ServerEvenInfoUpdated


export interface ResultMessageBase {
  message_id: string;
}

export interface ErrorResultMessage extends ResultMessageBase {
  error_code: number;
  details?: string;
}

export interface SuccessResultMessage extends ResultMessageBase {
  result: any; // Adjust according to the expected structure
}

export interface WebSocketConfig {
  host: string;
  port: string;
  scheme: string;
  path: string;
}

export enum UpdateSource {
  MAIN_NET_DCL = "main-net-dcl",
  TEST_NET_DCL = "test-net-dcl",
  LOCAL = "local"
}

export interface MatterSoftwareVersion {
  vid: number
  pid: number
  software_version: number
  software_version_string: string
  firmware_information?: string
  min_applicable_software_version: number
  max_applicable_software_version: number
  release_notes_url?: string
  update_source: UpdateSource
}

export interface CommissioningParameters {
  setup_pin_code: number
  setup_manual_code: string
  setup_qr_code: string
}

export interface CommissionableNodeData {
  instance_name?: string
  host_name?: string
  port?: number
  long_discriminator?: number
  vendor_id?: number
  product_id?: number
  commissioning_mode?: number
  device_type?: number
  device_name?: string
  pairing_instruction?: string
  pairing_hint?: number
  mrp_retry_interval_idle?: number
  mrp_retry_interval_active?: number
  supports_tcp?: boolean
  addresses?: string[]
  rotating_id?: string
}

export interface MatterFabricData {
  fabric_id?: number
  vendor_id?: number
  fabric_index?: number
  fabric_label?: string
  vendor_name?: string
}


export type NotificationType = "success" | "info" | "warning" | "error";
export type NodePingResult = Record<string, boolean>;
