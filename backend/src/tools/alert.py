from datetime import datetime
from typing import Dict, Any, List


class AlertAgent:
    """
    Manages notifications and alerts:
    - Sends Slack/Email notifications
    - Generates summary reports
    - Creates audit trails
    - Monitors system status
    """
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.name = "alert"
    
    async def send_alerts(
        self,
        event_summary: Dict[str, Any],
        severity: str = "info"
    ) -> Dict[str, Any]:
        """
        Main entry point for sending alerts
        
        Called by Google ADK as a tool
        """
        print(f"\nALERT AGENT: Generating {severity} alerts")
        
        # 1. Generate summary message
        summary = self._generate_summary(event_summary)
        
        # 2. Determine recipients
        recipients = self._determine_recipients(severity)
        
        # 3. Send notifications (mock in demo)
        notifications_sent = []
        
        if self.demo_mode:
            # Mock sending
            for channel in ["slack", "email"]:
                notification = await self._send_notification(
                    channel=channel,
                    recipients=recipients,
                    message=summary,
                    severity=severity
                )
                notifications_sent.append(notification)
                print(f"Sent {channel} notification to {len(recipients[channel])} recipient(s)")
        
        # 4. Create audit record
        audit_record = self._create_audit_record(
            event_summary=event_summary,
            notifications=notifications_sent
        )
        
        return {
            "status": "success",
            "notifications_sent": notifications_sent,
            "recipients_notified": sum(len(r) for r in recipients.values()),
            "channels_used": list(recipients.keys()),
            "audit_record": audit_record,
            "summary": summary,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_summary(self, event_data: Dict) -> str:
        """Generate human-readable summary"""
        
        lines = []
        lines.append("=" * 50)
        lines.append("SUPPLY CHAIN AUTO-OPTIMIZATION COMPLETE")
        lines.append("=" * 50)
        lines.append("")
        
        # Event details
        if "event" in event_data:
            event = event_data["event"]
            if isinstance(event, str):
                lines.append(f"EVENT: {event}")
            else:
                lines.append(f"EVENT: {event.get('description', 'Unknown event')}")
                lines.append(f"REGION: {event.get('region', 'N/A')}")
            lines.append("")
        
        # Demand forecast
        if "demand" in event_data and event_data["demand"].get("spike_detected"):
            forecast = event_data["demand"]
            lines.append("DEMAND ANALYSIS:")
            lines.append(f"   Spike Detected: {forecast.get('spike_multiplier', 0)}x normal demand")
            lines.append(f"   Peak Demand: {forecast.get('peak_demand', 0)} units")
            lines.append(f"   Confidence: {forecast.get('confidence', 0)*100:.0f}%")
            lines.append("")
        
        # Inventory actions
        if "inventory" in event_data:
            inventory = event_data["inventory"]
            if inventory.get("transfers"):
                lines.append("INVENTORY OPTIMIZATION:")
                for t in inventory["transfers"][:2]:  # Show first 2
                    lines.append(f"   Transfer: {t.get('quantity', 0)} units from {t.get('from_warehouse', 'Unknown')}")
                if inventory.get("reorder_needed"):
                    lines.append(f"   External Order: {inventory.get('reorder_quantity', 0)} units")
                lines.append("")
        
        # Vendor selection
        if "vendor" in event_data and event_data["vendor"].get("vendor_selected"):
            vendor = event_data["vendor"]
            lines.append("VENDOR PROCUREMENT:")
            lines.append(f"   Supplier: {vendor.get('vendor_selected', 'N/A')}")
            lines.append(f"   Quantity: {vendor.get('quantity', 0)} units")
            lines.append(f"   Cost: ₹{vendor.get('total_price', 0):,}")
            lines.append(f"   Delivery: {vendor.get('delivery_date', 'TBD')}")
            lines.append("")
        
        # Routing
        if "routing" in event_data and event_data["routing"].get("routes"):
            routing = event_data["routing"]
            lines.append("DELIVERY SCHEDULED:")
            lines.append(f"   Routes Planned: {len(routing['routes'])}")
            lines.append(f"   Total Cost: ₹{routing.get('total_cost', 0):,}")
            lines.append(f"   Earliest Delivery: {routing.get('earliest_delivery', 'N/A')}")
            lines.append("")
        
        lines.append("=" * 50)
        lines.append("All actions completed automatically")
        lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def _determine_recipients(self, severity: str) -> Dict[str, List[str]]:
        """Determine who to notify based on severity"""
        
        recipients = {
            "slack": [],
            "email": []
        }
        
        if severity == "critical":
            recipients["slack"] = ["@supply-chain-director", "@operations-manager"]
            recipients["email"] = ["director@styleflow.in", "ops@styleflow.in"]
        elif severity == "high":
            recipients["slack"] = ["@supply-chain-manager"]
            recipients["email"] = ["scm@styleflow.in"]
        else:  # info
            recipients["slack"] = ["@supply-chain-team"]
            recipients["email"] = ["team@styleflow.in"]
        
        return recipients
    
    async def _send_notification(
        self,
        channel: str,
        recipients: Dict,
        message: str,
        severity: str
    ) -> Dict:
        """Send notification via channel (mock)"""
        
        return {
            "channel": channel,
            "recipients": recipients.get(channel, []),
            "message_preview": message[:100] + "...",
            "severity": severity,
            "sent_at": datetime.utcnow().isoformat(),
            "status": "sent"
        }
    
    def _create_audit_record(
        self,
        event_summary: Dict,
        notifications: List[Dict]
    ) -> Dict:
        """Create audit trail"""
        if not notifications:
            return {
                "status": "no_notifications",
                "event_data": event_summary,
                "agents_involved": ["demand", "inventory", "vendor", "routing", "alert"],
                "total_actions": 0,
                "created_at": datetime.utcnow().isoformat()
            }
        return {
            "audit_id": f"AUDIT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "event_data": event_summary,
            "notifications": notifications,
            "agents_involved": ["demand", "inventory", "vendor", "routing", "alert"],
            "total_actions": len(notifications) + len((event_summary.get("inventory") or {}).get("transfers", []) if isinstance(event_summary.get("inventory"), dict) else []),
            "created_at": datetime.utcnow().isoformat()
        }


# ADK Tool Definition
ALERT_AGENT_TOOL = {
    "name": "send_alerts",
    "description": """
    Send notifications to stakeholders about supply chain actions.
    Generates summary reports and creates audit trails.
    Use this as the final step after all other agents complete their work.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "event_summary": {
                "type": "object",
                "description": "Summary of all agent actions and results"
            },
            "severity": {
                "type": "string",
                "description": "Alert severity: info, high, or critical",
                "enum": ["info", "high", "critical"]
            }
        },
        "required": ["event_summary"]
    }
}


# Test
async def test_alert_agent():
    agent = AlertAgent(demo_mode=True)
    
    mock_summary = {
        "event": {"description": "Cyclone approaching Mumbai", "region": "Mumbai"},
        "demand": {"spike_detected": True, "spike_multiplier": 12, "peak_demand": 96},
        "inventory": {"transfers": [{"quantity": 180, "from_warehouse": "Delhi"}], "reorder_needed": True},
        "vendor": {"vendor_selected": "RainShield Fashion", "total_price": 70000}
    }
    
    result = await agent.send_alerts(event_summary=mock_summary, severity="high")
    print(f"\nSent {result['recipients_notified']} notifications")
    print("\n" + result['summary'])


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_alert_agent())
