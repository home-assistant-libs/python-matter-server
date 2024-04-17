import "@material/web/iconbutton/icon-button";
import { LitElement, css, html } from "lit";
import { customElement } from "lit/decorators.js";
import "@material/web/list/list";
import "@material/web/list/list-item";
import "@material/web/divider/divider";
import "@material/web/button/filled-button";
import "@material/web/button/outlined-button";
import "@material/web/button/text-button";
import "../../components/ha-svg-icon";
import { mdiFile } from "@mdi/js";
import "../../components/ha-svg-icon";
import {
  showAlertDialog,
  showPromptDialog,
} from "../../components/dialog-box/show-dialog-box";
import { MatterClient } from "../../client/client";

@customElement("server-details")
export class ServerDetails extends LitElement {

  public client?: MatterClient;

  protected render() {
    if (!this.client) return html``;

    const isProductionServer = location.href.includes(":5580") || location.href.includes("hassio_ingress");
    const serverAddressBase = this.client.url.split("://")[1].split(":")[0];

    return html`
      <md-list>
        <md-list-item>
            <div slot="headline">
                <b>Python Matter Server ${isProductionServer ? '' : `(${serverAddressBase})`}</b>
                ${this.client.connection.connected
        ? ""
        : html`<span class="status">OFFLINE</span>`}
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
            <md-outlined-button @click=${this._uploadDiagnosticsDumpFile}>Import node<ha-svg-icon slot="icon" .path=${mdiFile}></ha-svg-icon></md-outlined-button>
          </md-list-item>
      </md-list>
      <!-- hidden file element for the upload diagnostics -->
      <input
        type="file"
        id="fileElem"
        accept=".json"
        style="display:none" />
      </div>
  `;
  }

  private async _uploadDiagnosticsDumpFile() {
    if (
      !(await showPromptDialog(this, {
        title: "Add test node",
        text: "Do you want to add a test node from a diagnostics dump ?",
        confirmText: "Select file",
      }))
    ) {
      return;
    }
    const fileElem = this.shadowRoot!.getElementById('fileElem') as HTMLInputElement;
    const handleInput = (event: Event) => {
      fileElem!.removeEventListener('change', handleInput);
      if (fileElem.files!.length > 0) {
        const selectedFile = fileElem.files![0];
        console.log(selectedFile);
        var reader = new FileReader();
        reader.readAsText(selectedFile, "UTF-8");
        reader.onload = async () => {
          try {
            await this.client.importTestNode(reader.result?.toString() || '');
          } catch (err: any) {
            showAlertDialog(this, {
              title: "Failed to import test node",
              text: err.message,
            });
          }
        }
      }
      event.preventDefault();
    }
    fileElem!.addEventListener('change', handleInput);
    fileElem!.click();
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

  `;

}
