
/* Descriptions for SDK Objects. This file is auto generated, do not edit. */

export interface DeviceType {
  id: number;
  label: string;
  clusters: number[];
}

export interface ClusterAttributeDescription {
  id: number;
  cluster_id: number;
  label: string;
  type: string;
}

export interface ClusterDescription {
  id: number;
  label: string;
  attributes: { [attribute_id: string]: ClusterAttributeDescription }
}


export const device_types: Record<number, DeviceType> = {
  "4293984257": {
    "id": 4293984257,
    "label": "Orphan Clusters",
    "clusters": [
      66,
      67,
      28,
      68
    ]
  },
  "22": {
    "id": 22,
    "label": "Root Node",
    "clusters": [
      29,
      31,
      40,
      43,
      44,
      45,
      46,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      60,
      62,
      63,
      70
    ]
  },
  "17": {
    "id": 17,
    "label": "Power Source",
    "clusters": [
      29,
      47
    ]
  },
  "1296": {
    "id": 1296,
    "label": "Electrical Sensor",
    "clusters": [
      144,
      145,
      156,
      29
    ]
  },
  "18": {
    "id": 18,
    "label": "OTA Requestor",
    "clusters": [
      42,
      29
    ]
  },
  "20": {
    "id": 20,
    "label": "OTA Provider",
    "clusters": [
      41,
      29
    ]
  },
  "14": {
    "id": 14,
    "label": "Aggregator",
    "clusters": [
      29,
      37
    ]
  },
  "19": {
    "id": 19,
    "label": "Bridged Device",
    "clusters": [
      57,
      29,
      46,
      47
    ]
  },
  "256": {
    "id": 256,
    "label": "On/Off Light",
    "clusters": [
      98,
      3,
      4,
      6,
      8,
      29
    ]
  },
  "257": {
    "id": 257,
    "label": "Dimmable Light",
    "clusters": [
      98,
      3,
      4,
      6,
      8,
      29,
      30
    ]
  },
  "268": {
    "id": 268,
    "label": "Color Temperature Light",
    "clusters": [
      768,
      98,
      3,
      4,
      6,
      8,
      29
    ]
  },
  "269": {
    "id": 269,
    "label": "Extended Color Light",
    "clusters": [
      768,
      98,
      3,
      4,
      6,
      8,
      29
    ]
  },
  "266": {
    "id": 266,
    "label": "On/Off Plug-in Unit",
    "clusters": [
      98,
      3,
      4,
      6,
      8,
      29
    ]
  },
  "267": {
    "id": 267,
    "label": "Dimmable Plug-in Unit",
    "clusters": [
      98,
      3,
      4,
      6,
      8,
      29
    ]
  },
  "771": {
    "id": 771,
    "label": "Pump",
    "clusters": [
      512,
      1026,
      1027,
      1028,
      4,
      6,
      3,
      8,
      98,
      29,
      30
    ]
  },
  "259": {
    "id": 259,
    "label": "On/Off Light Switch",
    "clusters": [
      3,
      29,
      30
    ]
  },
  "260": {
    "id": 260,
    "label": "Dimmer Switch",
    "clusters": [
      3,
      29,
      30
    ]
  },
  "261": {
    "id": 261,
    "label": "Color Dimmer Switch",
    "clusters": [
      3,
      29,
      30
    ]
  },
  "2112": {
    "id": 2112,
    "label": "Control Bridge",
    "clusters": [
      3,
      29,
      30
    ]
  },
  "772": {
    "id": 772,
    "label": "Pump Controller",
    "clusters": [
      3,
      29,
      30
    ]
  },
  "15": {
    "id": 15,
    "label": "Generic Switch",
    "clusters": [
      64,
      65,
      3,
      59,
      29
    ]
  },
  "21": {
    "id": 21,
    "label": "Contact Sensor",
    "clusters": [
      29,
      3,
      69
    ]
  },
  "262": {
    "id": 262,
    "label": "Light Sensor",
    "clusters": [
      1024,
      3,
      29,
      30
    ]
  },
  "263": {
    "id": 263,
    "label": "Occupancy Sensor",
    "clusters": [
      3,
      29,
      30,
      1030
    ]
  },
  "770": {
    "id": 770,
    "label": "Temperature Sensor",
    "clusters": [
      1026,
      3,
      29
    ]
  },
  "773": {
    "id": 773,
    "label": "Pressure Sensor",
    "clusters": [
      1027,
      3,
      29
    ]
  },
  "774": {
    "id": 774,
    "label": "Flow Sensor",
    "clusters": [
      3,
      1028,
      29
    ]
  },
  "775": {
    "id": 775,
    "label": "Humidity Sensor",
    "clusters": [
      29,
      3,
      1029
    ]
  },
  "2128": {
    "id": 2128,
    "label": "On/Off Sensor",
    "clusters": [
      3,
      29,
      30
    ]
  },
  "10": {
    "id": 10,
    "label": "Door Lock",
    "clusters": [
      257,
      3,
      29
    ]
  },
  "11": {
    "id": 11,
    "label": "Door Lock Controller",
    "clusters": [
      56,
      29,
      30
    ]
  },
  "514": {
    "id": 514,
    "label": "Window Covering",
    "clusters": [
      258,
      3,
      4,
      98,
      29
    ]
  },
  "515": {
    "id": 515,
    "label": "Window Covering Controller",
    "clusters": [
      3,
      29,
      30
    ]
  },
  "768": {
    "id": 768,
    "label": "Heating/Cooling Unit",
    "clusters": [
      514,
      3,
      4,
      98,
      6,
      8,
      29,
      30
    ]
  },
  "769": {
    "id": 769,
    "label": "Thermostat",
    "clusters": [
      513,
      98,
      3,
      4,
      516,
      56,
      29,
      30
    ]
  },
  "43": {
    "id": 43,
    "label": "Fan",
    "clusters": [
      514,
      3,
      4,
      29
    ]
  },
  "35": {
    "id": 35,
    "label": "Casting Video Player",
    "clusters": [
      1283,
      1284,
      1285,
      1286,
      1287,
      1288,
      1289,
      1290,
      1291,
      1292,
      6,
      1294,
      29
    ]
  },
  "40": {
    "id": 40,
    "label": "Basic Video Player",
    "clusters": [
      1283,
      1284,
      1285,
      1286,
      1287,
      1288,
      1289,
      6,
      1291,
      29
    ]
  },
  "41": {
    "id": 41,
    "label": "Casting Video Client",
    "clusters": [
      1283,
      1284,
      1285,
      1286,
      1287,
      8,
      1289,
      1290,
      1288,
      1291,
      1293,
      1292,
      6,
      1294,
      29,
      30
    ]
  },
  "42": {
    "id": 42,
    "label": "Video Remote Control",
    "clusters": [
      1283,
      1284,
      1285,
      1286,
      1287,
      8,
      1289,
      1290,
      1288,
      1291,
      1292,
      6,
      1294,
      29,
      30
    ]
  },
  "34": {
    "id": 34,
    "label": "Speaker",
    "clusters": [
      8,
      3,
      29,
      6
    ]
  },
  "36": {
    "id": 36,
    "label": "Content App",
    "clusters": [
      3,
      1284,
      1285,
      1286,
      1289,
      1290,
      1292,
      1293,
      1294,
      29
    ]
  },
  "39": {
    "id": 39,
    "label": "Mode Select",
    "clusters": [
      80,
      3,
      29
    ]
  },
  "114": {
    "id": 114,
    "label": "Room Air Conditioner",
    "clusters": [
      513,
      1026,
      514,
      4,
      1029,
      516,
      6,
      3,
      98,
      29
    ]
  },
  "118": {
    "id": 118,
    "label": "Smoke CO Alarm",
    "clusters": [
      1026,
      3,
      4,
      1029,
      1036,
      47,
      92,
      29
    ]
  },
  "45": {
    "id": 45,
    "label": "Air Purifier",
    "clusters": [
      514,
      3,
      4,
      113,
      114,
      29
    ]
  },
  "44": {
    "id": 44,
    "label": "Air Quality Sensor",
    "clusters": [
      1026,
      3,
      1029,
      1066,
      1067,
      1036,
      1037,
      1070,
      1071,
      1069,
      1068,
      1043,
      1045,
      91,
      29
    ]
  },
  "117": {
    "id": 117,
    "label": "Dishwasher",
    "clusters": [
      96,
      3,
      6,
      29,
      86,
      89,
      93
    ]
  },
  "123": {
    "id": 123,
    "label": "Oven",
    "clusters": [
      3,
      29
    ]
  },
  "121": {
    "id": 121,
    "label": "Microwave Oven",
    "clusters": [
      96,
      514,
      3,
      29,
      94,
      95
    ]
  },
  "112": {
    "id": 112,
    "label": "Refrigerator",
    "clusters": [
      82,
      3,
      29,
      87
    ]
  },
  "115": {
    "id": 115,
    "label": "Laundry Washer",
    "clusters": [
      96,
      3,
      6,
      81,
      83,
      86,
      29
    ]
  },
  "124": {
    "id": 124,
    "label": "Laundry Dryer",
    "clusters": [
      96,
      3,
      6,
      74,
      81,
      86,
      29
    ]
  },
  "122": {
    "id": 122,
    "label": "Extractor Hood",
    "clusters": [
      514,
      3,
      113,
      114,
      29
    ]
  },
  "116": {
    "id": 116,
    "label": "Robotic Vacuum Cleaner",
    "clusters": [
      97,
      3,
      84,
      85,
      29
    ]
  },
  "113": {
    "id": 113,
    "label": "Temperature Controlled Cabinet",
    "clusters": [
      1026,
      72,
      73,
      82,
      86,
      29
    ]
  },
  "65": {
    "id": 65,
    "label": "Water Freeze Detector",
    "clusters": [
      128,
      3,
      69,
      29
    ]
  },
  "66": {
    "id": 66,
    "label": "Water Valve",
    "clusters": [
      129,
      3,
      29
    ]
  },
  "67": {
    "id": 67,
    "label": "Water Leak Detector",
    "clusters": [
      128,
      3,
      69,
      29
    ]
  },
  "68": {
    "id": 68,
    "label": "Rain Sensor",
    "clusters": [
      128,
      3,
      69,
      29
    ]
  },
  "4293984272": {
    "id": 4293984272,
    "label": "Network Infrastructure Manager",
    "clusters": [
      29
    ]
  },
  "4293984259": {
    "id": 4293984259,
    "label": "All-clusters-app Server Example",
    "clusters": [
      768,
      257,
      1026,
      259,
      4,
      3,
      6,
      98,
      8,
      29,
      30
    ]
  },
  "4293984258": {
    "id": 4293984258,
    "label": "Secondary Network Commissioning Device Type",
    "clusters": [
      49,
      29
    ]
  },
  "120": {
    "id": 120,
    "label": "Cooktop",
    "clusters": [
      3,
      29,
      6
    ]
  },
  "119": {
    "id": 119,
    "label": "Cook Surface",
    "clusters": [
      1026,
      29,
      86
    ]
  },
  "1292": {
    "id": 1292,
    "label": "EVSE",
    "clusters": [
      1026,
      3,
      157,
      153,
      29
    ]
  }
}

