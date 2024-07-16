

export const showCommissionNodeDialog = async (
  ) => {
    await import("./commission-node-dialog");
    const dialog = document.createElement("commission-node-dialog");
    document.querySelector("matter-dashboard-app")?.renderRoot.appendChild(dialog);
  }