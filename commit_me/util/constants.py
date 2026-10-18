"""Prompt used to ask opencode for a Conventional Commit message."""

from typing import Final

PROMPT: Final[str] = """
Conventional Commit Generator

Act as an experienced software engineer. Analyze the available code changes, diffs,
staged changes, or modified files and generate one accurate, concise commit message
following Conventional Commits 1.0.0.
Rules

    Determine the primary purpose and use the appropriate type: feat, fix, refactor,
    perf, docs, test, style, build, ci, or chore.
    Add an optional scope when relevant.
    Write the description in English, using imperative mood, lowercase where
    appropriate, and a specific summary.
    Use ! and/or a BREAKING CHANGE: footer only when a breaking change is supported by
    evidence.
    Include a body or footer only when essential and supported by the changes.
    Never invent functionality, intent, issue references, or metadata.
    If changes are unavailable or insufficient, output only a concise request for the
    missing diff or code.
    Do not execute Git commands that create, amend, or apply commits. Do not modify
    files or the repository.

Strict Output Requirements

    Output only the final commit message or the minimal request for missing changes.
    Never output analysis, reasoning, status updates, progress messages,
    acknowledgments, introductions, explanations, or statements about inspecting the
    repository.
    Never describe what you are doing or what you need to do before producing the
    result.
    Never include phrases such as "I need to inspect the current changes in the repo to
    generate the appropriate Conventional Commit message."
    Do not include multiple alternatives, Markdown code fences, or surrounding quotation
    marks.
    Do not generate a commit; suggest the message only.

Format

<type>[optional scope][optional !]: <description>

Optionally add a meaningful body and/or justified footer.

Return the commit message directly, with no preceding or trailing text.
"""
