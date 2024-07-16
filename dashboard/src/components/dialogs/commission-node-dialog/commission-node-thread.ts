import { consume } from "@lit/context";
import "@material/web/textfield/outlined-text-field";
import type { MdOutlinedTextField } from "@material/web/textfield/outlined-text-field";
import { LitElement, html } from "lit";
import { customElement, property, query } from "lit/decorators.js";
import { MatterClient } from "../../../client/client";
import { clientContext } from "../../../client/client-context";

@customElement("commission-node-thread")
export class CommissionNodeThread extends LitElement {
  @consume({ context: clientContext, subscribe: true })
  @property({ attribute: false })
  public client!: MatterClient;

  @query("md-outlined-text-field[label='Thread dataset']")
  private _datasetField!: MdOutlinedTextField;
  @query("md-outlined-text-field[label='Pairing code']")
  private _pairingCodeField!: MdOutlinedTextField;

  protected render() {
    if (!this.client.serverInfo.thread_credentials_set) {
      return html`<md-outlined-text-field label="Thread dataset">
        </md-outlined-text-field>
        <md-outlined-button @click=${this._setThreadDataset}
          >Set Thread Dataset</md-outlined-button
        >`;
    }
    return html`<md-outlined-text-field label="Pairing code">
      </md-outlined-text-field>
      <md-outlined-button @click=${this._commissionNode}
        >Commission</md-outlined-button
      >`;
  }

  private _setThreadDataset() {
    const dataset = this._datasetField.value;
    if (!dataset) {
      alert("Dataset is required");
      return;
    }
    this.client.setThreadOperationalDataset(dataset);
  }

  private async _commissionNode() {
    try {
      await this.client.commissionWithCode(this._pairingCodeField.value, false);
    } catch (e) {}
  }
}
