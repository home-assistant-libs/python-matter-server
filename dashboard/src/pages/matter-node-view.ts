import "@material/web/iconbutton/icon-button";
import { LitElement, css, html } from "lit";
import { customElement, property } from "lit/decorators.js";
import { MatterClient } from "../client/client";
import "../components/ha-svg-icon";
import { mdiArrowLeft, mdiChatProcessing } from "@mdi/js";
import { MatterNode } from "../client/models/node";
import {
  showAlertDialog,
  showPromptDialog,
} from "../components/dialog-box/show-dialog-box";

declare global {
  interface HTMLElementTagNameMap {
    "matter-node-view": MatterNodeView;
  }
}

@customElement("matter-node-view")
class MatterNodeView extends LitElement {
  public client!: MatterClient;

  @property()
  public node?: MatterNode;

  render() {
    if (!this.node) {
      return html`
        <p>Node not found!</p>
        <button
          @click=${() => {
            history.back();
          }}
        >
          Back
        </button>
      `;
    }

    return html`
      <div class="header">
        <a href="#">
          <md-icon-button>
            <ha-svg-icon .path=${mdiArrowLeft}></ha-svg-icon>
          </md-icon-button>
        </a>

        <div>Node ${this.node.node_id}</div>
        <div class="flex"></div>
        <div class="actions">
          <md-icon-button @click=${this._reinterview} title="Reinterview node">
            <ha-svg-icon .path=${mdiChatProcessing}></ha-svg-icon>
          </md-icon-button>
        </div>
      </div>
      <div class="container">
        <pre>${JSON.stringify(this.node.data, undefined, 2)}</pre>
      </div>
    `;
  }

  private async _reinterview() {
    if (
      !(await showPromptDialog(this, {
        title: "Reinterview",
        text: "Are you sure you want to reinterview this node?",
        confirmText: "Reinterview",
      }))
    ) {
      return;
    }
    try {
      await this.client.interviewNode(this.node!.node_id);
      showAlertDialog(this, {
        title: "Reinterview node",
        text: "Success!",
      });
    } catch (err: any) {
      showAlertDialog(this, {
        title: "Failed to reinterview node",
        text: err.message,
      });
    }
  }

  static styles = css`
    :host {
      display: block;
      background-color: var(--md-sys-color-background);
    }

    .header {
      background-color: var(--md-sys-color-primary);
      color: var(--md-sys-color-on-primary);
      --icon-primary-color: var(--md-sys-color-on-primary);
      font-weight: 400;
      display: flex;
      align-items: center;
      padding-right: 8px;
      height: 48px;
    }

    md-icon-button {
      margin-right: 8px;
    }

    .flex {
      flex: 1;
    }

    .container {
      padding: 16px;
      max-width: 600px;
      margin: 0 auto;
    }
  `;
}
