import { MatterClient } from "../../../client/client";
import { MatterNode } from "../../../client/models/node";

export const showNodeBindingDialog = async (
  client: MatterClient,
  node: MatterNode,
  bindingPath: string
) => {
  await import("./node-binding-dialog");
  const dialog = document.createElement("node-binding-dialog");
  dialog.client = client;
  dialog.node = node;
  dialog.bindingPath = bindingPath;
  document
    .querySelector("matter-dashboard-app")
    ?.renderRoot.appendChild(dialog);
};
