# ✏️ your comment: name, course, dataset, what the program does (you can finish this at the end)

import csv
import unicodedata
import os
from datetime import date

CAMPAIGN_FILE = "campaigns_C.csv"
RESULT_FILE = "result.csv"


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


# ✏️ your comment
def simplify(text):
    text = unicodedata.normalize("NFD", text.strip().lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return " ".join(text.split())


# ✏️ your comment
def get_player_name():
    while True:
        name = input("What is your name? ").strip()
        if name:
            return name
        print("Please type at least one character.")


# ✏️ your comment
def ask_choice(question, options):
    print("\n" + question)
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")
    while True:
        answer = input("Your answer (number or name): ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        for option in options:
            if simplify(answer) == simplify(option):
                return option
        print(f"Not in the list. Type a number between 1 and {len(options)} or a name from the list.")


# ✏️ your comment
def ask_number(question):
    print("\n" + question)
    while True:
        answer = input("Your answer: ").replace("%", "").replace(",", ".").strip()
        try:
            return float(answer)
        except ValueError:
            print("That is not a valid number, please try again (example: 3.12).")


# ✏️ your comment
def check_answer(player_answer, correct_answer):
    if isinstance(correct_answer, str):
        is_right = simplify(player_answer) == simplify(correct_answer)
    else:
        is_right = abs(player_answer - correct_answer) < 0.001
    if is_right:
        print("Correct!")
        return 1
    print(f"Wrong. The correct answer was: {correct_answer}")
    return 0


# ✏️ your comment
def play_quiz(valid, answers):
    campaign_names = [c["name"] for c in valid]
    channel_names = sorted(answers["channel_totals"])
    score = 0

    player = ask_choice("Q1. Which campaign has the best CTR?", campaign_names)
    score += check_answer(player, answers["best_ctr"])

    if answers["highest_cpa"] is None:
        print("\nQ2 skipped: no campaign has conversions, so no CPA can be computed.")
    else:
        player = ask_choice("Q2. Which campaign has the highest CPA?", campaign_names)
        score += check_answer(player, answers["highest_cpa"])

    player = ask_number("Q3. How many campaigns have a ROAS above 3?")
    score += check_answer(player, answers["roas_count"])

    player = ask_choice("Q4. Which channel generated the most conversions in total?", channel_names)
    score += check_answer(player, answers["best_channel"])

    player = ask_number("Q5. What is the average CTR across all campaigns, in %, rounded to two decimals? (e.g. 2.45)")
    score += check_answer(player, answers["average_ctr"])

    return score


# ✏️ your comment
def save_result(filename, name, score, total):
    new_file = not os.path.exists(filename)
    with open(filename, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["name", "score", "date"])
        writer.writerow([name, f"{score}/{total}", date.today().isoformat()])


# ✏️ your comment
def load_results(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


# ✏️ your comment
def show_kpi_table(valid):
    print("\nCampaign audit")
    print(f"{'Campaign':<20}{'Channel':<14}{'CTR':>8}{'CPA':>10}{'ROAS':>8}")
    for c in valid:
        cpa = f"{c['cpa']:.2f}" if c["cpa"] is not None else "n/a"
        roas = f"{c['roas']:.2f}" if c["roas"] is not None else "n/a"
        print(f"{c['name']:<20}{c['channel']:<14}{c['ctr'] * 100:>7.2f}%{cpa:>10}{roas:>8}")


# ✏️ your comment
def main():
    step = "start"
    try:
        step = "read_campaigns"
        campaigns = read_campaigns(CAMPAIGN_FILE)
        if not campaigns:
            print(f"No campaigns found in {CAMPAIGN_FILE}.")
            return

        step = "compute_kpis"
        valid = compute_kpis(campaigns)
        if not valid:
            print("No campaign can be used for the calculations.")
            return

        step = "compute_answers"
        answers = compute_answers(valid)

        print("\n=== Campaign Audit Quiz ===")
        step = "get_player_name"
        name = get_player_name()

        step = "play_quiz"
        score = play_quiz(valid, answers)
        print(f"\n{name}, your final score is {score}/5")

        step = "save_result"
        save_result(RESULT_FILE, name, score, 5)
        print(f"Your result was saved in {RESULT_FILE}.")

        step = "load_results"
        history = load_results(RESULT_FILE)
        print("\nAll saved results:")
        for line in history:
            print(f"  {line['date']}  {line['name']}: {line['score']}")

        show_kpi_table(valid)

    except FileNotFoundError as error:
        print(f"Error in {step}: file not found ({error.filename}).")
    except PermissionError as error:
        print(f"Error in {step}: no permission to use the file ({error.filename}).")
    except (KeyboardInterrupt, EOFError):
        print("\nGame stopped by the player. Nothing was saved.")
    except Exception as error:
        print(f"Unexpected error in {step}: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()