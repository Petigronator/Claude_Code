"""Idea-scoring table for strategy/2026-11-24-first-verdict.md (Risk Bro).

Version 2 (2026-11-24): scored for Roy's chosen segment, ACTIVE investors and
ACTIVE traders (not beginners, not passive index investors), per Roy's input
relayed by the COO. Beginner confusion (B) is out of scope and not scored.

Scores are the analyst's judgement (1-5, 5 = better for Roy) based on:
  research/2026-11-24-market-and-competitors.md
  legal/2026-11-24-investment-advice-regulation.md
No new data was collected. "advantage" includes founder-market fit (Roy is an
active investor), which is CONDITIONAL on his self-interview confirming he has
the problem.

Weighted total: pain x2 and regulatory safety x2 (signals and buy/sell timing
are licensed territory, so regulatory risk matters more for traders), all other
criteria x1. Max raw = 40, max weighted = 50.
Run: python 2026-11-24-first-verdict-scores.py
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

CRITERIA = [
    ("pain", "כאב", 2),
    ("market", "גודל שוק", 1),
    ("competition", "תחרות (5=מעט)", 1),
    ("advantage", "יתרון לא-הוגן (כולל התאמת מייסד)", 1),
    ("test_cost", "עלות בדיקה (5=זול)", 1),
    ("revenue_time", "זמן להכנסה (5=מהר)", 1),
    ("zero_budget", "התאמה לתקציב אפס", 1),
    ("reg_safety", "בטיחות רגולטורית (5=בטוח)", 2),
]

# id, name, evidence strength, scores in CRITERIA order
IDEAS = [
    ("N1", "שמירה על הכללים של עצמי תחת לחץ (פאניקה, FOMO, שבירת כללים)",
     "בינוני, גלובלי; סותר בישראל", [3, 2, 2, 4, 4, 3, 4, 4]),
    ("A", "הבנת הסיכון לפני כניסה לפוזיציה ('כמה זה יכול לרדת')",
     "בינוני, גלובלי", [3, 2, 2, 4, 4, 3, 4, 3]),
    ("T1", "תחקיר הטריידים של עצמי (איזו התנהגות שלי מפסידה)",
     "עקיף בלבד", [2, 2, 2, 4, 4, 3, 4, 3]),
    ("N2", "סיכון בשקלים לאחזקות בארה\"ב (מטבע)",
     "אין תלונה; פער מבני", [2, 2, 3, 3, 4, 2, 4, 4]),
    ("C", "לא יודעים במה לסמוך",
     "חלש לישראל", [2, 2, 1, 3, 4, 2, 3, 2]),
    ("E0", "הניסוח המקורי: 'זירוז החלטות'",
     "אין ראיה", [2, 2, 2, 3, 4, 2, 3, 1]),
]

PAIN_GATE = 3  # an idea with pain below this is not a stand-alone candidate


def weighted(scores: list[int]) -> int:
    return sum(s * c[2] for s, c in zip(scores, CRITERIA))


def main() -> None:
    header = (["#", "בעיה מועמדת", "חוזק ראיה"] + [c[1] for c in CRITERIA]
              + ["סה\"כ (40)", "משוקלל (50)", "שער כאב"])
    print("| " + " | ".join(header) + " |")
    print("|" + "---|" * len(header))
    for idea_id, name, evidence, scores in sorted(IDEAS, key=lambda i: -weighted(i[3])):
        assert len(scores) == len(CRITERIA) and all(1 <= s <= 5 for s in scores)
        gate = "עובר" if scores[0] >= PAIN_GATE else "נכשל"
        row = ([idea_id, name, evidence] + [str(s) for s in scores]
               + [str(sum(scores)), str(weighted(scores)), gate])
        print("| " + " | ".join(row) + " |")


if __name__ == "__main__":
    main()
