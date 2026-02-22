"""
Content Ranker — Scores, ranks, filters, and deduplicates collected items.
Normalizes engagement across platforms and picks the top outperforming content.
"""

from difflib import SequenceMatcher
import config


def _similarity(a, b):
    """Calculate title similarity ratio (0.0 to 1.0)."""
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def _deduplicate(items, threshold=0.65):
    """Remove items with very similar titles."""
    unique = []
    for item in items:
        is_duplicate = False
        for existing in unique:
            if _similarity(item["title"], existing["title"]) > threshold:
                # Keep the one with higher engagement
                if item["engagement"] > existing["engagement"]:
                    unique.remove(existing)
                    unique.append(item)
                is_duplicate = True
                break
        if not is_duplicate:
            unique.append(item)
    return unique


def _normalize_scores(items):
    """
    Normalize engagement scores within each source category.
    This makes scores comparable across platforms.
    """
    # Group by source category
    categories = {}
    for item in items:
        cat = item["source_category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    # Normalize each category to 0-100 scale
    for cat, cat_items in categories.items():
        if not cat_items:
            continue

        scores = [i["engagement"] for i in cat_items]
        max_score = max(scores) if scores else 1
        min_score = min(scores) if scores else 0
        score_range = max_score - min_score if max_score != min_score else 1

        for item in cat_items:
            item["normalized_score"] = (
                (item["engagement"] - min_score) / score_range * 100
            )

    return items


def rank_and_filter(items):
    """
    Main ranking pipeline:
    1. Deduplicate similar items
    2. Normalize scores across platforms
    3. Pick top items per source
    4. Sort by normalized score
    5. Cap total items
    """
    if not items:
        return []

    # Step 1: Deduplicate
    items = _deduplicate(items)

    # Step 2: Normalize scores
    items = _normalize_scores(items)

    # Step 3: Group by source category and pick top N from each
    categories = {}
    for item in items:
        cat = item["source_category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    top_items = []
    for cat, cat_items in categories.items():
        # Sort by engagement within category
        cat_items.sort(key=lambda x: x.get("engagement", 0), reverse=True)
        top_items.extend(cat_items[: config.MAX_ITEMS_PER_SOURCE])

    # Step 4: Sort all by normalized score
    top_items.sort(key=lambda x: x.get("normalized_score", 0), reverse=True)

    # Step 5: Cap total
    top_items = top_items[: config.MAX_TOTAL_ITEMS]

    return top_items


def group_by_type(items):
    """
    Group items into categories for email display:
    - 🔥 Top Stories (highest engagement across all)
    - 📺 Trending Videos
    - 🚀 New AI Tools
    - 📰 News Roundup
    """
    groups = {
        "top_stories": [],
        "videos": [],
        "tools": [],
        "news": [],
    }

    for item in items:
        if item["content_type"] == "video":
            groups["videos"].append(item)
        elif item["content_type"] == "tool":
            groups["tools"].append(item)
        elif item["source_category"] == "News":
            groups["news"].append(item)
        else:
            groups["top_stories"].append(item)

    # Sort each group by engagement
    for key in groups:
        groups[key].sort(key=lambda x: x.get("engagement", 0), reverse=True)

    return groups
