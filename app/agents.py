"""Stage: the planner and the reviewer. Replaced in week 5.

Week 5 builds a planner, a free plan validator, and a reviewer on Pydantic
AI, against a toy repository. The pattern transfers to this application and
the repository does not, so this is one of the two stages you write rather
than copy. Keep the shapes week 5 taught you, minus `suspect_file`, which
named a file in the toy repository:

    Plan(goal: str, steps: list[str])      flat, because nested fails
    validate_plan(plan) -> tuple[bool, list[str]]
    Verdict(decision: "approve" | "reject", reason: str)

and provide the two functions `pipeline.py` calls, plus the name of the
model your agents use, so the trace records it:

    make_plan(question: str) -> Plan
    review(question: str, answer: str, evidence: list[str]) -> Verdict | None
    MODEL_NAME: str                         for example LARGE.name

Your `validate_plan` checks steps against the tools the agent actually has
(`tools.REGISTRY`) instead of week 5's KNOWN_FILES. Your reviewer sees the
answer and the evidence and not the agent's reasoning, for the reason week 5
gave: a reviewer that inherits the reasoning inherits the mistake.

`review` returning None means "not reviewed". The stub returns None rather
than an approval, because a stub that approves everything would be a stub
claiming to have checked something.

If week 5 measured that the plain loop wins, keep all three pass-throughs
and delete all three `@stub` lines below, and say so in DECISIONS.md. A
pass-through you chose is a design. One you skipped is a stub.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field
from .tools import REGISTRY
from .stub import stub


class Plan(BaseModel):
    goal: str
    steps: list[str]


class Verdict(BaseModel):
    decision: Literal["approve", "reject"]
    reason: str = Field(max_length=200)


def make_plan(question: str) -> Plan:
    from pydantic_ai import Agent, PromptedOutput
    from project.models import LARGE, pydantic_ai_model

    planner = Agent(
        pydantic_ai_model(LARGE),
        output_type=PromptedOutput(Plan),
        retries=3,
        system_prompt=(
            "Make a short plan to answer the user's question. "
            "Use only search_services and compute as steps. "
            "Use compute only if a calculation is needed. "
            "Keep the plan between 1 and 6 steps."
            "Each step must be exactly a tool name, with no other text. "
            "For example, steps should be ['search_services']."
        )
    )

    return planner.run_sync(question).output


def validate_plan(plan: Plan) -> tuple[bool, list[str]]:
    problems = []

    if not 1 <= len(plan.steps) <= 6:
        problems.append("Plan must have between 1 and 6 steps.")

    if not plan.goal.strip():
        problems.append("The goal is missing.")

    for step in plan.steps:
        if step.strip() not in REGISTRY:
            problems.append(f"Unknown tool: {step}")

    return len(problems) == 0, problems



def review(question: str, answer: str,
           evidence: list[str]) -> Verdict | None:
    from pydantic_ai import Agent, PromptedOutput
    from project.models import LARGE, pydantic_ai_model

    reviewer = Agent(
        pydantic_ai_model(LARGE),
        output_type=PromptedOutput(Verdict),
        retries=3,
        system_prompt=(
            "Check if the answer matches the question and the evidence. "
            "Reject answers that invent information. "
            "Approve if the answer is supported by the evidence. "
            "Return only JSON with decision and reason."
        )
    )

    prompt = (
        f"Question: {question}\n"
        f"Answer: {answer}\n"
        f"Evidence: {evidence}"
    )

    return reviewer.run_sync(prompt).output