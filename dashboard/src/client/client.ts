import { MatterNode } from "./models/node";
import { Connection } from "./connection";
import { InvalidServerVersion } from "./exceptions";
import {
  APICommands,
  ErrorResultMessage,
  EventMessage,
  NodePingResult,
  SuccessResultMessage,
} from "./models/model";

export class MatterClient {
  public connection = new Connection(this.url);
  public nodes: Record<number, MatterNode> = {};
  public serverBaseAddress = this.url.split("://")[1].split(":")[0] || '';
  private _result_futures: Record<
    string,
    { resolve: (value: any) => void; reject: (reason?: any) => void }
  > = {};
  private msgId = 0;
  private eventListeners: Record<string, Array<() => void>> = {};

  constructor(public url: string, public isProduction: boolean) {
    this.url = url;
    this.isProduction = isProduction;
  }

  get serverInfo() {
    return this.connection.serverInfo!;
  }

  addEventListener(event: string, listener: () => void) {
    if (!this.eventListeners[event]) {
      this.eventListeners[event] = [];
    }
    this.eventListeners[event].push(listener);
    return () => {
      this.eventListeners[event] = this.eventListeners[event].filter(
        (l) => l !== listener
      );
    };
  }

  async commissionWithCode(code: string, networkOnly: boolean): Promise<MatterNode> {
    return await this.sendCommand("commission_with_code", 0, { code: code, network_only: networkOnly }) as MatterNode;
  }

  async setWifiCredentials(ssid: string, credentials: string) {
    await this.sendCommand("set_wifi_credentials", 0, { ssid, credentials })
  }

  async setThreadOperationalDataset(dataset: string) {
    await this.sendCommand("set_thread_dataset", 0, { dataset })
  }

  async openCommissioningWindow(
    nodeId: number,
    timeout = 300,
    iteration = 1000,
    option = 1,
    distriminator: number | undefined = undefined
  ) {
    console.log("TODO");
  }

  async discoverCommissionableNodes() {
    console.log("TODO");
  }

  async getMatterFabrics(nodeId: number) {
    console.log("TODO");
  }

  async removeMatterFabric(nodeId: number, fabricId: number) {
    console.log("TODO");
  }

  async pingNode(nodeId: number): Promise<NodePingResult> {
    return await this.sendCommand("ping_node", 0, { node_id: nodeId });
  }

  async getNodeIPAddresses(nodeId: number, preferCache = false, scoped = false): Promise<string[]> {
    return await this.sendCommand("get_node_ip_addresses", 0, { node_id: nodeId, prefer_cache: preferCache, scoped: scoped });
  }

  async removeNode(nodeId: number) {
    await this.sendCommand("remove_node", 0, { node_id: nodeId });
  }

  async interviewNode(nodeId: number) {
    await this.sendCommand("interview_node", 0, { node_id: nodeId });
  }

  async importTestNode(dump: string) {
    await this.sendCommand("import_test_node", 0, { dump });
  }

  async writeAttribute(nodeId: number, attributePath: string, value: any) {
    await this.sendCommand("write_attribute", 0, { node_id: nodeId, attribute_path: attributePath, value: value });
  }

  async sendCommand<T extends keyof APICommands>(
    command: T,
    require_schema: number | undefined = undefined,
    args: APICommands[T]["requestArgs"]
  ): Promise<APICommands[T]["response"]> {
    if (require_schema && this.serverInfo.schema_version < require_schema) {
      throw new InvalidServerVersion(
        "Command not available due to incompatible server version. Update the Matter " +
        `Server to a version that supports at least api schema ${require_schema}.`
      );
    }

    const messageId = ++this.msgId;

    const message = {
      message_id: messageId.toString(),
      command,
      args,
    };

    const messagePromise = new Promise<Promise<APICommands[T]["response"]>>(
      (resolve, reject) => {
        this._result_futures[messageId] = { resolve, reject };
        this.connection.sendMessage(message);
      }
    );

    messagePromise.finally(() => {
      delete this._result_futures[messageId];
    });

    return messagePromise;
  }

  async connect() {
    if (this.connection.connected) {
      return;
    }
    await this.connection.connect((msg) => this._handleIncomingMessage(msg));
  }

  disconnect(clearStorage = true) {
    // disconnect from the server and clear the stored serveraddress
    if (this.connection && this.connection.connected) {
      this.connection.disconnect();
    }
    if (clearStorage) {
      localStorage.removeItem("matterURL");
      location.reload();
    }
  }

  async startListening() {
    await this.connect();

    const nodesArray = await this.sendCommand("start_listening", 0, {});

    const nodes: Record<number, MatterNode> = {};
    for (const node of nodesArray) {
      nodes[node.node_id] = new MatterNode(node);
    }
    this.nodes = nodes;
  }

  private _handleIncomingMessage(msg: any) {
    if ("event" in msg) {
      this._handleEventMessage(msg as EventMessage);
      return;
    }

    if ("error_code" in msg) {
      const errorResult = msg as ErrorResultMessage;
      const promise = this._result_futures[errorResult.message_id];
      if (promise) {
        promise.reject(new Error(errorResult.details));
        delete this._result_futures[errorResult.message_id];
      }
      return;
    }

    if ("result" in msg) {
      const result = msg as SuccessResultMessage;
      const promise = this._result_futures[result.message_id];
      if (promise) {
        promise.resolve(result.result);
        delete this._result_futures[result.message_id];
      }
      return;
    }

    console.warn("Received message with unknown format", msg);
  }

  private _handleEventMessage(event: EventMessage) {
    console.log("Incoming event", event);

    if (event.event === "node_added") {
      const node = new MatterNode(event.data);
      this.nodes = { ...this.nodes, [node.node_id]: node };
      this.fireEvent("nodes_changed");
      return;
    }
    if (event.event === "node_removed") {
      delete this.nodes[event.data];
      this.nodes = { ...this.nodes };
      this.fireEvent("nodes_changed");
      return;
    }

    if (event.event === "node_updated") {
      const node = new MatterNode(event.data);
      this.nodes = { ...this.nodes, [node.node_id]: node };
      this.fireEvent("nodes_changed");
      return;
    }

    if (event.event === "attribute_updated") {
      const [nodeId, attributeKey, attributeValue] = event.data;
      const node = new MatterNode(this.nodes[nodeId]);
      node.attributes[attributeKey] = attributeValue;
      this.nodes = { ...this.nodes, [node.node_id]: node };
      this.fireEvent("nodes_changed");
      return;
    }
  }

  private fireEvent(event: string, data?: any) {
    const listeners = this.eventListeners[event];
    if (listeners) {
      for (const listener of listeners) {
        listener();
      }
    }
  }
}
