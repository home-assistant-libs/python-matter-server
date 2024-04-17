import "@material/web/iconbutton/icon-button";
import "@material/web/divider/divider";
import "@material/web/list/list";
import "@material/web/list/list-item";
import { LitElement, css, html } from "lit";
import { customElement, property } from "lit/decorators.js";
import { MatterClient } from "../client/client";
import "../components/ha-svg-icon";
import "./components/header";
import "./components/server-details";
import "./components/footer";
import { mdiChevronRight } from "@mdi/js";
import memoizeOne from "memoize-one";

declare global {
  interface HTMLElementTagNameMap {
    "matter-server-view": MatterServerView;
  }
}

@customElement("matter-server-view")
class MatterServerView extends LitElement {
  public client!: MatterClient;

  @property()
  public nodes!: MatterClient["nodes"];

  private nodeEntries = memoizeOne((nodes: this["nodes"]) =>
    Object.entries(nodes)
  );

  render() {
    const nodes = this.nodeEntries(this.nodes);

    return html`

    <dashboard-header
        title="Python Matter Server"
        .client=${this.client}
      ></dashboard-header>

      <!-- server details section -->
      <div class="container">
      <server-details
          .client=${this.client}
        ></server-details>
      </div>

      <!-- Nodes listing -->
      <div class="container">
        <md-list>
          <md-list-item>
            <div slot="headline">
                <b>Nodes</b>
            </div>
          </md-list-item>
          ${nodes.map(([id, node]) => {
      return html`
              <md-list-item type="link" href=${`#node/${node.node_id}`}>
                <div slot="headline">
                Node ${node.node_id}
                  ${node.available
          ? ""
          : html`<span class="status">OFFLINE</span>`}
                </div>
                <div slot="supporting-text">${node.nodeLabel ? `${node.nodeLabel} | ` : nothing} ${node.vendorName} | ${node.productName}</div>
                <ha-svg-icon slot="end" .path=${mdiChevronRight}></ha-svg-icon>
              </md-list-item>
            `;
    })}
        </md-list>
      </div>
      <dashboard-footer />
    `;
  }





  static styles = css`
    :host {
      display: flex;
      background-color: var(--md-sys-color-background);
      box-sizing: border-box;
      flex-direction: column;
    }

    .container {
      padding: 16px;
      max-width: 95%;
      margin: 0 auto;
      flex: 1;
      width: 100%;
    }

    @media (max-width: 600px) {
      .container {
        padding: 16px 0;
      }
    }

    span[slot="start"] {
      width: 40px;
      text-align: center;
    }

    .status {
      color: var(--danger-color);
      font-weight: bold;
      font-size: 0.8em;
    }

  `;
}
