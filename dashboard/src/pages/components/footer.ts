import { LitElement, css, html } from "lit";
import { customElement } from "lit/decorators.js";


@customElement("dashboard-footer")
export class DashboardFooter extends LitElement {

  protected render() {
    return html`
    <div class="footer">
      Python Matter Server is a project by Nabu Casa.
      <a href="https://www.nabucasa.com">Fund development</a>
    </div>
    `;
  }

  static styles = css`
    .footer {
      padding: 16px;
      text-align: center;
      font-size: 0.8em;
      color: var(--md-sys-color-on-surface);
      display: flex;
      flex-direction: column;
      position: relative;
    clear: both;
    }

    .footer a {
      color: var(--md-sys-color-on-surface);
    }
  `;

}
