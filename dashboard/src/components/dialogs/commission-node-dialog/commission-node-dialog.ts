import "@material/web/button/text-button";
import "@material/web/dialog/dialog";
import "@material/web/list/list";
import "@material/web/list/list-item";
import { html, LitElement } from "lit";
import { customElement, property, state } from "lit/decorators.js";
import { MatterNode } from "../../../client/models/node";
import { preventDefault } from "../../../util/prevent_default";
import { MatterClient } from "../../../client/client";

@customElement("commission-node-dialog")
export class ComissionNodeDialog extends LitElement {

  @property({ attribute: false }) public client!: MatterClient;

  @state() private _mode?: "wifi" | "thread" | "existing";
  
  protected render() {
    return html`
      <md-dialog open @cancel=${preventDefault} @closed=${this._handleClosed}>
        <div slot="headline">Commission node</div>
        <div slot="content" @node-commissioned=${this._nodeCommissioned}>
          ${!this._mode
            ? html`<md-list>
                <md-list-item type="button" .disabled=${!this.client.serverInfo.bluetooth_enabled} @click=${this._commissionWifi}
                  >Commission new WiFi device</md-list-item
                >
                <md-list-item type="button" .disabled=${!this.client.serverInfo.bluetooth_enabled} @click=${this._commissionThread}
                  >Commission new Thread device</md-list-item
                >
                <md-list-item type="button" @click=${this._commissionExisting}
                  >Commission existing device</md-list-item
                >
              </md-list>`
            : this._mode === "wifi"
              ? html`<commission-node-wifi></commission-node-wifi>`
              : this._mode === "thread"
                ? html`<commission-node-thread></commission-node-thread>`
                : html`<commission-node-existing></commission-node-existing>`}
        </div>
        <div slot="actions">
          <md-text-button @click=${this._close}>Cancel</md-text-button>
        </div>
      </md-dialog>
    `;
  }

  private _commissionWifi() {
    if (!this.client.serverInfo.bluetooth_enabled) {
      return;
    }
    import("./commission-node-wifi");
    this._mode = "wifi";
  }

  private _commissionThread() {
    if (!this.client.serverInfo.bluetooth_enabled) {
      return;
    }
    import("./commission-node-thread");
    this._mode = "thread";
  }

  private _commissionExisting() {
    import("./commission-node-existing");
    this._mode = "existing";
  }

  private _nodeCommissioned(ev: CustomEvent<MatterNode>) {
    window.location.href = `#node/${ev.detail.node_id}`;
    this._close();
  }

  private _close() {
    this.shadowRoot!.querySelector("md-dialog")!.close();
  }

  private _handleClosed() {
    this.parentNode!.removeChild(this);
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "commission-node-dialog": ComissionNodeDialog;
  }

  interface HASSDomEvents {
    "node-commissioned": MatterNode;
  }
}
