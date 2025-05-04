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
import { consume } from "@lit/context";
import { clientContext } from "../../../client/client-context";

@customElement("node-binding-dialog")
export class NodeBindingDialog extends LitElement {
  @consume({ context: clientContext, subscribe: true })
  @property({ attribute: false })
  public client!: MatterClient;

  @property()
  public node?: MatterNode;

  @property({ attribute: false })
  endpoint!: number;

  @query("md-outlined-text-field[label='target node id']")
  private _targetNodeId!: MdOutlinedTextField;

  @query("md-outlined-text-field[label='target endpoint']")
  private _targetEndpoint!: MdOutlinedTextField;

  private fetchBindingEntry(): BindingEntryStruct[] {
    const bindings_raw: [] = this.node!.attributes[this.endpoint + "/30/0"];
    return Object.values(bindings_raw).map((value) =>
      BindingEntryDataTransformer.transform(value),
    );
  }

  private fetchACLEntry(targetNodeId: number): AccessControlEntryStruct[] {
    const acl_cluster_raw: [InputType] =
      this.client.nodes[targetNodeId].attributes["0/31/0"];
    return Object.values(acl_cluster_raw).map((value: InputType) =>
      AccessControlEntryDataTransformer.transform(value),
    );
  }

  private async deleteBindingHandler(index: number): Promise<void> {
    const rawBindings = this.fetchBindingEntry();
    try {
      const targetNodeId = rawBindings[index].node;
      await this.removeNodeAtACLEntry(this.node!.node_id, targetNodeId);
      const updatedBindings = this.removeBindingAtIndex(rawBindings, index);
      await this.syncBindingUpdates(updatedBindings, index);
    } catch (error) {
      this.handleBindingDeletionError(error);
    }
  }

  private async removeNodeAtACLEntry(
    sourceNodeId: number,
    targetNodeId: number,
  ): Promise<void> {
    const aclEntries = this.fetchACLEntry(targetNodeId);

    const updatedACLEntries = aclEntries
      .map((entry) => this.removeSubjectAtACL(sourceNodeId, entry))
      .filter((entry): entry is Exclude<typeof entry, null> => entry !== null);

    await this.client.setACLEntry(targetNodeId, updatedACLEntries);
  }

  private removeSubjectAtACL(
    nodeId: number,
    entry: AccessControlEntryStruct,
  ): AccessControlEntryStruct | null {
    const shouldRemoveSubject = entry.subjects?.includes(nodeId);

    if (!shouldRemoveSubject) return entry;

    const updatedSubjects = entry.subjects.filter(
      (nodeId) => nodeId !== this.node!.node_id,
    );

    return updatedSubjects.length > 0
      ? { ...entry, subjects: updatedSubjects }
      : null;
  }

  private removeBindingAtIndex(
    bindings: BindingEntryStruct[],
    index: number,
  ): BindingEntryStruct[] {
    return [...bindings.slice(0, index), ...bindings.slice(index + 1)];
  }

  private async syncBindingUpdates(
    updatedBindings: BindingEntryStruct[],
    index: number,
  ): Promise<void> {
    await this.client.setNodeBinding(
      this.node!.node_id,
      this.endpoint,
      updatedBindings,
    );

    const attributePath = `${this.endpoint}/30/0`;
    const updatedAttributes = {
      ...this.node!.attributes,
      [attributePath]: this.removeBindingAtIndex(
        this.node!.attributes[attributePath],
        index,
      ),
    };

    this.node!.attributes = updatedAttributes;
    this.requestUpdate();
  }

  private handleBindingDeletionError(error: unknown): void {
    const errorMessage = error instanceof Error ? error.message : String(error);
    console.error(`Binding deletion failed: ${errorMessage}`);
  }

  private async _updateEntry<T>(
    targetId: number,
    path: string,
    entry: T,
    transformFn: (value: InputType) => T,
    updateFn: (targetId: number, entries: T[]) => Promise<any>,
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
    entry: AccessControlEntryStruct,
  ) {
    try {
      const result = (await this._updateEntry(
        targetNodeId,
        "0/31/0",
        entry,
        AccessControlEntryDataTransformer.transform,
        this.client.setACLEntry.bind(this.client),
      )) as { [key: string]: { Status: number } };
      return result["0"].Status === 0;
    } catch (err) {
      console.error("add acl error:", err);
      return false;
    }
  }

  private async add_bindings(
    endpoint: number,
    bindingEntry: BindingEntryStruct,
  ) {
    const bindings = this.fetchBindingEntry();
    bindings.push(bindingEntry);
    try {
      const result = (await this.client.setNodeBinding(
        this.node!.node_id,
        endpoint,
        bindings,
      )) as { [key: string]: { Status: number } };
      return result["0"].Status === 0;
    } catch (err) {
      console.log("add bindings error:", err);
      return false;
    }
  }

  async addBindingHandler() {
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

    const endpoint = this.endpoint;
    const bindingEntry: BindingEntryStruct = {
      node: targetNodeId,
      endpoint: targetEndpoint,
      group: undefined,
      cluster: undefined,
      fabricIndex: undefined,
    };

    const result_binding = await this.add_bindings(endpoint, bindingEntry);

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
    const bindings = this.node!.attributes[this.endpoint + "/30/0"];

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
                        BindingEntryDataTransformer.transform(entry),
                      )}
                    </div>
                    <div slot="end">
                      <md-text-button
                        @click=${() => this.deleteBindingHandler(index)}
                      >delete</md-text-button
                    </div>
                  </md-list-item>
                `,
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
          <md-text-button @click=${this.addBindingHandler}>Add</md-text-button>
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
