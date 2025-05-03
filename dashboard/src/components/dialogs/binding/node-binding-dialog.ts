import "@material/web/button/text-button";
import "@material/web/dialog/dialog";
import "@material/web/list/list";
import "@material/web/list/list-item";
import "../../../components/ha-svg-icon";
import "@material/web/textfield/outlined-text-field";
import type { MdOutlinedTextField } from "@material/web/textfield/outlined-text-field";

import { html, LitElement } from "lit";
import { customElement, property, query } from "lit/decorators.js";
import { MatterNode } from "../../../client/models/node";
import { preventDefault } from "../../../util/prevent_default";
import { MatterClient } from "../../../client/client";
import {
  InputType,
  AccessControlEntryStruct,
  AccessControlEntryDataTransformer,
  BindingEntryStruct,
  BindingEntryDataTransformer,
} from "./model";

@customElement("node-binding-dialog")
export class NodeBindingDialog extends LitElement {
  @property({ attribute: false }) public client!: MatterClient;

  @property()
  public node?: MatterNode;

  @property({ attribute: false })
  bindingPath!: string;

  @query("md-outlined-text-field[label='target node id']")
  private _targetNodeId!: MdOutlinedTextField;

  @query("md-outlined-text-field[label='target endpoint']")
  private _targetEndpoint!: MdOutlinedTextField;

  private _transformBindingStruct(): BindingEntryStruct[] {
    const bindings_raw: [] = this.node!.attributes[this.bindingPath];
    return Object.values(bindings_raw).map((value) =>
      BindingEntryDataTransformer.transform(value)
    );
  }

  private _transformACLStruct(
    targetNodeId: number
  ): AccessControlEntryStruct[] {
    const acl_cluster_raw: [InputType] =
      this.client.nodes[targetNodeId].attributes["0/31/0"];
    return Object.values(acl_cluster_raw).map((value: InputType) =>
      AccessControlEntryDataTransformer.transform(value)
    );
  }

  async _bindingDelete(index: number) {
    const endpoint = this.bindingPath.split("/")[0];
    const bindings = this._transformBindingStruct();
    const targetNodeId = bindings[index].node;

    try {
      const acl_cluster = this._transformACLStruct(targetNodeId);
      const _acl_cluster = acl_cluster
        .map((entry) => {
          if (entry.subjects && entry.subjects.includes(this.node!.node_id)) {
            entry.subjects = entry.subjects.filter(
              (nodeId) => nodeId !== this.node!.node_id
            );
            if (entry.subjects.length === 0) {
              return null;
            }
          }
          return entry;
        })
        .filter((entry) => entry !== null);
      this.client.setACLEntry(targetNodeId, _acl_cluster);
    } catch (err) {
      console.log(err);
    }

    bindings.splice(index, 1);
    try {
      await this.client.setNodeBinding(
        this.node!.node_id,
        parseInt(endpoint, 10),
        bindings
      );
      this.node!.attributes[this.bindingPath].splice(index, 1);
      this.requestUpdate();
    } catch (err) {
      console.error("Failed to delete binding:", err);
    }
  }

  private async _updateEntry<T>(
    targetId: number,
    path: string,
    entry: T,
    transformFn: (value: InputType) => T,
    updateFn: (targetId: number, entries: T[]) => Promise<any>
  ) {
    try {
      const rawEntries: [InputType] =
        this.client.nodes[targetId].attributes[path];
      const entries = Object.values(rawEntries).map(transformFn);
      entries.push(entry);
      return await updateFn(targetId, entries);
    } catch (err) {
      console.log(err);
    }
  }

  private async add_target_acl(
    targetNodeId: number,
    entry: AccessControlEntryStruct
  ) {
    try {
      const result = (await this._updateEntry(
        targetNodeId,
        "0/31/0",
        entry,
        AccessControlEntryDataTransformer.transform,
        this.client.setACLEntry.bind(this.client)
      )) as { [key: string]: { Status: number } };
      return result["0"].Status === 0;
    } catch (err) {
      console.error("add acl error:", err);
      return false;
    }
  }

  private async add_bindings(
    endpoint: number,
    bindingEntry: BindingEntryStruct
  ) {
    const bindings = this._transformBindingStruct();
    bindings.push(bindingEntry);
    try {
      const result = (await this.client.setNodeBinding(
        this.node!.node_id,
        endpoint,
        bindings
      )) as { [key: string]: { Status: number } };
      return result["0"].Status === 0;
    } catch (err) {
      console.log("add bindings error:", err);
      return false;
    }
  }

  async _bindingAdd() {
    const targetNodeId = parseInt(this._targetNodeId.value, 10);
    const targetEndpoint = parseInt(this._targetEndpoint.value, 10);

    if (isNaN(targetNodeId) || targetNodeId <= 0) {
      alert("Please enter a valid target node ID");
      return;
    }
    if (isNaN(targetEndpoint) || targetEndpoint < 0) {
      alert("Please enter a valid target endpoint");
      return;
    }

    const acl_entry: AccessControlEntryStruct = {
      privilege: 5,
      authMode: 2,
      subjects: [this.node!.node_id],
      targets: undefined,
      fabricIndex: this.client.connection.serverInfo!.fabric_id,
    };
    const result_acl = await this.add_target_acl(targetNodeId, acl_entry);
    if (!result_acl) return;

    const endpoint = this.bindingPath.split("/")[0];
    const bindingEntry: BindingEntryStruct = {
      node: targetNodeId,
      endpoint: targetEndpoint,
      group: undefined,
      cluster: undefined,
      fabricIndex: undefined,
    };

    const result_binding = await this.add_bindings(
      parseInt(endpoint, 10),
      bindingEntry
    );

    if (result_binding) {
      this.requestUpdate();
    }
  }

  private _close() {
    this.shadowRoot!.querySelector("md-dialog")!.close();
  }

  private _handleClosed() {
    this.parentNode!.removeChild(this);
  }

  protected render() {
    const bindings = this.node!.attributes[this.bindingPath];

    return html`
      <md-dialog open @cancel=${preventDefault} @closed=${this._handleClosed}>
        <div slot="headline">
          <div>Binding Add</div>
        </div>
        <div slot="content">
          <div>
            <md-list>
              ${Object.values(bindings).map(
                (entry, index) => html`
                  <md-list-item>
                    <div slot="supporting-text">
                      ${JSON.stringify(
                        BindingEntryDataTransformer.transform(entry)
                      )}
                    </div>
                    <div slot="end">
                      <md-text-button
                        @click=${() => this._bindingDelete(index)}
                      >delete</md-text-button
                    </div>
                  </md-list-item>
                `
              )}
            </md-list>
            <div>
              <md-outlined-text-field
                label="target node id"
              ></md-outlined-text-field>
              <md-outlined-text-field
                label="target endpoint"
              ></md-outlined-text-field>
            </div>
          </div>
        </div>
        <div slot="actions">
          <md-text-button @click=${this._bindingAdd}>Add</md-text-button>
          <md-text-button @click=${this._close}>Cancel</md-text-button>
        </div>
      </md-dialog>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "node-binding-dialog": NodeBindingDialog;
  }
}
