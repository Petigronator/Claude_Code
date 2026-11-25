# Venture: Rulemark (formerly Risk Bro; backup name Firmline)

> Agents read this file first. "TBD" means Roy has not decided yet: do not guess.

## Basics
- **One-liner (draft):** a tool that helps private investors make investment decisions
  faster and with more confidence.
- **Type:** startup (fintech / investing), SaaS: installable software + website, real-time streaming
- **Stage:** idea (an old university prototype exists)
- **Started:** 2026-11-24 (prototype from March 2024)
- **Owner:** Roy

## Origin
Roy's B.A. project from 2024: a PySide6 desktop app. The user enters a stock ticker and a
date range; the app downloads prices from Yahoo Finance (yfinance) and shows the standard
deviation, the variance and a price chart, and can send results to Telegram.
~350 lines of Python, no tests, no Git. Code: `C:/Py_OOP_Project/Risk_BroV1.01`
(outside OneDrive; read-only for agents until Roy decides otherwise).
Technical assessment: `product/2026-11-24-prototype-assessment.md`.

## Customer and market
- **Target customer:** active private investors and active traders (Roy, 2026-11-24).
  Not beginners or passive index investors.
- **Founder fit:** Roy is an active investor himself: his own decisions are the first case study.
- **Problem (Roy's words):** "זירוז קבלת החלטות": investors are slow and unsure when
  deciding. The exact decision and pain: TBD, to be found through research and interviews.
- **Market:** Israel first (Hebrew speakers trading US stocks), global later. US stocks only in v1.

## Output rules for agents
- **Language of deliverables for Roy:** Hebrew.
- **Product language:** Hebrew (RTL) and English, switchable.
- **Voice and tone:** professional, clear, no hype. Never promise returns.
- **Product rule:** never a buy or sell signal. Insights only: factual, the same for every
  user, with the calculation visible (e.g. "volatility is 2.3x its 30-day average").

## Goals and constraints
- **Current goal:** decide whether there is a real, reachable problem worth building for,
  and what the smallest testable version is.
- **Budget:** zero. Lean, free MVP: no money talk until Roy has seen and used the app.
- **Regulatory flag (traders):** trading signals ("שירות איתות") and buy/sell timing are licensed
  activities. The product stays on the analytics and self-service side.
- **Regulatory flag:** in Israel, investment advice and portfolio management are licensed
  activities (Israel Securities Authority). Every product idea must be checked against
  this before it is built. legal-regulatory owns this question.
- **Ruled out:** none yet.

## Where things are
- New code (outside OneDrive): `C:/Users/Petigro/dev/risk-bro` (branch `dev`, venv `.venv`, Python 3.13)
- Old prototype (read-only): `C:/Py_OOP_Project/Risk_BroV1.01`
- Notion page: none
- Tasks: `docs/task-ledger.md` · Decisions: `decisions.md`
- Deliverables: `research/`, `strategy/`, `finance/`, `marketing/`, `product/`, `ops/`, `legal/`
