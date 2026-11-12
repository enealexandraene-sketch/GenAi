# Week 5: a planner, an executor, and a second agent

Copy this into your `DECISIONS.md` and fill it in.

---

## Week 5

**Run conditions.** model: qwen2.5:7b | framework: Pydantic AI 0.8.1 | runs per architecture: 3 | served locally (recorded runs) | date: 2026-08-11 | table from: the recording

### 1. The plan schema

What I tried first, and what happened:

[I didn't try the nested version because the instructions said it causes errors with the model.]

What I shipped, and why it is shaped that way:

[I used goal: str, steps: list[str] and suspect_file: str. I kept it simple because a list of strings is enough for the plan and avoids the problems with nested objects.]

### 2. The validator

| check | what it catches |
|2 to 6 steps |Plans that are too short or too long |
|Valid file | Files that don't exist|
|Testing step | Plans that don't mention tests|
|No test edits | Plans that try to change the tests|

On a failed check my system [rejects the plan], because [it's better to catch problems before trying to fix the code].

### 3. The three-way table

| architecture | green | tokens (mean) | seconds (mean) |
| A baseline | 0/3 |4646 | 165.4|
| B planner | 2/3 |1465 |80.3 |
| C planner + reviewer | 0/3 | 1987| 91.8|

### 4. Why the baseline fails

[The baseline tries to find and fix the bug directly without making a plan first. The planner works better because it splits the task into steps and checks the plan before making changes. Both use the same model, so the difference comes from how they approach the task]

### 5. The reviewer

Verdicts across my runs: [0 ] approve, [ 3] reject.

Would I ship it: [ no]. Extra cost: [ 522] tokens, [11.5 ] seconds per run.

The case where it would earn its cost:

[If the fixer proposes a change that makes the tests pass but is still wrong, the reviewer could catch it.]

### 6. What my verifier cannot catch

[Changing OFF_PEAK_FROM_HOUR from 20 to 19 would make all the tests pass, but it would still be wrong because bookings at 19:00 would get a discount they shouldn't.The verifier wouldn't catch this because there isn't a test checking that bookings at 19:00 don't get the off-peak discount.]

### Deferred

[Anything you did not get to, and why.]
