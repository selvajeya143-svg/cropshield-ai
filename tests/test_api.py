"""Tests for FastAPI HTTP endpoints."""

import pytest
from unittest.mock import patch, MagicMock

from backend.main import (
    health_check,
    get_wiki_status,
    validate_wiki,
    get_current_environment,
    fetch_environment,
    perform_diagnosis,
    llm_health_check,
)
from backend.services.wiki_service import WikiService
from backend.services.diagnostic_service import DiagnosticService
from backend.schemas import (
    DiagnosisRequest,
    DiagnosisResponse,
    StrongestAlternative,
    EnvironmentalContext,
)


def test_health_check():
    data = health_check()
    assert data["status"] == "healthy"
    assert "wiki_installed" in data
    assert "service" in data


def test_wiki_status_uninstalled():
    """When wiki is uninstalled, status endpoint returns 'Wiki not installed'."""
    with patch.object(WikiService, "is_installed", return_value=False):
        data = get_wiki_status()
        assert data["installed"] is False
        assert data["status"] == "Wiki not installed"
        assert data["crop_count"] == 0


def test_validate_wiki_uninstalled():
    """When wiki is uninstalled, validate endpoint returns gracefully."""
    with patch.object(WikiService, "is_installed", return_value=False):
        data = validate_wiki()
        assert data.installed is False
        assert data.status == "Wiki not installed"


def test_environment_endpoint():
    data = get_current_environment()
    assert hasattr(data, "temperature_c")
    assert hasattr(data, "relative_humidity_percent")


def test_fetch_environment_endpoint():
    data = fetch_environment(lat=19.7515, lon=75.7139, season="kharif")
    assert hasattr(data, "temperature_c")
    assert data.season == "kharif"
    assert data.latitude == 19.7515
    assert data.longitude == 75.7139


def test_predict_endpoint_proxy():
    """Test the /predict endpoint matching server.mjs reverse proxy."""
    mock_diag = DiagnosisResponse(
        crop="Rice",
        diagnosis="Blast",
        confidence=0.95,
        decisive_features=["spindle_diamond_shape"],
        environmental_support=["high_humidity"],
        strongest_alternative=StrongestAlternative(name="Brown Spot", reason_less_likely="oval spots"),
        uncertainty=[],
        wiki_sources=["wiki/agriculture/Rice/Blast.md"]
    )

    with patch.object(WikiService, "is_installed", return_value=True), \
         patch.object(DiagnosticService, "diagnose", return_value=mock_diag):
        payload = DiagnosisRequest(
            crop="Rice",
            image="data:image/jpeg;base64,dGVzdA==",
            environmental_context=EnvironmentalContext(
                latitude=19.7515,
                longitude=75.7139,
                temperature_c=26.0,
                relative_humidity_percent=90.0
            )
        )
        data = perform_diagnosis(payload)
        assert data.crop == "Rice"
        assert data.diagnosis == "Blast"
        assert data.confidence == 0.95


def test_llm_health_check_endpoint():
    """Test the /api/llm/health and /health/llm diagnostic endpoints."""
    data = llm_health_check()
    assert "provider" in data
    assert data["provider"] in ["alibaba", "groq", "gemini"]
    assert "category" in data
    assert "status_code" in data
    assert "healthy" in data or "is_healthy" in data
    assert data["category"] in [
        "healthy_200",
        "authentication_401",
        "permission_403",
        "rate_limit_429",
        "server_5xx",
        "network_error",
        "network_403",
        "model_permission_403",
        "network_unreachable",
    ]


def test_offline_edge_benchmarks_endpoint():
    """Test /api/offline/benchmarks returns verified ARM Edge metrics."""
    from backend.main import get_offline_benchmarks
    data = get_offline_benchmarks()
    assert "target_hardware" in data
    assert "ARM" in data["target_hardware"]
    assert "vision_model" in data
    assert "MobileNetV3" in data["vision_model"]
    assert "peak_memory_mb" in data
    assert data["peak_memory_mb"] < 1500  # Capped within ARM device constraints
    assert "power_consumption_watts" in data


def test_offline_edge_diagnosis_pipeline():
    """Test /api/offline/diagnose executes sequential workflow offline."""
    from backend.main import perform_offline_edge_diagnosis
    payload = {
        "image": "data:image/jpeg;base64,dGVzdA==",
        "crop": "Rice",
        "lang": "en"
    }
    result = perform_offline_edge_diagnosis(payload)
    assert result["status"] == "success"
    assert result["is_offline"] is True
    assert "ARM Edge" in result["runtime_environment"]
    assert "pipeline_stages" in result
    assert "vision_disease_detection" in result["pipeline_stages"]
    assert "llama_advisory_layer" in result["pipeline_stages"]
    assert "final_diagnosis" in result
    assert result["final_diagnosis"]["crop"] == "Rice"
    assert len(result["final_diagnosis"]["chemical_dosage_15L"]) > 0
