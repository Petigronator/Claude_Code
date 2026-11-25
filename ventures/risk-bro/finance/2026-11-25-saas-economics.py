"""Rulemark (risk-bro) SaaS unit economics: 3 data models x 3 scenarios.

Rerun:  py -3 2026-11-25-saas-economics.py
Every input is tagged in the comment: [OFFICIAL] vendor/exchange/gov page,
[SECONDARY] review/aggregator, [CTO] from product/2026-11-24-realtime-mvp-plan.md,
[ASSUMPTION] CFO assumption. Prices to users are in ILS incl. VAT; vendor costs in USD.
"""
import math

SCEN = ["pess", "base", "opt"]
HEB = {"pess": "פסימי", "base": "בסיס", "opt": "אופטימי"}

# ---------- macro ----------
FX = {"pess": 3.40,    # [ASSUMPTION] weak-shekel stress (USD costs get dearer)
      "base": 3.157,   # [OFFICIAL] Bank of Israel representative rate, 2026-11-03
      "opt": 2.859}    # [SECONDARY] BoI rate reported by Globes, May 2026 (2026 low)
VAT = 0.18             # [SECONDARY, consistent with gov.il 2025 order] 18% since 2025-01-01

# ---------- payments ----------
PAY_PCT = 0.05         # [OFFICIAL] Paddle pay-as-you-go 5% + $0.50, merchant of record, no monthly fee
PAY_FIX_USD = 0.50

# ---------- fixed operating costs (all models) ----------
HOST_USD = {"pess": 25, "base": 12, "opt": 6}      # [ASSUMPTION] VPS $4-6 per CTO + DB/backup headroom
DOMAIN_USD = 15 / 12                                # [CTO] domain ~$10-15/yr
ACCOUNTANT_ILS = {"pess": 350, "base": 250, "opt": 150}  # [ASSUMPTION] bookkeeping for osek patur/murshe
INFRA_PER_USER_USD = {"pess": 0.30, "base": 0.10, "opt": 0.05}  # [ASSUMPTION] bandwidth/ws/db per user

# ---------- user price (ILS / month incl. VAT) ----------
PRICE_RT = {"pess": 29, "base": 49, "opt": 79}      # [ASSUMPTION] anchored to benchmarks (TradingView Essential $14.95 ~ ILS 47)
PRICE_DELAYED = {"pess": 19, "base": 29, "opt": 49} # [ASSUMPTION] delayed data breaks the real-time core -> lower WTP

# ---------- data cost per model ----------
MODELS = {
    "A": {  # licensed real-time redistribution/display
        "name": "A. רישיון זמן אמת",
        "price": PRICE_RT,
        "data_fixed_usd": {"pess": 10_000,  # [CTO upper bound] + [SECONDARY Intrinio: SIP exchange fees $10-20k/mo]
                           "base": 2_499,   # [OFFICIAL] Massive Stocks Business, monthly billing, "No exchange fees" (FMV price)
                           "opt": 500},     # [OFFICIAL, legacy page] Intrinio IEX real-time $6,000/yr, display, no per-user fees
        "data_user_usd": {"pess": 2.0,      # [OFFICIAL] Nasdaq Basic non-pro $1 + Cboe non-pro $1 per user/month
                          "base": 0.0, "opt": 0.0},
    },
    "B": {  # 15-minute delayed
        "name": "B. השהיה 15 דק'",
        "price": PRICE_DELAYED,
        "data_fixed_usd": {"pess": 2_998,   # [OFFICIAL] Massive Business 2,499 + Full Market Delayed add-on 499 (if add-on needs base plan)
                           "base": 499,     # [OFFICIAL price, NOT VERIFIED standalone] Full Market Delayed add-on alone
                           "opt": 100},     # [ASSUMPTION] cheap commercial delayed/EOD plan
        "data_user_usd": {"pess": 0.0, "base": 0.0, "opt": 0.0},  # [ASSUMPTION] delayed usually no per-user exchange fee
    },
    "C": {  # bring your own key, computed in the user's browser
        "name": "C. BYOK (מפתח של המשתמש)",
        "price": PRICE_RT,
        "data_fixed_usd": {"pess": 0, "base": 0, "opt": 0},   # user holds the data relationship
        "data_user_usd": {"pess": 0.0, "base": 0.0, "opt": 0.0},
    },
}

CONVERSION = {"pess": 0.02, "base": 0.03, "opt": 0.05}  # [ASSUMPTION] free -> paid freemium conversion
TARGET_PROFIT_ILS = 10_000                              # [ASSUMPTION] "worth Roy's time" monthly pre-tax profit
OSEK_PATUR_CEILING_ILS = 120_000                        # [ASSUMPTION, NOT VERIFIED for 2026] annual turnover ceiling


