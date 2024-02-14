import { CommandMessage, ServerInfoMessage } from "./models/model";

export class Connection {
  public serverInfo?: ServerInfoMessage = undefined;

  private socket?: WebSocket;

  constructor(public ws_server_url: string) {
    this.ws_server_url = ws_server_url;
  }

  get connected() {
    return this.socket?.readyState === WebSocket.OPEN;
  }

  async connect(onMessage: (msg: Record<string, any>) => void) {
    if (this.socket) {
      throw new Error("Already connected");
    }

    console.debug("Trying to connect");

    return new Promise((resolve, reject) => {
      this.socket = new WebSocket(this.ws_server_url);

      this.socket.onopen = () => {
        console.log("WebSocket Connected");
      };

      this.socket.onclose = (event) => {
        console.log(
          `WebSocket Closed: Code=${event.code}, Reason=${event.reason}`
        );
        reject(new Error("Connection Closed"));
      };

      this.socket.onerror = (error) => {
        console.error("WebSocket Error: ", error);
        console.dir(error);
        reject(new Error("WebSocket Error"));
      };

      this.socket.onmessage = (event: MessageEvent) => {
        const data = JSON.parse(event.data);
        console.log("WebSocket OnMessage", data);
        if (!this.serverInfo) {
          this.serverInfo = data;
          resolve(undefined);
          return;
        }
        onMessage(data);
      };
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = undefined;
    }
  }

  sendMessage(message: CommandMessage): void {
    if (!this.socket) {
      throw new Error("Not connected");
    }
    console.log("WebSocket send message", message);
    this.socket.send(JSON.stringify(message));
  }
}

export default Connection;
