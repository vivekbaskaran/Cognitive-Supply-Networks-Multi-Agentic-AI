export interface ToolCardProps {
  title: string;
  children: React.ReactNode;
  isStreaming?: boolean;
}

export type AgentState = {
  workflow_state?: {
    product_sku?: string;
    region?: string;
    event_type?: string;

    spike_detected?: boolean;
    peak_demand?: number;
    total_7day_demand?: number;
    confidence?: number;

    stock_levels?: Record<string, number>;
    gap_size?: number;
    reorder_needed?: boolean;

    po_number?: string;
    vendor_name?: string;
    delivery_date?: string;

    transfers?: object[];
    routes?: Record<string, unknown>[];

    alert_severity?: string;

    execution_trace?: {
      agent: string;
      tool: string;
      input: unknown;
      output: unknown;
      timestamp?: string;
    }[];
  };
};
