import "@material/web/iconbutton/icon-button";
import { LitElement, css, html } from "lit";
import { guard } from 'lit/directives/guard.js';
import { customElement, property } from "lit/decorators.js";
import "@material/web/list/list";
import "@material/web/list/list-item";
import "@material/web/divider/divider";
import { MatterClient } from "../client/client";
import "../components/ha-svg-icon";
import "./components/header";
import "./components/node-details";
import { mdiChatProcessing, mdiChevronRight, mdiTrashCan } from "@mdi/js";
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

function getUniqueEndpoints(node: MatterNode) {
  // extract unique endpoints from the node attributes, as (sorted) array
  return Array.from(new Set(Object.keys(node!.attributes).map(key => Number(key.split("/")[0])))).sort((a, b) => { return a - b });
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
      <dashboard-header
        .title=${'Node ' + this.node.node_id}
        backButton="#"
        .actions=${[
        {
          label: "Reinterview node",
          icon: mdiChatProcessing,
          action: this._reinterview
        },
        {
          label: "Remove node",
          icon: mdiTrashCan,
          action: this._remove
        }
      ]}
      ></dashboard-header>

      <!-- node details section -->
      <div class="container">
      <node-details
          .node=${this.node}
        ></node-details>
      </div>

      <!-- Node Endpoints listing -->
      <div class="container">
        <md-list>
          <md-list-item>
            <div slot="headline">
                <b>Endpoints</b>
            </div>
          </md-list-item>

          ${guard([this.node?.attributes.length], () => getUniqueEndpoints(this.node!).map((endPointId) => {
        return html`
                <md-list-item type="link" href=${`#node/${this.node!.node_id}/${endPointId}`}>
                  <div slot="headline">
                    Endpoint ${endPointId}
                  </div>
                  <ha-svg-icon slot="end" .path=${mdiChevronRight}></ha-svg-icon>
                </md-list-item>
              `;
      }))}
        </md-list>
      </div>

      <dashboard-footer />
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
      location.reload();
    } catch (err: any) {
      showAlertDialog(this, {
        title: "Failed to reinterview node",
        text: err.message,
      });
    }
  }

  private async _remove() {
    if (
      !(await showPromptDialog(this, {
        title: "Remove",
        text: "Are you sure you want to remove this node?",
        confirmText: "Remove",
      }))
    ) {
      return;
    }
    try {
      await this.client.removeNode(this.node!.node_id);
      location.replace("#");
    } catch (err: any) {
      showAlertDialog(this, {
        title: "Failed to remove node",
        text: err.message,
      });
    }
  }

  static styles = css`

    :host {
      display: flex;
      background-color: var(--md-sys-color-background);
      box-sizing: border-box;
      flex-direction: column;
      min-height: 100vh;
    }

    .container {
      padding: 16px;
      max-width: 95%;
      margin: 0 auto;
      width: 100%;
    }

    @media (max-width: 600px) {
      .container {
        padding: 16px 0;
      }
    }

    .status {
      color: var(--danger-color);
      font-weight: bold;
      font-size: 0.8em;
    }
  `;
}
