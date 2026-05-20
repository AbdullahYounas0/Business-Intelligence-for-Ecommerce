# E-Commerce Intelligence Hub

A production-grade, full-stack business intelligence platform that turns raw e-commerce data into actionable insights — powered by **Google BigQuery**, **GPT-4o**, and a live **React dashboard**.

Built as a portfolio project demonstrating: BigQuery analytics, GPT-4o integration, real-time WebSockets, scheduled background jobs, and a full Python + React system.

---

## What This Project Does

The platform continuously monitors your e-commerce operation across three core intelligence modules:

| Module | What it watches | How often | Output |
|---|---|---|---|
| **Churn & Retention** | Customer RFM scores | Daily | GPT win-back emails, Slack alert |
| **Order & Inventory** | Stock levels, stalled orders | Every 15 min | Live dashboard alerts, Slack |
| **Review Sentiment** | Product reviews | Daily + weekly | Sentiment charts, email digest |

All three modules share a single React dashboard that streams inventory alerts via WebSocket in real time, while churn and sentiment panels auto-refresh from the REST API.

---

## Use Cases

### 1. Prevent Customer Churn Before It Happens
The RFM (Recency, Frequency, Monetary) engine scores every customer daily against your BigQuery order history. Customers who slip below the configurable threshold are flagged as at-risk. GPT-4o then drafts a personalized win-back email for each one — you click once to review and send.

### 2. Never Run Out of Stock During a Demand Spike
The inventory monitor runs every 15 minutes. It detects low-stock conditions, stalled fulfillment, and sudden demand spikes. When an anomaly is found, GPT-4o converts the raw data into a plain-English action recommendation. The alert broadcasts live to the dashboard and Slack `#inventory-ops`.

### 3. Turn Customer Reviews into Product Strategy
Every review is classified daily by GPT-4o: positive/negative/neutral sentiment, topic tags, and an urgency flag for severe complaints. A weekly narrative report synthesises the patterns into actionable product recommendations, delivered on Monday mornings via email digest.

### 4. Track AI Spend in Real Time
The Cost Audit panel shows GPT-4o token usage and USD cost per module per day, pulled from a `gpt_calls` audit table in BigQuery.

---

## Benefits

- **Zero manual monitoring** — scheduled jobs run automatically; you act only when alerted
- **GPT-4o in context** — raw data never leaves your environment; only anonymised summaries go to the API
- **PII-safe** — Microsoft Presidio masks all customer names and emails before they touch GPT-4o
- **Works without API keys** — the entire dashboard runs on mock data if no `.env` is configured
- **BigQuery-native** — no ORM, no intermediate database; your data lives where it belongs
- **Observable** — every GPT call is logged with token counts and cost

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Churn &     │  │  Inventory   │  │  Review          │  │
│  │  Retention   │  │  Monitor     │  │  Sentiment       │  │
│  │  (daily)     │  │  (15 min)    │  │  (daily/weekly)  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         └─────────────────┼────────────────────┘            │
│                    ┌──────▼───────┐                          │
│                    │  BigQuery    │  ← raw / features / audit│
│                    └──────┬───────┘                          │
│         ┌─────────────────┼────────────────────┐            │
│    ┌────▼─────┐    ┌──────▼────┐    ┌──────────▼────┐      │
│    │ WebSocket │    │  Slack   │    │  Resend Email │      │
│    │  /ws      │    │ Webhooks │    │  Digest       │      │
│    └────┬─────┘    └──────────┘    └───────────────┘      │
└─────────┼────────────────────────────────────────────────────┘
          ▼
┌─────────────────────────────────────────────────────────────┐
│                     React Dashboard                          │
│  AlertsFeed · ChurnTable · SentimentChart · CostAudit        │
└─────────────────────────────────────────────────────────────┘
```

### BigQuery Schema

```
ecom_raw          — source of truth
  ├── orders        (order_id, customer_id, product_id, total_price, status, created_at)
  ├── products      (product_id, sku, category, units_available, reorder_threshold, price)
  └── reviews       (review_id, product_id, customer_name, rating, body, created_at)

