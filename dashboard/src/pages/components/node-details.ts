import "@material/web/button/filled-button";
import "@material/web/button/outlined-button";
import "@material/web/button/text-button";
import "@material/web/divider/divider";
import "@material/web/iconbutton/icon-button";
import "@material/web/list/list";
import "@material/web/list/list-item";
import {
  mdiChatProcessing,
  mdiShareVariant,
  mdiTrashCan,
  mdiUpdate,
  mdiLink,
} from "@mdi/js";

import { consume } from "@lit/context";
import { LitElement, css, html, nothing } from "lit";
import { customElement, property, state } from "lit/decorators.js";
import { MatterClient } from "../../client/client";
import { DeviceType } from "../../client/models/descriptions";
import { MatterNode } from "../../client/models/node";
import {
  showAlertDialog,
  showPromptDialog,
} from "../../components/dialog-box/show-dialog-box";
import "../../components/ha-svg-icon";
import { getEndpointDeviceTypes } from "../matter-endpoint-view";
import { bindingContext } from "./context";
import { showNodeBindingDialog } from "../../components/dialogs/binding/show-node-binding-dialog";

function getNodeDeviceTypes(node: MatterNode): DeviceType[] {
  const uniqueEndpoints = new Set(
    Object.keys(node!.attributes).map((key) => Number(key.split("/")[0]))
  );
  const allDeviceTypes: Set<DeviceType> = new Set();
  uniqueEndpoints.forEach((endpointId) => {
    getEndpointDeviceTypes(node, endpointId).forEach((deviceType) => {
      allDeviceTypes.add(deviceType);
    });
  });
  return Array.from(allDeviceTypes);
}

@customElement("node-details")
export class NodeDetails extends LitElement {
  public client!: MatterClient;

  @property() public node?: MatterNode;

  @state()
  private _updateInitiated: boolean = false;

  @consume({ context: bindingContext })
  @property({ attribute: false })
  bindingPath!: string;

  protected render() {
    if (!this.node) return html``;

    const bindings = this.node.attributes[this.bindingPath];

    return html`
      <md-list>
        <md-list-item>
            <div slot="headline">
                <b>Node ${this.node.node_id} ${this.node.nodeLabel}</b>
                ${this.node.available
        ? nothing
        : html`<span class="status">OFFLINE</span>`
      }
      </div>
        </md-list-item>
        <md-list-item>
          <div slot="supporting-text">
            <span class="left">VendorName: </span>${this.node.vendorName}
          </div>
          <div slot="supporting-text">
            <span class="left">productName: </span>${this.node.productName}
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
          ${this.node.is_bridge
        ? ""
        : html` <div slot="supporting-text">
                  <span class="left">All device types: </span
                  >${getNodeDeviceTypes(this.node)
            .map((deviceType) => {
              return deviceType.label;
            })
            .join(" / ")}
                </div>`
      }
        </md-list-item>
        <md-list-item class="btn">
            <md-outlined-button @click=${this._reinterview}>Interview<ha-svg-icon slot="icon" .path=${mdiChatProcessing}></ha-svg-icon></md-outlined-button>
            ${this._updateInitiated || (this.node.updateState || 0) > 1 ? html`
                <md-outlined-button disabled>Update in progress (${this.node.updateStateProgress || 0}%)<ha-svg-icon slot="icon" .path=${mdiUpdate}></ha-svg-icon></md-outlined-button>`
        : html`<md-outlined-button @click=${this._searchUpdate}>Update<ha-svg-icon slot="icon" .path=${mdiUpdate}></ha-svg-icon></md-outlined-button>`}

          ${bindings
            ? html` 
              <md-outlined-button @click=${this._binding}> 
                Binding 
                <ha-svg-icon slot="icon" .path=${mdiLink}></ha-svg-icon>
              </md-outlined-button>
              `
            : nothing}

            <md-outlined-button @click=${this._openCommissioningWindow}>Share<ha-svg-icon slot="icon" .path=${mdiShareVariant}></ha-svg-icon></md-outlined-button>
            <md-outlined-button @click=${this._remove}>Remove<ha-svg-icon slot="icon" .path=${mdiTrashCan}></ha-svg-icon></md-outlined-button>
          </md-list-item>
      </md-list>
  `;
  }

  private async _reinterview() {
    if (
      !(await showPromptDialog({
        title: "Reinterview",
        text: "Are you sure you want to reinterview this node?",
        confirmText: "Reinterview",
      }))
    ) {
      return;
    }
    try {
      await this.client.interviewNode(this.node!.node_id);
      showAlertDialog({
        title: "Reinterview node",
        text: "Success!",
      });
      location.reload();
    } catch (err: any) {
      showAlertDialog({
        title: "Failed to reinterview node",
        text: err.message,
      });
    }
  }

  private async _remove() {
    if (
      !(await showPromptDialog({
        title: "Remove",
        text: "Are you sure you want to remove this node?",
        confirmText: "Remove",
      }))
    ) {
      return;
    }
    try {
      await this.client.removeNode(this.node!.node_id);
      // make sure to navigate back to the root if node details was opened
      location.replace("#");
    } catch (err: any) {
      showAlertDialog({
        title: "Failed to remove node",
        text: err.message,
      });
    }
  }

  private async _binding() {
    try {
      showNodeBindingDialog(this.client!, this.node!, this.bindingPath!);
    } catch (err: any) {
      console.log(err);
    }
  }

  private async _searchUpdate() {
    const nodeUpdate = await this.client.checkNodeUpdate(this.node!.node_id);
    if (!nodeUpdate) {
      showAlertDialog({
        title: "No update available",
        text: "No update available for this node",
      });
      return;
    }
    if (
      !(await showPromptDialog({
        title: "Firmware update available",
        text: `Found a firmware update for this node on ${nodeUpdate.update_source}.
          Do you want to update this node to version ${nodeUpdate.software_version_string}?
          Note that updating firmware is at your own risk and may cause the device to
          malfunction or needs additional handling such as power cycling it and/or recommisisoning it.
          Use with care.\n${nodeUpdate.firmware_information}`,
        confirmText: "Start Update",
      }))
    ) {
      return;
    }
    try {
      this._updateInitiated = true;
      await this.client.updateNode(this.node!.node_id, nodeUpdate.software_version);
    } catch (err: any) {
      showAlertDialog({
        title: "Failed to update node",
        text: err.message,
      });
    } finally {
      this._updateInitiated = false
    }
  }

  private async _openCommissioningWindow() {
    if (
      !(await showPromptDialog({
        title: "Share device",
        text: "Do you want to share this device with another Matter controller (open commissioning window)?",
        confirmText: "Share",
      }))
    ) {
      return;
    }
    try {
      const shareCode = await this.client.openCommissioningWindow(this.node!.node_id);
      showAlertDialog({
        title: "Share device",
        text: `Setup code: ${shareCode.setup_manual_code}`,
      });
    } catch (err: any) {
      showAlertDialog({
        title: "Failed to open commissioning window on node",
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
