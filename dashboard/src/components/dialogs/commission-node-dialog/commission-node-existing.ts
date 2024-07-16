import { consume } from "@lit/context";
import "@material/web/textfield/outlined-text-field";
import "@material/web/progress/circular-progress";
import type { MdOutlinedTextField } from "@material/web/textfield/outlined-text-field";
import { LitElement, html, nothing } from "lit";
import { customElement, property, query, state } from "lit/decorators.js";
import { MatterClient } from "../../../client/client";
import { clientContext } from "../../../client/client-context";
import { fireEvent } from "../../../util/fire_event";

@customElement("commission-node-existing")
export class CommissionNodeExisting extends LitElement {
  @consume({ context: clientContext, subscribe: true })
  @property({ attribute: false })
  public client!: MatterClient;

  @state()
  private _loading: boolean = false;

  @query("md-outlined-text-field[label='Share code']")
  private _pairingCodeField!: MdOutlinedTextField;

  protected render() {
    return html`<md-outlined-text-field label="Share code" .disabled="${this._loading}">
      </md-outlined-text-field>
      <br />
      <br />
      <md-outlined-button @click=${this._commissionNode} .disabled="${this._loading}"
        >Commission</md-outlined-button
      >${this._loading ? html`<md-circular-progress indeterminate></md-circular-progress>` : nothing}`;
  }

  private async _commissionNode() {
    this._loading = true;
    try {
      const node = await this.client.commissionWithCode(this._pairingCodeField.value, false);
      fireEvent(this, "node-commissioned", node);
    } catch (err) {
      alert(`Error commissioning node: ${(err as Error).message}`);
    } finally {
      this._loading = false;
    }
  }
}
