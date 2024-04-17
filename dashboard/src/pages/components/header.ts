import "@material/web/iconbutton/icon-button";
import { LitElement, css, html } from "lit";
import { customElement, property } from "lit/decorators.js";
import "@material/web/list/list";
import "@material/web/list/list-item";
import "@material/web/divider/divider";
import "@material/web/button/outlined-button";
import "../../components/ha-svg-icon";
import { mdiArrowLeft, mdiLogout } from "@mdi/js";


interface HeaderAction {
  label: string;
  icon: string;
  action: void;
}

@customElement("dashboard-header")
export class DashboardHeader extends LitElement {

  @property() public backButton?: string;
  @property() public actions?: HeaderAction[];

  protected render() {
    const isProductionServer = location.href.includes(":5580") || location.href.includes("hassio_ingress");
    return html`
      <div class="header">

      <!-- optional back button -->
        ${this.backButton ? html`
        <a .href=${this.backButton}>
          <md-icon-button>
            <ha-svg-icon .path=${mdiArrowLeft}></ha-svg-icon>
          </md-icon-button>
        </a>` : ''}

      <div>${this.title || ''}</div>
      <div class="flex"></div>
      <div class="actions">
      ${this.actions?.map((action) => {
      return html`
          <md-icon-button @click=${action.action} .title=${action.label}>
                <ha-svg-icon .path=${action.icon}></ha-svg-icon>
            </md-icon-button>
          `
    })}
      <!-- optional logout button -->
      ${isProductionServer
        ? ""
        : html`
          <md-icon-button @click=${this._disconnect}>
            <ha-svg-icon .path=${mdiLogout}></ha-svg-icon>
          </md-icon-button>
          `}
      </div>
    </div>
    `;
  }

  private _disconnect() {
    localStorage.removeItem("matterURL");
    location.reload();
  }

  static styles = css`

    .header {
      background-color: var(--md-sys-color-primary);
      color: var(--md-sys-color-on-primary);
      --icon-primary-color: var(--md-sys-color-on-primary);
      font-weight: 400;
      display: flex;
      align-items: center;
      padding-left: 18px;
      padding-right: 8px;
      height: 48px;
    }

    md-icon-button {
      margin-right: 8px;
    }

    .flex {
      flex: 1;
    }

  `;

}
