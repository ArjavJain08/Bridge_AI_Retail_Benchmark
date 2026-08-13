# ⚡ Retail Price, Promotion & Brand Positioning Engine

An end-to-end, enterprise-grade competitive intelligence platform that benchmarks multi-brand retail positioning, tracks pricing promotional dynamics, calculates weighted brand compliance scores, and deploys Machine Learning for automated price anomaly detection.

---

## 📌 Executive Summary

This platform provides real-time side-by-side positioning benchmarks across international e-commerce channels (e.g., Newegg US, Mercado Libre Brazil). It gives brand strategists and channel managers granular visibility into Share of Shelf, Share of Voice, promotional price swings, and page rubric compliance.

---

## 🏗 System Architecture & Data Pipeline

The pipeline follows a modular, decoupled architecture consisting of four core stages:

```text
┌─────────────────────────┐     ┌──────────────────────────┐
│   Data Extraction       │ ──> │   Machine Learning       │
│  (Async APIs / Mock)    │     │  (Isolation Forest AI)   │
└─────────────────────────┘     └──────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────┐     ┌──────────────────────────┐
│ Streamlit Interactive UI│ <── │  SQLite Data Storage     │
│  (Cached Analytics)     │     │  (retail_advanced.db)    │
└─────────────────────────┘     └──────────────────────────┘
