import { createContext } from "@lit/context";
import type { MatterClient } from "./client";

export const clientContext = createContext<MatterClient>('client');