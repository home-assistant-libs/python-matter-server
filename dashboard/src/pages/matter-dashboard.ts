import "@material/web/iconbutton/icon-button";
import "@material/web/divider/divider";
import "@material/web/list/list";
import "@material/web/list/list-item";
import { LitElement, css, html } from "lit";
import { customElement, property } from "lit/decorators.js";
import { MatterClient } from "../client/client";
import "../components/ha-svg-icon";
import "./components/header";
import "./components/footer";
import { mdiChevronRight, mdiFile } from "@mdi/js";
import memoizeOne from "memoize-one";
import { showAlertDialog, showPromptDialog } from "../components/dialog-box/show-dialog-box";

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

    <dashboard-header
        title="Python Matter Server"
        .actions=${[
        {
          label: "Upload diagnostics dump",
          icon: mdiFile,
          action: this._uploadDiagnosticsDumpFile
        }
      ]}
      ></dashboard-header>

      <!-- hidden file element for the upload diagnostics -->
      <input
        type="file"
        id="fileElem"
        accept=".json"
        style="display:none" />

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
      <dashboard-footer />
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
