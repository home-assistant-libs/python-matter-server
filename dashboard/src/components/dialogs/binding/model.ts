export type InputType = {
  [key: string]: number | number[] | undefined;
};

export interface BindingEntryStruct {
  node: number;
  group: number | undefined;
  endpoint: number;
  cluster: number | undefined;
  fabricIndex: number | undefined;
}

export type AccessControlEntryStruct = {
  privilege: number;
  authMode: number;
  subjects: number[];
  targets: number[] | undefined;
  fabricIndex: number;
};

export class AccessControlEntryDataTransformer {
  private static readonly KEY_MAPPING: {
    [inputKey: string]: keyof AccessControlEntryStruct;
  } = {
    "1": "privilege",
    "2": "authMode",
    "3": "subjects",
    "4": "targets",
    "254": "fabricIndex",
  };

  public static transform(input: any): AccessControlEntryStruct {
    if (!input || typeof input !== "object") {
      throw new Error("Invalid input: expected an object");
    }

    const result: Partial<AccessControlEntryStruct> = {};
    const keyMapping = AccessControlEntryDataTransformer.KEY_MAPPING;

    for (const key in input) {
      if (key in keyMapping) {
        const mappedKey = keyMapping[key];
        if (mappedKey) {
          const value = input[key];
          if (value === undefined) continue;
          if (mappedKey === "subjects" || mappedKey === "targets") {
            result[mappedKey] = Array.isArray(value) ? value : undefined;
          } else {
            result[mappedKey] = value;
          }
        }
      }
    }

    if (
      result.privilege === undefined ||
      result.authMode === undefined ||
      result.subjects === undefined ||
      result.fabricIndex === undefined
    ) {
      throw new Error("Missing required fields in AccessControlEntryStruct");
    }

    return result as AccessControlEntryStruct;
  }
}

export class BindingEntryDataTransformer {
  private static readonly KEY_MAPPING: {
    [inputKey: string]: keyof BindingEntryStruct;
  } = {
    "1": "node",
    "3": "endpoint",
    "4": "cluster",
    "254": "fabricIndex",
  };

  public static transform(input: any): BindingEntryStruct {
    if (!input || typeof input !== "object") {
      throw new Error("Invalid input: expected an object");
    }

    const result: Partial<BindingEntryStruct> = {};
    const keyMapping = BindingEntryDataTransformer.KEY_MAPPING;

    for (const key in input) {
      if (key in keyMapping) {
        const mappedKey = keyMapping[key];
        if (mappedKey) {
          const value = input[key];
          if (value === undefined) {
            continue;
          }
          if (mappedKey === "fabricIndex") {
            result[mappedKey] = value === undefined ? undefined : Number(value);
          } else if (mappedKey === "node" || mappedKey === "endpoint") {
            result[mappedKey] = Number(value);
          } else {
            result[mappedKey] = value as BindingEntryStruct[typeof mappedKey];
          }
        }
      }
    }

    // Validate required fields
    if (
      result.node === undefined ||
      result.endpoint === undefined ||
      result.fabricIndex === undefined
    ) {
      throw new Error("Missing required fields in BindingEntryStruct");
    }

    return result as BindingEntryStruct;
  }
}
