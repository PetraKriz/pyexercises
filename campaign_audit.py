# =============================================================================
# Campaign Audit Quiz - Python Programming final exam (Session 8), SKEMA
# Petra Krizkova - dataset: campaigns_C.csv
#
# What the program does:
#   1. reads the campaign file (a raw export: ";" separator, decimal comma)
#   2. computes CTR, CPA and ROAS for each campaign
#   3. asks the player five questions about the campaigns
#   4. checks each answer and counts the score
#   5. shows the final score
#   6. saves the player name, score and date in result.csv
#
# Data rules handled: a campaign with no impressions is left out of every
# calculation, a campaign with 0 conversions has no CPA (but stays for the
# rest), and amounts with a decimal comma are converted to numbers.
#
# Status: everything works. Tested with right answers, wrong answers,
# invalid input (letters instead of numbers) and stopping the game (Ctrl+C).
# =============================================================================

import csv
import unicodedata
import os
from datetime import date

CAMPAIGN_FILE = "campaigns_C.csv"
RESULT_FILE = "result.csv"


# Turns the text of one cell into a number the program can calculate with.
# An empty cell returns None, and the European comma becomes a dot (50917,23 -> 50917.23).
def to_number(text):
    text = text.strip()
    if text == "":
        return None
    return float(text.replace(",", "."))


# Opens the campaign file and returns a list with one dictionary per campaign.
# The file uses ";" between columns, and utf-8-sig removes an invisible character
# at the start of the file (and reads the "é" in Café correctly).
# Columns are read by their name, so the empty column in the file is simply ignored.
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


# Computes CTR, CPA and ROAS for each campaign and keeps only the campaigns
# that can be used. Returns the list of valid campaigns.
def compute_kpis(campaigns):
    valid = []
    for c in campaigns:
        # Data rule 1: no impressions -> the campaign is excluded from every calculation
        if c["impressions"] is None or c["impressions"] == 0:
            print(f"Note: '{c['name']}' has no impressions and is excluded from all calculations.")
            continue

        c["ctr"] = c["clicks"] / c["impressions"]

        # Data rule 2: 0 conversions -> no CPA (to avoid dividing by zero),
        # but the campaign stays in the list for CTR and ROAS
        if c["conversions"]:
            c["cpa"] = c["cost"] / c["conversions"]
        else:
            c["cpa"] = None

        # ROAS = revenue / cost, with the same protection in case a cost is 0
        if c["cost"]:
            c["roas"] = c["revenue"] / c["cost"]
        else:
            c["roas"] = None

        valid.append(c)
    return valid


# Computes the correct answer to each of the five questions from the data,
# so no answer is typed by hand. Returns them together in one dictionary.
def compute_answers(valid):
    # Q1: the campaign with the highest CTR
    best_ctr = max(valid, key=lambda c: c["ctr"])

    # Q2: the highest CPA, only among campaigns that have a CPA
    # (None if no campaign has conversions, so the program doesn't crash)
    with_cpa = [c for c in valid if c["cpa"] is not None]
    if with_cpa:
        highest_cpa = max(with_cpa, key=lambda c: c["cpa"])["name"]
    else:
        highest_cpa = None

    # Q3: count the campaigns with a ROAS above 3
    roas_count = len([c for c in valid if c["roas"] is not None and c["roas"] > 3])

    # Q4: add up the conversions of each channel, then take the channel with the biggest total
    totals = {}
    for c in valid:
        totals[c["channel"]] = totals.get(c["channel"], 0) + c["conversions"]
    best_channel = max(totals, key=totals.get)

    # Q5: average of all the CTRs, shown in % and rounded to 2 decimals (done in the return)
    average_ctr = sum(c["ctr"] for c in valid) / len(valid)

    return {
        "best_ctr": best_ctr["name"],
        "highest_cpa": highest_cpa,
        "roas_count": roas_count,
        "best_channel": best_channel,
        "channel_totals": totals,
        "average_ctr": round(average_ctr * 100, 2),
    }


# Makes text easy to compare: lowercase, no accents, no extra spaces.
# So "cafe loyalty" typed by the player matches "Café Loyalty".
def simplify(text):
    text = unicodedata.normalize("NFD", text.strip().lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return " ".join(text.split())


# Asks for the player's name and keeps asking until something is typed.
def get_player_name():
    while True:
        name = input("What is your name? ").strip()
        if name:
            return name
        print("Please type at least one character.")


# Shows a question with a numbered list of options. The player can type the
# number or the name. Anything else -> the question is asked again.
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


# Asks a question whose answer is a number. Accepts "3.12", "3,12" or "3.12 %".
# try/except catches text that is not a number, so the program asks again instead of crashing.
def ask_number(question):
    print("\n" + question)
    while True:
        answer = input("Your answer: ").replace("%", "").replace(",", ".").strip()
        try:
            return float(answer)
        except ValueError:
            print("That is not a valid number, please try again (example: 3.12).")


# Compares the player's answer with the correct one and prints Correct or Wrong.
# Returns 1 point if right and 0 if wrong. Numbers are compared with a tiny
# tolerance because decimal numbers are never perfectly exact in Python.
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


# Asks the five questions in order and adds up the points. Returns the score.
# Q2 is skipped if no campaign has a CPA.
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


# Adds one line (name, score, date) at the end of result.csv.
# "a" (append) keeps the older results; the header is written only the first time.
def save_result(filename, name, score, total):
    new_file = not os.path.exists(filename)
    with open(filename, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["name", "score", "date"])
        writer.writerow([name, f"{score}/{total}", date.today().isoformat()])


# Reads all the saved results from result.csv.
# Returns an empty list if the file does not exist yet, instead of crashing.
def load_results(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


# Prints a table with the CTR, CPA and ROAS of each campaign, rounded to 2 decimals.
# Shown at the end of the game so it doesn't give away the answers.
def show_kpi_table(valid):
    print("\nCampaign audit")
    print(f"{'Campaign':<20}{'Channel':<14}{'CTR':>8}{'CPA':>10}{'ROAS':>8}")
    for c in valid:
        cpa = f"{c['cpa']:.2f}" if c["cpa"] is not None else "n/a"
        roas = f"{c['roas']:.2f}" if c["roas"] is not None else "n/a"
        print(f"{c['name']:<20}{c['channel']:<14}{c['ctr'] * 100:>7.2f}%{cpa:>10}{roas:>8}")


# Main function: runs every step of the program in order.
# The variable "step" remembers which function is running, so if an error happens
# the message says exactly which function failed, and the program stops cleanly
# instead of crashing.
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