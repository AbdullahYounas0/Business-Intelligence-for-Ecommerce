# E-Commerce Intelligence Hub

A production-grade business intelligence platform for e-commerce — powered by **Google BigQuery**, **GPT-4o**, and a live **React dashboard**.

---

## Quick Start (No API Keys Required)

```bash
git clone https://github.com/AbdullahYounas0/Business-Intelligence-for-Ecommerce.git
cd Business-Intelligence-for-Ecommerce
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

Open http://localhost:8000 — the dashboard loads immediately with realistic mock data.

---

## Architecture

```
FastAPI backend ──► BigQuery (3 datasets)
     │                  └── ecom_raw        (orders, products, reviews)
     │                  └── ecom_features   (rfm_scores, alerts, review_analysis)
     │                  └── ecom_audit      (gpt_calls, cost tracking)
     ├── WebSocket /ws ──► React dashboard (live alerts)
     ├── APScheduler   ──► churn (daily), inventory (15min), sentiment (daily)
     ├── Slack webhooks
     └── Resend email digest (Monday 8am)

React frontend (Vite + Tailwind + Recharts)
     ├── AlertsFeed    — live inventory alerts via WebSocket
     ├── ChurnTable    — at-risk customers + GPT win-back email modal
     ├── SentimentChart — review sentiment by topic (Recharts)
     └── CostAudit     — GPT token usage + cost per module
```

---

## Three Modules

### 1. Churn & Retention
Computes RFM (Recency, Frequency, Monetary) scores daily against BigQuery orders. Customers below the threshold are flagged as at-risk. GPT-4o drafts a personalized win-back email per customer. Delivered via Slack `#retention` + Monday digest email.

### 2. Order & Inventory Intelligence
Runs every 15 minutes — detects low stock, stalled orders, and demand spikes. GPT-4o converts anomaly data into plain-English action recommendations. Broadcasts alerts live to the dashboard and Slack `#inventory-ops`.

### 3. Review Sentiment Analytics
Classifies reviews daily: sentiment, topic tags, urgency flag. GPT-4o generates a weekly narrative summary every Monday. Displayed on the dashboard sentiment panel + included in the digest email.

---

## Author

**Abdullah Younas** — f191010@nu.edu.pk — [GitHub](https://github.com/AbdullahYounas0)
