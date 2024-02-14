import { MatterClient } from "../client/client";

async function main() {
  import("../pages/matter-dashboard-app");

  // Turn httpX url into wsX url and append "/ws"
  let url = "ws" + new URL("./ws", location.href).toString().substring(4);

  // Inside Home Assistant ingress, we will not prompt for the URL
  if (!location.pathname.endsWith("/ingress")) {
    let storageUrl = localStorage.getItem("matterURL");
    if (!storageUrl) {
      storageUrl = prompt(
        "Enter Matter URL",
        "ws://homeassistant.local:5580/ws"
      );
      if (!storageUrl) {
        alert("Unable to connect without URL");
        return;
      }
      localStorage.setItem("matterURL", storageUrl);
    }
    url = storageUrl;
  }

  const client = new MatterClient(url);

  const dashboard = document.createElement("matter-dashboard-app");
  dashboard.client = client;
  document.body.append(dashboard);
}

main();
