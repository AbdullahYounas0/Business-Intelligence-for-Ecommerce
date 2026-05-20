import pytest
from src.modules.churn.scorer import compute_rfm
from src.ingestion.mock_data import mock_at_risk_customers, mock_orders


def test_compute_rfm_returns_one_row_per_customer():
    orders = mock_orders()
    result = compute_rfm(orders)
    customer_ids = {r["customer_id"] for r in result}
    assert len(result) == len(customer_ids)


def test_rfm_score_is_bounded():
    orders = mock_orders()
    result = compute_rfm(orders)
    for row in result:
        assert 0 <= row["rfm_score"] <= 100


def test_mock_at_risk_customers_have_required_fields():
    customers = mock_at_risk_customers()
    required = {"customer_id", "name", "email", "rfm_score", "last_order_date", "lifetime_value"}
    for c in customers:
        assert required.issubset(c.keys())


def test_mock_at_risk_customers_below_threshold():
    customers = mock_at_risk_customers()
    for c in customers:
        assert c["rfm_score"] < 30
