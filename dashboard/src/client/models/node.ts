export class MatterNode {
  node_id: number;
  date_commissioned: string; // Dates will be strings in JSON
  last_interview: string;
  interview_version: number;
  available: boolean;
  is_bridge: boolean;
  attributes: { [key: string]: any };
  attribute_subscriptions: Array<[number | null, number | null, number | null]>;

  constructor(public data: Record<string, any>) {
    this.node_id = data.node_id;
    this.date_commissioned = data.date_commissioned;
    this.last_interview = data.last_interview;
    this.interview_version = data.interview_version;
    this.available = data.available;
    this.is_bridge = data.is_bridge;
    this.attributes = data.attributes;
    this.attribute_subscriptions = data.attribute_subscriptions;
  }

  get nodeLabel(): string | undefined {
    return this.attributes["0/40/5"];
  }

  get vendorName(): string {
    return this.attributes["0/40/1"];
  }

  get productName(): string {
    return this.attributes["0/40/3"];
  }

  get serialNumber(): string {
    return this.attributes["0/40/15"];
  }

  update(data: Record<string, any>): MatterNode {
    return new MatterNode({ ...this.data, ...data });
  }
}
