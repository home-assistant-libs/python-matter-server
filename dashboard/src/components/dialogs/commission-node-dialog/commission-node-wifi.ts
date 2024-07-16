import { consume } from "@lit/context";
import "@material/web/textfield/outlined-text-field";
import type { MdOutlinedTextField } from "@material/web/textfield/outlined-text-field";
import { LitElement, html } from "lit";
import { customElement, property, query } from "lit/decorators.js";
import { MatterClient } from "../../../client/client";
import { clientContext } from "../../../client/client-context";

@customElement("commission-node-wifi")
export class CommissionNodeWifi extends LitElement {
  @consume({ context: clientContext, subscribe: true })
  @property({ attribute: false })
  public client!: MatterClient;

  @query("md-outlined-text-field[label='SSID']")
  private _ssidField!: MdOutlinedTextField;
  @query("md-outlined-text-field[label='Password']")
  private _passwordField!: MdOutlinedTextField;
  @query("md-outlined-text-field[label='Pairing code']")
  private _pairingCodeField!: MdOutlinedTextField;

  protected render() {
    if (!this.client.serverInfo.wifi_credentials_set) {
      return html`<md-outlined-text-field label="SSID">
        </md-outlined-text-field>
        <md-outlined-text-field label="Password" type="password">
        </md-outlined-text-field>
        <md-outlined-button @click=${this._setWifiCredentials}
          >Set WiFi Credentials</md-outlined-button
        >`;
    }
    return html`<md-outlined-text-field label="Pairing code">
      </md-outlined-text-field>
      <md-outlined-button @click=${this._commissionNode}
        >Commission</md-outlined-button
      >`;
  }

  private _setWifiCredentials() {
    const ssid = this._ssidField.value;
    if (!ssid) {
      alert("SSID is required");
      return;
    }
    const password = this._passwordField.value;
    if (!password) {
      alert("Password is required");
      return;
    }
    this.client.setWifiCredentials(ssid, password);
  }

  private async _commissionNode() {
    try {
      await this.client.commissionWithCode(this._pairingCodeField.value, false);
    } catch (e) {}
  }
}
