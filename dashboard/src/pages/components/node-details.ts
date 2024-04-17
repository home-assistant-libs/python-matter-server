import "@material/web/iconbutton/icon-button";
import { LitElement, css, html, nothing } from "lit";
import { customElement, property } from "lit/decorators.js";
import "@material/web/list/list";
import "@material/web/list/list-item";
import "@material/web/divider/divider";
import "@material/web/button/filled-button";
import "@material/web/button/outlined-button";
import "@material/web/button/text-button";
import "../../components/ha-svg-icon";
import { MatterNode } from "../../client/models/node";
import { mdiChatProcessing, mdiTrashCan } from "@mdi/js";
import "../../components/ha-svg-icon";
import {
  showAlertDialog,
  showPromptDialog,
} from "../../components/dialog-box/show-dialog-box";
import { MatterClient } from "../../client/client";
import { getEndpointDeviceTypes } from "../matter-endpoint-view";
import { DeviceType } from "../../client/models/descriptions";


function getNodeDeviceTypes(node: MatterNode): DeviceType[] {
  const uniqueEndpoints = new Set(Object.keys(node!.attributes).map(key => Number(key.split("/")[0])))
  const allDeviceTypes: Set<DeviceType> = new Set();
  uniqueEndpoints.forEach(endpointId => {
    getEndpointDeviceTypes(node, endpointId).forEach(deviceType => {
      allDeviceTypes.add(deviceType);
    })
  });
  return Array.from(allDeviceTypes);
}

@customElement("node-details")
export class NodeDetails extends LitElement {

  public client!: MatterClient;

  @property() public node?: MatterNode;

  protected render() {
    if (!this.node) return html``;
    return html`
      <md-list>
        <md-list-item>
            <div slot="headline">
                <b>Node ${this.node.node_id} ${this.node.nodeLabel}</b>
                ${this.node.available
        ? nothing
        : html`<span class="status">OFFLINE</span>`}
      </div>
        </md-list-item>
        <md-list-item>
          <div slot="supporting-text">
            <span class="left">VendorName: </div>${this.node.vendorName}
          </div>
          <div slot="supporting-text">
            <span class="left">productName: </div>${this.node.productName}
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
          ${this.node.is_bridge ? '' : html`
            <div slot="supporting-text">
              <span class="left">All device types: </span>${getNodeDeviceTypes(this.node).map(deviceType => { return deviceType.label }).join(" / ")}
            </div>`
      }
        </md-list-item>
        <md-list-item class="btn">
          <span>
            <md-outlined-button @click=${this._reinterview}>Interview node<ha-svg-icon slot="icon" .path=${mdiChatProcessing}></ha-svg-icon></md-outlined-button>
            <md-outlined-button @click=${this._remove}>Remove node<ha-svg-icon slot="icon"  .path=${mdiTrashCan}></ha-svg-icon></md-outlined-button>
          </md-list-item>
      </md-list>
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

  .btn {
    --md-outlined-button-container-shape: 0px;
  }

    .left {
      width: 30%;
      display: inline-table;
    }
    .whitespace {
      height: 15px;
    }

    .status {
      color: var(--danger-color);
      font-weight: bold;
      font-size: 0.8em;
    }

  `;

}
