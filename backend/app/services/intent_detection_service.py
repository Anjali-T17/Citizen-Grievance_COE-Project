import re
from typing import Dict, Any, List

# Multilingual Intent Definitions (English, Tamil, Hindi)
INTENT_CATALOG = [
    {
        "intent_id": "INTENT_PWD_01",
        "category": "Road Potholes & Infrastructure",
        "target_department_id": "DEPT_PWD",
        "target_department_name": "Public Works Department (PWD)",
        "mandate_id": "MND_PWD_01",
        "keywords": [
            "pothole", "road", "tar", "asphalt", "bridge", "crater", "pavement",
            "சாலை", "குழி", "தார்ச் சாலை", "பாலம்", "சேதம்",
            "सड़क", "गड्ढा", "डामर", "पुल", "क्षतिग्रस्त"
        ]
    },
    {
        "intent_id": "INTENT_WATER_02",
        "category": "Water Leakage & Sewage Drainage",
        "target_department_id": "DEPT_WATER",
        "target_department_name": "Water Supply & Sewerage Board",
        "mandate_id": "MND_WATER_02",
        "keywords": [
            "water", "leak", "pipe", "sewage", "drain", "burst", "drinking water", "overflow",
            "குடிநீர்", "கசிவு", "குழாய்", "சாக்கடை", "கழிவுநீர்", "நீர் கசிவு",
            "पानी", "रिसव", "पाइप", "सीवर", "नाली", "पेयजल", "जलभराव"
        ]
    },
    {
        "intent_id": "INTENT_SAN_03",
        "category": "Garbage & Waste Sanitation",
        "target_department_id": "DEPT_SAN",
        "target_department_name": "Sanitation & Waste Management Dept",
        "mandate_id": "MND_SAN_03",
        "keywords": [
            "garbage", "trash", "waste", "bin", "cleanliness", "dump", "stench", "litter",
            "குப்பை", "கழிவு", "துப்புரவு", "துர்நாற்றம்", "சாக்கடை கழிவு",
            "कचरा", "कूड़ा", "सफाई", "बदबू", "कूड़ेदान", "अपशिष्ट"
        ]
    },
    {
        "intent_id": "INTENT_ELEC_04",
        "category": "Streetlighting & Electrical Lines",
        "target_department_id": "DEPT_ELEC",
        "target_department_name": "Electricity & Streetlighting Board",
        "mandate_id": "MND_ELEC_04",
        "keywords": [
            "streetlight", "electricity", "pole", "wire", "power", "dark", "sparking", "transformer",
            "தெருவிளக்கு", "மின்சாரம்", "மின்கம்பம்", "மின் கசிவு", "இருட்டு",
            "स्ट्रीट लाइट", "बिजली", "खंभा", "तार", "अंधेरा", "ट्रांसफार्मर"
        ]
    },
    {
        "intent_id": "INTENT_HEALTH_05",
        "category": "Public Health & Disease Prevention",
        "target_department_id": "DEPT_HEALTH",
        "target_department_name": "Public Health & Hygiene Dept",
        "mandate_id": "MND_HEALTH_05",
        "keywords": [
            "mosquito", "fever", "stagnant", "dengue", "hygiene", "spraying", "fogging", "contamination",
            "கொசு", "காய்ச்சல்", "தேங்கிய நீர்", "டெங்கு", "மருந்து தெளிப்பு",
            "मच्छर", "बुखार", "ठहरा हुआ पानी", "डेंगी", "फॉगिंग", "स्वास्थ्य"
        ]
    }
]

class IntentDetectionService:
    def detect_intent(self, description: str, category_hint: str = None) -> Dict[str, Any]:
        cleaned_text = re.sub(r'[^\w\s\u0B80-\u0BFF\u0900-\u097F]', ' ', description.lower())
        
        best_intent = None
        max_matches = 0
        matched_keywords = []

        for intent in INTENT_CATALOG:
            matches = [kw for kw in intent["keywords"] if kw.lower() in cleaned_text]
            if len(matches) > max_matches:
                max_matches = len(matches)
                best_intent = intent
                matched_keywords = matches

        # Also check category hint if provided (e.g. Roads, Water, Garbage, Lighting)
        if category_hint and not best_intent:
            hint = category_hint.lower()
            for intent in INTENT_CATALOG:
                if any(kw in hint for kw in intent["keywords"]):
                    best_intent = intent
                    matched_keywords = [category_hint]
                    max_matches = 1
                    break

        if not best_intent or max_matches == 0:
            return {
                "detected_intent": "Ambiguous / General Grievance",
                "target_department_id": "DEPT_GENERAL",
                "target_department_name": "General Grievance Review Board",
                "mandate_id": "MND_GEN_00",
                "confidence_score": 0.35,
                "is_ambiguous": True,
                "matched_keywords": [],
                "explanation": "Complaint description is ambiguous or low confidence. Routed to General Review Queue for human confirmation."
            }

        confidence = round(min(0.65 + (max_matches * 0.15), 0.98), 3)

        return {
            "detected_intent": best_intent["category"],
            "target_department_id": best_intent["target_department_id"],
            "target_department_name": best_intent["target_department_name"],
            "mandate_id": best_intent["mandate_id"],
            "confidence_score": confidence,
            "is_ambiguous": False,
            "matched_keywords": matched_keywords,
            "explanation": f"Matched intent '{best_intent['category']}' with {round(confidence*100, 1)}% confidence using multilingual NLP & keywords ({', '.join(matched_keywords[:3])})."
        }

intent_service = IntentDetectionService()
