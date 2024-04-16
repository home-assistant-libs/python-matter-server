import "@material/web/iconbutton/icon-button";
import { LitElement, css, html } from "lit";
import { customElement, property } from "lit/decorators.js";
import "@material/web/list/list";
import "@material/web/list/list-item";
import "@material/web/divider/divider";
import "@material/web/button/filled-button";
import "../../components/ha-svg-icon";
import { MatterNode } from "../../client/models/node";


@customElement("node-details")
export class NodeDetails extends LitElement {

  @property() public node?: MatterNode;

  protected render() {
    if (!this.node) return html``;
    return html`
      <md-list>
        <md-list-item>
            <div slot="headline">
                <b>Node ${this.node.node_id} ${this.node.nodeLabel}</b>
                ${this.node.available
        ? ""
        : html`<span class="status">OFFLINE</span>`}
      </div>
        </md-list-item>
        <md-list-item>
          <div slot="supporting-text">
            <div class="left">VendorName: </div>${this.node.vendorName}
          </div>
          <div slot="supporting-text">
          <div class="left">productName: </div>${this.node.productName}
          </div>
          <div slot="supporting-text">
          <span class="left">Commissioned: </span>${this.node.date_commissioned}
          </div>
          <div slot="supporting-text">
          <span class="left">Last interviewed: </span>${this.node.last_interview}
          </div>
          <div slot="supporting-text">
          <span class="left">Is bridge: </span>${this.node.is_bridge}
          </div>
          <div slot="supporting-text">
          <span class="left">Serialnumber: </span>${this.node.serialNumber}
          </div>
        </md-list-item>
      </md-list>
  `;
  }

  static styles = css`

    .left {
      width: 30%;
      display: inline-table;
    }
    .whitespace {
      height: 15px;
    }

  `;

}
