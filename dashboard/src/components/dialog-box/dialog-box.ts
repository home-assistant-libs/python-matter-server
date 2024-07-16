import "@material/web/button/text-button";
import "@material/web/dialog/dialog";
import { html, LitElement } from "lit";
import { customElement, property } from "lit/decorators.js";
import { preventDefault } from "../../util/prevent_default";
import type { PromptDialogBoxParams } from "./show-dialog-box";
@customElement("dialox-box")
export class DialogBox extends LitElement {
  @property({ attribute: false }) public params!: PromptDialogBoxParams;

  @property({ attribute: false }) public dialogResult!: (
    result: boolean
  ) => void;

  @property() public type!: "alert" | "prompt";

  protected render() {
    const params = this.params;
    return html`
      <md-dialog open @cancel=${preventDefault} @closed=${this._handleClosed}>
        ${params.title ? html`<div slot="headline">${params.title}</div>` : ""}
        ${params.text ? html`<div slot="content">${params.text}</div>` : ""}
        <div slot="actions">
          ${this.type === "prompt"
            ? html`
                <md-text-button @click=${this._cancel}>
                  ${params.cancelText || "Cancel"}
                </md-text-button>
              `
            : ""}
          <md-text-button @click=${this._confirm}>
            ${params.confirmText || "OK"}
          </md-text-button>
        </div>
      </md-dialog>
    `;
  }

  private _cancel() {
    this._setResult(false);
  }

  private _confirm() {
    this._setResult(true);
  }

  _setResult(result: boolean) {
    this.dialogResult(result);
    this.shadowRoot!.querySelector("md-dialog")!.close();
  }

  private _handleClosed() {
    this.parentElement!.removeChild(this);
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "dialox-box": DialogBox;
  }
}
