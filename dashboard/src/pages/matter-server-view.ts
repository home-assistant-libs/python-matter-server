import "@material/web/iconbutton/icon-button";
import { LitElement, css, html } from "lit";
import { customElement } from "lit/decorators.js";
import { MatterClient } from "../client/client";
import "../components/ha-svg-icon";
import { mdiArrowLeft } from "@mdi/js";

declare global {
  interface HTMLElementTagNameMap {
    "matter-server-view": MatterServerView;
  }
}

@customElement("matter-server-view")
class MatterServerView extends LitElement {
  public client!: MatterClient;

  render() {
    return html`
      <div class="header">
        <a href="#">
          <md-icon-button>
            <ha-svg-icon .path=${mdiArrowLeft}></ha-svg-icon>
          </md-icon-button>
        </a>

        <div>Matter Server</div>
        <div class="flex"></div>
        <div class="actions"></div>
      </div>
      <div class="container">
        <pre>${JSON.stringify(this.client.serverInfo, undefined, 2)}</pre>
      </div>
    `;
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
      flex: 1;
    }
  `;
}
