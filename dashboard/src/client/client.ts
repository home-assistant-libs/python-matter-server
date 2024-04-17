import { MatterNode } from "./models/node";
import { Connection } from "./connection";
import { InvalidServerVersion } from "./exceptions";
import {
  APICommands,
  ErrorResultMessage,
  EventMessage,
  SuccessResultMessage,
} from "./models/model";

export class MatterClient {
  public connection = new Connection(this.url);
  public nodes: Record<number, MatterNode> = {};
  private _result_futures: Record<
    string,
    { resolve: (value: any) => void; reject: (reason?: any) => void }
  > = {};
  private msgId = 0;
  private eventListeners: Record<string, Array<() => void>> = {};

  constructor(public url: string) {
    this.url = url;
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

  async commissionWithCode(code: string, networkOnly: boolean) {
    console.log("TODO");
  }

  async commissionOnNetwork(setup_pin_code: number, ip_addr: string) {
    console.log("TODO");
  }

  async setWifiCredentials(ssid: string, credentials: string) {
    console.log("TODO");
  }

  async setThreadOperationalDataset(dataset: string) {
    console.log("TODO");
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

  async pingNode(nodeId: number) {
    await this.sendCommand("ping_node", 0, { node_id: nodeId });
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
      const nodeId = (event.data as Array<any>)[0] as number;
      const attributeKey = (event.data as Array<any>)[1] as string;
      const attributeValue = (event.data as Array<any>)[2] as any;
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
