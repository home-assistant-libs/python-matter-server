import { MatterClient } from "../client/client";

async function main() {
  import("../pages/matter-dashboard-app");

  let url = "";

  // Detect if we're running in the (production) webserver included in the matter server or not.
  const isProductionServer = location.href.includes(":5580") || location.href.includes("hassio_ingress");

  if (!isProductionServer) {
    // development server, ask for url to matter server
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
  else {
    // assume production server running inside the matter server
    // Turn httpX url into wsX url and append "/ws"
    let baseUrl = window.location.origin + window.location.pathname;
    if (baseUrl.endsWith('/')) { baseUrl = baseUrl.slice(0, -1); }
    url = baseUrl.replace('http', 'ws') + '/ws';
    console.log(`Connecting to Matter Server API using url: ${url}`);
  }

  const client = new MatterClient(url, isProductionServer);

  const dashboard = document.createElement("matter-dashboard-app");
  dashboard.client = client;
  document.body.append(dashboard);
}

main();
