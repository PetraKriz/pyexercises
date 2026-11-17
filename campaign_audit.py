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


# temporary test (we'll remove it later)
data = read_campaigns(CAMPAIGN_FILE)
for c in data:
    print(c)