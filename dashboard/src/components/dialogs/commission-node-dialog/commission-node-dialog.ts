import "@material/web/button/text-button";
import "@material/web/dialog/dialog";
import "@material/web/list/list";
import "@material/web/list/list-item";
import { html, LitElement } from "lit";
import { customElement, state } from "lit/decorators.js";
import { preventDefault } from "../../../util/prevent_default";

@customElement("commission-node-dialog")
export class ComissionNodeDialog extends LitElement {
  @state() private _mode?: "wifi" | "thread" | "existing";

  protected render() {
    return html`
      <md-dialog open @cancel=${preventDefault} @closed=${this._handleClosed}>
        <div slot="headline">Commission node</div>
        <div slot="content">
          ${!this._mode
            ? html`<md-list>
                <md-list-item type="button" @click=${this._commissionWifi}
                  >Commission new WiFi device</md-list-item
                >
                <md-list-item type="button" @click=${this._commissionThread}
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
    import("./commission-node-wifi");
    this._mode = "wifi";
  }

  private _commissionThread() {
    import("./commission-node-thread");
    this._mode = "thread";
  }

  private _commissionExisting() {
    import("./commission-node-existing");
    this._mode = "existing";
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
}
