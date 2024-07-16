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
    response: NodePingResult;
  };
  import_test_node: {
    requestArgs: { dump: string; };
    response: null;
  };
  get_node_ip_addresses: {
    requestArgs: { node_id: number, prefer_cache: boolean, scoped: boolean };
    response: string[];
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

export type EventMessage = ServerEventNodeAdded | ServerEventNodeUpdated | ServerEventNodeRemoved | ServerEventNodeEvent | ServerEventAttributeUpdated | ServerEventServerShutdown | ServerEventEndpointAdded | ServerEventEndpointRemoved


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

export type NotificationType = "success" | "info" | "warning" | "error";
export type NodePingResult = Record<string, boolean>;
