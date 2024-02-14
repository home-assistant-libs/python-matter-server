import "@material/web/dialog/dialog";
import "@material/web/button/text-button";
import { html, LitElement } from "lit";
import { customElement, property } from "lit/decorators.js";
import { preventDefault } from "../../util/prevent_default";
import type { PromptDialogBoxParams } from "./show-dialog-box";
@customElement("dialox-box")
export class DialogBox extends LitElement {
  @property() public params!: PromptDialogBoxParams;

  @property() public dialogResult!: (result: boolean) => void;

  @property() public type!: "alert" | "prompt";

  protected render() {
    const params = this.params;
    return html`
      <md-dialog open @cancel=${preventDefault} @close=${this._handleClose}>
        ${params.title ? html`<div slot="headline">${params.title}</div>` : ""}
        ${params.text ? html`<div slot="content">${params.text}</div>` : ""}
        <div slot="actions">
          ${this.type === "prompt"
            ? html`
                <md-text-button @click=${() => this._setResult(false)}>
                  ${params.cancelText || "Cancel"}
                </md-text-button>
              `
            : ""}
          <md-text-button @click=${() => this._setResult(true)}>
            ${params.confirmText || "OK"}
          </md-text-button>
        </div>
      </md-dialog>
    `;
  }

  _setResult(result: boolean) {
    this.dialogResult(result);
    this.shadowRoot!.querySelector("md-dialog")!.close();
  }

  private _handleClose() {
    this.parentElement!.removeChild(this);
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "dialox-box": DialogBox;
  }
}
