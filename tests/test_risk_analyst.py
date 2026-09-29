from types import SimpleNamespace

from llm.risk_analyst import RiskContext, generate_note, template_summary, ungrounded_numbers


def context(**changes):
    values = dict(
        pd=0.12,
        band="High",
        cutoff=0.16,
        exposure=500000,
        lgd=0.45,
        expected_loss=27000,
        portfolio_default_rate=0.0807,
        band_default_rate=0.13,
        drivers=[
            dict(feature="EXT_SOURCE_3", applicant_value="0.21", typical_value="0.54", effect=0.4, direction="raises")
        ],
    )
    values.update(changes)
    return RiskContext(**values)


def fake_client(text):
    reply = SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])
    return SimpleNamespace(messages=SimpleNamespace(create=lambda **kwargs: reply))


def test_invalid_probability_rejected():
    try:
        context(pd=1.4)
    except ValueError:
        return
    raise AssertionError("pd above 1 was accepted")


def test_template_uses_only_context_numbers():
    ctx = context()
    assert ungrounded_numbers(template_summary(ctx), ctx) == []


def test_grounded_llm_text_is_returned():
    ctx = context()
    text = "Risk is High at 12.0% default probability, against a portfolio rate of 8.1%."
    note, source = generate_note(ctx, fake_client(text))
    assert source == "llm" and note == text


def test_invented_number_falls_back_to_template():
    ctx = context()
    note, source = generate_note(ctx, fake_client("Default probability is 12% and the applicant earns 73,000 a year."))
    assert source.startswith("template")
    assert "73,000" not in note


def test_no_client_uses_template():
    assert generate_note(context())[1] == "template"
