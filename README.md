# StoreLab (KyroAI)
> **Eliminating Hardware Startup Death: Validate physical product demand before cutting steel or ordering inventory.**
> Built for the **Google DeepMind & Google Cloud Startup Buildathon India 2026** (nasscom | Headstart | H2S).

---

## 💡 The Problem
**9 out of 10 physical hardware and consumer brands fail for one brutal reason: Inventory Capital Risk.**

Founders spend ₹15L–₹50L upfront on tooling, molds, minimum-order-quantity (MOQ) manufacturing, and warehouse logistics *before* knowing if a single customer will actually open their wallet. Current validation methods are broken:
- **Kickstarter/Indiegogo**: Require 6–9 months of video production, agency fees, and high burn before day one.
- **Static Landing Pages**: Suffer 80%+ bounce rates because buyers can't touch, inspect, or build emotional connection with physical products.
- **Surveys & Forms**: People say "I'd buy this!" for free, then vanish when asked for payment or commitment.

---

## ⚡ The Solution: StoreLab
StoreLab is a **zero-inventory hardware validation engine**. It turns physical 3D CAD/concept designs into interactive, photorealistic web-native prototypes with high-intent commitment loops:

1. **Photorealistic 3D Spatial Sandbox**: Prospective customers inspect ergonomics, swap materials/finishes in real-time, and view desktop setups in a browser-native 3D studio.
2. **Intent-Gated Waitlist Pipeline**: Filters phantom clicks from genuine buyer demand through automated transactional email handshakes, duplicate-proofing, and anti-bot honeypot traps.
3. **AI-Driven Demand Intelligence**: Ingests viewport interaction telemetry, conversion velocity, and customer price-point sentiment to tell founders: *"Product A will sell 4,000 units at ₹799; kill Product B."*

---

## 🤖 Google AI & DeepMind Stack Integration

| Layer | Google Technology | Role in StoreLab |
| :--- | :--- | :--- |
| **Agentic Workflow** | **Google Antigravity** | End-to-end autonomous agent workflow used to scaffold, refactor, and maintain the full-stack architecture, run verification suites, and optimize multi-tier deployments. |
| **Generative Intelligence** | **Gemini 2.0 Flash & Gemini 1.5 Pro** | Multimodal reasoning over customer feedback, clickstream heatmaps, and product variant engagement to produce automated **Demand Validation Reports**. |
| **Developer Platform** | **Google AI Studio** | Rapid prompt engineering, evaluation benchmarks, and few-shot calibration for consumer intent scoring. |
| **Cloud Infrastructure** | **Google Cloud Platform (GCP)** | Cloud Run container orchestration, Cloud Storage for 3D glTF/GLB assets, and Firestore/BigQuery telemetry pipeline. |

---

## 🏗️ System Architecture

```
storelab/
├── backend/                   # High-concurrency FastAPI Microservice
│   ├── app/
│   │   ├── api/               # Modular REST endpoints (products, waitlist, analytics, owner)
│   │   ├── config.py          # Unified pydantic-settings & security configuration
│   │   ├── db/                # Supabase PostgreSQL engine & SQL seed schemas
│   │   ├── models/            # Strict Pydantic v2 domain schemas (single source of truth)
│   │   ├── services/          # Pure business logic (rate-limiter, email, analytics)
│   │   └── main.py            # ASGI application root
│   ├── tests/                 # Automated validation & test harness
│   ├── Dockerfile             # Production container definition
│   └── requirements.txt
│
├── frontend/                  # Next.js 16 (React 19) App Router
│   ├── app/                   # Server & Client rendered pages (/storelab-3d, /dashboard)
│   ├── components/            # Atomic, accessible design system (Tailwind CSS v4)
│   ├── hooks/                 # Real-time state hooks (useProducts, useAnalytics)
│   ├── lib/                   # API client, TypeScript interfaces & telemetry contracts
│   └── Dockerfile
│
├── docker-compose.yml         # Local & cloud multi-container orchestrator
├── main.py                    # Zero-friction root launcher
└── Makefile                   # Developer productivity commands
```

---

## 🚀 Live Features Built & Verified

- **Interactive 3D Studio (`/storelab-3d`)**: WebGL/Canvas viewport letting buyers test physical proportions, finishes, and features live.
- **Fraud-Proof Waitlist Engine**:
  - *Anti-Bot Honeypots*: Traps automated scrapers and malicious submission bots silently.
  - *Sliding-Window Rate Limiting*: Protects endpoints from registration floods.
  - *Transactional SMTP Dispatches*: Sends immediate branded confirmation emails with unique waitlist tracking numbers.
  - *GDPR/DPDP Compliant*: One-click delete/opt-out capability.
- **Real-Time Founder Analytics Dashboard (`/dashboard`)**:
  - Token-gated access (`X-Admin-Key`) for founders and investors.
  - Live signup counts, product-by-product breakdown, and conversion velocity charts.

---

## 🛠️ Quickstart (Running in Under 60 Seconds)

### 1. Prerequisites
- Python 3.11+
- Node.js 20+

### 2. Start Backend
```bash
# From workspace root
uvicorn main:app --reload --port 8000
```
API Documentation & Swagger: `http://localhost:8000/docs`

### 3. Start Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to interact with the platform.

### 4. Running with Docker
```bash
docker-compose up --build
```

---

## 🧪 Testing & Reliability

Our backend and frontend include end-to-end verification suites:
```bash
# Frontend build verification
cd frontend && npm run build

# Backend verification
cd backend && python tests/verify_endpoints.py
```

---

## 🏆 Why StoreLab Wins the Buildathon

1. **Solves a Real Economic Pain**: Solves India's physical product manufacturing bottleneck — democratizing hardware creation for D2C creators.
2. **Deep Google AI Synergy**: Built with **Google Antigravity** workflows and powered by **Gemini multimodal models**.
3. **Production-Ready Today**: Not a slide-only mock. Fully functional Next.js 16 frontend, high-performance FastAPI backend, Supabase DB persistence, and Dockerized deployment.
