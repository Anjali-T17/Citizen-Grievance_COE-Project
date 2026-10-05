from typing import Dict, Any
from app.services.intent_detection_service import intent_service

DEPARTMENT_MANDATES = {
    "DEPT_PWD": {
        "mandate_id": "MND_PWD_01",
        "department_name": "Public Works Department (PWD)",
        "jurisdiction": "Municipal Roads, Bridges, Pavements & Structural Infra",
        "sla_hours": 48,
        "priority": "Medium",
        "assigned_role": "PWD_ROAD_ENGINEER",
        "mandatory_action": "Inspect pavement structural damage, deploy repair crew, patch asphalt.",
        "rule_summary": "PWD Mandate MND_PWD_01 covers road, pothole, and bridge maintenance within municipal limits."
    },
    "DEPT_WATER": {
        "mandate_id": "MND_WATER_02",
        "department_name": "Water Supply & Sewerage Board",
        "jurisdiction": "Water Supply Lines, Sewerage Mains & Drainage",
        "sla_hours": 24,
        "priority": "High",
        "assigned_role": "WATER_LINE_INSPECTOR",
        "mandatory_action": "Isolate pipe leakage, restore clean water pressure, clear drainage blockages.",
        "rule_summary": "Water Board Mandate MND_WATER_02 handles pipe bursts, drinking water leaks, and main sewer overflows."
    },
    "DEPT_SAN": {
        "mandate_id": "MND_SAN_03",
        "department_name": "Sanitation & Waste Management Dept",
        "jurisdiction": "Solid Waste Collection, Garbage Bins & Street Sweeping",
        "sla_hours": 24,
        "priority": "Medium",
        "assigned_role": "SAN_SANITY_OFFICER",
        "mandatory_action": "Dispatch compactor truck, empty overflowing bins, apply disinfectant.",
        "rule_summary": "Sanitation Mandate MND_SAN_03 dictates 24h SLA for solid waste removal and public hygiene."
    },
    "DEPT_ELEC": {
        "mandate_id": "MND_ELEC_04",
        "department_name": "Electricity & Streetlighting Board",
        "jurisdiction": "Public Lighting, Electrical Distribution Poles & Transformers",
        "sla_hours": 24,
        "priority": "High",
        "assigned_role": "ELEC_LINE_OFFICER",
        "mandatory_action": "Check fuse box, repair line wiring, replace burnt LED bulbs.",
        "rule_summary": "Electricity Mandate MND_ELEC_04 requires immediate hazard isolation and streetlight repairs."
    },
    "DEPT_HEALTH": {
        "mandate_id": "MND_HEALTH_05",
        "department_name": "Public Health & Hygiene Dept",
        "jurisdiction": "Vector Control, Stagnant Water Fogging & Health Risk Mitigation",
        "sla_hours": 48,
        "priority": "Medium",
        "assigned_role": "HEALTH_HYGIENE_INSPECTOR",
        "mandatory_action": "Spray larvicide on stagnant water, conduct anti-dengue fogging drive.",
        "rule_summary": "Health Mandate MND_HEALTH_05 enforces vector control and stagnant water disease prevention."
    },
    "DEPT_GENERAL": {
        "mandate_id": "MND_GEN_00",
        "department_name": "General Grievance Review Board",
        "jurisdiction": "Unclassified / Multi-departmental Complaints",
        "sla_hours": 72,
        "priority": "Low",
        "assigned_role": "ROUTING_OFFICER",
        "mandatory_action": "Review ambiguous complaint details, seek citizen clarification, manually assign department.",
        "rule_summary": "General Mandate MND_GEN_00 routes low-confidence or multi-department grievances to human review queue."
    }
}

class RoutingEngine:
    def route_complaint(self, description: str, category_hint: str = None, urgent_flag: bool = False) -> Dict[str, Any]:
        # 1. Intent Detection
        intent_res = intent_service.detect_intent(description, category_hint)
        dept_id = intent_res["target_department_id"]
        
        # 2. Department Mandate Evaluation
        mandate = DEPARTMENT_MANDATES.get(dept_id, DEPARTMENT_MANDATES["DEPT_GENERAL"])
        
        # Priority & SLA Adjustments
        priority = "High" if (urgent_flag or mandate["priority"] == "High") else mandate["priority"]
        sla = 12 if (urgent_flag and priority == "High") else mandate["sla_hours"]
        
        explanation = (
            f"1. Intent Analysis: Detected '{intent_res['detected_intent']}' ({round(intent_res['confidence_score']*100,1)}% confidence).\n"
            f"2. Department Mandate Match: Matched Mandate {mandate['mandate_id']} ({mandate['department_name']}).\n"
            f"3. SLA & Priority Rule: Assigned {priority} Priority with {sla}-hour SLA timeframe.\n"
            f"4. Mandatory Action: {mandate['mandatory_action']}"
        )

        return {
            "detected_intent": intent_res["detected_intent"],
            "target_department_id": dept_id,
            "target_department_name": mandate["department_name"],
            "matched_mandate_id": mandate["mandate_id"],
            "confidence_score": intent_res["confidence_score"],
            "priority": priority,
            "sla_hours": sla,
            "assigned_role": mandate["assigned_role"],
            "jurisdiction": mandate["jurisdiction"],
            "mandatory_action": mandate["mandatory_action"],
            "routing_explanation": explanation,
            "is_ambiguous": intent_res["is_ambiguous"],
            "matched_keywords": intent_res.get("matched_keywords", [])
        }

routing_engine = RoutingEngine()
