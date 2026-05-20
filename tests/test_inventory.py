import pytest
from src.modules.inventory.monitor import detect_anomalies
from src.ingestion.mock_data import mock_products, mock_orders, mock_inventory_alerts


def test_detect_low_stock():
    products = [
        {"product_id": "p1", "title": "Widget", "sku": "SKU-001",
         "units_available": 3, "pending_orders": 5}
    ]
    alerts = detect_anomalies(products, [])
    assert any(a["type"] == "low_stock" for a in alerts)


def test_no_alert_when_stock_sufficient():
    products = [
        {"product_id": "p1", "title": "Widget", "sku": "SKU-001",
         "units_available": 50, "pending_orders": 2}
    ]
    alerts = detect_anomalies(products, [])
    assert len(alerts) == 0


def test_stalled_order_detection():
    from datetime import datetime, timedelta, timezone
    old_time = (datetime.now(timezone.utc) - timedelta(hours=30)).isoformat()
    orders = [{"order_id": "o1", "status": "unfulfilled", "created_at": old_time,
               "product_title": "Widget", "product_id": "p1", "sku": "SKU-001"}]
    alerts = detect_anomalies([], orders)
    assert any(a["type"] == "stalled_order" for a in alerts)


def test_mock_alerts_have_required_fields():
    alerts = mock_inventory_alerts()
    required = {"alert_id", "type", "severity", "product_title", "gpt_recommendation"}
    for a in alerts:
        assert required.issubset(a.keys())
