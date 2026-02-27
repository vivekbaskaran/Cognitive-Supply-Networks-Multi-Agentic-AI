"use client";

import {
  useRenderToolCall,
} from "@copilotkit/react-core";
import { CopilotChat, CopilotKitCSSProperties } from "@copilotkit/react-ui";
import { ToolCard } from "@/components/Tool";
// import { WorkflowDebugger } from "@/components/Workflow";

export default function CopilotKitPage() {

  useRenderToolCall({
    name: "forecast_demand",
    description: "Demand forecasting tool",
    parameters: [
      { name: "product_sku", type: "string", required: true },
      { name: "region", type: "string", required: true },
    ],
    render: ({ args, result }) => (
      <ToolCard title="📈 Demand Forecast">
        <p>
          SKU: <b>{args.product_sku}</b> | Region: <b>{args.region}</b>
        </p>
        <div style={{ maxHeight: 200, overflow: "auto" }}>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      </ToolCard>
    ),
  });

  useRenderToolCall({
    name: "optimize_inventory",
    description: "Inventory optimization",
    parameters: [
      { name: "product_sku", type: "string", required: true },
      { name: "region", type: "string", required: true },
      { name: "forecasted_demand", type: "number", required: true },
    ],
    render: ({ result }) => (
      <ToolCard title="📦 Inventory Optimization">
        <div style={{ maxHeight: 200, overflow: "auto" }}>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      </ToolCard>
    ),
  });

  useRenderToolCall({
    name: "transfer_to_agent",
    description: "Agent transfered",
    parameters: [
      { name: "agent_name", type: "string", required: true },
    ],
    render: ({ args }) => (
      <ToolCard title="🔄 Agent transfered">
        <div style={{ maxHeight: 200, overflow: "auto" }}>
          <p>
            Agent: <b>{args.agent_name}</b>
          </p>
        </div>
      </ToolCard>
    ),
  });

  useRenderToolCall({
    name: "negotiate_with_vendor",
    description: "Vendor negotiation",
    parameters: [
      { name: "product_sku", type: "string", required: true },
      { name: "quantity", type: "number", required: true },
    ],
    render: ({ result }) => (
      <ToolCard title="🏭 Vendor Order">
        <div style={{ maxHeight: 200, overflow: "auto" }}>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      </ToolCard>
    ),
  });

  useRenderToolCall({
    name: "plan_delivery_route",
    description: "Route planning",
    parameters: [{ name: "transfers", type: "object[]", required: true }],
    render: ({ result }) => (
      <ToolCard title="🚚 Delivery Routing">
        <div style={{ maxHeight: 200, overflow: "auto" }}>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      </ToolCard>
    ),
  });

  useRenderToolCall({
    name: "send_supply_alerts",
    description: "Supply alerts",
    parameters: [
      { name: "event_description", type: "string", required: true },
      { name: "region", type: "string", required: true },
    ],
    render: ({ result }) => (
      <ToolCard title="🚨 Alert Sent">
        <div style={{ maxHeight: 200, overflow: "auto" }}>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      </ToolCard>
    ),
  });

  useRenderToolCall({
    name: "list_all_products",
    description: "List all products in the supply chain",
    parameters: [],
    render: ({ result }) => {
      const products = Array.isArray(result)
        ? result
        : Array.isArray(result?.products)
          ? result.products
          : [];
      console.log("Rendering Product Catalog with products:", products);

      return (
        <ToolCard title="📦 Product Catalog">
          <div style={{ maxHeight: 200, overflow: "auto" }}>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        </ToolCard>
      );
    },
  });

  return (
    <main
      style={
        { "--copilot-kit-primary-color": "#6366f1" } as CopilotKitCSSProperties
      }
      className="h-screen flex flex-col"
    >
      <div className="h-16 flex items-center justify-center bg-gray-100 font-bold text-2xl text-gray-900">
        Supply Chain Network Assistant 🕵️‍♀️
      </div>

      <div className="flex flex-1 overflow-hidden">
        <div className="w-full border-r">
          <CopilotChat
            className="h-full"
            instructions="You are a supply chain orchestrator. Delegate tasks to specialists in the correct order."
            disableSystemMessage={true}
            labels={{
              title: "Supply Chain Assistant",
              initial: "How can I help with your supply chain today?",
              placeholder: "Ask about demand, inventory, vendors...",
            }}
          />
        </div>

        {/* <WorkflowDebugger /> */}
      </div>
    </main>
  );
}
