import "@material/web/iconbutton/icon-button";
import "@material/web/divider/divider";
import "@material/web/list/list";
import "@material/web/list/list-item";
import { LitElement, css, html } from "lit";
import { customElement, property } from "lit/decorators.js";
import { MatterClient } from "../client/client";
import "../components/ha-svg-icon";
import { mdiChevronRight, mdiLogout } from "@mdi/js";
import memoizeOne from "memoize-one";

declare global {
  interface HTMLElementTagNameMap {
    "matter-dashboard": MatterDashboard;
  }
}

@customElement("matter-dashboard")
class MatterDashboard extends LitElement {
  public client!: MatterClient;

  @property()
  public nodes!: MatterClient["nodes"];

  private nodeEntries = memoizeOne((nodes: this["nodes"]) =>
    Object.entries(nodes)
  );

  render() {
    const nodes = this.nodeEntries(this.nodes);

    return html`
      <div class="header">
        <div>Python Matter Server</div>
        <div class="actions">
          <md-icon-button @click=${this._disconnect}>
            <ha-svg-icon .path=${mdiLogout}></ha-svg-icon>
          </md-icon-button>
        </div>
      </div>
      <div class="container">
        <md-list>
          <md-list-item type="link" href=${`#server`}>
            <span slot="start"></span>
            <div slot="headline">Matter Server</div>
            <div slot="supporting-text">
              ${this.client.serverInfo.sdk_version}
            </div>
            <ha-svg-icon slot="end" .path=${mdiChevronRight}></ha-svg-icon>
          </md-list-item>
          <md-divider></md-divider>
          ${nodes.map(([id, node]) => {
            return html`
              <md-list-item type="link" href=${`#node/${node.node_id}`}>
                <span slot="start">${node.node_id}</span>
                <div slot="headline">
                  ${node.vendorName} ${node.productName}
                  ${node.available
                    ? ""
                    : html`<span class="status">OFFLINE</span>`}
                </div>
                <div slot="supporting-text">${node.serialNumber}</div>
                <ha-svg-icon slot="end" .path=${mdiChevronRight}></ha-svg-icon>
              </md-list-item>
            `;
          })}
        </md-list>
      </div>
      <div class="footer">
        Python Matter Server is a project by Nabu Casa.
        <a href="https://www.nabucasa.com">Fund development</a>
      </div>
    `;
  }

  private _disconnect() {
    localStorage.removeItem("matterURL");
    location.reload();
  }

  static styles = css`
    :host {
      display: flex;
      background-color: var(--md-sys-color-background);
      box-sizing: border-box;
      flex-direction: column;
      min-height: 100vh;
    }

    .header {
      background-color: var(--md-sys-color-primary);
      color: var(--md-sys-color-on-primary);
      --icon-primary-color: var(--md-sys-color-on-primary);
      font-weight: 400;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-left: 16px;
      padding-right: 8px;
      height: 48px;
    }

    .container {
      padding: 16px;
      max-width: 600px;
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

    .footer {
      padding: 16px;
      text-align: center;
      font-size: 0.8em;
      color: var(--md-sys-color-on-surface);
    }

    .footer a {
      color: var(--md-sys-color-on-surface);
    }
  `;
}
