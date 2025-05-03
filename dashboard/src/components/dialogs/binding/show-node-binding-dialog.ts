import { MatterClient } from "../../../client/client";
import { MatterNode } from "../../../client/models/node";

export const showNodeBindingDialog = async (
  client: MatterClient,
  node: MatterNode,
  endpoint: number,
) => {
  await import("./node-binding-dialog");
  const dialog = document.createElement("node-binding-dialog");
  dialog.client = client;
  dialog.node = node;
  dialog.endpoint = endpoint;
  document
    .querySelector("matter-dashboard-app")
    ?.renderRoot.appendChild(dialog);
};
