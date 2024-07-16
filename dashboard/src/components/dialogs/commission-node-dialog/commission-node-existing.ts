import { consume } from "@lit/context";
import "@material/web/textfield/outlined-text-field";
import type { MdOutlinedTextField } from "@material/web/textfield/outlined-text-field";
import { LitElement, html } from "lit";
import { customElement, property, query } from "lit/decorators.js";
import { MatterClient } from "../../../client/client";
import { clientContext } from "../../../client/client-context";
import { fireEvent } from "../../../util/fire_event";

@customElement("commission-node-existing")
export class CommissionNodeExisting extends LitElement {
  @consume({ context: clientContext, subscribe: true })
  @property({ attribute: false })
  public client!: MatterClient;

  @query("md-outlined-text-field[label='Share code']")
  private _pairingCodeField!: MdOutlinedTextField;

  protected render() {
    return html`<md-outlined-text-field label="Share code">
      </md-outlined-text-field>
      <md-outlined-button @click=${this._commissionNode}
        >Commission</md-outlined-button
      >`;
  }

  private async _commissionNode() {
    try {
      const node = await this.client.commissionWithCode(this._pairingCodeField.value, false);
      fireEvent(this, "node-commissioned", node);
    } catch (e) {
        alert(`Error commissioning node: ${e.message}`);
    }
  }
}