ecom_features     — computed outputs
  ├── rfm_scores       (customer_id, rfm_score, recency_days, frequency, monetary)
  ├── inventory_alerts (alert_id, type, severity, gpt_recommendation, created_at)
  └── review_analysis  (review_id, sentiment, topics[], urgent, created_at)

ecom_audit        — observability
  └── gpt_calls        (module, model, prompt_tokens, completion_tokens, cost_usd)
```

---

## Quick Start (No API Keys)

```bash
git clone https://github.com/AbdullahYounas0/Business-Intelligence-for-Ecommerce.git
cd Business-Intelligence-for-Ecommerce
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
uvicorn src.api.main:app --reload
# Open http://localhost:8000
```

Seed mock data at any time:
```bash
curl -X POST http://localhost:8000/demo
```

---

## Full Setup (Live BigQuery Data)

### Prerequisites
- Python 3.12+, Node.js 20+
- Google Cloud account with BigQuery enabled
- OpenAI API key (GPT-4o access)

### Steps

```bash
# 1. Copy env template
cp .env.example .env
# Edit .env with your keys

# 2. Authenticate with Google Cloud
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID

# 3. Create BigQuery datasets
bq mk --dataset YOUR_PROJECT_ID:ecom_raw
bq mk --dataset YOUR_PROJECT_ID:ecom_features
bq mk --dataset YOUR_PROJECT_ID:ecom_audit

# 4. Start backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# 5. Build frontend
cd frontend && npm install && npm run build
```

---

## Project Structure

```
ecom-intelligence-hub/
├── src/
│   ├── api/main.py              # FastAPI app, WebSocket manager, lifespan
│   ├── modules/
│   │   ├── churn/               # RFM scorer, win-back generator, routes
│   │   ├── inventory/           # Anomaly alerter, monitor, routes
│   │   └── sentiment/           # Review classifier, reporter, routes
│   ├── shared/                  # BigQuery client, GPT-4o wrapper, PII masker
│   ├── delivery/                # WebSocket, email, Slack
│   └── ingestion/               # CSV loader, webhook handler, mock data
├── frontend/                    # React 18 + TypeScript + Vite
│   └── src/components/          # AlertsFeed, ChurnTable, SentimentChart, CostAudit
├── tests/                       # Unit tests for all three modules
├── requirements.txt
└── .env.example
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/churn/at-risk` | At-risk customers with RFM scores |
| POST | `/churn/winback/{id}` | Generate GPT-4o win-back email |
| GET | `/inventory/alerts` | Active inventory anomaly alerts |
| GET | `/inventory/forecast` | Stock depletion forecast per SKU |
| GET | `/sentiment/summary` | Sentiment breakdown by topic |
| GET | `/sentiment/report` | Latest GPT-4o weekly narrative |
| GET | `/analytics/costs` | GPT token usage + cost per module |
| POST | `/ingest/upload?table=orders` | CSV upload → BigQuery |
| POST | `/ingest/webhook/{source}` | Real-time Shopify webhook |
| POST | `/demo` | Seed BigQuery with mock data |
| WS | `/ws` | Real-time alert feed |

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, APScheduler |
| Database | Google BigQuery |
| AI | OpenAI GPT-4o |
| PII | Microsoft Presidio |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Recharts |
| Delivery | Slack Incoming Webhooks, Resend |

---

## Security

- **PII masking**: Customer data anonymised with Microsoft Presidio before GPT-4o
- **Rate limiting**: SlowAPI protects every endpoint
- **Secrets**: Environment variables only — never in source code
- **BigQuery IAM**: Use `roles/bigquery.dataEditor` + `roles/bigquery.jobUser` only

---

## Author

**Abdullah Younas**
- Email: f191010@nu.edu.pk
- GitHub: [AbdullahYounas0](https://github.com/AbdullahYounas0)