export const clusters: Record<number, ClusterDescription> = {
  "3": {
    "id": 3,
    "label": "Identify",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 3,
        "label": "IdentifyTime",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 3,
        "label": "IdentifyType",
        "type": "aenum IdentifyTypeEnum"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 3,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 3,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 3,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 3,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 3,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 3,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "4": {
    "id": 4,
    "label": "Groups",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 4,
        "label": "NameSupport",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 4,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 4,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 4,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 4,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 4,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 4,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "6": {
    "id": 6,
    "label": "OnOff",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 6,
        "label": "OnOff",
        "type": "bool"
      },
      "16384": {
        "id": 16384,
        "cluster_id": 6,
        "label": "GlobalSceneControl",
        "type": "Optional[bool]"
      },
      "16385": {
        "id": 16385,
        "cluster_id": 6,
        "label": "OnTime",
        "type": "Optional[uint]"
      },
      "16386": {
        "id": 16386,
        "cluster_id": 6,
        "label": "OffWaitTime",
        "type": "Optional[uint]"
      },
      "16387": {
        "id": 16387,
        "cluster_id": 6,
        "label": "StartUpOnOff",
        "type": "Union[NoneType, Nullable, OnOff.Enums.StartUpOnOffEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 6,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 6,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 6,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 6,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 6,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 6,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "7": {
    "id": 7,
    "label": "OnOffSwitchConfiguration",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 7,
        "label": "SwitchType",
        "type": "uint"
      },
      "16": {
        "id": 16,
        "cluster_id": 7,
        "label": "SwitchActions",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 7,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 7,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 7,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 7,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 7,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 7,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "8": {
    "id": 8,
    "label": "LevelControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 8,
        "label": "CurrentLevel",
        "type": "Union[Nullable, uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 8,
        "label": "RemainingTime",
        "type": "Optional[uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 8,
        "label": "MinLevel",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 8,
        "label": "MaxLevel",
        "type": "Optional[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 8,
        "label": "CurrentFrequency",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 8,
        "label": "MinFrequency",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 8,
        "label": "MaxFrequency",
        "type": "Optional[uint]"
      },
      "15": {
        "id": 15,
        "cluster_id": 8,
        "label": "Options",
        "type": "uint"
      },
      "16": {
        "id": 16,
        "cluster_id": 8,
        "label": "OnOffTransitionTime",
        "type": "Optional[uint]"
      },
      "17": {
        "id": 17,
        "cluster_id": 8,
        "label": "OnLevel",
        "type": "Union[Nullable, uint]"
      },
      "18": {
        "id": 18,
        "cluster_id": 8,
        "label": "OnTransitionTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "19": {
        "id": 19,
        "cluster_id": 8,
        "label": "OffTransitionTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "20": {
        "id": 20,
        "cluster_id": 8,
        "label": "DefaultMoveRate",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "16384": {
        "id": 16384,
        "cluster_id": 8,
        "label": "StartUpCurrentLevel",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 8,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 8,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 8,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 8,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 8,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 8,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "15": {
    "id": 15,
    "label": "BinaryInputBasic",
    "attributes": {
      "4": {
        "id": 4,
        "cluster_id": 15,
        "label": "ActiveText",
        "type": "Optional[str]"
      },
      "28": {
        "id": 28,
        "cluster_id": 15,
        "label": "Description",
        "type": "Optional[str]"
      },
      "46": {
        "id": 46,
        "cluster_id": 15,
        "label": "InactiveText",
        "type": "Optional[str]"
      },
      "81": {
        "id": 81,
        "cluster_id": 15,
        "label": "OutOfService",
        "type": "bool"
      },
      "84": {
        "id": 84,
        "cluster_id": 15,
        "label": "Polarity",
        "type": "Optional[uint]"
      },
      "85": {
        "id": 85,
        "cluster_id": 15,
        "label": "PresentValue",
        "type": "bool"
      },
      "103": {
        "id": 103,
        "cluster_id": 15,
        "label": "Reliability",
        "type": "Optional[uint]"
      },
      "111": {
        "id": 111,
        "cluster_id": 15,
        "label": "StatusFlags",
        "type": "uint"
      },
      "256": {
        "id": 256,
        "cluster_id": 15,
        "label": "ApplicationType",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 15,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 15,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 15,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 15,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 15,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 15,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "28": {
    "id": 28,
    "label": "PulseWidthModulation",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 28,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 28,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 28,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 28,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 28,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 28,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "29": {
    "id": 29,
    "label": "Descriptor",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 29,
        "label": "DeviceTypeList",
        "type": "List[Descriptor.Structs.DeviceTypeStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 29,
        "label": "ServerList",
        "type": "List[uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 29,
        "label": "ClientList",
        "type": "List[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 29,
        "label": "PartsList",
        "type": "List[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 29,
        "label": "TagList",
        "type": "Optional[List[Descriptor.Structs.SemanticTagStruct]]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 29,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 29,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 29,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 29,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 29,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 29,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "30": {
    "id": 30,
    "label": "Binding",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 30,
        "label": "Binding",
        "type": "List[Binding.Structs.TargetStruct]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 30,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 30,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 30,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 30,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 30,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 30,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "31": {
    "id": 31,
    "label": "AccessControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 31,
        "label": "Acl",
        "type": "List[AccessControl.Structs.AccessControlEntryStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 31,
        "label": "Extension",
        "type": "Optional[List[AccessControl.Structs.AccessControlExtensionStruct]]"
      },
      "2": {
        "id": 2,
        "cluster_id": 31,
        "label": "SubjectsPerAccessControlEntry",
        "type": "uint"
      },
      "3": {
        "id": 3,
        "cluster_id": 31,
        "label": "TargetsPerAccessControlEntry",
        "type": "uint"
      },
      "4": {
        "id": 4,
        "cluster_id": 31,
        "label": "AccessControlEntriesPerFabric",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 31,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 31,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 31,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 31,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 31,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 31,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "37": {
    "id": 37,
    "label": "Actions",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 37,
        "label": "ActionList",
        "type": "List[Actions.Structs.ActionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 37,
        "label": "EndpointLists",
        "type": "List[Actions.Structs.EndpointListStruct]"
      },
      "2": {
        "id": 2,
        "cluster_id": 37,
        "label": "SetupURL",
        "type": "Optional[str]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 37,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 37,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 37,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 37,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 37,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 37,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "40": {
    "id": 40,
    "label": "BasicInformation",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 40,
        "label": "DataModelRevision",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 40,
        "label": "VendorName",
        "type": "str"
      },
      "2": {
        "id": 2,
        "cluster_id": 40,
        "label": "VendorID",
        "type": "uint"
      },
      "3": {
        "id": 3,
        "cluster_id": 40,
        "label": "ProductName",
        "type": "str"
      },
      "4": {
        "id": 4,
        "cluster_id": 40,
        "label": "ProductID",
        "type": "uint"
      },
      "5": {
        "id": 5,
        "cluster_id": 40,
        "label": "NodeLabel",
        "type": "str"
      },
      "6": {
        "id": 6,
        "cluster_id": 40,
        "label": "Location",
        "type": "str"
      },
      "7": {
        "id": 7,
        "cluster_id": 40,
        "label": "HardwareVersion",
        "type": "uint"
      },
      "8": {
        "id": 8,
        "cluster_id": 40,
        "label": "HardwareVersionString",
        "type": "str"
      },
      "9": {
        "id": 9,
        "cluster_id": 40,
        "label": "SoftwareVersion",
        "type": "uint"
      },
      "10": {
        "id": 10,
        "cluster_id": 40,
        "label": "SoftwareVersionString",
        "type": "str"
      },
      "11": {
        "id": 11,
        "cluster_id": 40,
        "label": "ManufacturingDate",
        "type": "Optional[str]"
      },
      "12": {
        "id": 12,
        "cluster_id": 40,
        "label": "PartNumber",
        "type": "Optional[str]"
      },
      "13": {
        "id": 13,
        "cluster_id": 40,
        "label": "ProductURL",
        "type": "Optional[str]"
      },
      "14": {
        "id": 14,
        "cluster_id": 40,
        "label": "ProductLabel",
        "type": "Optional[str]"
      },
      "15": {
        "id": 15,
        "cluster_id": 40,
        "label": "SerialNumber",
        "type": "Optional[str]"
      },
      "16": {
        "id": 16,
        "cluster_id": 40,
        "label": "LocalConfigDisabled",
        "type": "Optional[bool]"
      },
      "17": {
        "id": 17,
        "cluster_id": 40,
        "label": "Reachable",
        "type": "Optional[bool]"
      },
      "18": {
        "id": 18,
        "cluster_id": 40,
        "label": "UniqueID",
        "type": "Optional[str]"
      },
      "19": {
        "id": 19,
        "cluster_id": 40,
        "label": "CapabilityMinima",
        "type": "BasicInformation.Structs.CapabilityMinimaStruct"
      },
      "20": {
        "id": 20,
        "cluster_id": 40,
        "label": "ProductAppearance",
        "type": "Optional[BasicInformation.Structs.ProductAppearanceStruct]"
      },
      "21": {
        "id": 21,
        "cluster_id": 40,
        "label": "SpecificationVersion",
        "type": "uint"
      },
      "22": {
        "id": 22,
        "cluster_id": 40,
        "label": "MaxPathsPerInvoke",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 40,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 40,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 40,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 40,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 40,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 40,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "41": {
    "id": 41,
    "label": "OtaSoftwareUpdateProvider",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 41,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 41,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 41,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 41,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 41,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 41,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "42": {
    "id": 42,
    "label": "OtaSoftwareUpdateRequestor",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 42,
        "label": "DefaultOTAProviders",
        "type": "List[OtaSoftwareUpdateRequestor.Structs.ProviderLocation]"
      },
      "1": {
        "id": 1,
        "cluster_id": 42,
        "label": "UpdatePossible",
        "type": "bool"
      },
      "2": {
        "id": 2,
        "cluster_id": 42,
        "label": "UpdateState",
        "type": "aenum UpdateStateEnum"
      },
      "3": {
        "id": 3,
        "cluster_id": 42,
        "label": "UpdateStateProgress",
        "type": "Union[Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 42,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 42,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 42,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 42,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 42,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 42,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "43": {
    "id": 43,
    "label": "LocalizationConfiguration",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 43,
        "label": "ActiveLocale",
        "type": "str"
      },
      "1": {
        "id": 1,
        "cluster_id": 43,
        "label": "SupportedLocales",
        "type": "List[str]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 43,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 43,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 43,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 43,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 43,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 43,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "44": {
    "id": 44,
    "label": "TimeFormatLocalization",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 44,
        "label": "HourFormat",
        "type": "aenum HourFormatEnum"
      },
      "1": {
        "id": 1,
        "cluster_id": 44,
        "label": "ActiveCalendarType",
        "type": "Optional[TimeFormatLocalization.Enums.CalendarTypeEnum]"
      },
      "2": {
        "id": 2,
        "cluster_id": 44,
        "label": "SupportedCalendarTypes",
        "type": "Optional[List[TimeFormatLocalization.Enums.CalendarTypeEnum]]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 44,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 44,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 44,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 44,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 44,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 44,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "45": {
    "id": 45,
    "label": "UnitLocalization",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 45,
        "label": "TemperatureUnit",
        "type": "Optional[UnitLocalization.Enums.TempUnitEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 45,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 45,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 45,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 45,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 45,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 45,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "46": {
    "id": 46,
    "label": "PowerSourceConfiguration",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 46,
        "label": "Sources",
        "type": "List[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 46,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 46,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 46,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 46,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 46,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 46,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "47": {
    "id": 47,
    "label": "PowerSource",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 47,
        "label": "Status",
        "type": "aenum PowerSourceStatusEnum"
      },
      "1": {
        "id": 1,
        "cluster_id": 47,
        "label": "Order",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 47,
        "label": "Description",
        "type": "str"
      },
      "3": {
        "id": 3,
        "cluster_id": 47,
        "label": "WiredAssessedInputVoltage",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 47,
        "label": "WiredAssessedInputFrequency",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 47,
        "label": "WiredCurrentType",
        "type": "Optional[PowerSource.Enums.WiredCurrentTypeEnum]"
      },
      "6": {
        "id": 6,
        "cluster_id": 47,
        "label": "WiredAssessedCurrent",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 47,
        "label": "WiredNominalVoltage",
        "type": "Optional[uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 47,
        "label": "WiredMaximumCurrent",
        "type": "Optional[uint]"
      },
      "9": {
        "id": 9,
        "cluster_id": 47,
        "label": "WiredPresent",
        "type": "Optional[bool]"
      },
      "10": {
        "id": 10,
        "cluster_id": 47,
        "label": "ActiveWiredFaults",
        "type": "Optional[List[PowerSource.Enums.WiredFaultEnum]]"
      },
      "11": {
        "id": 11,
        "cluster_id": 47,
        "label": "BatVoltage",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "12": {
        "id": 12,
        "cluster_id": 47,
        "label": "BatPercentRemaining",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "13": {
        "id": 13,
        "cluster_id": 47,
        "label": "BatTimeRemaining",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "14": {
        "id": 14,
        "cluster_id": 47,
        "label": "BatChargeLevel",
        "type": "Optional[PowerSource.Enums.BatChargeLevelEnum]"
      },
      "15": {
        "id": 15,
        "cluster_id": 47,
        "label": "BatReplacementNeeded",
        "type": "Optional[bool]"
      },
      "16": {
        "id": 16,
        "cluster_id": 47,
        "label": "BatReplaceability",
        "type": "Optional[PowerSource.Enums.BatReplaceabilityEnum]"
      },
      "17": {
        "id": 17,
        "cluster_id": 47,
        "label": "BatPresent",
        "type": "Optional[bool]"
      },
      "18": {
        "id": 18,
        "cluster_id": 47,
        "label": "ActiveBatFaults",
        "type": "Optional[List[PowerSource.Enums.BatFaultEnum]]"
      },
      "19": {
        "id": 19,
        "cluster_id": 47,
        "label": "BatReplacementDescription",
        "type": "Optional[str]"
      },
      "20": {
        "id": 20,
        "cluster_id": 47,
        "label": "BatCommonDesignation",
        "type": "Optional[PowerSource.Enums.BatCommonDesignationEnum]"
      },
      "21": {
        "id": 21,
        "cluster_id": 47,
        "label": "BatANSIDesignation",
        "type": "Optional[str]"
      },
      "22": {
        "id": 22,
        "cluster_id": 47,
        "label": "BatIECDesignation",
        "type": "Optional[str]"
      },
      "23": {
        "id": 23,
        "cluster_id": 47,
        "label": "BatApprovedChemistry",
        "type": "Optional[PowerSource.Enums.BatApprovedChemistryEnum]"
      },
      "24": {
        "id": 24,
        "cluster_id": 47,
        "label": "BatCapacity",
        "type": "Optional[uint]"
      },
      "25": {
        "id": 25,
        "cluster_id": 47,
        "label": "BatQuantity",
        "type": "Optional[uint]"
      },
      "26": {
        "id": 26,
        "cluster_id": 47,
        "label": "BatChargeState",
        "type": "Optional[PowerSource.Enums.BatChargeStateEnum]"
      },
      "27": {
        "id": 27,
        "cluster_id": 47,
        "label": "BatTimeToFullCharge",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "28": {
        "id": 28,
        "cluster_id": 47,
        "label": "BatFunctionalWhileCharging",
        "type": "Optional[bool]"
      },
      "29": {
        "id": 29,
        "cluster_id": 47,
        "label": "BatChargingCurrent",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "30": {
        "id": 30,
        "cluster_id": 47,
        "label": "ActiveBatChargeFaults",
        "type": "Optional[List[PowerSource.Enums.BatChargeFaultEnum]]"
      },
      "31": {
        "id": 31,
        "cluster_id": 47,
        "label": "EndpointList",
        "type": "List[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 47,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 47,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 47,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 47,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 47,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 47,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "48": {
    "id": 48,
    "label": "GeneralCommissioning",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 48,
        "label": "Breadcrumb",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 48,
        "label": "BasicCommissioningInfo",
        "type": "GeneralCommissioning.Structs.BasicCommissioningInfo"
      },
      "2": {
        "id": 2,
        "cluster_id": 48,
        "label": "RegulatoryConfig",
        "type": "aenum RegulatoryLocationTypeEnum"
      },
      "3": {
        "id": 3,
        "cluster_id": 48,
        "label": "LocationCapability",
        "type": "aenum RegulatoryLocationTypeEnum"
      },
      "4": {
        "id": 4,
        "cluster_id": 48,
        "label": "SupportsConcurrentConnection",
        "type": "bool"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 48,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 48,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 48,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 48,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 48,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 48,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "49": {
    "id": 49,
    "label": "NetworkCommissioning",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 49,
        "label": "MaxNetworks",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 49,
        "label": "Networks",
        "type": "List[NetworkCommissioning.Structs.NetworkInfoStruct]"
      },
      "2": {
        "id": 2,
        "cluster_id": 49,
        "label": "ScanMaxTimeSeconds",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 49,
        "label": "ConnectMaxTimeSeconds",
        "type": "Optional[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 49,
        "label": "InterfaceEnabled",
        "type": "bool"
      },
      "5": {
        "id": 5,
        "cluster_id": 49,
        "label": "LastNetworkingStatus",
        "type": "Union[Nullable, NetworkCommissioning.Enums.NetworkCommissioningStatusEnum]"
      },
      "6": {
        "id": 6,
        "cluster_id": 49,
        "label": "LastNetworkID",
        "type": "Union[Nullable, bytes]"
      },
      "7": {
        "id": 7,
        "cluster_id": 49,
        "label": "LastConnectErrorValue",
        "type": "Union[Nullable, int]"
      },
      "8": {
        "id": 8,
        "cluster_id": 49,
        "label": "SupportedWiFiBands",
        "type": "Optional[List[NetworkCommissioning.Enums.WiFiBandEnum]]"
      },
      "9": {
        "id": 9,
        "cluster_id": 49,
        "label": "SupportedThreadFeatures",
        "type": "Optional[uint]"
      },
      "10": {
        "id": 10,
        "cluster_id": 49,
        "label": "ThreadVersion",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 49,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 49,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 49,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 49,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 49,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 49,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "50": {
    "id": 50,
    "label": "DiagnosticLogs",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 50,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 50,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 50,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 50,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 50,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 50,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "51": {
    "id": 51,
    "label": "GeneralDiagnostics",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 51,
        "label": "NetworkInterfaces",
        "type": "List[GeneralDiagnostics.Structs.NetworkInterface]"
      },
      "1": {
        "id": 1,
        "cluster_id": 51,
        "label": "RebootCount",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 51,
        "label": "UpTime",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 51,
        "label": "TotalOperationalHours",
        "type": "Optional[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 51,
        "label": "BootReason",
        "type": "Optional[GeneralDiagnostics.Enums.BootReasonEnum]"
      },
      "5": {
        "id": 5,
        "cluster_id": 51,
        "label": "ActiveHardwareFaults",
        "type": "Optional[List[GeneralDiagnostics.Enums.HardwareFaultEnum]]"
      },
      "6": {
        "id": 6,
        "cluster_id": 51,
        "label": "ActiveRadioFaults",
        "type": "Optional[List[GeneralDiagnostics.Enums.RadioFaultEnum]]"
      },
      "7": {
        "id": 7,
        "cluster_id": 51,
        "label": "ActiveNetworkFaults",
        "type": "Optional[List[GeneralDiagnostics.Enums.NetworkFaultEnum]]"
      },
      "8": {
        "id": 8,
        "cluster_id": 51,
        "label": "TestEventTriggersEnabled",
        "type": "bool"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 51,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 51,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 51,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 51,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 51,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 51,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "52": {
    "id": 52,
    "label": "SoftwareDiagnostics",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 52,
        "label": "ThreadMetrics",
        "type": "Optional[List[SoftwareDiagnostics.Structs.ThreadMetricsStruct]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 52,
        "label": "CurrentHeapFree",
        "type": "Optional[uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 52,
        "label": "CurrentHeapUsed",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 52,
        "label": "CurrentHeapHighWatermark",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 52,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 52,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 52,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 52,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 52,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 52,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "53": {
    "id": 53,
    "label": "ThreadNetworkDiagnostics",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 53,
        "label": "Channel",
        "type": "Union[Nullable, uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 53,
        "label": "RoutingRole",
        "type": "Union[Nullable, ThreadNetworkDiagnostics.Enums.RoutingRoleEnum]"
      },
      "2": {
        "id": 2,
        "cluster_id": 53,
        "label": "NetworkName",
        "type": "Union[Nullable, str]"
      },
      "3": {
        "id": 3,
        "cluster_id": 53,
        "label": "PanId",
        "type": "Union[Nullable, uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 53,
        "label": "ExtendedPanId",
        "type": "Union[Nullable, uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 53,
        "label": "MeshLocalPrefix",
        "type": "Union[Nullable, bytes]"
      },
      "6": {
        "id": 6,
        "cluster_id": 53,
        "label": "OverrunCount",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 53,
        "label": "NeighborTable",
        "type": "List[ThreadNetworkDiagnostics.Structs.NeighborTableStruct]"
      },
      "8": {
        "id": 8,
        "cluster_id": 53,
        "label": "RouteTable",
        "type": "List[ThreadNetworkDiagnostics.Structs.RouteTableStruct]"
      },
      "9": {
        "id": 9,
        "cluster_id": 53,
        "label": "PartitionId",
        "type": "Union[Nullable, uint]"
      },
      "10": {
        "id": 10,
        "cluster_id": 53,
        "label": "Weighting",
        "type": "Union[Nullable, uint]"
      },
      "11": {
        "id": 11,
        "cluster_id": 53,
        "label": "DataVersion",
        "type": "Union[Nullable, uint]"
      },
      "12": {
        "id": 12,
        "cluster_id": 53,
        "label": "StableDataVersion",
        "type": "Union[Nullable, uint]"
      },
      "13": {
        "id": 13,
        "cluster_id": 53,
        "label": "LeaderRouterId",
        "type": "Union[Nullable, uint]"
      },
      "14": {
        "id": 14,
        "cluster_id": 53,
        "label": "DetachedRoleCount",
        "type": "Optional[uint]"
      },
      "15": {
        "id": 15,
        "cluster_id": 53,
        "label": "ChildRoleCount",
        "type": "Optional[uint]"
      },
      "16": {
        "id": 16,
        "cluster_id": 53,
        "label": "RouterRoleCount",
        "type": "Optional[uint]"
      },
      "17": {
        "id": 17,
        "cluster_id": 53,
        "label": "LeaderRoleCount",
        "type": "Optional[uint]"
      },
      "18": {
        "id": 18,
        "cluster_id": 53,
        "label": "AttachAttemptCount",
        "type": "Optional[uint]"
      },
      "19": {
        "id": 19,
        "cluster_id": 53,
        "label": "PartitionIdChangeCount",
        "type": "Optional[uint]"
      },
      "20": {
        "id": 20,
        "cluster_id": 53,
        "label": "BetterPartitionAttachAttemptCount",
        "type": "Optional[uint]"
      },
      "21": {
        "id": 21,
        "cluster_id": 53,
        "label": "ParentChangeCount",
        "type": "Optional[uint]"
      },
      "22": {
        "id": 22,
        "cluster_id": 53,
        "label": "TxTotalCount",
        "type": "Optional[uint]"
      },
      "23": {
        "id": 23,
        "cluster_id": 53,
        "label": "TxUnicastCount",
        "type": "Optional[uint]"
      },
      "24": {
        "id": 24,
        "cluster_id": 53,
        "label": "TxBroadcastCount",
        "type": "Optional[uint]"
      },
      "25": {
        "id": 25,
        "cluster_id": 53,
        "label": "TxAckRequestedCount",
        "type": "Optional[uint]"
      },
      "26": {
        "id": 26,
        "cluster_id": 53,
        "label": "TxAckedCount",
        "type": "Optional[uint]"
      },
      "27": {
        "id": 27,
        "cluster_id": 53,
        "label": "TxNoAckRequestedCount",
        "type": "Optional[uint]"
      },
      "28": {
        "id": 28,
        "cluster_id": 53,
        "label": "TxDataCount",
        "type": "Optional[uint]"
      },
      "29": {
        "id": 29,
        "cluster_id": 53,
        "label": "TxDataPollCount",
        "type": "Optional[uint]"
      },
      "30": {
        "id": 30,
        "cluster_id": 53,
        "label": "TxBeaconCount",
        "type": "Optional[uint]"
      },
      "31": {
        "id": 31,
        "cluster_id": 53,
        "label": "TxBeaconRequestCount",
        "type": "Optional[uint]"
      },
      "32": {
        "id": 32,
        "cluster_id": 53,
        "label": "TxOtherCount",
        "type": "Optional[uint]"
      },
      "33": {
        "id": 33,
        "cluster_id": 53,
        "label": "TxRetryCount",
        "type": "Optional[uint]"
      },
      "34": {
        "id": 34,
        "cluster_id": 53,
        "label": "TxDirectMaxRetryExpiryCount",
        "type": "Optional[uint]"
      },
      "35": {
        "id": 35,
        "cluster_id": 53,
        "label": "TxIndirectMaxRetryExpiryCount",
        "type": "Optional[uint]"
      },
      "36": {
        "id": 36,
        "cluster_id": 53,
        "label": "TxErrCcaCount",
        "type": "Optional[uint]"
      },
      "37": {
        "id": 37,
        "cluster_id": 53,
        "label": "TxErrAbortCount",
        "type": "Optional[uint]"
      },
      "38": {
        "id": 38,
        "cluster_id": 53,
        "label": "TxErrBusyChannelCount",
        "type": "Optional[uint]"
      },
      "39": {
        "id": 39,
        "cluster_id": 53,
        "label": "RxTotalCount",
        "type": "Optional[uint]"
      },
      "40": {
        "id": 40,
        "cluster_id": 53,
        "label": "RxUnicastCount",
        "type": "Optional[uint]"
      },
      "41": {
        "id": 41,
        "cluster_id": 53,
        "label": "RxBroadcastCount",
        "type": "Optional[uint]"
      },
      "42": {
        "id": 42,
        "cluster_id": 53,
        "label": "RxDataCount",
        "type": "Optional[uint]"
      },
      "43": {
        "id": 43,
        "cluster_id": 53,
        "label": "RxDataPollCount",
        "type": "Optional[uint]"
      },
      "44": {
        "id": 44,
        "cluster_id": 53,
        "label": "RxBeaconCount",
        "type": "Optional[uint]"
      },
      "45": {
        "id": 45,
        "cluster_id": 53,
        "label": "RxBeaconRequestCount",
        "type": "Optional[uint]"
      },
      "46": {
        "id": 46,
        "cluster_id": 53,
        "label": "RxOtherCount",
        "type": "Optional[uint]"
      },
      "47": {
        "id": 47,
        "cluster_id": 53,
        "label": "RxAddressFilteredCount",
        "type": "Optional[uint]"
      },
      "48": {
        "id": 48,
        "cluster_id": 53,
        "label": "RxDestAddrFilteredCount",
        "type": "Optional[uint]"
      },
      "49": {
        "id": 49,
        "cluster_id": 53,
        "label": "RxDuplicatedCount",
        "type": "Optional[uint]"
      },
      "50": {
        "id": 50,
        "cluster_id": 53,
        "label": "RxErrNoFrameCount",
        "type": "Optional[uint]"
      },
      "51": {
        "id": 51,
        "cluster_id": 53,
        "label": "RxErrUnknownNeighborCount",
        "type": "Optional[uint]"
      },
      "52": {
        "id": 52,
        "cluster_id": 53,
        "label": "RxErrInvalidSrcAddrCount",
        "type": "Optional[uint]"
      },
      "53": {
        "id": 53,
        "cluster_id": 53,
        "label": "RxErrSecCount",
        "type": "Optional[uint]"
      },
      "54": {
        "id": 54,
        "cluster_id": 53,
        "label": "RxErrFcsCount",
        "type": "Optional[uint]"
      },
      "55": {
        "id": 55,
        "cluster_id": 53,
        "label": "RxErrOtherCount",
        "type": "Optional[uint]"
      },
      "56": {
        "id": 56,
        "cluster_id": 53,
        "label": "ActiveTimestamp",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "57": {
        "id": 57,
        "cluster_id": 53,
        "label": "PendingTimestamp",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "58": {
        "id": 58,
        "cluster_id": 53,
        "label": "Delay",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "59": {
        "id": 59,
        "cluster_id": 53,
        "label": "SecurityPolicy",
        "type": "Union[Nullable, ThreadNetworkDiagnostics.Structs.SecurityPolicy]"
      },
      "60": {
        "id": 60,
        "cluster_id": 53,
        "label": "ChannelPage0Mask",
        "type": "Union[Nullable, bytes]"
      },
      "61": {
        "id": 61,
        "cluster_id": 53,
        "label": "OperationalDatasetComponents",
        "type": "Union[Nullable, ThreadNetworkDiagnostics.Structs.OperationalDatasetComponents]"
      },
      "62": {
        "id": 62,
        "cluster_id": 53,
        "label": "ActiveNetworkFaultsList",
        "type": "List[ThreadNetworkDiagnostics.Enums.NetworkFaultEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 53,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 53,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 53,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 53,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 53,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 53,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "54": {
    "id": 54,
    "label": "WiFiNetworkDiagnostics",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 54,
        "label": "Bssid",
        "type": "Union[Nullable, bytes]"
      },
      "1": {
        "id": 1,
        "cluster_id": 54,
        "label": "SecurityType",
        "type": "Union[Nullable, WiFiNetworkDiagnostics.Enums.SecurityTypeEnum]"
      },
      "2": {
        "id": 2,
        "cluster_id": 54,
        "label": "WiFiVersion",
        "type": "Union[Nullable, WiFiNetworkDiagnostics.Enums.WiFiVersionEnum]"
      },
      "3": {
        "id": 3,
        "cluster_id": 54,
        "label": "ChannelNumber",
        "type": "Union[Nullable, uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 54,
        "label": "Rssi",
        "type": "Union[Nullable, int]"
      },
      "5": {
        "id": 5,
        "cluster_id": 54,
        "label": "BeaconLostCount",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 54,
        "label": "BeaconRxCount",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 54,
        "label": "PacketMulticastRxCount",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 54,
        "label": "PacketMulticastTxCount",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "9": {
        "id": 9,
        "cluster_id": 54,
        "label": "PacketUnicastRxCount",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "10": {
        "id": 10,
        "cluster_id": 54,
        "label": "PacketUnicastTxCount",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "11": {
        "id": 11,
        "cluster_id": 54,
        "label": "CurrentMaxRate",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "12": {
        "id": 12,
        "cluster_id": 54,
        "label": "OverrunCount",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 54,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 54,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 54,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 54,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 54,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 54,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "55": {
    "id": 55,
    "label": "EthernetNetworkDiagnostics",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 55,
        "label": "PHYRate",
        "type": "Union[NoneType, Nullable, EthernetNetworkDiagnostics.Enums.PHYRateEnum]"
      },
      "1": {
        "id": 1,
        "cluster_id": 55,
        "label": "FullDuplex",
        "type": "Union[NoneType, Nullable, bool]"
      },
      "2": {
        "id": 2,
        "cluster_id": 55,
        "label": "PacketRxCount",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 55,
        "label": "PacketTxCount",
        "type": "Optional[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 55,
        "label": "TxErrCount",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 55,
        "label": "CollisionCount",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 55,
        "label": "OverrunCount",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 55,
        "label": "CarrierDetect",
        "type": "Union[NoneType, Nullable, bool]"
      },
      "8": {
        "id": 8,
        "cluster_id": 55,
        "label": "TimeSinceReset",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 55,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 55,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 55,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 55,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 55,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 55,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "56": {
    "id": 56,
    "label": "TimeSynchronization",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 56,
        "label": "UTCTime",
        "type": "Union[Nullable, uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 56,
        "label": "Granularity",
        "type": "aenum GranularityEnum"
      },
      "2": {
        "id": 2,
        "cluster_id": 56,
        "label": "TimeSource",
        "type": "Optional[TimeSynchronization.Enums.TimeSourceEnum]"
      },
      "3": {
        "id": 3,
        "cluster_id": 56,
        "label": "TrustedTimeSource",
        "type": "Union[NoneType, Nullable, TimeSynchronization.Structs.TrustedTimeSourceStruct]"
      },
      "4": {
        "id": 4,
        "cluster_id": 56,
        "label": "DefaultNTP",
        "type": "Union[NoneType, Nullable, str]"
      },
      "5": {
        "id": 5,
        "cluster_id": 56,
        "label": "TimeZone",
        "type": "Optional[List[TimeSynchronization.Structs.TimeZoneStruct]]"
      },
      "6": {
        "id": 6,
        "cluster_id": 56,
        "label": "DSTOffset",
        "type": "Optional[List[TimeSynchronization.Structs.DSTOffsetStruct]]"
      },
      "7": {
        "id": 7,
        "cluster_id": 56,
        "label": "LocalTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 56,
        "label": "TimeZoneDatabase",
        "type": "Optional[TimeSynchronization.Enums.TimeZoneDatabaseEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 56,
        "label": "NTPServerAvailable",
        "type": "Optional[bool]"
      },
      "10": {
        "id": 10,
        "cluster_id": 56,
        "label": "TimeZoneListMaxSize",
        "type": "Optional[uint]"
      },
      "11": {
        "id": 11,
        "cluster_id": 56,
        "label": "DSTOffsetListMaxSize",
        "type": "Optional[uint]"
      },
      "12": {
        "id": 12,
        "cluster_id": 56,
        "label": "SupportsDNSResolve",
        "type": "Optional[bool]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 56,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 56,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 56,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 56,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 56,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 56,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "57": {
    "id": 57,
    "label": "BridgedDeviceBasicInformation",
    "attributes": {
      "1": {
        "id": 1,
        "cluster_id": 57,
        "label": "VendorName",
        "type": "Optional[str]"
      },
      "2": {
        "id": 2,
        "cluster_id": 57,
        "label": "VendorID",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 57,
        "label": "ProductName",
        "type": "Optional[str]"
      },
      "5": {
        "id": 5,
        "cluster_id": 57,
        "label": "NodeLabel",
        "type": "Optional[str]"
      },
      "7": {
        "id": 7,
        "cluster_id": 57,
        "label": "HardwareVersion",
        "type": "Optional[uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 57,
        "label": "HardwareVersionString",
        "type": "Optional[str]"
      },
      "9": {
        "id": 9,
        "cluster_id": 57,
        "label": "SoftwareVersion",
        "type": "Optional[uint]"
      },
      "10": {
        "id": 10,
        "cluster_id": 57,
        "label": "SoftwareVersionString",
        "type": "Optional[str]"
      },
      "11": {
        "id": 11,
        "cluster_id": 57,
        "label": "ManufacturingDate",
        "type": "Optional[str]"
      },
      "12": {
        "id": 12,
        "cluster_id": 57,
        "label": "PartNumber",
        "type": "Optional[str]"
      },
      "13": {
        "id": 13,
        "cluster_id": 57,
        "label": "ProductURL",
        "type": "Optional[str]"
      },
      "14": {
        "id": 14,
        "cluster_id": 57,
        "label": "ProductLabel",
        "type": "Optional[str]"
      },
      "15": {
        "id": 15,
        "cluster_id": 57,
        "label": "SerialNumber",
        "type": "Optional[str]"
      },
      "17": {
        "id": 17,
        "cluster_id": 57,
        "label": "Reachable",
        "type": "bool"
      },
      "18": {
        "id": 18,
        "cluster_id": 57,
        "label": "UniqueID",
        "type": "Optional[str]"
      },
      "20": {
        "id": 20,
        "cluster_id": 57,
        "label": "ProductAppearance",
        "type": "Optional[BridgedDeviceBasicInformation.Structs.ProductAppearanceStruct]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 57,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 57,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 57,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 57,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 57,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 57,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "59": {
    "id": 59,
    "label": "Switch",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 59,
        "label": "NumberOfPositions",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 59,
        "label": "CurrentPosition",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 59,
        "label": "MultiPressMax",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 59,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 59,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 59,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 59,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 59,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 59,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "60": {
    "id": 60,
    "label": "AdministratorCommissioning",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 60,
        "label": "WindowStatus",
        "type": "aenum CommissioningWindowStatusEnum"
      },
      "1": {
        "id": 1,
        "cluster_id": 60,
        "label": "AdminFabricIndex",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 60,
        "label": "AdminVendorId",
        "type": "Union[Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 60,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 60,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 60,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 60,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 60,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 60,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "62": {
    "id": 62,
    "label": "OperationalCredentials",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 62,
        "label": "NOCs",
        "type": "List[OperationalCredentials.Structs.NOCStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 62,
        "label": "Fabrics",
        "type": "List[OperationalCredentials.Structs.FabricDescriptorStruct]"
      },
      "2": {
        "id": 2,
        "cluster_id": 62,
        "label": "SupportedFabrics",
        "type": "uint"
      },
      "3": {
        "id": 3,
        "cluster_id": 62,
        "label": "CommissionedFabrics",
        "type": "uint"
      },
      "4": {
        "id": 4,
        "cluster_id": 62,
        "label": "TrustedRootCertificates",
        "type": "List[bytes]"
      },
      "5": {
        "id": 5,
        "cluster_id": 62,
        "label": "CurrentFabricIndex",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 62,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 62,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 62,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 62,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 62,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 62,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "63": {
    "id": 63,
    "label": "GroupKeyManagement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 63,
        "label": "GroupKeyMap",
        "type": "List[GroupKeyManagement.Structs.GroupKeyMapStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 63,
        "label": "GroupTable",
        "type": "List[GroupKeyManagement.Structs.GroupInfoMapStruct]"
      },
      "2": {
        "id": 2,
        "cluster_id": 63,
        "label": "MaxGroupsPerFabric",
        "type": "uint"
      },
      "3": {
        "id": 3,
        "cluster_id": 63,
        "label": "MaxGroupKeysPerFabric",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 63,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 63,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 63,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 63,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 63,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 63,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "64": {
    "id": 64,
    "label": "FixedLabel",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 64,
        "label": "LabelList",
        "type": "List[FixedLabel.Structs.LabelStruct]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 64,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 64,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 64,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 64,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 64,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 64,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "65": {
    "id": 65,
    "label": "UserLabel",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 65,
        "label": "LabelList",
        "type": "List[UserLabel.Structs.LabelStruct]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 65,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 65,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 65,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 65,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 65,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 65,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "66": {
    "id": 66,
    "label": "ProxyConfiguration",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 66,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 66,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 66,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 66,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 66,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 66,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "67": {
    "id": 67,
    "label": "ProxyDiscovery",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 67,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 67,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 67,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 67,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 67,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 67,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "68": {
    "id": 68,
    "label": "ProxyValid",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 68,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 68,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 68,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 68,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 68,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 68,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "69": {
    "id": 69,
    "label": "BooleanState",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 69,
        "label": "StateValue",
        "type": "bool"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 69,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 69,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 69,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 69,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 69,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 69,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "70": {
    "id": 70,
    "label": "IcdManagement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 70,
        "label": "IdleModeDuration",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 70,
        "label": "ActiveModeDuration",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 70,
        "label": "ActiveModeThreshold",
        "type": "uint"
      },
      "3": {
        "id": 3,
        "cluster_id": 70,
        "label": "RegisteredClients",
        "type": "Optional[List[IcdManagement.Structs.MonitoringRegistrationStruct]]"
      },
      "4": {
        "id": 4,
        "cluster_id": 70,
        "label": "ICDCounter",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 70,
        "label": "ClientsSupportedPerFabric",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 70,
        "label": "UserActiveModeTriggerHint",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 70,
        "label": "UserActiveModeTriggerInstruction",
        "type": "Optional[str]"
      },
      "8": {
        "id": 8,
        "cluster_id": 70,
        "label": "OperatingMode",
        "type": "Optional[IcdManagement.Enums.OperatingModeEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 70,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 70,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 70,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 70,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 70,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 70,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "71": {
    "id": 71,
    "label": "Timer",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 71,
        "label": "SetTime",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 71,
        "label": "TimeRemaining",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 71,
        "label": "TimerState",
        "type": "aenum TimerStatusEnum"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 71,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 71,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 71,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 71,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 71,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 71,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "72": {
    "id": 72,
    "label": "OvenCavityOperationalState",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 72,
        "label": "PhaseList",
        "type": "Union[Nullable, List[str]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 72,
        "label": "CurrentPhase",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 72,
        "label": "CountdownTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 72,
        "label": "OperationalStateList",
        "type": "List[OvenCavityOperationalState.Structs.OperationalStateStruct]"
      },
      "4": {
        "id": 4,
        "cluster_id": 72,
        "label": "OperationalState",
        "type": "aenum OperationalStateEnum"
      },
      "5": {
        "id": 5,
        "cluster_id": 72,
        "label": "OperationalError",
        "type": "OvenCavityOperationalState.Structs.ErrorStateStruct"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 72,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 72,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 72,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 72,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 72,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 72,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "73": {
    "id": 73,
    "label": "OvenMode",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 73,
        "label": "SupportedModes",
        "type": "List[OvenMode.Structs.ModeOptionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 73,
        "label": "CurrentMode",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 73,
        "label": "StartUpMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 73,
        "label": "OnMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 73,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 73,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 73,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 73,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 73,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 73,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "74": {
    "id": 74,
    "label": "LaundryDryerControls",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 74,
        "label": "SupportedDrynessLevels",
        "type": "List[LaundryDryerControls.Enums.DrynessLevelEnum]"
      },
      "1": {
        "id": 1,
        "cluster_id": 74,
        "label": "SelectedDrynessLevel",
        "type": "Union[Nullable, LaundryDryerControls.Enums.DrynessLevelEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 74,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 74,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 74,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 74,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 74,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 74,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "80": {
    "id": 80,
    "label": "ModeSelect",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 80,
        "label": "Description",
        "type": "str"
      },
      "1": {
        "id": 1,
        "cluster_id": 80,
        "label": "StandardNamespace",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 80,
        "label": "SupportedModes",
        "type": "List[ModeSelect.Structs.ModeOptionStruct]"
      },
      "3": {
        "id": 3,
        "cluster_id": 80,
        "label": "CurrentMode",
        "type": "uint"
      },
      "4": {
        "id": 4,
        "cluster_id": 80,
        "label": "StartUpMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 80,
        "label": "OnMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 80,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 80,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 80,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 80,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 80,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 80,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "81": {
    "id": 81,
    "label": "LaundryWasherMode",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 81,
        "label": "SupportedModes",
        "type": "List[LaundryWasherMode.Structs.ModeOptionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 81,
        "label": "CurrentMode",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 81,
        "label": "StartUpMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 81,
        "label": "OnMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 81,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 81,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 81,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 81,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 81,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 81,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "82": {
    "id": 82,
    "label": "RefrigeratorAndTemperatureControlledCabinetMode",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 82,
        "label": "SupportedModes",
        "type": "List[RefrigeratorAndTemperatureControlledCabinetMode.Structs.ModeOptionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 82,
        "label": "CurrentMode",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 82,
        "label": "StartUpMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 82,
        "label": "OnMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 82,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 82,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 82,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 82,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 82,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 82,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "83": {
    "id": 83,
    "label": "LaundryWasherControls",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 83,
        "label": "SpinSpeeds",
        "type": "Optional[List[str]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 83,
        "label": "SpinSpeedCurrent",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 83,
        "label": "NumberOfRinses",
        "type": "Optional[LaundryWasherControls.Enums.NumberOfRinsesEnum]"
      },
      "3": {
        "id": 3,
        "cluster_id": 83,
        "label": "SupportedRinses",
        "type": "Optional[List[LaundryWasherControls.Enums.NumberOfRinsesEnum]]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 83,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 83,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 83,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 83,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 83,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 83,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "84": {
    "id": 84,
    "label": "RvcRunMode",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 84,
        "label": "SupportedModes",
        "type": "List[RvcRunMode.Structs.ModeOptionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 84,
        "label": "CurrentMode",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 84,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 84,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 84,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 84,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 84,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 84,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "85": {
    "id": 85,
    "label": "RvcCleanMode",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 85,
        "label": "SupportedModes",
        "type": "List[RvcCleanMode.Structs.ModeOptionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 85,
        "label": "CurrentMode",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 85,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 85,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 85,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 85,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 85,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 85,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "86": {
    "id": 86,
    "label": "TemperatureControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 86,
        "label": "TemperatureSetpoint",
        "type": "Optional[int]"
      },
      "1": {
        "id": 1,
        "cluster_id": 86,
        "label": "MinTemperature",
        "type": "Optional[int]"
      },
      "2": {
        "id": 2,
        "cluster_id": 86,
        "label": "MaxTemperature",
        "type": "Optional[int]"
      },
      "3": {
        "id": 3,
        "cluster_id": 86,
        "label": "Step",
        "type": "Optional[int]"
      },
      "4": {
        "id": 4,
        "cluster_id": 86,
        "label": "SelectedTemperatureLevel",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 86,
        "label": "SupportedTemperatureLevels",
        "type": "Optional[List[str]]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 86,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 86,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 86,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 86,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 86,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 86,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "87": {
    "id": 87,
    "label": "RefrigeratorAlarm",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 87,
        "label": "Mask",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 87,
        "label": "State",
        "type": "uint"
      },
      "3": {
        "id": 3,
        "cluster_id": 87,
        "label": "Supported",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 87,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 87,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 87,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 87,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 87,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 87,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "89": {
    "id": 89,
    "label": "DishwasherMode",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 89,
        "label": "SupportedModes",
        "type": "List[DishwasherMode.Structs.ModeOptionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 89,
        "label": "CurrentMode",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 89,
        "label": "StartUpMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 89,
        "label": "OnMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 89,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 89,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 89,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 89,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 89,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 89,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "91": {
    "id": 91,
    "label": "AirQuality",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 91,
        "label": "AirQuality",
        "type": "aenum AirQualityEnum"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 91,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 91,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 91,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 91,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 91,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 91,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "92": {
    "id": 92,
    "label": "SmokeCoAlarm",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 92,
        "label": "ExpressedState",
        "type": "aenum ExpressedStateEnum"
      },
      "1": {
        "id": 1,
        "cluster_id": 92,
        "label": "SmokeState",
        "type": "Optional[SmokeCoAlarm.Enums.AlarmStateEnum]"
      },
      "2": {
        "id": 2,
        "cluster_id": 92,
        "label": "COState",
        "type": "Optional[SmokeCoAlarm.Enums.AlarmStateEnum]"
      },
      "3": {
        "id": 3,
        "cluster_id": 92,
        "label": "BatteryAlert",
        "type": "aenum AlarmStateEnum"
      },
      "4": {
        "id": 4,
        "cluster_id": 92,
        "label": "DeviceMuted",
        "type": "Optional[SmokeCoAlarm.Enums.MuteStateEnum]"
      },
      "5": {
        "id": 5,
        "cluster_id": 92,
        "label": "TestInProgress",
        "type": "bool"
      },
      "6": {
        "id": 6,
        "cluster_id": 92,
        "label": "HardwareFaultAlert",
        "type": "bool"
      },
      "7": {
        "id": 7,
        "cluster_id": 92,
        "label": "EndOfServiceAlert",
        "type": "aenum EndOfServiceEnum"
      },
      "8": {
        "id": 8,
        "cluster_id": 92,
        "label": "InterconnectSmokeAlarm",
        "type": "Optional[SmokeCoAlarm.Enums.AlarmStateEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 92,
        "label": "InterconnectCOAlarm",
        "type": "Optional[SmokeCoAlarm.Enums.AlarmStateEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 92,
        "label": "ContaminationState",
        "type": "Optional[SmokeCoAlarm.Enums.ContaminationStateEnum]"
      },
      "11": {
        "id": 11,
        "cluster_id": 92,
        "label": "SmokeSensitivityLevel",
        "type": "Optional[SmokeCoAlarm.Enums.SensitivityEnum]"
      },
      "12": {
        "id": 12,
        "cluster_id": 92,
        "label": "ExpiryDate",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 92,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 92,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 92,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 92,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 92,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 92,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "93": {
    "id": 93,
    "label": "DishwasherAlarm",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 93,
        "label": "Mask",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 93,
        "label": "Latch",
        "type": "Optional[uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 93,
        "label": "State",
        "type": "uint"
      },
      "3": {
        "id": 3,
        "cluster_id": 93,
        "label": "Supported",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 93,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 93,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 93,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 93,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 93,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 93,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "94": {
    "id": 94,
    "label": "MicrowaveOvenMode",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 94,
        "label": "SupportedModes",
        "type": "List[MicrowaveOvenMode.Structs.ModeOptionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 94,
        "label": "CurrentMode",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 94,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 94,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 94,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 94,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 94,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 94,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "95": {
    "id": 95,
    "label": "MicrowaveOvenControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 95,
        "label": "CookTime",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 95,
        "label": "MaxCookTime",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 95,
        "label": "PowerSetting",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 95,
        "label": "MinPower",
        "type": "Optional[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 95,
        "label": "MaxPower",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 95,
        "label": "PowerStep",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 95,
        "label": "SupportedWatts",
        "type": "Optional[List[uint]]"
      },
      "7": {
        "id": 7,
        "cluster_id": 95,
        "label": "SelectedWattIndex",
        "type": "Optional[uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 95,
        "label": "WattRating",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 95,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 95,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 95,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 95,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 95,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 95,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "96": {
    "id": 96,
    "label": "OperationalState",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 96,
        "label": "PhaseList",
        "type": "Union[Nullable, List[str]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 96,
        "label": "CurrentPhase",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 96,
        "label": "CountdownTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 96,
        "label": "OperationalStateList",
        "type": "List[OperationalState.Structs.OperationalStateStruct]"
      },
      "4": {
        "id": 4,
        "cluster_id": 96,
        "label": "OperationalState",
        "type": "aenum OperationalStateEnum"
      },
      "5": {
        "id": 5,
        "cluster_id": 96,
        "label": "OperationalError",
        "type": "OperationalState.Structs.ErrorStateStruct"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 96,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 96,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 96,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 96,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 96,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 96,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "97": {
    "id": 97,
    "label": "RvcOperationalState",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 97,
        "label": "PhaseList",
        "type": "Union[Nullable, List[str]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 97,
        "label": "CurrentPhase",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 97,
        "label": "CountdownTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 97,
        "label": "OperationalStateList",
        "type": "List[RvcOperationalState.Structs.OperationalStateStruct]"
      },
      "4": {
        "id": 4,
        "cluster_id": 97,
        "label": "OperationalState",
        "type": "uint"
      },
      "5": {
        "id": 5,
        "cluster_id": 97,
        "label": "OperationalError",
        "type": "RvcOperationalState.Structs.ErrorStateStruct"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 97,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 97,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 97,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 97,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 97,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 97,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "98": {
    "id": 98,
    "label": "ScenesManagement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 98,
        "label": "LastConfiguredBy",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 98,
        "label": "SceneTableSize",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 98,
        "label": "FabricSceneInfo",
        "type": "List[ScenesManagement.Structs.SceneInfoStruct]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 98,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 98,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 98,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 98,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 98,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 98,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "113": {
    "id": 113,
    "label": "HepaFilterMonitoring",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 113,
        "label": "Condition",
        "type": "Optional[uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 113,
        "label": "DegradationDirection",
        "type": "Optional[HepaFilterMonitoring.Enums.DegradationDirectionEnum]"
      },
      "2": {
        "id": 2,
        "cluster_id": 113,
        "label": "ChangeIndication",
        "type": "aenum ChangeIndicationEnum"
      },
      "3": {
        "id": 3,
        "cluster_id": 113,
        "label": "InPlaceIndicator",
        "type": "Optional[bool]"
      },
      "4": {
        "id": 4,
        "cluster_id": 113,
        "label": "LastChangedTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 113,
        "label": "ReplacementProductList",
        "type": "Optional[List[HepaFilterMonitoring.Structs.ReplacementProductStruct]]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 113,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 113,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 113,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 113,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 113,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 113,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "114": {
    "id": 114,
    "label": "ActivatedCarbonFilterMonitoring",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 114,
        "label": "Condition",
        "type": "Optional[uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 114,
        "label": "DegradationDirection",
        "type": "Optional[ActivatedCarbonFilterMonitoring.Enums.DegradationDirectionEnum]"
      },
      "2": {
        "id": 2,
        "cluster_id": 114,
        "label": "ChangeIndication",
        "type": "aenum ChangeIndicationEnum"
      },
      "3": {
        "id": 3,
        "cluster_id": 114,
        "label": "InPlaceIndicator",
        "type": "Optional[bool]"
      },
      "4": {
        "id": 4,
        "cluster_id": 114,
        "label": "LastChangedTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 114,
        "label": "ReplacementProductList",
        "type": "Optional[List[ActivatedCarbonFilterMonitoring.Structs.ReplacementProductStruct]]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 114,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 114,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 114,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 114,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 114,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 114,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "128": {
    "id": 128,
    "label": "BooleanStateConfiguration",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 128,
        "label": "CurrentSensitivityLevel",
        "type": "Optional[uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 128,
        "label": "SupportedSensitivityLevels",
        "type": "Optional[uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 128,
        "label": "DefaultSensitivityLevel",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 128,
        "label": "AlarmsActive",
        "type": "Optional[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 128,
        "label": "AlarmsSuppressed",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 128,
        "label": "AlarmsEnabled",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 128,
        "label": "AlarmsSupported",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 128,
        "label": "SensorFault",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 128,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 128,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 128,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 128,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 128,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 128,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "129": {
    "id": 129,
    "label": "ValveConfigurationAndControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 129,
        "label": "OpenDuration",
        "type": "Union[Nullable, uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 129,
        "label": "DefaultOpenDuration",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 129,
        "label": "AutoCloseTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 129,
        "label": "RemainingDuration",
        "type": "Union[Nullable, uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 129,
        "label": "CurrentState",
        "type": "Union[Nullable, ValveConfigurationAndControl.Enums.ValveStateEnum]"
      },
      "5": {
        "id": 5,
        "cluster_id": 129,
        "label": "TargetState",
        "type": "Union[Nullable, ValveConfigurationAndControl.Enums.ValveStateEnum]"
      },
      "6": {
        "id": 6,
        "cluster_id": 129,
        "label": "CurrentLevel",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 129,
        "label": "TargetLevel",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 129,
        "label": "DefaultOpenLevel",
        "type": "Optional[uint]"
      },
      "9": {
        "id": 9,
        "cluster_id": 129,
        "label": "ValveFault",
        "type": "Optional[uint]"
      },
      "10": {
        "id": 10,
        "cluster_id": 129,
        "label": "LevelStep",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 129,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 129,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 129,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 129,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 129,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 129,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "144": {
    "id": 144,
    "label": "ElectricalPowerMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 144,
        "label": "PowerMode",
        "type": "aenum PowerModeEnum"
      },
      "1": {
        "id": 1,
        "cluster_id": 144,
        "label": "NumberOfMeasurementTypes",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 144,
        "label": "Accuracy",
        "type": "List[ElectricalPowerMeasurement.Structs.MeasurementAccuracyStruct]"
      },
      "3": {
        "id": 3,
        "cluster_id": 144,
        "label": "Ranges",
        "type": "Optional[List[ElectricalPowerMeasurement.Structs.MeasurementRangeStruct]]"
      },
      "4": {
        "id": 4,
        "cluster_id": 144,
        "label": "Voltage",
        "type": "Union[NoneType, Nullable, int]"
      },
      "5": {
        "id": 5,
        "cluster_id": 144,
        "label": "ActiveCurrent",
        "type": "Union[NoneType, Nullable, int]"
      },
      "6": {
        "id": 6,
        "cluster_id": 144,
        "label": "ReactiveCurrent",
        "type": "Union[NoneType, Nullable, int]"
      },
      "7": {
        "id": 7,
        "cluster_id": 144,
        "label": "ApparentCurrent",
        "type": "Union[NoneType, Nullable, int]"
      },
      "8": {
        "id": 8,
        "cluster_id": 144,
        "label": "ActivePower",
        "type": "Union[Nullable, int]"
      },
      "9": {
        "id": 9,
        "cluster_id": 144,
        "label": "ReactivePower",
        "type": "Union[NoneType, Nullable, int]"
      },
      "10": {
        "id": 10,
        "cluster_id": 144,
        "label": "ApparentPower",
        "type": "Union[NoneType, Nullable, int]"
      },
      "11": {
        "id": 11,
        "cluster_id": 144,
        "label": "RMSVoltage",
        "type": "Union[NoneType, Nullable, int]"
      },
      "12": {
        "id": 12,
        "cluster_id": 144,
        "label": "RMSCurrent",
        "type": "Union[NoneType, Nullable, int]"
      },
      "13": {
        "id": 13,
        "cluster_id": 144,
        "label": "RMSPower",
        "type": "Union[NoneType, Nullable, int]"
      },
      "14": {
        "id": 14,
        "cluster_id": 144,
        "label": "Frequency",
        "type": "Union[NoneType, Nullable, int]"
      },
      "15": {
        "id": 15,
        "cluster_id": 144,
        "label": "HarmonicCurrents",
        "type": "Union[NoneType, Nullable, List[ElectricalPowerMeasurement.Structs.HarmonicMeasurementStruct]]"
      },
      "16": {
        "id": 16,
        "cluster_id": 144,
        "label": "HarmonicPhases",
        "type": "Union[NoneType, Nullable, List[ElectricalPowerMeasurement.Structs.HarmonicMeasurementStruct]]"
      },
      "17": {
        "id": 17,
        "cluster_id": 144,
        "label": "PowerFactor",
        "type": "Union[NoneType, Nullable, int]"
      },
      "18": {
        "id": 18,
        "cluster_id": 144,
        "label": "NeutralCurrent",
        "type": "Union[NoneType, Nullable, int]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 144,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 144,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 144,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 144,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 144,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 144,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "145": {
    "id": 145,
    "label": "ElectricalEnergyMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 145,
        "label": "Accuracy",
        "type": "ElectricalEnergyMeasurement.Structs.MeasurementAccuracyStruct"
      },
      "1": {
        "id": 1,
        "cluster_id": 145,
        "label": "CumulativeEnergyImported",
        "type": "Union[NoneType, Nullable, ElectricalEnergyMeasurement.Structs.EnergyMeasurementStruct]"
      },
      "2": {
        "id": 2,
        "cluster_id": 145,
        "label": "CumulativeEnergyExported",
        "type": "Union[NoneType, Nullable, ElectricalEnergyMeasurement.Structs.EnergyMeasurementStruct]"
      },
      "3": {
        "id": 3,
        "cluster_id": 145,
        "label": "PeriodicEnergyImported",
        "type": "Union[NoneType, Nullable, ElectricalEnergyMeasurement.Structs.EnergyMeasurementStruct]"
      },
      "4": {
        "id": 4,
        "cluster_id": 145,
        "label": "PeriodicEnergyExported",
        "type": "Union[NoneType, Nullable, ElectricalEnergyMeasurement.Structs.EnergyMeasurementStruct]"
      },
      "5": {
        "id": 5,
        "cluster_id": 145,
        "label": "CumulativeEnergyReset",
        "type": "Union[NoneType, Nullable, ElectricalEnergyMeasurement.Structs.CumulativeEnergyResetStruct]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 145,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 145,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 145,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 145,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 145,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 145,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "150": {
    "id": 150,
    "label": "DemandResponseLoadControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 150,
        "label": "LoadControlPrograms",
        "type": "List[DemandResponseLoadControl.Structs.LoadControlProgramStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 150,
        "label": "NumberOfLoadControlPrograms",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 150,
        "label": "Events",
        "type": "List[DemandResponseLoadControl.Structs.LoadControlEventStruct]"
      },
      "3": {
        "id": 3,
        "cluster_id": 150,
        "label": "ActiveEvents",
        "type": "List[DemandResponseLoadControl.Structs.LoadControlEventStruct]"
      },
      "4": {
        "id": 4,
        "cluster_id": 150,
        "label": "NumberOfEventsPerProgram",
        "type": "uint"
      },
      "5": {
        "id": 5,
        "cluster_id": 150,
        "label": "NumberOfTransitions",
        "type": "uint"
      },
      "6": {
        "id": 6,
        "cluster_id": 150,
        "label": "DefaultRandomStart",
        "type": "uint"
      },
      "7": {
        "id": 7,
        "cluster_id": 150,
        "label": "DefaultRandomDuration",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 150,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 150,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 150,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 150,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 150,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 150,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "151": {
    "id": 151,
    "label": "Messages",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 151,
        "label": "Messages",
        "type": "List[Messages.Structs.MessageStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 151,
        "label": "ActiveMessageIDs",
        "type": "List[bytes]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 151,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 151,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 151,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 151,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 151,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 151,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "152": {
    "id": 152,
    "label": "DeviceEnergyManagement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 152,
        "label": "ESAType",
        "type": "aenum ESATypeEnum"
      },
      "1": {
        "id": 1,
        "cluster_id": 152,
        "label": "ESACanGenerate",
        "type": "bool"
      },
      "2": {
        "id": 2,
        "cluster_id": 152,
        "label": "ESAState",
        "type": "aenum ESAStateEnum"
      },
      "3": {
        "id": 3,
        "cluster_id": 152,
        "label": "AbsMinPower",
        "type": "int"
      },
      "4": {
        "id": 4,
        "cluster_id": 152,
        "label": "AbsMaxPower",
        "type": "int"
      },
      "5": {
        "id": 5,
        "cluster_id": 152,
        "label": "PowerAdjustmentCapability",
        "type": "Union[NoneType, Nullable, List[DeviceEnergyManagement.Structs.PowerAdjustStruct]]"
      },
      "6": {
        "id": 6,
        "cluster_id": 152,
        "label": "Forecast",
        "type": "Union[NoneType, Nullable, DeviceEnergyManagement.Structs.ForecastStruct]"
      },
      "7": {
        "id": 7,
        "cluster_id": 152,
        "label": "OptOutState",
        "type": "Optional[DeviceEnergyManagement.Enums.OptOutStateEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 152,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 152,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 152,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 152,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 152,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 152,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "153": {
    "id": 153,
    "label": "EnergyEvse",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 153,
        "label": "State",
        "type": "Union[Nullable, EnergyEvse.Enums.StateEnum]"
      },
      "1": {
        "id": 1,
        "cluster_id": 153,
        "label": "SupplyState",
        "type": "aenum SupplyStateEnum"
      },
      "2": {
        "id": 2,
        "cluster_id": 153,
        "label": "FaultState",
        "type": "aenum FaultStateEnum"
      },
      "3": {
        "id": 3,
        "cluster_id": 153,
        "label": "ChargingEnabledUntil",
        "type": "Union[Nullable, uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 153,
        "label": "DischargingEnabledUntil",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 153,
        "label": "CircuitCapacity",
        "type": "int"
      },
      "6": {
        "id": 6,
        "cluster_id": 153,
        "label": "MinimumChargeCurrent",
        "type": "int"
      },
      "7": {
        "id": 7,
        "cluster_id": 153,
        "label": "MaximumChargeCurrent",
        "type": "int"
      },
      "8": {
        "id": 8,
        "cluster_id": 153,
        "label": "MaximumDischargeCurrent",
        "type": "Optional[int]"
      },
      "9": {
        "id": 9,
        "cluster_id": 153,
        "label": "UserMaximumChargeCurrent",
        "type": "Optional[int]"
      },
      "10": {
        "id": 10,
        "cluster_id": 153,
        "label": "RandomizationDelayWindow",
        "type": "Optional[uint]"
      },
      "35": {
        "id": 35,
        "cluster_id": 153,
        "label": "NextChargeStartTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "36": {
        "id": 36,
        "cluster_id": 153,
        "label": "NextChargeTargetTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "37": {
        "id": 37,
        "cluster_id": 153,
        "label": "NextChargeRequiredEnergy",
        "type": "Union[NoneType, Nullable, int]"
      },
      "38": {
        "id": 38,
        "cluster_id": 153,
        "label": "NextChargeTargetSoC",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "39": {
        "id": 39,
        "cluster_id": 153,
        "label": "ApproximateEVEfficiency",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "48": {
        "id": 48,
        "cluster_id": 153,
        "label": "StateOfCharge",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "49": {
        "id": 49,
        "cluster_id": 153,
        "label": "BatteryCapacity",
        "type": "Union[NoneType, Nullable, int]"
      },
      "50": {
        "id": 50,
        "cluster_id": 153,
        "label": "VehicleID",
        "type": "Union[NoneType, Nullable, str]"
      },
      "64": {
        "id": 64,
        "cluster_id": 153,
        "label": "SessionID",
        "type": "Union[Nullable, uint]"
      },
      "65": {
        "id": 65,
        "cluster_id": 153,
        "label": "SessionDuration",
        "type": "Union[Nullable, uint]"
      },
      "66": {
        "id": 66,
        "cluster_id": 153,
        "label": "SessionEnergyCharged",
        "type": "Union[Nullable, int]"
      },
      "67": {
        "id": 67,
        "cluster_id": 153,
        "label": "SessionEnergyDischarged",
        "type": "Union[NoneType, Nullable, int]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 153,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 153,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 153,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 153,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 153,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 153,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "155": {
    "id": 155,
    "label": "EnergyPreference",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 155,
        "label": "EnergyBalances",
        "type": "Optional[List[EnergyPreference.Structs.BalanceStruct]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 155,
        "label": "CurrentEnergyBalance",
        "type": "Optional[uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 155,
        "label": "EnergyPriorities",
        "type": "Optional[List[EnergyPreference.Enums.EnergyPriorityEnum]]"
      },
      "3": {
        "id": 3,
        "cluster_id": 155,
        "label": "LowPowerModeSensitivities",
        "type": "Optional[List[EnergyPreference.Structs.BalanceStruct]]"
      },
      "4": {
        "id": 4,
        "cluster_id": 155,
        "label": "CurrentLowPowerModeSensitivity",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 155,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 155,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 155,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 155,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 155,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 155,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "156": {
    "id": 156,
    "label": "PowerTopology",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 156,
        "label": "AvailableEndpoints",
        "type": "Optional[List[uint]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 156,
        "label": "ActiveEndpoints",
        "type": "Optional[List[uint]]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 156,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 156,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 156,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 156,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 156,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 156,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "157": {
    "id": 157,
    "label": "EnergyEvseMode",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 157,
        "label": "SupportedModes",
        "type": "List[EnergyEvseMode.Structs.ModeOptionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 157,
        "label": "CurrentMode",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 157,
        "label": "StartUpMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 157,
        "label": "OnMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 157,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 157,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 157,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 157,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 157,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 157,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "159": {
    "id": 159,
    "label": "DeviceEnergyManagementMode",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 159,
        "label": "SupportedModes",
        "type": "List[DeviceEnergyManagementMode.Structs.ModeOptionStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 159,
        "label": "CurrentMode",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 159,
        "label": "StartUpMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 159,
        "label": "OnMode",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 159,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 159,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 159,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 159,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 159,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 159,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "257": {
    "id": 257,
    "label": "DoorLock",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 257,
        "label": "LockState",
        "type": "Union[Nullable, DoorLock.Enums.DlLockState]"
      },
      "1": {
        "id": 1,
        "cluster_id": 257,
        "label": "LockType",
        "type": "aenum DlLockType"
      },
      "2": {
        "id": 2,
        "cluster_id": 257,
        "label": "ActuatorEnabled",
        "type": "bool"
      },
      "3": {
        "id": 3,
        "cluster_id": 257,
        "label": "DoorState",
        "type": "Union[NoneType, Nullable, DoorLock.Enums.DoorStateEnum]"
      },
      "4": {
        "id": 4,
        "cluster_id": 257,
        "label": "DoorOpenEvents",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 257,
        "label": "DoorClosedEvents",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 257,
        "label": "OpenPeriod",
        "type": "Optional[uint]"
      },
      "17": {
        "id": 17,
        "cluster_id": 257,
        "label": "NumberOfTotalUsersSupported",
        "type": "Optional[uint]"
      },
      "18": {
        "id": 18,
        "cluster_id": 257,
        "label": "NumberOfPINUsersSupported",
        "type": "Optional[uint]"
      },
      "19": {
        "id": 19,
        "cluster_id": 257,
        "label": "NumberOfRFIDUsersSupported",
        "type": "Optional[uint]"
      },
      "20": {
        "id": 20,
        "cluster_id": 257,
        "label": "NumberOfWeekDaySchedulesSupportedPerUser",
        "type": "Optional[uint]"
      },
      "21": {
        "id": 21,
        "cluster_id": 257,
        "label": "NumberOfYearDaySchedulesSupportedPerUser",
        "type": "Optional[uint]"
      },
      "22": {
        "id": 22,
        "cluster_id": 257,
        "label": "NumberOfHolidaySchedulesSupported",
        "type": "Optional[uint]"
      },
      "23": {
        "id": 23,
        "cluster_id": 257,
        "label": "MaxPINCodeLength",
        "type": "Optional[uint]"
      },
      "24": {
        "id": 24,
        "cluster_id": 257,
        "label": "MinPINCodeLength",
        "type": "Optional[uint]"
      },
      "25": {
        "id": 25,
        "cluster_id": 257,
        "label": "MaxRFIDCodeLength",
        "type": "Optional[uint]"
      },
      "26": {
        "id": 26,
        "cluster_id": 257,
        "label": "MinRFIDCodeLength",
        "type": "Optional[uint]"
      },
      "27": {
        "id": 27,
        "cluster_id": 257,
        "label": "CredentialRulesSupport",
        "type": "Optional[uint]"
      },
      "28": {
        "id": 28,
        "cluster_id": 257,
        "label": "NumberOfCredentialsSupportedPerUser",
        "type": "Optional[uint]"
      },
      "33": {
        "id": 33,
        "cluster_id": 257,
        "label": "Language",
        "type": "Optional[str]"
      },
      "34": {
        "id": 34,
        "cluster_id": 257,
        "label": "LEDSettings",
        "type": "Optional[uint]"
      },
      "35": {
        "id": 35,
        "cluster_id": 257,
        "label": "AutoRelockTime",
        "type": "uint"
      },
      "36": {
        "id": 36,
        "cluster_id": 257,
        "label": "SoundVolume",
        "type": "Optional[uint]"
      },
      "37": {
        "id": 37,
        "cluster_id": 257,
        "label": "OperatingMode",
        "type": "aenum OperatingModeEnum"
      },
      "38": {
        "id": 38,
        "cluster_id": 257,
        "label": "SupportedOperatingModes",
        "type": "uint"
      },
      "39": {
        "id": 39,
        "cluster_id": 257,
        "label": "DefaultConfigurationRegister",
        "type": "Optional[uint]"
      },
      "40": {
        "id": 40,
        "cluster_id": 257,
        "label": "EnableLocalProgramming",
        "type": "Optional[bool]"
      },
      "41": {
        "id": 41,
        "cluster_id": 257,
        "label": "EnableOneTouchLocking",
        "type": "Optional[bool]"
      },
      "42": {
        "id": 42,
        "cluster_id": 257,
        "label": "EnableInsideStatusLED",
        "type": "Optional[bool]"
      },
      "43": {
        "id": 43,
        "cluster_id": 257,
        "label": "EnablePrivacyModeButton",
        "type": "Optional[bool]"
      },
      "44": {
        "id": 44,
        "cluster_id": 257,
        "label": "LocalProgrammingFeatures",
        "type": "Optional[uint]"
      },
      "48": {
        "id": 48,
        "cluster_id": 257,
        "label": "WrongCodeEntryLimit",
        "type": "Optional[uint]"
      },
      "49": {
        "id": 49,
        "cluster_id": 257,
        "label": "UserCodeTemporaryDisableTime",
        "type": "Optional[uint]"
      },
      "50": {
        "id": 50,
        "cluster_id": 257,
        "label": "SendPINOverTheAir",
        "type": "Optional[bool]"
      },
      "51": {
        "id": 51,
        "cluster_id": 257,
        "label": "RequirePINforRemoteOperation",
        "type": "Optional[bool]"
      },
      "53": {
        "id": 53,
        "cluster_id": 257,
        "label": "ExpiringUserTimeout",
        "type": "Optional[uint]"
      },
      "128": {
        "id": 128,
        "cluster_id": 257,
        "label": "AliroReaderVerificationKey",
        "type": "Union[NoneType, Nullable, bytes]"
      },
      "129": {
        "id": 129,
        "cluster_id": 257,
        "label": "AliroReaderGroupIdentifier",
        "type": "Union[NoneType, Nullable, bytes]"
      },
      "130": {
        "id": 130,
        "cluster_id": 257,
        "label": "AliroReaderGroupSubIdentifier",
        "type": "Optional[bytes]"
      },
      "131": {
        "id": 131,
        "cluster_id": 257,
        "label": "AliroExpeditedTransactionSupportedProtocolVersions",
        "type": "Optional[List[bytes]]"
      },
      "132": {
        "id": 132,
        "cluster_id": 257,
        "label": "AliroGroupResolvingKey",
        "type": "Union[NoneType, Nullable, bytes]"
      },
      "133": {
        "id": 133,
        "cluster_id": 257,
        "label": "AliroSupportedBLEUWBProtocolVersions",
        "type": "Optional[List[bytes]]"
      },
      "134": {
        "id": 134,
        "cluster_id": 257,
        "label": "AliroBLEAdvertisingVersion",
        "type": "Optional[uint]"
      },
      "135": {
        "id": 135,
        "cluster_id": 257,
        "label": "NumberOfAliroCredentialIssuerKeysSupported",
        "type": "Optional[uint]"
      },
      "136": {
        "id": 136,
        "cluster_id": 257,
        "label": "NumberOfAliroEndpointKeysSupported",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 257,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 257,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 257,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 257,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 257,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 257,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "258": {
    "id": 258,
    "label": "WindowCovering",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 258,
        "label": "Type",
        "type": "aenum Type"
      },
      "1": {
        "id": 1,
        "cluster_id": 258,
        "label": "PhysicalClosedLimitLift",
        "type": "Optional[uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 258,
        "label": "PhysicalClosedLimitTilt",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 258,
        "label": "CurrentPositionLift",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 258,
        "label": "CurrentPositionTilt",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 258,
        "label": "NumberOfActuationsLift",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 258,
        "label": "NumberOfActuationsTilt",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 258,
        "label": "ConfigStatus",
        "type": "uint"
      },
      "8": {
        "id": 8,
        "cluster_id": 258,
        "label": "CurrentPositionLiftPercentage",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "9": {
        "id": 9,
        "cluster_id": 258,
        "label": "CurrentPositionTiltPercentage",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "10": {
        "id": 10,
        "cluster_id": 258,
        "label": "OperationalStatus",
        "type": "uint"
      },
      "11": {
        "id": 11,
        "cluster_id": 258,
        "label": "TargetPositionLiftPercent100ths",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "12": {
        "id": 12,
        "cluster_id": 258,
        "label": "TargetPositionTiltPercent100ths",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "13": {
        "id": 13,
        "cluster_id": 258,
        "label": "EndProductType",
        "type": "aenum EndProductType"
      },
      "14": {
        "id": 14,
        "cluster_id": 258,
        "label": "CurrentPositionLiftPercent100ths",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "15": {
        "id": 15,
        "cluster_id": 258,
        "label": "CurrentPositionTiltPercent100ths",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "16": {
        "id": 16,
        "cluster_id": 258,
        "label": "InstalledOpenLimitLift",
        "type": "Optional[uint]"
      },
      "17": {
        "id": 17,
        "cluster_id": 258,
        "label": "InstalledClosedLimitLift",
        "type": "Optional[uint]"
      },
      "18": {
        "id": 18,
        "cluster_id": 258,
        "label": "InstalledOpenLimitTilt",
        "type": "Optional[uint]"
      },
      "19": {
        "id": 19,
        "cluster_id": 258,
        "label": "InstalledClosedLimitTilt",
        "type": "Optional[uint]"
      },
      "23": {
        "id": 23,
        "cluster_id": 258,
        "label": "Mode",
        "type": "uint"
      },
      "26": {
        "id": 26,
        "cluster_id": 258,
        "label": "SafetyStatus",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 258,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 258,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 258,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 258,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 258,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 258,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "259": {
    "id": 259,
    "label": "BarrierControl",
    "attributes": {
      "1": {
        "id": 1,
        "cluster_id": 259,
        "label": "BarrierMovingState",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 259,
        "label": "BarrierSafetyStatus",
        "type": "uint"
      },
      "3": {
        "id": 3,
        "cluster_id": 259,
        "label": "BarrierCapabilities",
        "type": "uint"
      },
      "4": {
        "id": 4,
        "cluster_id": 259,
        "label": "BarrierOpenEvents",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 259,
        "label": "BarrierCloseEvents",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 259,
        "label": "BarrierCommandOpenEvents",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 259,
        "label": "BarrierCommandCloseEvents",
        "type": "Optional[uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 259,
        "label": "BarrierOpenPeriod",
        "type": "Optional[uint]"
      },
      "9": {
        "id": 9,
        "cluster_id": 259,
        "label": "BarrierClosePeriod",
        "type": "Optional[uint]"
      },
      "10": {
        "id": 10,
        "cluster_id": 259,
        "label": "BarrierPosition",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 259,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 259,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 259,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 259,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 259,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 259,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "512": {
    "id": 512,
    "label": "PumpConfigurationAndControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 512,
        "label": "MaxPressure",
        "type": "Union[Nullable, int]"
      },
      "1": {
        "id": 1,
        "cluster_id": 512,
        "label": "MaxSpeed",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 512,
        "label": "MaxFlow",
        "type": "Union[Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 512,
        "label": "MinConstPressure",
        "type": "Union[NoneType, Nullable, int]"
      },
      "4": {
        "id": 4,
        "cluster_id": 512,
        "label": "MaxConstPressure",
        "type": "Union[NoneType, Nullable, int]"
      },
      "5": {
        "id": 5,
        "cluster_id": 512,
        "label": "MinCompPressure",
        "type": "Union[NoneType, Nullable, int]"
      },
      "6": {
        "id": 6,
        "cluster_id": 512,
        "label": "MaxCompPressure",
        "type": "Union[NoneType, Nullable, int]"
      },
      "7": {
        "id": 7,
        "cluster_id": 512,
        "label": "MinConstSpeed",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 512,
        "label": "MaxConstSpeed",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "9": {
        "id": 9,
        "cluster_id": 512,
        "label": "MinConstFlow",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "10": {
        "id": 10,
        "cluster_id": 512,
        "label": "MaxConstFlow",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "11": {
        "id": 11,
        "cluster_id": 512,
        "label": "MinConstTemp",
        "type": "Union[NoneType, Nullable, int]"
      },
      "12": {
        "id": 12,
        "cluster_id": 512,
        "label": "MaxConstTemp",
        "type": "Union[NoneType, Nullable, int]"
      },
      "16": {
        "id": 16,
        "cluster_id": 512,
        "label": "PumpStatus",
        "type": "Optional[uint]"
      },
      "17": {
        "id": 17,
        "cluster_id": 512,
        "label": "EffectiveOperationMode",
        "type": "aenum OperationModeEnum"
      },
      "18": {
        "id": 18,
        "cluster_id": 512,
        "label": "EffectiveControlMode",
        "type": "aenum ControlModeEnum"
      },
      "19": {
        "id": 19,
        "cluster_id": 512,
        "label": "Capacity",
        "type": "Union[Nullable, int]"
      },
      "20": {
        "id": 20,
        "cluster_id": 512,
        "label": "Speed",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "21": {
        "id": 21,
        "cluster_id": 512,
        "label": "LifetimeRunningHours",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "22": {
        "id": 22,
        "cluster_id": 512,
        "label": "Power",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "23": {
        "id": 23,
        "cluster_id": 512,
        "label": "LifetimeEnergyConsumed",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "32": {
        "id": 32,
        "cluster_id": 512,
        "label": "OperationMode",
        "type": "aenum OperationModeEnum"
      },
      "33": {
        "id": 33,
        "cluster_id": 512,
        "label": "ControlMode",
        "type": "Optional[PumpConfigurationAndControl.Enums.ControlModeEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 512,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 512,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 512,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 512,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 512,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 512,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "513": {
    "id": 513,
    "label": "Thermostat",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 513,
        "label": "LocalTemperature",
        "type": "Union[Nullable, int]"
      },
      "1": {
        "id": 1,
        "cluster_id": 513,
        "label": "OutdoorTemperature",
        "type": "Union[NoneType, Nullable, int]"
      },
      "2": {
        "id": 2,
        "cluster_id": 513,
        "label": "Occupancy",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 513,
        "label": "AbsMinHeatSetpointLimit",
        "type": "Optional[int]"
      },
      "4": {
        "id": 4,
        "cluster_id": 513,
        "label": "AbsMaxHeatSetpointLimit",
        "type": "Optional[int]"
      },
      "5": {
        "id": 5,
        "cluster_id": 513,
        "label": "AbsMinCoolSetpointLimit",
        "type": "Optional[int]"
      },
      "6": {
        "id": 6,
        "cluster_id": 513,
        "label": "AbsMaxCoolSetpointLimit",
        "type": "Optional[int]"
      },
      "7": {
        "id": 7,
        "cluster_id": 513,
        "label": "PICoolingDemand",
        "type": "Optional[uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 513,
        "label": "PIHeatingDemand",
        "type": "Optional[uint]"
      },
      "9": {
        "id": 9,
        "cluster_id": 513,
        "label": "HVACSystemTypeConfiguration",
        "type": "Optional[uint]"
      },
      "16": {
        "id": 16,
        "cluster_id": 513,
        "label": "LocalTemperatureCalibration",
        "type": "Optional[int]"
      },
      "17": {
        "id": 17,
        "cluster_id": 513,
        "label": "OccupiedCoolingSetpoint",
        "type": "Optional[int]"
      },
      "18": {
        "id": 18,
        "cluster_id": 513,
        "label": "OccupiedHeatingSetpoint",
        "type": "Optional[int]"
      },
      "19": {
        "id": 19,
        "cluster_id": 513,
        "label": "UnoccupiedCoolingSetpoint",
        "type": "Optional[int]"
      },
      "20": {
        "id": 20,
        "cluster_id": 513,
        "label": "UnoccupiedHeatingSetpoint",
        "type": "Optional[int]"
      },
      "21": {
        "id": 21,
        "cluster_id": 513,
        "label": "MinHeatSetpointLimit",
        "type": "Optional[int]"
      },
      "22": {
        "id": 22,
        "cluster_id": 513,
        "label": "MaxHeatSetpointLimit",
        "type": "Optional[int]"
      },
      "23": {
        "id": 23,
        "cluster_id": 513,
        "label": "MinCoolSetpointLimit",
        "type": "Optional[int]"
      },
      "24": {
        "id": 24,
        "cluster_id": 513,
        "label": "MaxCoolSetpointLimit",
        "type": "Optional[int]"
      },
      "25": {
        "id": 25,
        "cluster_id": 513,
        "label": "MinSetpointDeadBand",
        "type": "Optional[int]"
      },
      "26": {
        "id": 26,
        "cluster_id": 513,
        "label": "RemoteSensing",
        "type": "Optional[uint]"
      },
      "27": {
        "id": 27,
        "cluster_id": 513,
        "label": "ControlSequenceOfOperation",
        "type": "aenum ControlSequenceOfOperationEnum"
      },
      "28": {
        "id": 28,
        "cluster_id": 513,
        "label": "SystemMode",
        "type": "aenum SystemModeEnum"
      },
      "30": {
        "id": 30,
        "cluster_id": 513,
        "label": "ThermostatRunningMode",
        "type": "Optional[Thermostat.Enums.ThermostatRunningModeEnum]"
      },
      "32": {
        "id": 32,
        "cluster_id": 513,
        "label": "StartOfWeek",
        "type": "Optional[Thermostat.Enums.StartOfWeekEnum]"
      },
      "33": {
        "id": 33,
        "cluster_id": 513,
        "label": "NumberOfWeeklyTransitions",
        "type": "Optional[uint]"
      },
      "34": {
        "id": 34,
        "cluster_id": 513,
        "label": "NumberOfDailyTransitions",
        "type": "Optional[uint]"
      },
      "35": {
        "id": 35,
        "cluster_id": 513,
        "label": "TemperatureSetpointHold",
        "type": "Optional[Thermostat.Enums.TemperatureSetpointHoldEnum]"
      },
      "36": {
        "id": 36,
        "cluster_id": 513,
        "label": "TemperatureSetpointHoldDuration",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "37": {
        "id": 37,
        "cluster_id": 513,
        "label": "ThermostatProgrammingOperationMode",
        "type": "Optional[uint]"
      },
      "41": {
        "id": 41,
        "cluster_id": 513,
        "label": "ThermostatRunningState",
        "type": "Optional[uint]"
      },
      "48": {
        "id": 48,
        "cluster_id": 513,
        "label": "SetpointChangeSource",
        "type": "Optional[Thermostat.Enums.SetpointChangeSourceEnum]"
      },
      "49": {
        "id": 49,
        "cluster_id": 513,
        "label": "SetpointChangeAmount",
        "type": "Union[NoneType, Nullable, int]"
      },
      "50": {
        "id": 50,
        "cluster_id": 513,
        "label": "SetpointChangeSourceTimestamp",
        "type": "Optional[uint]"
      },
      "52": {
        "id": 52,
        "cluster_id": 513,
        "label": "OccupiedSetback",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "53": {
        "id": 53,
        "cluster_id": 513,
        "label": "OccupiedSetbackMin",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "54": {
        "id": 54,
        "cluster_id": 513,
        "label": "OccupiedSetbackMax",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "55": {
        "id": 55,
        "cluster_id": 513,
        "label": "UnoccupiedSetback",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "56": {
        "id": 56,
        "cluster_id": 513,
        "label": "UnoccupiedSetbackMin",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "57": {
        "id": 57,
        "cluster_id": 513,
        "label": "UnoccupiedSetbackMax",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "58": {
        "id": 58,
        "cluster_id": 513,
        "label": "EmergencyHeatDelta",
        "type": "Optional[uint]"
      },
      "64": {
        "id": 64,
        "cluster_id": 513,
        "label": "ACType",
        "type": "Optional[Thermostat.Enums.ACTypeEnum]"
      },
      "65": {
        "id": 65,
        "cluster_id": 513,
        "label": "ACCapacity",
        "type": "Optional[uint]"
      },
      "66": {
        "id": 66,
        "cluster_id": 513,
        "label": "ACRefrigerantType",
        "type": "Optional[Thermostat.Enums.ACRefrigerantTypeEnum]"
      },
      "67": {
        "id": 67,
        "cluster_id": 513,
        "label": "ACCompressorType",
        "type": "Optional[Thermostat.Enums.ACCompressorTypeEnum]"
      },
      "68": {
        "id": 68,
        "cluster_id": 513,
        "label": "ACErrorCode",
        "type": "Optional[uint]"
      },
      "69": {
        "id": 69,
        "cluster_id": 513,
        "label": "ACLouverPosition",
        "type": "Optional[Thermostat.Enums.ACLouverPositionEnum]"
      },
      "70": {
        "id": 70,
        "cluster_id": 513,
        "label": "ACCoilTemperature",
        "type": "Union[NoneType, Nullable, int]"
      },
      "71": {
        "id": 71,
        "cluster_id": 513,
        "label": "ACCapacityformat",
        "type": "Optional[Thermostat.Enums.ACCapacityFormatEnum]"
      },
      "72": {
        "id": 72,
        "cluster_id": 513,
        "label": "PresetTypes",
        "type": "Optional[List[Thermostat.Structs.PresetTypeStruct]]"
      },
      "73": {
        "id": 73,
        "cluster_id": 513,
        "label": "ScheduleTypes",
        "type": "Optional[List[Thermostat.Structs.ScheduleTypeStruct]]"
      },
      "74": {
        "id": 74,
        "cluster_id": 513,
        "label": "NumberOfPresets",
        "type": "Optional[uint]"
      },
      "75": {
        "id": 75,
        "cluster_id": 513,
        "label": "NumberOfSchedules",
        "type": "Optional[uint]"
      },
      "76": {
        "id": 76,
        "cluster_id": 513,
        "label": "NumberOfScheduleTransitions",
        "type": "Optional[uint]"
      },
      "77": {
        "id": 77,
        "cluster_id": 513,
        "label": "NumberOfScheduleTransitionPerDay",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "78": {
        "id": 78,
        "cluster_id": 513,
        "label": "ActivePresetHandle",
        "type": "Union[NoneType, Nullable, bytes]"
      },
      "79": {
        "id": 79,
        "cluster_id": 513,
        "label": "ActiveScheduleHandle",
        "type": "Union[NoneType, Nullable, bytes]"
      },
      "80": {
        "id": 80,
        "cluster_id": 513,
        "label": "Presets",
        "type": "Optional[List[Thermostat.Structs.PresetStruct]]"
      },
      "81": {
        "id": 81,
        "cluster_id": 513,
        "label": "Schedules",
        "type": "Optional[List[Thermostat.Structs.ScheduleStruct]]"
      },
      "82": {
        "id": 82,
        "cluster_id": 513,
        "label": "PresetsSchedulesEditable",
        "type": "Optional[bool]"
      },
      "83": {
        "id": 83,
        "cluster_id": 513,
        "label": "TemperatureSetpointHoldPolicy",
        "type": "Optional[uint]"
      },
      "84": {
        "id": 84,
        "cluster_id": 513,
        "label": "SetpointHoldExpiryTimestamp",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "85": {
        "id": 85,
        "cluster_id": 513,
        "label": "QueuedPreset",
        "type": "Union[NoneType, Nullable, Thermostat.Structs.QueuedPresetStruct]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 513,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 513,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 513,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 513,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 513,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 513,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "514": {
    "id": 514,
    "label": "FanControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 514,
        "label": "FanMode",
        "type": "aenum FanModeEnum"
      },
      "1": {
        "id": 1,
        "cluster_id": 514,
        "label": "FanModeSequence",
        "type": "aenum FanModeSequenceEnum"
      },
      "2": {
        "id": 2,
        "cluster_id": 514,
        "label": "PercentSetting",
        "type": "Union[Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 514,
        "label": "PercentCurrent",
        "type": "uint"
      },
      "4": {
        "id": 4,
        "cluster_id": 514,
        "label": "SpeedMax",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 514,
        "label": "SpeedSetting",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 514,
        "label": "SpeedCurrent",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 514,
        "label": "RockSupport",
        "type": "Optional[uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 514,
        "label": "RockSetting",
        "type": "Optional[uint]"
      },
      "9": {
        "id": 9,
        "cluster_id": 514,
        "label": "WindSupport",
        "type": "Optional[uint]"
      },
      "10": {
        "id": 10,
        "cluster_id": 514,
        "label": "WindSetting",
        "type": "Optional[uint]"
      },
      "11": {
        "id": 11,
        "cluster_id": 514,
        "label": "AirflowDirection",
        "type": "Optional[FanControl.Enums.AirflowDirectionEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 514,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 514,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 514,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 514,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 514,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 514,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "516": {
    "id": 516,
    "label": "ThermostatUserInterfaceConfiguration",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 516,
        "label": "TemperatureDisplayMode",
        "type": "aenum TemperatureDisplayModeEnum"
      },
      "1": {
        "id": 1,
        "cluster_id": 516,
        "label": "KeypadLockout",
        "type": "aenum KeypadLockoutEnum"
      },
      "2": {
        "id": 2,
        "cluster_id": 516,
        "label": "ScheduleProgrammingVisibility",
        "type": "Optional[ThermostatUserInterfaceConfiguration.Enums.ScheduleProgrammingVisibilityEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 516,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 516,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 516,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 516,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 516,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 516,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "768": {
    "id": 768,
    "label": "ColorControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 768,
        "label": "CurrentHue",
        "type": "Optional[uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 768,
        "label": "CurrentSaturation",
        "type": "Optional[uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 768,
        "label": "RemainingTime",
        "type": "Optional[uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 768,
        "label": "CurrentX",
        "type": "Optional[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 768,
        "label": "CurrentY",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 768,
        "label": "DriftCompensation",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 768,
        "label": "CompensationText",
        "type": "Optional[str]"
      },
      "7": {
        "id": 7,
        "cluster_id": 768,
        "label": "ColorTemperatureMireds",
        "type": "Optional[uint]"
      },
      "8": {
        "id": 8,
        "cluster_id": 768,
        "label": "ColorMode",
        "type": "uint"
      },
      "15": {
        "id": 15,
        "cluster_id": 768,
        "label": "Options",
        "type": "uint"
      },
      "16": {
        "id": 16,
        "cluster_id": 768,
        "label": "NumberOfPrimaries",
        "type": "Union[Nullable, uint]"
      },
      "17": {
        "id": 17,
        "cluster_id": 768,
        "label": "Primary1X",
        "type": "Optional[uint]"
      },
      "18": {
        "id": 18,
        "cluster_id": 768,
        "label": "Primary1Y",
        "type": "Optional[uint]"
      },
      "19": {
        "id": 19,
        "cluster_id": 768,
        "label": "Primary1Intensity",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "21": {
        "id": 21,
        "cluster_id": 768,
        "label": "Primary2X",
        "type": "Optional[uint]"
      },
      "22": {
        "id": 22,
        "cluster_id": 768,
        "label": "Primary2Y",
        "type": "Optional[uint]"
      },
      "23": {
        "id": 23,
        "cluster_id": 768,
        "label": "Primary2Intensity",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "25": {
        "id": 25,
        "cluster_id": 768,
        "label": "Primary3X",
        "type": "Optional[uint]"
      },
      "26": {
        "id": 26,
        "cluster_id": 768,
        "label": "Primary3Y",
        "type": "Optional[uint]"
      },
      "27": {
        "id": 27,
        "cluster_id": 768,
        "label": "Primary3Intensity",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "32": {
        "id": 32,
        "cluster_id": 768,
        "label": "Primary4X",
        "type": "Optional[uint]"
      },
      "33": {
        "id": 33,
        "cluster_id": 768,
        "label": "Primary4Y",
        "type": "Optional[uint]"
      },
      "34": {
        "id": 34,
        "cluster_id": 768,
        "label": "Primary4Intensity",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "36": {
        "id": 36,
        "cluster_id": 768,
        "label": "Primary5X",
        "type": "Optional[uint]"
      },
      "37": {
        "id": 37,
        "cluster_id": 768,
        "label": "Primary5Y",
        "type": "Optional[uint]"
      },
      "38": {
        "id": 38,
        "cluster_id": 768,
        "label": "Primary5Intensity",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "40": {
        "id": 40,
        "cluster_id": 768,
        "label": "Primary6X",
        "type": "Optional[uint]"
      },
      "41": {
        "id": 41,
        "cluster_id": 768,
        "label": "Primary6Y",
        "type": "Optional[uint]"
      },
      "42": {
        "id": 42,
        "cluster_id": 768,
        "label": "Primary6Intensity",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "48": {
        "id": 48,
        "cluster_id": 768,
        "label": "WhitePointX",
        "type": "Optional[uint]"
      },
      "49": {
        "id": 49,
        "cluster_id": 768,
        "label": "WhitePointY",
        "type": "Optional[uint]"
      },
      "50": {
        "id": 50,
        "cluster_id": 768,
        "label": "ColorPointRX",
        "type": "Optional[uint]"
      },
      "51": {
        "id": 51,
        "cluster_id": 768,
        "label": "ColorPointRY",
        "type": "Optional[uint]"
      },
      "52": {
        "id": 52,
        "cluster_id": 768,
        "label": "ColorPointRIntensity",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "54": {
        "id": 54,
        "cluster_id": 768,
        "label": "ColorPointGX",
        "type": "Optional[uint]"
      },
      "55": {
        "id": 55,
        "cluster_id": 768,
        "label": "ColorPointGY",
        "type": "Optional[uint]"
      },
      "56": {
        "id": 56,
        "cluster_id": 768,
        "label": "ColorPointGIntensity",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "58": {
        "id": 58,
        "cluster_id": 768,
        "label": "ColorPointBX",
        "type": "Optional[uint]"
      },
      "59": {
        "id": 59,
        "cluster_id": 768,
        "label": "ColorPointBY",
        "type": "Optional[uint]"
      },
      "60": {
        "id": 60,
        "cluster_id": 768,
        "label": "ColorPointBIntensity",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "16384": {
        "id": 16384,
        "cluster_id": 768,
        "label": "EnhancedCurrentHue",
        "type": "Optional[uint]"
      },
      "16385": {
        "id": 16385,
        "cluster_id": 768,
        "label": "EnhancedColorMode",
        "type": "uint"
      },
      "16386": {
        "id": 16386,
        "cluster_id": 768,
        "label": "ColorLoopActive",
        "type": "Optional[uint]"
      },
      "16387": {
        "id": 16387,
        "cluster_id": 768,
        "label": "ColorLoopDirection",
        "type": "Optional[uint]"
      },
      "16388": {
        "id": 16388,
        "cluster_id": 768,
        "label": "ColorLoopTime",
        "type": "Optional[uint]"
      },
      "16389": {
        "id": 16389,
        "cluster_id": 768,
        "label": "ColorLoopStartEnhancedHue",
        "type": "Optional[uint]"
      },
      "16390": {
        "id": 16390,
        "cluster_id": 768,
        "label": "ColorLoopStoredEnhancedHue",
        "type": "Optional[uint]"
      },
      "16394": {
        "id": 16394,
        "cluster_id": 768,
        "label": "ColorCapabilities",
        "type": "uint"
      },
      "16395": {
        "id": 16395,
        "cluster_id": 768,
        "label": "ColorTempPhysicalMinMireds",
        "type": "Optional[uint]"
      },
      "16396": {
        "id": 16396,
        "cluster_id": 768,
        "label": "ColorTempPhysicalMaxMireds",
        "type": "Optional[uint]"
      },
      "16397": {
        "id": 16397,
        "cluster_id": 768,
        "label": "CoupleColorTempToLevelMinMireds",
        "type": "Optional[uint]"
      },
      "16400": {
        "id": 16400,
        "cluster_id": 768,
        "label": "StartUpColorTemperatureMireds",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 768,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 768,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 768,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 768,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 768,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 768,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "769": {
    "id": 769,
    "label": "BallastConfiguration",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 769,
        "label": "PhysicalMinLevel",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 769,
        "label": "PhysicalMaxLevel",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 769,
        "label": "BallastStatus",
        "type": "Optional[uint]"
      },
      "16": {
        "id": 16,
        "cluster_id": 769,
        "label": "MinLevel",
        "type": "uint"
      },
      "17": {
        "id": 17,
        "cluster_id": 769,
        "label": "MaxLevel",
        "type": "uint"
      },
      "20": {
        "id": 20,
        "cluster_id": 769,
        "label": "IntrinsicBallastFactor",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "21": {
        "id": 21,
        "cluster_id": 769,
        "label": "BallastFactorAdjustment",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "32": {
        "id": 32,
        "cluster_id": 769,
        "label": "LampQuantity",
        "type": "uint"
      },
      "48": {
        "id": 48,
        "cluster_id": 769,
        "label": "LampType",
        "type": "Optional[str]"
      },
      "49": {
        "id": 49,
        "cluster_id": 769,
        "label": "LampManufacturer",
        "type": "Optional[str]"
      },
      "50": {
        "id": 50,
        "cluster_id": 769,
        "label": "LampRatedHours",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "51": {
        "id": 51,
        "cluster_id": 769,
        "label": "LampBurnHours",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "52": {
        "id": 52,
        "cluster_id": 769,
        "label": "LampAlarmMode",
        "type": "Optional[uint]"
      },
      "53": {
        "id": 53,
        "cluster_id": 769,
        "label": "LampBurnHoursTripPoint",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 769,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 769,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 769,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 769,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 769,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 769,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1024": {
    "id": 1024,
    "label": "IlluminanceMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1024,
        "label": "MeasuredValue",
        "type": "Union[Nullable, uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1024,
        "label": "MinMeasuredValue",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1024,
        "label": "MaxMeasuredValue",
        "type": "Union[Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1024,
        "label": "Tolerance",
        "type": "Optional[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1024,
        "label": "LightSensorType",
        "type": "Union[NoneType, Nullable, IlluminanceMeasurement.Enums.LightSensorTypeEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1024,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1024,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1024,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1024,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1024,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1024,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1026": {
    "id": 1026,
    "label": "TemperatureMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1026,
        "label": "MeasuredValue",
        "type": "Union[Nullable, int]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1026,
        "label": "MinMeasuredValue",
        "type": "Union[Nullable, int]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1026,
        "label": "MaxMeasuredValue",
        "type": "Union[Nullable, int]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1026,
        "label": "Tolerance",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1026,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1026,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1026,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1026,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1026,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1026,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1027": {
    "id": 1027,
    "label": "PressureMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1027,
        "label": "MeasuredValue",
        "type": "Union[Nullable, int]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1027,
        "label": "MinMeasuredValue",
        "type": "Union[Nullable, int]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1027,
        "label": "MaxMeasuredValue",
        "type": "Union[Nullable, int]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1027,
        "label": "Tolerance",
        "type": "Optional[uint]"
      },
      "16": {
        "id": 16,
        "cluster_id": 1027,
        "label": "ScaledValue",
        "type": "Union[NoneType, Nullable, int]"
      },
      "17": {
        "id": 17,
        "cluster_id": 1027,
        "label": "MinScaledValue",
        "type": "Union[NoneType, Nullable, int]"
      },
      "18": {
        "id": 18,
        "cluster_id": 1027,
        "label": "MaxScaledValue",
        "type": "Union[NoneType, Nullable, int]"
      },
      "19": {
        "id": 19,
        "cluster_id": 1027,
        "label": "ScaledTolerance",
        "type": "Optional[uint]"
      },
      "20": {
        "id": 20,
        "cluster_id": 1027,
        "label": "Scale",
        "type": "Optional[int]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1027,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1027,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1027,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1027,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1027,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1027,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1028": {
    "id": 1028,
    "label": "FlowMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1028,
        "label": "MeasuredValue",
        "type": "Union[Nullable, uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1028,
        "label": "MinMeasuredValue",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1028,
        "label": "MaxMeasuredValue",
        "type": "Union[Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1028,
        "label": "Tolerance",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1028,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1028,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1028,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1028,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1028,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1028,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1029": {
    "id": 1029,
    "label": "RelativeHumidityMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1029,
        "label": "MeasuredValue",
        "type": "Union[Nullable, uint]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1029,
        "label": "MinMeasuredValue",
        "type": "Union[Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1029,
        "label": "MaxMeasuredValue",
        "type": "Union[Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1029,
        "label": "Tolerance",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1029,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1029,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1029,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1029,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1029,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1029,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1030": {
    "id": 1030,
    "label": "OccupancySensing",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1030,
        "label": "Occupancy",
        "type": "uint"
      },
      "1": {
        "id": 1,
        "cluster_id": 1030,
        "label": "OccupancySensorType",
        "type": "aenum OccupancySensorTypeEnum"
      },
      "2": {
        "id": 2,
        "cluster_id": 1030,
        "label": "OccupancySensorTypeBitmap",
        "type": "uint"
      },
      "16": {
        "id": 16,
        "cluster_id": 1030,
        "label": "PIROccupiedToUnoccupiedDelay",
        "type": "Optional[uint]"
      },
      "17": {
        "id": 17,
        "cluster_id": 1030,
        "label": "PIRUnoccupiedToOccupiedDelay",
        "type": "Optional[uint]"
      },
      "18": {
        "id": 18,
        "cluster_id": 1030,
        "label": "PIRUnoccupiedToOccupiedThreshold",
        "type": "Optional[uint]"
      },
      "32": {
        "id": 32,
        "cluster_id": 1030,
        "label": "UltrasonicOccupiedToUnoccupiedDelay",
        "type": "Optional[uint]"
      },
      "33": {
        "id": 33,
        "cluster_id": 1030,
        "label": "UltrasonicUnoccupiedToOccupiedDelay",
        "type": "Optional[uint]"
      },
      "34": {
        "id": 34,
        "cluster_id": 1030,
        "label": "UltrasonicUnoccupiedToOccupiedThreshold",
        "type": "Optional[uint]"
      },
      "48": {
        "id": 48,
        "cluster_id": 1030,
        "label": "PhysicalContactOccupiedToUnoccupiedDelay",
        "type": "Optional[uint]"
      },
      "49": {
        "id": 49,
        "cluster_id": 1030,
        "label": "PhysicalContactUnoccupiedToOccupiedDelay",
        "type": "Optional[uint]"
      },
      "50": {
        "id": 50,
        "cluster_id": 1030,
        "label": "PhysicalContactUnoccupiedToOccupiedThreshold",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1030,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1030,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1030,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1030,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1030,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1030,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1036": {
    "id": 1036,
    "label": "CarbonMonoxideConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1036,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1036,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1036,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1036,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1036,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1036,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1036,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1036,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1036,
        "label": "MeasurementUnit",
        "type": "Optional[CarbonMonoxideConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1036,
        "label": "MeasurementMedium",
        "type": "Optional[CarbonMonoxideConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1036,
        "label": "LevelValue",
        "type": "Optional[CarbonMonoxideConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1036,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1036,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1036,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1036,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1036,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1036,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1037": {
    "id": 1037,
    "label": "CarbonDioxideConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1037,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1037,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1037,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1037,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1037,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1037,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1037,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1037,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1037,
        "label": "MeasurementUnit",
        "type": "Optional[CarbonDioxideConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1037,
        "label": "MeasurementMedium",
        "type": "Optional[CarbonDioxideConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1037,
        "label": "LevelValue",
        "type": "Optional[CarbonDioxideConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1037,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1037,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1037,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1037,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1037,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1037,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1043": {
    "id": 1043,
    "label": "NitrogenDioxideConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1043,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1043,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1043,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1043,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1043,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1043,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1043,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1043,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1043,
        "label": "MeasurementUnit",
        "type": "Optional[NitrogenDioxideConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1043,
        "label": "MeasurementMedium",
        "type": "Optional[NitrogenDioxideConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1043,
        "label": "LevelValue",
        "type": "Optional[NitrogenDioxideConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1043,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1043,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1043,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1043,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1043,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1043,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1045": {
    "id": 1045,
    "label": "OzoneConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1045,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1045,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1045,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1045,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1045,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1045,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1045,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1045,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1045,
        "label": "MeasurementUnit",
        "type": "Optional[OzoneConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1045,
        "label": "MeasurementMedium",
        "type": "Optional[OzoneConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1045,
        "label": "LevelValue",
        "type": "Optional[OzoneConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1045,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1045,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1045,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1045,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1045,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1045,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1066": {
    "id": 1066,
    "label": "Pm25ConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1066,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1066,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1066,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1066,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1066,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1066,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1066,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1066,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1066,
        "label": "MeasurementUnit",
        "type": "Optional[Pm25ConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1066,
        "label": "MeasurementMedium",
        "type": "Optional[Pm25ConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1066,
        "label": "LevelValue",
        "type": "Optional[Pm25ConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1066,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1066,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1066,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1066,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1066,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1066,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1067": {
    "id": 1067,
    "label": "FormaldehydeConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1067,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1067,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1067,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1067,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1067,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1067,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1067,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1067,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1067,
        "label": "MeasurementUnit",
        "type": "Optional[FormaldehydeConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1067,
        "label": "MeasurementMedium",
        "type": "Optional[FormaldehydeConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1067,
        "label": "LevelValue",
        "type": "Optional[FormaldehydeConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1067,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1067,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1067,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1067,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1067,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1067,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1068": {
    "id": 1068,
    "label": "Pm1ConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1068,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1068,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1068,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1068,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1068,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1068,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1068,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1068,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1068,
        "label": "MeasurementUnit",
        "type": "Optional[Pm1ConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1068,
        "label": "MeasurementMedium",
        "type": "Optional[Pm1ConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1068,
        "label": "LevelValue",
        "type": "Optional[Pm1ConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1068,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1068,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1068,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1068,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1068,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1068,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1069": {
    "id": 1069,
    "label": "Pm10ConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1069,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1069,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1069,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1069,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1069,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1069,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1069,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1069,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1069,
        "label": "MeasurementUnit",
        "type": "Optional[Pm10ConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1069,
        "label": "MeasurementMedium",
        "type": "Optional[Pm10ConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1069,
        "label": "LevelValue",
        "type": "Optional[Pm10ConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1069,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1069,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1069,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1069,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1069,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1069,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1070": {
    "id": 1070,
    "label": "TotalVolatileOrganicCompoundsConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1070,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1070,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1070,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1070,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1070,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1070,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1070,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1070,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1070,
        "label": "MeasurementUnit",
        "type": "Optional[TotalVolatileOrganicCompoundsConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1070,
        "label": "MeasurementMedium",
        "type": "Optional[TotalVolatileOrganicCompoundsConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1070,
        "label": "LevelValue",
        "type": "Optional[TotalVolatileOrganicCompoundsConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1070,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1070,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1070,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1070,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1070,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1070,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1071": {
    "id": 1071,
    "label": "RadonConcentrationMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1071,
        "label": "MeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1071,
        "label": "MinMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1071,
        "label": "MaxMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1071,
        "label": "PeakMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1071,
        "label": "PeakMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1071,
        "label": "AverageMeasuredValue",
        "type": "Union[NoneType, Nullable, float32]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1071,
        "label": "AverageMeasuredValueWindow",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1071,
        "label": "Uncertainty",
        "type": "Optional[float32]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1071,
        "label": "MeasurementUnit",
        "type": "Optional[RadonConcentrationMeasurement.Enums.MeasurementUnitEnum]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1071,
        "label": "MeasurementMedium",
        "type": "Optional[RadonConcentrationMeasurement.Enums.MeasurementMediumEnum]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1071,
        "label": "LevelValue",
        "type": "Optional[RadonConcentrationMeasurement.Enums.LevelValueEnum]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1071,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1071,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1071,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1071,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1071,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1071,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1283": {
    "id": 1283,
    "label": "WakeOnLan",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1283,
        "label": "MACAddress",
        "type": "Optional[str]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1283,
        "label": "LinkLocalAddress",
        "type": "Optional[bytes]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1283,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1283,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1283,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1283,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1283,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1283,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1284": {
    "id": 1284,
    "label": "Channel",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1284,
        "label": "ChannelList",
        "type": "Optional[List[Channel.Structs.ChannelInfoStruct]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1284,
        "label": "Lineup",
        "type": "Union[NoneType, Nullable, Channel.Structs.LineupInfoStruct]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1284,
        "label": "CurrentChannel",
        "type": "Union[NoneType, Nullable, Channel.Structs.ChannelInfoStruct]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1284,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1284,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1284,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1284,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1284,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1284,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1285": {
    "id": 1285,
    "label": "TargetNavigator",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1285,
        "label": "TargetList",
        "type": "List[TargetNavigator.Structs.TargetInfoStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1285,
        "label": "CurrentTarget",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1285,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1285,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1285,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1285,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1285,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1285,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1286": {
    "id": 1286,
    "label": "MediaPlayback",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1286,
        "label": "CurrentState",
        "type": "aenum PlaybackStateEnum"
      },
      "1": {
        "id": 1,
        "cluster_id": 1286,
        "label": "StartTime",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1286,
        "label": "Duration",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1286,
        "label": "SampledPosition",
        "type": "Union[NoneType, Nullable, MediaPlayback.Structs.PlaybackPositionStruct]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1286,
        "label": "PlaybackSpeed",
        "type": "Optional[float32]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1286,
        "label": "SeekRangeEnd",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1286,
        "label": "SeekRangeStart",
        "type": "Union[NoneType, Nullable, uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1286,
        "label": "ActiveAudioTrack",
        "type": "Union[NoneType, Nullable, MediaPlayback.Structs.TrackStruct]"
      },
      "8": {
        "id": 8,
        "cluster_id": 1286,
        "label": "AvailableAudioTracks",
        "type": "Union[NoneType, Nullable, List[MediaPlayback.Structs.TrackStruct]]"
      },
      "9": {
        "id": 9,
        "cluster_id": 1286,
        "label": "ActiveTextTrack",
        "type": "Union[NoneType, Nullable, MediaPlayback.Structs.TrackStruct]"
      },
      "10": {
        "id": 10,
        "cluster_id": 1286,
        "label": "AvailableTextTracks",
        "type": "Union[NoneType, Nullable, List[MediaPlayback.Structs.TrackStruct]]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1286,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1286,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1286,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1286,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1286,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1286,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1287": {
    "id": 1287,
    "label": "MediaInput",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1287,
        "label": "InputList",
        "type": "List[MediaInput.Structs.InputInfoStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1287,
        "label": "CurrentInput",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1287,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1287,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1287,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1287,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1287,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1287,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1288": {
    "id": 1288,
    "label": "LowPower",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 1288,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1288,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1288,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1288,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1288,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1288,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1289": {
    "id": 1289,
    "label": "KeypadInput",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 1289,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1289,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1289,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1289,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1289,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1289,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1290": {
    "id": 1290,
    "label": "ContentLauncher",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1290,
        "label": "AcceptHeader",
        "type": "Optional[List[str]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1290,
        "label": "SupportedStreamingProtocols",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1290,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1290,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1290,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1290,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1290,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1290,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1291": {
    "id": 1291,
    "label": "AudioOutput",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1291,
        "label": "OutputList",
        "type": "List[AudioOutput.Structs.OutputInfoStruct]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1291,
        "label": "CurrentOutput",
        "type": "uint"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1291,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1291,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1291,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1291,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1291,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1291,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1292": {
    "id": 1292,
    "label": "ApplicationLauncher",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1292,
        "label": "CatalogList",
        "type": "Optional[List[uint]]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1292,
        "label": "CurrentApp",
        "type": "Union[NoneType, Nullable, ApplicationLauncher.Structs.ApplicationEPStruct]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1292,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1292,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1292,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1292,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1292,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1292,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1293": {
    "id": 1293,
    "label": "ApplicationBasic",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1293,
        "label": "VendorName",
        "type": "Optional[str]"
      },
      "1": {
        "id": 1,
        "cluster_id": 1293,
        "label": "VendorID",
        "type": "Optional[uint]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1293,
        "label": "ApplicationName",
        "type": "str"
      },
      "3": {
        "id": 3,
        "cluster_id": 1293,
        "label": "ProductID",
        "type": "Optional[uint]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1293,
        "label": "Application",
        "type": "ApplicationBasic.Structs.ApplicationStruct"
      },
      "5": {
        "id": 5,
        "cluster_id": 1293,
        "label": "Status",
        "type": "aenum ApplicationStatusEnum"
      },
      "6": {
        "id": 6,
        "cluster_id": 1293,
        "label": "ApplicationVersion",
        "type": "str"
      },
      "7": {
        "id": 7,
        "cluster_id": 1293,
        "label": "AllowedVendorList",
        "type": "List[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1293,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1293,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1293,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1293,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1293,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1293,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1294": {
    "id": 1294,
    "label": "AccountLogin",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 1294,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1294,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1294,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1294,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1294,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1294,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1295": {
    "id": 1295,
    "label": "ContentControl",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 1295,
        "label": "Enabled",
        "type": "bool"
      },
      "1": {
        "id": 1,
        "cluster_id": 1295,
        "label": "OnDemandRatings",
        "type": "Optional[List[ContentControl.Structs.RatingNameStruct]]"
      },
      "2": {
        "id": 2,
        "cluster_id": 1295,
        "label": "OnDemandRatingThreshold",
        "type": "Optional[str]"
      },
      "3": {
        "id": 3,
        "cluster_id": 1295,
        "label": "ScheduledContentRatings",
        "type": "Optional[List[ContentControl.Structs.RatingNameStruct]]"
      },
      "4": {
        "id": 4,
        "cluster_id": 1295,
        "label": "ScheduledContentRatingThreshold",
        "type": "Optional[str]"
      },
      "5": {
        "id": 5,
        "cluster_id": 1295,
        "label": "ScreenDailyTime",
        "type": "Optional[uint]"
      },
      "6": {
        "id": 6,
        "cluster_id": 1295,
        "label": "RemainingScreenTime",
        "type": "Optional[uint]"
      },
      "7": {
        "id": 7,
        "cluster_id": 1295,
        "label": "BlockUnrated",
        "type": "bool"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 1295,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1295,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1295,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1295,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1295,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1295,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "1296": {
    "id": 1296,
    "label": "ContentAppObserver",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 1296,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 1296,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 1296,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 1296,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 1296,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 1296,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "2820": {
    "id": 2820,
    "label": "ElectricalMeasurement",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 2820,
        "label": "MeasurementType",
        "type": "Optional[uint]"
      },
      "256": {
        "id": 256,
        "cluster_id": 2820,
        "label": "DcVoltage",
        "type": "Optional[int]"
      },
      "257": {
        "id": 257,
        "cluster_id": 2820,
        "label": "DcVoltageMin",
        "type": "Optional[int]"
      },
      "258": {
        "id": 258,
        "cluster_id": 2820,
        "label": "DcVoltageMax",
        "type": "Optional[int]"
      },
      "259": {
        "id": 259,
        "cluster_id": 2820,
        "label": "DcCurrent",
        "type": "Optional[int]"
      },
      "260": {
        "id": 260,
        "cluster_id": 2820,
        "label": "DcCurrentMin",
        "type": "Optional[int]"
      },
      "261": {
        "id": 261,
        "cluster_id": 2820,
        "label": "DcCurrentMax",
        "type": "Optional[int]"
      },
      "262": {
        "id": 262,
        "cluster_id": 2820,
        "label": "DcPower",
        "type": "Optional[int]"
      },
      "263": {
        "id": 263,
        "cluster_id": 2820,
        "label": "DcPowerMin",
        "type": "Optional[int]"
      },
      "264": {
        "id": 264,
        "cluster_id": 2820,
        "label": "DcPowerMax",
        "type": "Optional[int]"
      },
      "512": {
        "id": 512,
        "cluster_id": 2820,
        "label": "DcVoltageMultiplier",
        "type": "Optional[uint]"
      },
      "513": {
        "id": 513,
        "cluster_id": 2820,
        "label": "DcVoltageDivisor",
        "type": "Optional[uint]"
      },
      "514": {
        "id": 514,
        "cluster_id": 2820,
        "label": "DcCurrentMultiplier",
        "type": "Optional[uint]"
      },
      "515": {
        "id": 515,
        "cluster_id": 2820,
        "label": "DcCurrentDivisor",
        "type": "Optional[uint]"
      },
      "516": {
        "id": 516,
        "cluster_id": 2820,
        "label": "DcPowerMultiplier",
        "type": "Optional[uint]"
      },
      "517": {
        "id": 517,
        "cluster_id": 2820,
        "label": "DcPowerDivisor",
        "type": "Optional[uint]"
      },
      "768": {
        "id": 768,
        "cluster_id": 2820,
        "label": "AcFrequency",
        "type": "Optional[uint]"
      },
      "769": {
        "id": 769,
        "cluster_id": 2820,
        "label": "AcFrequencyMin",
        "type": "Optional[uint]"
      },
      "770": {
        "id": 770,
        "cluster_id": 2820,
        "label": "AcFrequencyMax",
        "type": "Optional[uint]"
      },
      "771": {
        "id": 771,
        "cluster_id": 2820,
        "label": "NeutralCurrent",
        "type": "Optional[uint]"
      },
      "772": {
        "id": 772,
        "cluster_id": 2820,
        "label": "TotalActivePower",
        "type": "Optional[int]"
      },
      "773": {
        "id": 773,
        "cluster_id": 2820,
        "label": "TotalReactivePower",
        "type": "Optional[int]"
      },
      "774": {
        "id": 774,
        "cluster_id": 2820,
        "label": "TotalApparentPower",
        "type": "Optional[uint]"
      },
      "775": {
        "id": 775,
        "cluster_id": 2820,
        "label": "Measured1stHarmonicCurrent",
        "type": "Optional[int]"
      },
      "776": {
        "id": 776,
        "cluster_id": 2820,
        "label": "Measured3rdHarmonicCurrent",
        "type": "Optional[int]"
      },
      "777": {
        "id": 777,
        "cluster_id": 2820,
        "label": "Measured5thHarmonicCurrent",
        "type": "Optional[int]"
      },
      "778": {
        "id": 778,
        "cluster_id": 2820,
        "label": "Measured7thHarmonicCurrent",
        "type": "Optional[int]"
      },
      "779": {
        "id": 779,
        "cluster_id": 2820,
        "label": "Measured9thHarmonicCurrent",
        "type": "Optional[int]"
      },
      "780": {
        "id": 780,
        "cluster_id": 2820,
        "label": "Measured11thHarmonicCurrent",
        "type": "Optional[int]"
      },
      "781": {
        "id": 781,
        "cluster_id": 2820,
        "label": "MeasuredPhase1stHarmonicCurrent",
        "type": "Optional[int]"
      },
      "782": {
        "id": 782,
        "cluster_id": 2820,
        "label": "MeasuredPhase3rdHarmonicCurrent",
        "type": "Optional[int]"
      },
      "783": {
        "id": 783,
        "cluster_id": 2820,
        "label": "MeasuredPhase5thHarmonicCurrent",
        "type": "Optional[int]"
      },
      "784": {
        "id": 784,
        "cluster_id": 2820,
        "label": "MeasuredPhase7thHarmonicCurrent",
        "type": "Optional[int]"
      },
      "785": {
        "id": 785,
        "cluster_id": 2820,
        "label": "MeasuredPhase9thHarmonicCurrent",
        "type": "Optional[int]"
      },
      "786": {
        "id": 786,
        "cluster_id": 2820,
        "label": "MeasuredPhase11thHarmonicCurrent",
        "type": "Optional[int]"
      },
      "1024": {
        "id": 1024,
        "cluster_id": 2820,
        "label": "AcFrequencyMultiplier",
        "type": "Optional[uint]"
      },
      "1025": {
        "id": 1025,
        "cluster_id": 2820,
        "label": "AcFrequencyDivisor",
        "type": "Optional[uint]"
      },
      "1026": {
        "id": 1026,
        "cluster_id": 2820,
        "label": "PowerMultiplier",
        "type": "Optional[uint]"
      },
      "1027": {
        "id": 1027,
        "cluster_id": 2820,
        "label": "PowerDivisor",
        "type": "Optional[uint]"
      },
      "1028": {
        "id": 1028,
        "cluster_id": 2820,
        "label": "HarmonicCurrentMultiplier",
        "type": "Optional[int]"
      },
      "1029": {
        "id": 1029,
        "cluster_id": 2820,
        "label": "PhaseHarmonicCurrentMultiplier",
        "type": "Optional[int]"
      },
      "1280": {
        "id": 1280,
        "cluster_id": 2820,
        "label": "InstantaneousVoltage",
        "type": "Optional[int]"
      },
      "1281": {
        "id": 1281,
        "cluster_id": 2820,
        "label": "InstantaneousLineCurrent",
        "type": "Optional[uint]"
      },
      "1282": {
        "id": 1282,
        "cluster_id": 2820,
        "label": "InstantaneousActiveCurrent",
        "type": "Optional[int]"
      },
      "1283": {
        "id": 1283,
        "cluster_id": 2820,
        "label": "InstantaneousReactiveCurrent",
        "type": "Optional[int]"
      },
      "1284": {
        "id": 1284,
        "cluster_id": 2820,
        "label": "InstantaneousPower",
        "type": "Optional[int]"
      },
      "1285": {
        "id": 1285,
        "cluster_id": 2820,
        "label": "RmsVoltage",
        "type": "Optional[uint]"
      },
      "1286": {
        "id": 1286,
        "cluster_id": 2820,
        "label": "RmsVoltageMin",
        "type": "Optional[uint]"
      },
      "1287": {
        "id": 1287,
        "cluster_id": 2820,
        "label": "RmsVoltageMax",
        "type": "Optional[uint]"
      },
      "1288": {
        "id": 1288,
        "cluster_id": 2820,
        "label": "RmsCurrent",
        "type": "Optional[uint]"
      },
      "1289": {
        "id": 1289,
        "cluster_id": 2820,
        "label": "RmsCurrentMin",
        "type": "Optional[uint]"
      },
      "1290": {
        "id": 1290,
        "cluster_id": 2820,
        "label": "RmsCurrentMax",
        "type": "Optional[uint]"
      },
      "1291": {
        "id": 1291,
        "cluster_id": 2820,
        "label": "ActivePower",
        "type": "Optional[int]"
      },
      "1292": {
        "id": 1292,
        "cluster_id": 2820,
        "label": "ActivePowerMin",
        "type": "Optional[int]"
      },
      "1293": {
        "id": 1293,
        "cluster_id": 2820,
        "label": "ActivePowerMax",
        "type": "Optional[int]"
      },
      "1294": {
        "id": 1294,
        "cluster_id": 2820,
        "label": "ReactivePower",
        "type": "Optional[int]"
      },
      "1295": {
        "id": 1295,
        "cluster_id": 2820,
        "label": "ApparentPower",
        "type": "Optional[uint]"
      },
      "1296": {
        "id": 1296,
        "cluster_id": 2820,
        "label": "PowerFactor",
        "type": "Optional[int]"
      },
      "1297": {
        "id": 1297,
        "cluster_id": 2820,
        "label": "AverageRmsVoltageMeasurementPeriod",
        "type": "Optional[uint]"
      },
      "1299": {
        "id": 1299,
        "cluster_id": 2820,
        "label": "AverageRmsUnderVoltageCounter",
        "type": "Optional[uint]"
      },
      "1300": {
        "id": 1300,
        "cluster_id": 2820,
        "label": "RmsExtremeOverVoltagePeriod",
        "type": "Optional[uint]"
      },
      "1301": {
        "id": 1301,
        "cluster_id": 2820,
        "label": "RmsExtremeUnderVoltagePeriod",
        "type": "Optional[uint]"
      },
      "1302": {
        "id": 1302,
        "cluster_id": 2820,
        "label": "RmsVoltageSagPeriod",
        "type": "Optional[uint]"
      },
      "1303": {
        "id": 1303,
        "cluster_id": 2820,
        "label": "RmsVoltageSwellPeriod",
        "type": "Optional[uint]"
      },
      "1536": {
        "id": 1536,
        "cluster_id": 2820,
        "label": "AcVoltageMultiplier",
        "type": "Optional[uint]"
      },
      "1537": {
        "id": 1537,
        "cluster_id": 2820,
        "label": "AcVoltageDivisor",
        "type": "Optional[uint]"
      },
      "1538": {
        "id": 1538,
        "cluster_id": 2820,
        "label": "AcCurrentMultiplier",
        "type": "Optional[uint]"
      },
      "1539": {
        "id": 1539,
        "cluster_id": 2820,
        "label": "AcCurrentDivisor",
        "type": "Optional[uint]"
      },
      "1540": {
        "id": 1540,
        "cluster_id": 2820,
        "label": "AcPowerMultiplier",
        "type": "Optional[uint]"
      },
      "1541": {
        "id": 1541,
        "cluster_id": 2820,
        "label": "AcPowerDivisor",
        "type": "Optional[uint]"
      },
      "1792": {
        "id": 1792,
        "cluster_id": 2820,
        "label": "OverloadAlarmsMask",
        "type": "Optional[uint]"
      },
      "1793": {
        "id": 1793,
        "cluster_id": 2820,
        "label": "VoltageOverload",
        "type": "Optional[int]"
      },
      "1794": {
        "id": 1794,
        "cluster_id": 2820,
        "label": "CurrentOverload",
        "type": "Optional[int]"
      },
      "2048": {
        "id": 2048,
        "cluster_id": 2820,
        "label": "AcOverloadAlarmsMask",
        "type": "Optional[uint]"
      },
      "2049": {
        "id": 2049,
        "cluster_id": 2820,
        "label": "AcVoltageOverload",
        "type": "Optional[int]"
      },
      "2050": {
        "id": 2050,
        "cluster_id": 2820,
        "label": "AcCurrentOverload",
        "type": "Optional[int]"
      },
      "2051": {
        "id": 2051,
        "cluster_id": 2820,
        "label": "AcActivePowerOverload",
        "type": "Optional[int]"
      },
      "2052": {
        "id": 2052,
        "cluster_id": 2820,
        "label": "AcReactivePowerOverload",
        "type": "Optional[int]"
      },
      "2053": {
        "id": 2053,
        "cluster_id": 2820,
        "label": "AverageRmsOverVoltage",
        "type": "Optional[int]"
      },
      "2054": {
        "id": 2054,
        "cluster_id": 2820,
        "label": "AverageRmsUnderVoltage",
        "type": "Optional[int]"
      },
      "2055": {
        "id": 2055,
        "cluster_id": 2820,
        "label": "RmsExtremeOverVoltage",
        "type": "Optional[int]"
      },
      "2056": {
        "id": 2056,
        "cluster_id": 2820,
        "label": "RmsExtremeUnderVoltage",
        "type": "Optional[int]"
      },
      "2057": {
        "id": 2057,
        "cluster_id": 2820,
        "label": "RmsVoltageSag",
        "type": "Optional[int]"
      },
      "2058": {
        "id": 2058,
        "cluster_id": 2820,
        "label": "RmsVoltageSwell",
        "type": "Optional[int]"
      },
      "2305": {
        "id": 2305,
        "cluster_id": 2820,
        "label": "LineCurrentPhaseB",
        "type": "Optional[uint]"
      },
      "2306": {
        "id": 2306,
        "cluster_id": 2820,
        "label": "ActiveCurrentPhaseB",
        "type": "Optional[int]"
      },
      "2307": {
        "id": 2307,
        "cluster_id": 2820,
        "label": "ReactiveCurrentPhaseB",
        "type": "Optional[int]"
      },
      "2309": {
        "id": 2309,
        "cluster_id": 2820,
        "label": "RmsVoltagePhaseB",
        "type": "Optional[uint]"
      },
      "2310": {
        "id": 2310,
        "cluster_id": 2820,
        "label": "RmsVoltageMinPhaseB",
        "type": "Optional[uint]"
      },
      "2311": {
        "id": 2311,
        "cluster_id": 2820,
        "label": "RmsVoltageMaxPhaseB",
        "type": "Optional[uint]"
      },
      "2312": {
        "id": 2312,
        "cluster_id": 2820,
        "label": "RmsCurrentPhaseB",
        "type": "Optional[uint]"
      },
      "2313": {
        "id": 2313,
        "cluster_id": 2820,
        "label": "RmsCurrentMinPhaseB",
        "type": "Optional[uint]"
      },
      "2314": {
        "id": 2314,
        "cluster_id": 2820,
        "label": "RmsCurrentMaxPhaseB",
        "type": "Optional[uint]"
      },
      "2315": {
        "id": 2315,
        "cluster_id": 2820,
        "label": "ActivePowerPhaseB",
        "type": "Optional[int]"
      },
      "2316": {
        "id": 2316,
        "cluster_id": 2820,
        "label": "ActivePowerMinPhaseB",
        "type": "Optional[int]"
      },
      "2317": {
        "id": 2317,
        "cluster_id": 2820,
        "label": "ActivePowerMaxPhaseB",
        "type": "Optional[int]"
      },
      "2318": {
        "id": 2318,
        "cluster_id": 2820,
        "label": "ReactivePowerPhaseB",
        "type": "Optional[int]"
      },
      "2319": {
        "id": 2319,
        "cluster_id": 2820,
        "label": "ApparentPowerPhaseB",
        "type": "Optional[uint]"
      },
      "2320": {
        "id": 2320,
        "cluster_id": 2820,
        "label": "PowerFactorPhaseB",
        "type": "Optional[int]"
      },
      "2321": {
        "id": 2321,
        "cluster_id": 2820,
        "label": "AverageRmsVoltageMeasurementPeriodPhaseB",
        "type": "Optional[uint]"
      },
      "2322": {
        "id": 2322,
        "cluster_id": 2820,
        "label": "AverageRmsOverVoltageCounterPhaseB",
        "type": "Optional[uint]"
      },
      "2323": {
        "id": 2323,
        "cluster_id": 2820,
        "label": "AverageRmsUnderVoltageCounterPhaseB",
        "type": "Optional[uint]"
      },
      "2324": {
        "id": 2324,
        "cluster_id": 2820,
        "label": "RmsExtremeOverVoltagePeriodPhaseB",
        "type": "Optional[uint]"
      },
      "2325": {
        "id": 2325,
        "cluster_id": 2820,
        "label": "RmsExtremeUnderVoltagePeriodPhaseB",
        "type": "Optional[uint]"
      },
      "2326": {
        "id": 2326,
        "cluster_id": 2820,
        "label": "RmsVoltageSagPeriodPhaseB",
        "type": "Optional[uint]"
      },
      "2327": {
        "id": 2327,
        "cluster_id": 2820,
        "label": "RmsVoltageSwellPeriodPhaseB",
        "type": "Optional[uint]"
      },
      "2561": {
        "id": 2561,
        "cluster_id": 2820,
        "label": "LineCurrentPhaseC",
        "type": "Optional[uint]"
      },
      "2562": {
        "id": 2562,
        "cluster_id": 2820,
        "label": "ActiveCurrentPhaseC",
        "type": "Optional[int]"
      },
      "2563": {
        "id": 2563,
        "cluster_id": 2820,
        "label": "ReactiveCurrentPhaseC",
        "type": "Optional[int]"
      },
      "2565": {
        "id": 2565,
        "cluster_id": 2820,
        "label": "RmsVoltagePhaseC",
        "type": "Optional[uint]"
      },
      "2566": {
        "id": 2566,
        "cluster_id": 2820,
        "label": "RmsVoltageMinPhaseC",
        "type": "Optional[uint]"
      },
      "2567": {
        "id": 2567,
        "cluster_id": 2820,
        "label": "RmsVoltageMaxPhaseC",
        "type": "Optional[uint]"
      },
      "2568": {
        "id": 2568,
        "cluster_id": 2820,
        "label": "RmsCurrentPhaseC",
        "type": "Optional[uint]"
      },
      "2569": {
        "id": 2569,
        "cluster_id": 2820,
        "label": "RmsCurrentMinPhaseC",
        "type": "Optional[uint]"
      },
      "2570": {
        "id": 2570,
        "cluster_id": 2820,
        "label": "RmsCurrentMaxPhaseC",
        "type": "Optional[uint]"
      },
      "2571": {
        "id": 2571,
        "cluster_id": 2820,
        "label": "ActivePowerPhaseC",
        "type": "Optional[int]"
      },
      "2572": {
        "id": 2572,
        "cluster_id": 2820,
        "label": "ActivePowerMinPhaseC",
        "type": "Optional[int]"
      },
      "2573": {
        "id": 2573,
        "cluster_id": 2820,
        "label": "ActivePowerMaxPhaseC",
        "type": "Optional[int]"
      },
      "2574": {
        "id": 2574,
        "cluster_id": 2820,
        "label": "ReactivePowerPhaseC",
        "type": "Optional[int]"
      },
      "2575": {
        "id": 2575,
        "cluster_id": 2820,
        "label": "ApparentPowerPhaseC",
        "type": "Optional[uint]"
      },
      "2576": {
        "id": 2576,
        "cluster_id": 2820,
        "label": "PowerFactorPhaseC",
        "type": "Optional[int]"
      },
      "2577": {
        "id": 2577,
        "cluster_id": 2820,
        "label": "AverageRmsVoltageMeasurementPeriodPhaseC",
        "type": "Optional[uint]"
      },
      "2578": {
        "id": 2578,
        "cluster_id": 2820,
        "label": "AverageRmsOverVoltageCounterPhaseC",
        "type": "Optional[uint]"
      },
      "2579": {
        "id": 2579,
        "cluster_id": 2820,
        "label": "AverageRmsUnderVoltageCounterPhaseC",
        "type": "Optional[uint]"
      },
      "2580": {
        "id": 2580,
        "cluster_id": 2820,
        "label": "RmsExtremeOverVoltagePeriodPhaseC",
        "type": "Optional[uint]"
      },
      "2581": {
        "id": 2581,
        "cluster_id": 2820,
        "label": "RmsExtremeUnderVoltagePeriodPhaseC",
        "type": "Optional[uint]"
      },
      "2582": {
        "id": 2582,
        "cluster_id": 2820,
        "label": "RmsVoltageSagPeriodPhaseC",
        "type": "Optional[uint]"
      },
      "2583": {
        "id": 2583,
        "cluster_id": 2820,
        "label": "RmsVoltageSwellPeriodPhaseC",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 2820,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 2820,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 2820,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 2820,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 2820,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 2820,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "4294048773": {
    "id": 4294048773,
    "label": "UnitTesting",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 4294048773,
        "label": "Boolean",
        "type": "bool"
      },
      "1": {
        "id": 1,
        "cluster_id": 4294048773,
        "label": "Bitmap8",
        "type": "uint"
      },
      "2": {
        "id": 2,
        "cluster_id": 4294048773,
        "label": "Bitmap16",
        "type": "uint"
      },
      "3": {
        "id": 3,
        "cluster_id": 4294048773,
        "label": "Bitmap32",
        "type": "uint"
      },
      "4": {
        "id": 4,
        "cluster_id": 4294048773,
        "label": "Bitmap64",
        "type": "uint"
      },
      "5": {
        "id": 5,
        "cluster_id": 4294048773,
        "label": "Int8u",
        "type": "uint"
      },
      "6": {
        "id": 6,
        "cluster_id": 4294048773,
        "label": "Int16u",
        "type": "uint"
      },
      "7": {
        "id": 7,
        "cluster_id": 4294048773,
        "label": "Int24u",
        "type": "uint"
      },
      "8": {
        "id": 8,
        "cluster_id": 4294048773,
        "label": "Int32u",
        "type": "uint"
      },
      "9": {
        "id": 9,
        "cluster_id": 4294048773,
        "label": "Int40u",
        "type": "uint"
      },
      "10": {
        "id": 10,
        "cluster_id": 4294048773,
        "label": "Int48u",
        "type": "uint"
      },
      "11": {
        "id": 11,
        "cluster_id": 4294048773,
        "label": "Int56u",
        "type": "uint"
      },
      "12": {
        "id": 12,
        "cluster_id": 4294048773,
        "label": "Int64u",
        "type": "uint"
      },
      "13": {
        "id": 13,
        "cluster_id": 4294048773,
        "label": "Int8s",
        "type": "int"
      },
      "14": {
        "id": 14,
        "cluster_id": 4294048773,
        "label": "Int16s",
        "type": "int"
      },
      "15": {
        "id": 15,
        "cluster_id": 4294048773,
        "label": "Int24s",
        "type": "int"
      },
      "16": {
        "id": 16,
        "cluster_id": 4294048773,
        "label": "Int32s",
        "type": "int"
      },
      "17": {
        "id": 17,
        "cluster_id": 4294048773,
        "label": "Int40s",
        "type": "int"
      },
      "18": {
        "id": 18,
        "cluster_id": 4294048773,
        "label": "Int48s",
        "type": "int"
      },
      "19": {
        "id": 19,
        "cluster_id": 4294048773,
        "label": "Int56s",
        "type": "int"
      },
      "20": {
        "id": 20,
        "cluster_id": 4294048773,
        "label": "Int64s",
        "type": "int"
      },
      "21": {
        "id": 21,
        "cluster_id": 4294048773,
        "label": "Enum8",
        "type": "uint"
      },
      "22": {
        "id": 22,
        "cluster_id": 4294048773,
        "label": "Enum16",
        "type": "uint"
      },
      "23": {
        "id": 23,
        "cluster_id": 4294048773,
        "label": "FloatSingle",
        "type": "float32"
      },
      "24": {
        "id": 24,
        "cluster_id": 4294048773,
        "label": "FloatDouble",
        "type": "float"
      },
      "25": {
        "id": 25,
        "cluster_id": 4294048773,
        "label": "OctetString",
        "type": "bytes"
      },
      "26": {
        "id": 26,
        "cluster_id": 4294048773,
        "label": "ListInt8u",
        "type": "List[uint]"
      },
      "27": {
        "id": 27,
        "cluster_id": 4294048773,
        "label": "ListOctetString",
        "type": "List[bytes]"
      },
      "28": {
        "id": 28,
        "cluster_id": 4294048773,
        "label": "ListStructOctetString",
        "type": "List[UnitTesting.Structs.TestListStructOctet]"
      },
      "29": {
        "id": 29,
        "cluster_id": 4294048773,
        "label": "LongOctetString",
        "type": "bytes"
      },
      "30": {
        "id": 30,
        "cluster_id": 4294048773,
        "label": "CharString",
        "type": "str"
      },
      "31": {
        "id": 31,
        "cluster_id": 4294048773,
        "label": "LongCharString",
        "type": "str"
      },
      "32": {
        "id": 32,
        "cluster_id": 4294048773,
        "label": "EpochUs",
        "type": "uint"
      },
      "33": {
        "id": 33,
        "cluster_id": 4294048773,
        "label": "EpochS",
        "type": "uint"
      },
      "34": {
        "id": 34,
        "cluster_id": 4294048773,
        "label": "VendorId",
        "type": "uint"
      },
      "35": {
        "id": 35,
        "cluster_id": 4294048773,
        "label": "ListNullablesAndOptionalsStruct",
        "type": "List[UnitTesting.Structs.NullablesAndOptionalsStruct]"
      },
      "36": {
        "id": 36,
        "cluster_id": 4294048773,
        "label": "EnumAttr",
        "type": "aenum SimpleEnum"
      },
      "37": {
        "id": 37,
        "cluster_id": 4294048773,
        "label": "StructAttr",
        "type": "UnitTesting.Structs.SimpleStruct"
      },
      "38": {
        "id": 38,
        "cluster_id": 4294048773,
        "label": "RangeRestrictedInt8u",
        "type": "uint"
      },
      "39": {
        "id": 39,
        "cluster_id": 4294048773,
        "label": "RangeRestrictedInt8s",
        "type": "int"
      },
      "40": {
        "id": 40,
        "cluster_id": 4294048773,
        "label": "RangeRestrictedInt16u",
        "type": "uint"
      },
      "41": {
        "id": 41,
        "cluster_id": 4294048773,
        "label": "RangeRestrictedInt16s",
        "type": "int"
      },
      "42": {
        "id": 42,
        "cluster_id": 4294048773,
        "label": "ListLongOctetString",
        "type": "List[bytes]"
      },
      "43": {
        "id": 43,
        "cluster_id": 4294048773,
        "label": "ListFabricScoped",
        "type": "List[UnitTesting.Structs.TestFabricScoped]"
      },
      "48": {
        "id": 48,
        "cluster_id": 4294048773,
        "label": "TimedWriteBoolean",
        "type": "bool"
      },
      "49": {
        "id": 49,
        "cluster_id": 4294048773,
        "label": "GeneralErrorBoolean",
        "type": "bool"
      },
      "50": {
        "id": 50,
        "cluster_id": 4294048773,
        "label": "ClusterErrorBoolean",
        "type": "bool"
      },
      "255": {
        "id": 255,
        "cluster_id": 4294048773,
        "label": "Unsupported",
        "type": "Optional[bool]"
      },
      "16384": {
        "id": 16384,
        "cluster_id": 4294048773,
        "label": "NullableBoolean",
        "type": "Union[Nullable, bool]"
      },
      "16385": {
        "id": 16385,
        "cluster_id": 4294048773,
        "label": "NullableBitmap8",
        "type": "Union[Nullable, uint]"
      },
      "16386": {
        "id": 16386,
        "cluster_id": 4294048773,
        "label": "NullableBitmap16",
        "type": "Union[Nullable, uint]"
      },
      "16387": {
        "id": 16387,
        "cluster_id": 4294048773,
        "label": "NullableBitmap32",
        "type": "Union[Nullable, uint]"
      },
      "16388": {
        "id": 16388,
        "cluster_id": 4294048773,
        "label": "NullableBitmap64",
        "type": "Union[Nullable, uint]"
      },
      "16389": {
        "id": 16389,
        "cluster_id": 4294048773,
        "label": "NullableInt8u",
        "type": "Union[Nullable, uint]"
      },
      "16390": {
        "id": 16390,
        "cluster_id": 4294048773,
        "label": "NullableInt16u",
        "type": "Union[Nullable, uint]"
      },
      "16391": {
        "id": 16391,
        "cluster_id": 4294048773,
        "label": "NullableInt24u",
        "type": "Union[Nullable, uint]"
      },
      "16392": {
        "id": 16392,
        "cluster_id": 4294048773,
        "label": "NullableInt32u",
        "type": "Union[Nullable, uint]"
      },
      "16393": {
        "id": 16393,
        "cluster_id": 4294048773,
        "label": "NullableInt40u",
        "type": "Union[Nullable, uint]"
      },
      "16394": {
        "id": 16394,
        "cluster_id": 4294048773,
        "label": "NullableInt48u",
        "type": "Union[Nullable, uint]"
      },
      "16395": {
        "id": 16395,
        "cluster_id": 4294048773,
        "label": "NullableInt56u",
        "type": "Union[Nullable, uint]"
      },
      "16396": {
        "id": 16396,
        "cluster_id": 4294048773,
        "label": "NullableInt64u",
        "type": "Union[Nullable, uint]"
      },
      "16397": {
        "id": 16397,
        "cluster_id": 4294048773,
        "label": "NullableInt8s",
        "type": "Union[Nullable, int]"
      },
      "16398": {
        "id": 16398,
        "cluster_id": 4294048773,
        "label": "NullableInt16s",
        "type": "Union[Nullable, int]"
      },
      "16399": {
        "id": 16399,
        "cluster_id": 4294048773,
        "label": "NullableInt24s",
        "type": "Union[Nullable, int]"
      },
      "16400": {
        "id": 16400,
        "cluster_id": 4294048773,
        "label": "NullableInt32s",
        "type": "Union[Nullable, int]"
      },
      "16401": {
        "id": 16401,
        "cluster_id": 4294048773,
        "label": "NullableInt40s",
        "type": "Union[Nullable, int]"
      },
      "16402": {
        "id": 16402,
        "cluster_id": 4294048773,
        "label": "NullableInt48s",
        "type": "Union[Nullable, int]"
      },
      "16403": {
        "id": 16403,
        "cluster_id": 4294048773,
        "label": "NullableInt56s",
        "type": "Union[Nullable, int]"
      },
      "16404": {
        "id": 16404,
        "cluster_id": 4294048773,
        "label": "NullableInt64s",
        "type": "Union[Nullable, int]"
      },
      "16405": {
        "id": 16405,
        "cluster_id": 4294048773,
        "label": "NullableEnum8",
        "type": "Union[Nullable, uint]"
      },
      "16406": {
        "id": 16406,
        "cluster_id": 4294048773,
        "label": "NullableEnum16",
        "type": "Union[Nullable, uint]"
      },
      "16407": {
        "id": 16407,
        "cluster_id": 4294048773,
        "label": "NullableFloatSingle",
        "type": "Union[Nullable, float32]"
      },
      "16408": {
        "id": 16408,
        "cluster_id": 4294048773,
        "label": "NullableFloatDouble",
        "type": "Union[Nullable, float]"
      },
      "16409": {
        "id": 16409,
        "cluster_id": 4294048773,
        "label": "NullableOctetString",
        "type": "Union[Nullable, bytes]"
      },
      "16414": {
        "id": 16414,
        "cluster_id": 4294048773,
        "label": "NullableCharString",
        "type": "Union[Nullable, str]"
      },
      "16420": {
        "id": 16420,
        "cluster_id": 4294048773,
        "label": "NullableEnumAttr",
        "type": "Union[Nullable, UnitTesting.Enums.SimpleEnum]"
      },
      "16421": {
        "id": 16421,
        "cluster_id": 4294048773,
        "label": "NullableStruct",
        "type": "Union[Nullable, UnitTesting.Structs.SimpleStruct]"
      },
      "16422": {
        "id": 16422,
        "cluster_id": 4294048773,
        "label": "NullableRangeRestrictedInt8u",
        "type": "Union[Nullable, uint]"
      },
      "16423": {
        "id": 16423,
        "cluster_id": 4294048773,
        "label": "NullableRangeRestrictedInt8s",
        "type": "Union[Nullable, int]"
      },
      "16424": {
        "id": 16424,
        "cluster_id": 4294048773,
        "label": "NullableRangeRestrictedInt16u",
        "type": "Union[Nullable, uint]"
      },
      "16425": {
        "id": 16425,
        "cluster_id": 4294048773,
        "label": "NullableRangeRestrictedInt16s",
        "type": "Union[Nullable, int]"
      },
      "16426": {
        "id": 16426,
        "cluster_id": 4294048773,
        "label": "WriteOnlyInt8u",
        "type": "Optional[uint]"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 4294048773,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 4294048773,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 4294048773,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 4294048773,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 4294048773,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 4294048773,
        "label": "ClusterRevision",
        "type": "uint"
      },
      "4294070017": {
        "id": 4294070017,
        "cluster_id": 4294048773,
        "label": "MeiInt8u",
        "type": "uint"
      }
    }
  },
  "4294048774": {
    "id": 4294048774,
    "label": "FaultInjection",
    "attributes": {
      "65528": {
        "id": 65528,
        "cluster_id": 4294048774,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 4294048774,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 4294048774,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 4294048774,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 4294048774,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 4294048774,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "4294048800": {
    "id": 4294048800,
    "label": "SampleMei",
    "attributes": {
      "0": {
        "id": 0,
        "cluster_id": 4294048800,
        "label": "FlipFlop",
        "type": "bool"
      },
      "65528": {
        "id": 65528,
        "cluster_id": 4294048800,
        "label": "GeneratedCommandList",
        "type": "List[uint]"
      },
      "65529": {
        "id": 65529,
        "cluster_id": 4294048800,
        "label": "AcceptedCommandList",
        "type": "List[uint]"
      },
      "65530": {
        "id": 65530,
        "cluster_id": 4294048800,
        "label": "EventList",
        "type": "List[uint]"
      },
      "65531": {
        "id": 65531,
        "cluster_id": 4294048800,
        "label": "AttributeList",
        "type": "List[uint]"
      },
      "65532": {
        "id": 65532,
        "cluster_id": 4294048800,
        "label": "FeatureMap",
        "type": "uint"
      },
      "65533": {
        "id": 65533,
        "cluster_id": 4294048800,
        "label": "ClusterRevision",
        "type": "uint"
      }
    }
  },
  "319486977": {
    "id": 319486977,
    "label": "EveCluster",
    "attributes": {
      "319422474": {
        "id": 319422474,
        "cluster_id": 319486977,
        "label": "Watt",
        "type": "float32"
      },
      "319422475": {
        "id": 319422475,
        "cluster_id": 319486977,
        "label": "WattAccumulated",
        "type": "float32"
      },
      "319422478": {
        "id": 319422478,
        "cluster_id": 319486977,
        "label": "WattAccumulatedControlPoint",
        "type": "float32"
      },
      "319422472": {
        "id": 319422472,
        "cluster_id": 319486977,
        "label": "Voltage",
        "type": "float32"
      },
      "319422473": {
        "id": 319422473,
        "cluster_id": 319486977,
        "label": "Current",
        "type": "float32"
      }
    }
  }
}
