# ✏️ your comment: name, course, dataset, what the program does (you can finish this at the end)

import csv

CAMPAIGN_FILE = "campaigns_C.csv"


# ✏️ your comment
def to_number(text):
    text = text.strip()
    if text == "":
        return None
    return float(text.replace(",", "."))


# ✏️ your comment
def read_campaigns(filename):
    campaigns = []
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            campaigns.append({
                "name": row["Campaign"].strip(),
                "channel": row["Channel"].strip(),
                "impressions": to_number(row["Impressions"]),
                "clicks": to_number(row["Clicks"]),
                "cost": to_number(row["Cost (€)"]),
                "conversions": to_number(row["Conversions"]),
                "revenue": to_number(row["Revenue (€)"]),
            })
    return campaigns


# ✏️ your comment
def compute_kpis(campaigns):
    valid = []
    for c in campaigns:
        # ✏️ your comment (data rule 1)
        if c["impressions"] is None or c["impressions"] == 0:
            print(f"Note: '{c['name']}' has no impressions and is excluded from all calculations.")
            continue

        c["ctr"] = c["clicks"] / c["impressions"]

        # ✏️ your comment (data rule 2)
        if c["conversions"]:
            c["cpa"] = c["cost"] / c["conversions"]
        else:
            c["cpa"] = None

        # ✏️ your comment
        if c["cost"]:
            c["roas"] = c["revenue"] / c["cost"]
        else:
            c["roas"] = None

        valid.append(c)
    return valid


# ✏️ your comment
def compute_answers(valid):
    # ✏️ your comment (Q1)
    best_ctr = max(valid, key=lambda c: c["ctr"])

    # ✏️ your comment (Q2)
    with_cpa = [c for c in valid if c["cpa"] is not None]
    if with_cpa:
        highest_cpa = max(with_cpa, key=lambda c: c["cpa"])["name"]
    else:
        highest_cpa = None

    # ✏️ your comment (Q3)
    roas_count = len([c for c in valid if c["roas"] is not None and c["roas"] > 3])

    # ✏️ your comment (Q4)
    totals = {}
    for c in valid:
        totals[c["channel"]] = totals.get(c["channel"], 0) + c["conversions"]
    best_channel = max(totals, key=totals.get)

    # ✏️ your comment (Q5)
    average_ctr = sum(c["ctr"] for c in valid) / len(valid)

    return {
        "best_ctr": best_ctr["name"],
        "highest_cpa": highest_cpa,
        "roas_count": roas_count,
        "best_channel": best_channel,
        "channel_totals": totals,
        "average_ctr": round(average_ctr * 100, 2),
    }


# temporary test (we'll remove it later)
data = read_campaigns(CAMPAIGN_FILE)
valid = compute_kpis(data)
answers = compute_answers(valid)
print(answers)