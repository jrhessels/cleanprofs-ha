# custom_components/cleanprofs/util.py
from __future__ import annotations
from datetime import date

# Normalize text for safe comparisons (handles None, trims spaces, lowercases).
def _norm(s: str | None) -> str:
    return (s or "").strip().lower()

# Return today's date in ISO format (YYYY-MM-DD).
def isoToday() -> str:
    return date.today().isoformat()

# Parse an ISO date string (YYYY-MM-DD) to a date object; return None if invalid.
def parseIsoDate(d: str) -> date | None:
    try:
        return date.fromisoformat(d)
    except Exception:
        return None

# Return a sorted, de-duplicated list of ISO date strings for the given product.
def uniqueSortedDates(items: list[dict], productName: str) -> list[str]:
    wanted = _norm(productName)
    dates: list[str] = []
    for item in items:
        if _norm(item.get("product_name")) != wanted:
            continue
        fullDate = item.get("full_date")
        if isinstance(fullDate, str):
            dates.append(fullDate)
    return sorted(set(dates))

# Return the next pickup date (YYYY-MM-DD) for the product, or None if not found.
def nextDate(items: list[dict], productName: str) -> str | None:
    today = isoToday()
    for d in uniqueSortedDates(items, productName):
        if d >= today:
            return d
    return None

# Return True if today is the pickup date for the product (based on nextDate()).
def isCleaningToday(items: list[dict], productName: str) -> bool:
    return nextDate(items, productName) == isoToday()