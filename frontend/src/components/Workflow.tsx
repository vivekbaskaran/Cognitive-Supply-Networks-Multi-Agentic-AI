import { AgentState } from "@/lib/types";
import {
  useCoAgent,
} from "@copilotkit/react-core";

/*
@INFO
We a
Reason: This WorkFlow is Just For Debugging Purpose. But, You can able to see this same with copilotkit tool call with name "Workflow State" in the UI.
*/
export function WorkflowDebugger() {
  const { state } = useCoAgent<AgentState>({
    name: "cognitive_supply_network_agent",
  });

  const wf = state?.workflow_state;

  if (!wf) {
    return (
      <div className="w-1/2 p-6 bg-linear-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <p className="text-gray-500 text-lg">
          Waiting for workflow to start...
        </p>
      </div>
    );
  }

  const steps = [
    { key: "forecast_demand", label: "Demand" },
    { key: "optimize_inventory", label: "Inventory" },
    { key: "negotiate_with_vendor", label: "Vendor" },
    { key: "plan_delivery_route", label: "Routing" },
    { key: "send_supply_alerts", label: "Alert" },
  ];

  const completedSteps = wf.execution_trace?.map((s) => s.tool) ?? [];

  return (
    <div className="w-1/2 p-6 overflow-auto bg-white border-l">
      <h2 className="text-xl font-bold mb-4">Supply Chain Workflow</h2>

      <div className="flex items-center justify-between mb-8">
        {steps.map((step, index) => {
          const isCompleted = completedSteps.includes(step.key);

          return (
            <div
              key={step.key}
              className="flex-1 flex flex-col items-center relative"
            >
              <div
                className={`w-10 h-10 flex items-center justify-center rounded-full text-sm font-bold
                ${
                  isCompleted
                    ? "bg-green-500 text-white"
                    : "bg-gray-200 text-gray-600"
                }`}
              >
                {index + 1}
              </div>
              <span className="mt-2 text-sm">{step.label}</span>

              {index !== steps.length - 1 && (
                <div className="absolute top-5 right-[-50%] w-full h-0.5 bg-gray-200 z-[-1]" />
              )}
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-2 gap-4 mb-8">
        <SummaryCard title="📈 Demand">
          <p>Peak: {wf.peak_demand ?? "-"} units</p>
          <p>7 Day: {wf.total_7day_demand ?? "-"}</p>
          <p>Confidence: {wf.confidence ?? "-"}</p>
        </SummaryCard>

        <SummaryCard title="📦 Inventory">
          <p>Gap: {wf.gap_size ?? "-"}</p>
          <p>
            Reorder:{" "}
            {wf.reorder_needed
              ? "Yes"
              : wf.reorder_needed === false
                ? "No"
                : "-"}
          </p>
        </SummaryCard>

        <SummaryCard title="🏭 Vendor">
          <p>PO: {wf.po_number ?? "-"}</p>
          <p>Vendor: {wf.vendor_name ?? "-"}</p>
        </SummaryCard>

        <SummaryCard title="🚚 Routing">
          <p>Routes: {wf.routes?.length ?? 0}</p>
          <p>Status: {wf.alert_severity ?? "-"}</p>
        </SummaryCard>
      </div>

      <h2 className="text-xl font-bold mb-4">Execution Timeline</h2>

      <div className="space-y-4">
        {wf.execution_trace?.map((step, i) => (
          <div key={i} className="bg-gray-50 border rounded-lg p-4 shadow-sm">
            <div className="flex justify-between items-center mb-2">
              <div className="font-semibold text-sm">{step.agent}</div>
              <div className="text-xs text-gray-400">{step.timestamp}</div>
            </div>

            <div className="text-xs text-indigo-600 font-medium mb-2">
              🔧 {step.tool}
            </div>

            <details className="text-xs">
              <summary className="cursor-pointer text-gray-500">
                View details
              </summary>
              <pre className="mt-2 bg-white p-2 rounded border">
                {JSON.stringify(step.output, null, 2)}
              </pre>
            </details>
          </div>
        ))}
      </div>
    </div>
  );
}

function SummaryCard({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="bg-linear-to-br from-gray-50 to-white border rounded-xl p-4 shadow-sm">
      <h3 className="font-semibold mb-2 text-sm">{title}</h3>
      <div className="text-sm text-gray-700 space-y-1">{children}</div>
    </div>
  );
}