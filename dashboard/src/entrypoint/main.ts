import { MatterClient } from "../client/client";

async function main() {
  import("../pages/matter-dashboard-app");

  let url = "";
  // Detect if we're running in the (production) webserver included in the matter server or not.
  if (location.href.includes(":5580")) {
    // production server running inside the matter server
    // Turn httpX url into wsX url and append "/ws"
    url = "ws" + new URL("./ws", location.href).toString().substring(4);
  } else {
    // dvelopment server, ask for url to matter server
    let storageUrl = localStorage.getItem("matterURL");
    if (!storageUrl) {
      storageUrl = prompt(
        "Enter Websocket URL to a running Matter Server",
        "ws://localhost:5580/ws"
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
