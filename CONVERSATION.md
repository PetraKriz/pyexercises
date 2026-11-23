# CONVERSATION.md - Campaign Audit Quiz (Session 8 final exam)

Petra Krizkova - dataset: campaigns_C.csv
AI assistant used: Claude (claude.ai). This log summarises our real exchanges,
in order, including the problems we hit and how we fixed them.

---

## Session 1 - 17 November 2026

### 1. Reading the instructions
- I gave the AI the professor's PDF (Session 8 final exam) and asked it to
  read all the guidelines so we could check the program against them.
- The AI made a checklist: the 6 steps, the 5 questions, the 3 formulas
  (CTR, CPA, ROAS), the 3 data rules, the 4 files to hand in and the grading.

### 2. Problem: my dataset was in the wrong format
- I first sent 5 files ending in `.numbers`. The AI found they were all the
  same table: my Mac had opened `campaigns_C.csv` in Apple Numbers and saved
  copies.
- Problem: Numbers "cleans" the file, so the real format was hidden
  (separator, decimal comma, encoding). Code written from that version could
  crash on the real CSV.
- Fix: I downloaded the CSV again from Teams and attached it without opening it.

### 3. What the raw CSV really contains (traps found)
- columns separated by `;`, not `,`
- decimal comma: `50917,23` means 50917.23
- an invisible character (BOM) at the start of the file, so the first column
  would be read as "\ufeffCampaign" instead of "Campaign"
- an empty column with no name between Conversions and Revenue (`;;`)
- B2B Webinar has an empty Impressions cell
- Monthly Newsletter and Blog Traffic have 0 conversions
- "Café" contains an accent

### 4. Expected answers computed before writing the program
- Q1 best CTR: Cart Retargeting (4.35%)
- Q2 highest CPA: Black Friday (96.10)
- Q3 campaigns with ROAS above 3: 5
- Q4 channel with most conversions: LinkedIn Ads (4665)
- Q5 average CTR: 3.12%
- Decision: Q5 is asked "in %" so the answer is 3.12 (not 0.03).

### 5. Setting up GitHub Codespaces
- I had never used GitHub. The AI explained Codespaces, the Explorer and the
  Terminal. I renamed `campaigns_C (1).csv` to `campaigns_C.csv`.
- I learned to save with Cmd+S and to back up with Commit + Sync after each step.

### 6. Building the program step by step (testing after each step)
- Step 1 - `to_number` + `read_campaigns`: delimiter=";", encoding="utf-8-sig",
  comma replaced by dot. Test: 12 campaigns printed, B2B Webinar impressions = None.
- Step 2 - `compute_kpis`: rule 1 (no impressions -> excluded), rule 2
  (0 conversions -> CPA = None, no division by zero). Test: 11 campaigns,
  Newsletter and Blog Traffic show CPA None.
- Step 3 - `compute_answers`: the 5 answers computed from the data. Test: all 5
  matched the expected answers above.
- Step 4 - quiz functions (`ask_choice`, `ask_number`, `check_answer`,
  `play_quiz`). Test: typed "abc" for a number (asked again, no crash),
  "3,12" with a comma (accepted), wrong answers (correct answer shown).
- Step 5 - `save_result`, `load_results`, `show_kpi_table`, `main()` with
  try/except that reports which function failed.

### 7. Hand checks (step 4 of the method: "compute one value by hand")
- Winter Sale CPA: 50917.23 / 1066 = 47.76 -> program: 47.76
- Cart Retargeting CTR: 56461 / 1298000 = 4.35% -> program: 4.35%
- Café Loyalty ROAS: 216323.06 / 7062.26 = 30.63 -> program: 30.63

### 8. Errors I hit while testing, and fixes
- In step 4 I typed "4" for Q2 instead of Q1. The program correctly said
  "Wrong" and showed Black Friday, so the answer check works.
- I accidentally typed "4" as my name, so result.csv saved "4, 4/5".
  Fix: deleted result.csv and ran the program again.
- My answers got one step ahead of the questions, and "3.12" ended up typed in
  the terminal after the game ("command not found"). Harmless.
- I stopped a bad run with Ctrl+C: the program printed "Game stopped by the
  player. Nothing was saved." instead of crashing.
- Final clean run: Petra Krizkova, 5/5, saved in result.csv.

---

## Session 2 - 23 November 2026

### 9. Comments
- The AI drafted a comment for every function, explaining the intent.
  I placed them in the file and read each one to make sure I understand it.
- Error: some comments inside functions were not lined up with the code
  (wrong indentation). Fix: added spaces/Tab so each "#" sits above the code.
- Checked with Find ("your comment") that no placeholder was left: No results.
- Test after adding comments: ran the program, stopped it with Ctrl+C at the
  name question -> "Game stopped by the player". Nothing broken.