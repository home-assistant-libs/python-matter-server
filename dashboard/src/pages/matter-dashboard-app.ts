import { LitElement, html, PropertyValueMap } from "lit";
import { customElement, state } from "lit/decorators.js";
import { MatterClient } from "../client/client";
import { MatterError } from "../client/exceptions";
import "./matter-dashboard";
import type { Route } from "../util/routing";
import "./matter-node-view";
import "./matter-server-view";

declare global {
  interface HTMLElementTagNameMap {
    "matter-dashboard-app": MatterDashboardApp;
  }
}

@customElement("matter-dashboard-app")
class MatterDashboardApp extends LitElement {
  @state() private _route: Route = {
    prefix: "",
    path: "",
  };

  public client!: MatterClient;

  @state()
  private _state: "connecting" | "connected" | "error" = "connecting";

  private _error: string | undefined;

  protected firstUpdated(
    _changedProperties: PropertyValueMap<any> | Map<PropertyKey, unknown>
  ): void {
    super.firstUpdated(_changedProperties);
    this.client.startListening().then(
      () => {
        this._state = "connected";
        this.client.addEventListener("nodes_changed", () =>
          this.requestUpdate()
        );
      },
      (err: MatterError) => {
        this._state = "error";
        this._error = err.message;
      }
    );

    // Handle history changes
    const updateRoute = () => {
      let [part1, part2] = location.hash.substring(1).split("/", 2);
      if (part2 === undefined) {
        part2 = part1;
        part1 = "";
      }
      this._route = {
        prefix: part1,
        path: part2,
      };
    };
    window.addEventListener("hashchange", updateRoute);
    updateRoute();
  }

  render() {
    if (this._state === "connecting") {
      return html`<p>Connecting...</p>`;
    }
    if (this._state === "error") {
      return html`
        <p>Error: ${this._error}</p>
        ${location.hostname === "localhost"
          ? html`
              <button @click=${this._clearLocalStorage}>
                Clear stored URL
              </button>
            `
          : ""}
      `;
    }
    if (this._route.prefix === "node") {
      return html`
        <matter-node-view
          .client=${this.client}
          .node=${this.client.nodes[parseInt(this._route.path, 10)]}
        ></matter-node-view>
      `;
    }
    if (this._route.path === "server") {
      return html`
        <matter-server-view .client=${this.client}></matter-server-view>
      `;
    }
    return html`<matter-dashboard
      .client=${this.client}
      .nodes=${this.client.nodes}
      .route=${this._route}
    ></matter-dashboard>`;
  }

  private _clearLocalStorage() {
    localStorage.removeItem("matterURL");
    location.reload();
  }
}
