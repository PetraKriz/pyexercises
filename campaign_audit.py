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


# temporary test (we'll remove it later)
data = read_campaigns(CAMPAIGN_FILE)
valid = compute_kpis(data)
for c in valid:
    print(c["name"], "CTR:", round(c["ctr"] * 100, 2), "% | CPA:", c["cpa"], "| ROAS:", c["roas"])