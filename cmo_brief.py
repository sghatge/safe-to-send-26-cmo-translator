"""Translate an AI governance setup into a one-page brief a CMO will actually read.

Each technical control maps to the business risk it removes. The brief lists what can no
longer happen, what still could (controls that are off), and the decisions leadership owns.
A jargon check refuses to print the brief if any technical term slipped in.
Standard library only.
"""
import json
import re
import sys

CONTROLS = {
    "approval_on_send": ("A campaign reaching customers without a named person approving it",
                         "every send is approved by a named person; large sends by two"),
    "presend_qa": ("Emails going out with no unsubscribe link, wrong prices or at 23:30",
                   "nine checks run before every send, whoever prepared it"),
    "consent_filter_check": ("Emailing people who never agreed to marketing",
                             "the audience is checked for marketing consent before sending"),
    "pii_masking": ("Customer names and emails being copied into an AI tool",
                    "the assistant only ever sees masked customer details"),
    "sql_write_block": ("The assistant deleting or changing customer records",
                        "the assistant can read data but never change it"),
    "protected_workflows": ("Privacy clean-up jobs being paused to save time",
                            "privacy and compliance processes can't be touched by the assistant"),
    "tamper_evident_log": ("Not being able to prove what happened after an incident",
                           "every decision is recorded in a log that shows any later edit"),
    "policy_tests_in_ci": ("A small rule change quietly removing a safeguard",
                           "every rule change is tested against our non-negotiables first"),
}
JARGON = ["mcp", "yaml", "json", "hash", "regex", "sql", "api", "ci", "llm", "pii", "token", "endpoint", "schema"]


def brief(setup):
    on = [c for c in CONTROLS if setup["controls"].get(c)]
    off = [c for c in CONTROLS if not setup["controls"].get(c)]
    lines = [f"# AI in campaign operations: where we stand ({setup['as_of']})", "",
             f"**In one line:** {len(on)} of {len(CONTROLS)} safeguards are in place. "
             + ("Nothing critical is open." if not off else f"{len(off)} risk(s) remain open and need a decision."), "",
             "## What can no longer happen"]
    lines += [f"- {CONTROLS[c][0]}: {CONTROLS[c][1]}." for c in on]
    if off:
        lines += ["", "## What could still happen"] + [f"- {CONTROLS[c][0]}." for c in off]
    lines += ["", "## Decisions we need from you"] + [f"- {d}" for d in setup["decisions"]]
    return "\n".join(lines)


def jargon(text):
    words = set(re.findall(r"[a-z]+", text.lower()))
    return sorted(w for w in JARGON if w in words)


def main(path):
    with open(path, encoding="utf-8") as fh:
        setup = json.load(fh)
    text = brief(setup)
    found = jargon(text)
    if found:
        raise SystemExit(f"Brief not printed: contains jargon {found}")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "examples/q4_setup.json")