def unit(model, s, overrides=None):
    o = overrides or {}
    fx = o.get("fx", FX[s])
    vat = o.get("vat", VAT)
    price = o.get("price", model["price"][s])
    data_fixed = o.get("data_fixed", model["data_fixed_usd"][s])
    data_user = o.get("data_user", model["data_user_usd"][s])
    net_rev = price / (1 + vat)
    pay_fee = price * PAY_PCT + PAY_FIX_USD * fx
    infra = INFRA_PER_USER_USD[s] * fx
    data_u = data_user * fx
    contrib = net_rev - pay_fee - infra - data_u
    fixed = (data_fixed + HOST_USD[s] + DOMAIN_USD) * fx + ACCOUNTANT_ILS[s]
    be = math.ceil(fixed / contrib) if contrib > 0 else None
    tgt = math.ceil((fixed + TARGET_PROFIT_ILS) / contrib) if contrib > 0 else None
    return dict(price=price, vat_amt=price - net_rev, net_rev=net_rev, pay_fee=pay_fee,
                infra=infra, data_u=data_u, contrib=contrib, fixed=fixed,
                data_fixed_ils=data_fixed * fx, be=be, tgt=tgt,
                free_needed=(math.ceil(be / CONVERSION[s]) if be else None),
                annual_rev_at_be=(be * price * 12 if be else None))


def f(x, d=1):
    return "—" if x is None else f"{x:,.{d}f}"


def main():
    print("## Unit economics per paying user (ILS / month)\n")
    for key, m in MODELS.items():
        print(f"### {m['name']}\n")
        print("| שורה | " + " | ".join(HEB[s] for s in SCEN) + " |")
        print("|---|" + "---|" * len(SCEN))
        rows = [("מחיר למשתמש כולל מע\"מ", "price"), ("מע\"מ 18%", "vat_amt"),
                ("הכנסה נטו", "net_rev"), ("עמלת סליקה (Paddle 5% + $0.50)", "pay_fee"),
                ("תשתית למשתמש", "infra"), ("דמי בורסה למשתמש", "data_u"),
                ("**תרומה למשתמש**", "contrib"), ("נתונים, קבוע לחודש", "data_fixed_ils"),
                ("**עלות קבועה כוללת לחודש**", "fixed")]
        R = {s: unit(m, s) for s in SCEN}
        for label, k in rows:
            print(f"| {label} | " + " | ".join(f(R[s][k]) for s in SCEN) + " |")
        print(f"| **נקודת איזון (משלמים)** | " + " | ".join(f(R[s]['be'], 0) for s in SCEN) + " |")
        print(f"| משלמים לרווח ₪{TARGET_PROFIT_ILS:,} לחודש | " + " | ".join(f(R[s]['tgt'], 0) for s in SCEN) + " |")
        print(f"| משתמשים חינמיים נדרשים (המרה {'/'.join(str(int(CONVERSION[s]*100))+'%' for s in SCEN)}) | "
              + " | ".join(f(R[s]['free_needed'], 0) for s in SCEN) + " |")
        print(f"| מחזור שנתי בנקודת האיזון | " + " | ".join(f(R[s]['annual_rev_at_be'], 0) for s in SCEN) + " |")
        print()

    # sensitivity on model A base: swing one input to its pess / opt value
    print("## Sensitivity: model A, base, break-even paying users\n")
    A = MODELS["A"]
    base_be = unit(A, "base")["be"]
    tests = [
        ("עלות נתונים קבועה ($10,000 / $500)", "data_fixed", A["data_fixed_usd"]["pess"], A["data_fixed_usd"]["opt"]),
        ("מחיר למשתמש (₪29 / ₪79)", "price", PRICE_RT["pess"], PRICE_RT["opt"]),
        ("דמי בורסה למשתמש ($2 / $0)", "data_user", 2.0, 0.0),
        ("שער דולר (3.40 / 2.859)", "fx", FX["pess"], FX["opt"]),
        ("מע\"מ (18% / 0% עוסק פטור)", "vat", 0.18, 0.0),
    ]
    print(f"| משתנה (ערך פסימי / אופטימי) | נקודת איזון: פסימי | בסיס | אופטימי | טווח |")
    print("|---|---|---|---|---|")
    out = []
    for label, k, lo, hi in tests:
        b_lo = unit(A, "base", {k: lo})["be"]
        b_hi = unit(A, "base", {k: hi})["be"]
        out.append((abs((b_lo or 10**9) - (b_hi or 0)), label, b_lo, b_hi))
    for rng, label, b_lo, b_hi in sorted(out, reverse=True):
        print(f"| {label} | {f(b_lo,0)} | {base_be} | {f(b_hi,0)} | {f(rng,0)} |")


if __name__ == "__main__":
    main()
