import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_a1_complaint_lifecycle_status_updates():
    """Test A1: Status transitions Submitted -> In Progress -> Resolved, invalid status rejection, RBAC enforcement."""
    # 1. Submit a complaint
    sub_res = client.post("/api/complaints", json={
        "description": "Pothole on Main Road near Bus Stop",
        "language": "English",
        "category": "Roads"
    })
    assert sub_res.status_code == 200
    cid = sub_res.json()["complaint_id"]

    # 2. Update status to 'In Progress' by officer
    up_res1 = client.patch(f"/api/complaints/{cid}/status", json={
        "status": "In Progress",
        "role": "Routing Officer",
        "user_id": "USER_002",
        "comment": "Work order issued to PWD repair crew."
    })
    assert up_res1.status_code == 200
    assert up_res1.json()["status"] == "In Progress"

    # 3. Update status to 'Resolved' by officer
    up_res2 = client.patch(f"/api/complaints/{cid}/status", json={
        "status": "Resolved",
        "role": "PWD Road Engineer",
        "user_id": "USER_003",
        "comment": "Pothole patched with asphalt and site inspected."
    })
    assert up_res2.status_code == 200
    assert up_res2.json()["status"] == "Resolved"

    # 4. Reject invalid transition (cannot revert Resolved complaint)
    up_res3 = client.patch(f"/api/complaints/{cid}/status", json={
        "status": "In Progress",
        "role": "Routing Officer"
    })
    assert up_res3.status_code == 400
    assert "Invalid transition" in up_res3.json()["detail"]

    # 5. Reject invalid status string
    up_res4 = client.patch(f"/api/complaints/{cid}/status", json={
        "status": "UNKNOWN_STATUS",
        "role": "Routing Officer"
    })
    assert up_res4.status_code == 400

    # 6. Reject unauthorized role (Citizen trying to resolve)
    sub_res2 = client.post("/api/complaints", json={"description": "Water pipe leak", "language": "English"})
    cid2 = sub_res2.json()["complaint_id"]
    up_res5 = client.patch(f"/api/complaints/{cid2}/status", json={
        "status": "Resolved",
        "role": "Citizen"
    })
    assert up_res5.status_code == 403
    assert "ACCESS DENIED" in up_res5.json()["detail"]

def test_a2_dynamic_discovery_uplift_analytics():
    """Test A2: Dynamic discovery and completion uplift analytics from DB."""
    response = client.get("/api/analytics/discovery-uplift")
    assert response.status_code == 200
    data = response.json()

    assert "baseline_discovery_rate" in data
    assert "assistant_discovery_rate" in data
    assert "discovery_uplift_percentage" in data
    assert "baseline_completion_rate" in data
    assert "assistant_completion_rate" in data
    assert "completion_uplift_percentage" in data
    assert "feature_level_results" in data
    assert "total_events" in data
    assert "total_users" in data

    # Check required underused feature keys F003, F006, F008
    feats = data["feature_level_results"]
    assert "F003" in feats
    assert "F006" in feats
    assert "F008" in feats

def test_a3_functional_translation_backend():
    """Test A3: Functional multilingual translation endpoint for Tamil, Hindi, English."""
    # Tamil translation
    t_res = client.post("/api/complaints/translate", json={
        "text": "சாலையில் பெரிய குழி உள்ளது வாகனங்கள் செல்ல முடியவில்லை",
        "source_language": "Tamil",
        "target_language": "English"
    })
    assert t_res.status_code == 200
    t_data = t_res.json()
    assert "pothole" in t_data["translated_text"].lower() or "road" in t_data["translated_text"].lower()
    assert t_data["source_language"] == "Tamil"
    assert t_data["target_language"] == "English"

    # Hindi translation
    h_res = client.post("/api/complaints/translate", json={
        "text": "पेयजल पाइप फट गया है और पानी बह रहा है",
        "source_language": "Hindi",
        "target_language": "English"
    })
    assert h_res.status_code == 200
    assert "water" in h_res.json()["translated_text"].lower() or "pipe" in h_res.json()["translated_text"].lower()

def test_a4_feature_experiment_metrics():
    """Test A4: Per-feature experiment metrics for F003, F006, F008."""
    response = client.get("/api/experiments/feature-uplift")
    assert response.status_code == 200
    data = response.json()

    assert "F003" in data
    assert "F006" in data
    assert "F008" in data

    f003 = data["F003"]
    assert f003["feature_id"] == "F003"
    assert "baseline_discovery_pct" in f003
    assert "assistant_discovery_pct" in f003
    assert "discovery_uplift_pct" in f003

def test_a5_standalone_tfidf_help_search():
    """Test A5: Standalone TF-IDF help search endpoint with semantic similarity scores."""
    response = client.post("/api/recommendations/help-search", json={
        "query": "translate complaint language",
        "role": "Routing Officer",
        "organisation": "GCMC"
    })
    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "translate complaint language"
    assert data["total_matches"] > 0
    top_match = data["results"][0]
    assert "feature_id" in top_match
    assert "similarity_score" in top_match
    assert top_match["similarity_score"] > 0.0
