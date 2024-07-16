import { MatterClient } from "../../../client/client";


export const showCommissionNodeDialog = async (client: MatterClient
  ) => {
    await import("./commission-node-dialog");
    const dialog = document.createElement("commission-node-dialog");
    dialog.client = client;
    document.querySelector("matter-dashboard-app")?.renderRoot.appendChild(dialog);
  }
