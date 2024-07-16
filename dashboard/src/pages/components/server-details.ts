import "@material/web/button/filled-button";
import "@material/web/button/outlined-button";
import "@material/web/button/text-button";
import "@material/web/divider/divider";
import "@material/web/iconbutton/icon-button";
import "@material/web/list/list";
import "@material/web/list/list-item";
import { mdiFile, mdiPlus } from "@mdi/js";
import { LitElement, css, html, nothing } from "lit";
import { customElement } from "lit/decorators.js";
import { MatterClient } from "../../client/client";
import {
  showAlertDialog,
  showPromptDialog,
} from "../../components/dialog-box/show-dialog-box";
import { showCommissionNodeDialog } from "../../components/dialogs/commission-node-dialog/show-commission-node-dialog";
import "../../components/ha-svg-icon";

@customElement("server-details")
export class ServerDetails extends LitElement {
  public client?: MatterClient;

  protected render() {
    if (!this.client) return html``;

    return html`
      <md-list>
        <md-list-item>
            <div slot="headline">
                <b>Python Matter Server ${this.client.isProduction ? "" : `(${this.client.serverBaseAddress})`}</b>
                ${
                  this.client.connection.connected
                    ? nothing
                    : html`<span class="status">OFFLINE</span>`
                }
      </div>
        </md-list-item>
        <md-list-item>
          <div slot="supporting-text">
            <div class="left">FabricId: </div>${this.client.serverInfo.fabric_id}
          </div>
          <div slot="supporting-text">
            <div class="left">Compressed FabricId: </div>${this.client.serverInfo.compressed_fabric_id}
          </div>
          <div slot="supporting-text">
            <div class="left">SDK Wheels Version: </div>${this.client.serverInfo.sdk_version}
          </div>
          <div slot="supporting-text">
            <div class="left">Schema Version: </div>${this.client.serverInfo.schema_version}
          </div>
          <div slot="supporting-text">
            <div class="left">Node count: </div>${Object.keys(this.client.nodes).length}
          </div>
        </md-list-item>
        <md-list-item class="btn">
          <span>
          <md-outlined-button @click=${this._commissionNode}>Commission node<ha-svg-icon slot="icon" .path=${mdiPlus}></ha-svg-icon></md-outlined-button>
          <md-outlined-button @click=${this._uploadDiagnosticsDumpFile}>Import node<ha-svg-icon slot="icon" .path=${mdiFile}></ha-svg-icon></md-outlined-button>
          </md-list-item>
      </md-list>
      <!-- hidden file element for the upload diagnostics -->
      <input
        @change=${this._onFileInput}
        type="file"
        id="fileElem"
        accept=".json"
        style="display:none" />
      </div>
  `;
  }

  private async _commissionNode() {
    showCommissionNodeDialog();
  }

  private async _uploadDiagnosticsDumpFile() {
    if (
      !(await showPromptDialog({
        title: "Add test node",
        text: "Do you want to add a test node from a diagnostics dump ?",
        confirmText: "Select file",
      }))
    ) {
      return;
    }
    // @ts-ignore:next-line
    const fileElem = this.renderRoot.getElementById(
      "fileElem"
    ) as HTMLInputElement;
    fileElem!.click();
  }

  private _onFileInput = (event: Event) => {
    const fileElem = event.target as HTMLInputElement;
    if (fileElem.files!.length > 0) {
      const selectedFile = fileElem.files![0];
      var reader = new FileReader();
      reader.readAsText(selectedFile, "UTF-8");
      reader.onload = async () => {
        try {
          await this.client!.importTestNode(reader.result?.toString() || "");
        } catch (err: any) {
          showAlertDialog({
            title: "Failed to import test node",
            text: err.message,
          });
        }
      };
    }
    event.preventDefault();
  };

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
  `;
}
