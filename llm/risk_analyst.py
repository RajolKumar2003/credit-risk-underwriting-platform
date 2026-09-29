import os
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

DISCLAIMER = "Educational model output, not a lending decision. Thresholds and loss assumptions are project-defined."

SYSTEM_PROMPT = (
    "You are a credit risk analyst assistant. You receive structured outputs from a probability-of-default "
    "model for one applicant. Write a short underwriting note of at most 150 words in three parts: "
    "the risk level, the main drivers, and what the numbers imply for the decision. "
    "Use only the numbers and features in the input; never invent figures, causes, or policies. "
    "Describe drivers as associations with model risk, not as reasons the person is untrustworthy. "
    "Do not mention age or gender. End with the sentence: " + DISCLAIMER
)


class Driver(BaseModel):
    feature: str
    applicant_value: str
    typical_value: str
    effect: float
    direction: Literal["raises", "lowers"]


class RiskContext(BaseModel):
    pd: float = Field(ge=0, le=1)
    band: str
    cutoff: float = Field(ge=0, le=1)
    exposure: float = Field(gt=0)
    lgd: float = Field(ge=0, le=1)
    expected_loss: float = Field(ge=0)
    portfolio_default_rate: float = Field(ge=0, le=1)
    band_default_rate: float = Field(ge=0, le=1)
    drivers: list[Driver] = Field(max_length=8)

    @field_validator("band")
    @classmethod
    def band_known(cls, value):
        if value not in {"Low", "Moderate", "Elevated", "High", "Very high"}:
            raise ValueError("unknown risk band")
        return value

    @property
    def within_cutoff(self):
        return self.pd <= self.cutoff


def build_user_message(context):
    return context.model_dump_json(indent=1)


def template_summary(context):
    side = "at or below" if context.within_cutoff else "above"
    lines = [
        f"Risk level: {context.band}. Predicted default probability is {context.pd * 100:.1f}% "
        f"against a portfolio rate of {context.portfolio_default_rate * 100:.1f}%; "
        f"applicants in this band defaulted {context.band_default_rate * 100:.1f}% of the time in validation.",
    ]
    if context.drivers:
        pieces = [f"{d.feature} ({d.direction} risk)" for d in context.drivers[:4]]
        lines.append("Main drivers: " + ", ".join(pieces) + ".")
    lines.append(
        f"The probability is {side} the illustrative approval cutoff of {context.cutoff * 100:.0f}%. "
        f"With an exposure of {context.exposure:,.0f} and LGD of {context.lgd * 100:.0f}%, "
        f"expected loss is {context.expected_loss:,.0f}."
    )
    lines.append(DISCLAIMER)
    return " ".join(lines)


def _allowed_numbers(context):
    values = [
        context.pd,
        context.cutoff,
        context.lgd,
        context.portfolio_default_rate,
        context.band_default_rate,
    ]
    allowed = [v * 100 for v in values] + values
    allowed += [context.exposure, context.expected_loss]
    for driver in context.drivers:
        allowed.append(abs(driver.effect))
        for text in (driver.applicant_value, driver.typical_value):
            allowed += [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*\.?\d*", text)]
    return allowed


def ungrounded_numbers(text, context):
    allowed = _allowed_numbers(context)
    problems = []
    for match in re.findall(r"\d[\d,]*\.?\d*", text):
        cleaned = match.replace(",", "").rstrip(".")
        if not cleaned:
            continue
        number = float(cleaned)
        if number <= 10 and "." not in cleaned:
            continue
        if not any(abs(number - a) <= max(0.06, 0.006 * abs(a)) for a in allowed):
            problems.append(match)
    return problems


def generate_note(context, client=None, model=None):
    if client is None:
        return template_summary(context), "template"
    model = model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")
    reply = client.messages.create(
        model=model,
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_message(context)}],
    )
    text = "".join(block.text for block in reply.content if getattr(block, "type", "") == "text").strip()
    if not text or ungrounded_numbers(text, context):
        return template_summary(context), "template (LLM output failed grounding check)"
    return text, "llm"


def default_client():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    import anthropic

    return anthropic.Anthropic(api_key=key)
