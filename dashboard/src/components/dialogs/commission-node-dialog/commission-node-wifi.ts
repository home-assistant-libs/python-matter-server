import { consume } from "@lit/context";
import "@material/web/textfield/outlined-text-field";
import "@material/web/progress/circular-progress";
import type { MdOutlinedTextField } from "@material/web/textfield/outlined-text-field";
import { LitElement, html, nothing } from "lit";
import { customElement, property, query, state } from "lit/decorators.js";
import { MatterClient } from "../../../client/client";
import { clientContext } from "../../../client/client-context";
import { fireEvent } from "../../../util/fire_event";

@customElement("commission-node-wifi")
export class CommissionNodeWifi extends LitElement {
  @consume({ context: clientContext, subscribe: true })
  @property({ attribute: false })
  public client!: MatterClient;

  @state()
  private _loading!: boolean;

  @query("md-outlined-text-field[label='SSID']")
  private _ssidField!: MdOutlinedTextField;
  @query("md-outlined-text-field[label='Password']")
  private _passwordField!: MdOutlinedTextField;
  @query("md-outlined-text-field[label='Pairing code']")
  private _pairingCodeField!: MdOutlinedTextField;

  protected render() {
    if (!this.client.serverInfo.wifi_credentials_set) {
      return html`<md-outlined-text-field label="SSID" .disabled="${this._loading}">
        </md-outlined-text-field>
        <md-outlined-text-field label="Password" type="password" .disabled="${this._loading}">
        </md-outlined-text-field>
        <br />
        <br />
        <md-outlined-button @click=${this._setWifiCredentials} .disabled="${this._loading}"
          >Set WiFi Credentials</md-outlined-button
        >${this._loading ? html`<md-circular-progress indeterminate .visible="${this._loading}"></md-circular-progress>` : nothing}`;
    }
    return html`<md-outlined-text-field label="Pairing code" ?disabled="${this._loading}">
      </md-outlined-text-field>
      <br />
      <br />
      <md-outlined-button @click=${this._commissionNode} ?disabled="${this._loading}"
        >Commission</md-outlined-button
      >${this._loading ? html`<md-circular-progress indeterminate></md-circular-progress>` : nothing}`;
  }

  private _setWifiCredentials() {
    this._loading = true;
    const ssid = this._ssidField.value;
    if (!ssid) {
      alert("SSID is required");
      this._loading = false;
      return;
    }
    const password = this._passwordField.value;
    if (!password) {
      alert("Password is required");
      this._loading = false;
      return;
    }
    try {
      this.client.setWifiCredentials(ssid, password);
      this._loading = false;
    } catch (err) {
      alert(`Error setting WiFi credentials: \n${(err as Error).message}`);
      this._loading = false;
    }
  }

  private async _commissionNode() {
    try {
      this._loading = true;
      if (!this._pairingCodeField.value) {
        alert("Pairing code is required");
        this._loading = false;
        return;
      }
      const node = await this.client.commissionWithCode(this._pairingCodeField.value, false);
      fireEvent(this, "node-commissioned", node);
      this._loading = false;
    } catch (err) {
      alert(`Error commissioning node: \n${(err as Error).message}`);
      this._loading = false;
    }
  }
}
