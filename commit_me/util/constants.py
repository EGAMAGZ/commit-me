"""Prompt used to ask opencode for a Conventional Commit message."""

from typing import Final

PROMPT: Final[str] = """
# Conventional Commit Message Generator

## Role
Act as an experienced software engineer. Analyze the code changes provided in the
current context and generate a clear, accurate, and concise Git commit message
following the **Conventional Commits 1.0.0 specification**.

## Instructions

1. Analyze the actual code changes, preferably using the Git diff, staged changes, or
modified files available in the current context.
2. Identify the primary purpose of the changes and select the most appropriate commit
type:
   - `feat`: Introduces a new feature.
   - `fix`: Fixes a bug.
   - `refactor`: Restructures code without changing its external behavior.
   - `perf`: Improves performance.
   - `docs`: Changes documentation.
   - `test`: Adds or modifies tests.
   - `style`: Changes formatting or code style without affecting functionality.
   - `build`: Changes build systems or external dependencies.
   - `ci`: Changes CI/CD configuration.
   - `chore`: Performs maintenance or other tasks that do not fit a more specific type.
3. Add an optional scope in parentheses when a relevant module, component, package, or
area of the codebase can be identified. For example: `feat(auth):`.
4. Write the commit description in **English**, using the imperative mood and a concise,
specific summary. Prefer lowercase text after the prefix.
5. Use the `!` suffix in the type/scope prefix and/or a `BREAKING CHANGE:` footer when
the changes introduce a breaking API or behavioral change. Do not infer breaking changes
without sufficient evidence.
6. Include an optional body only when additional context is necessary to explain the
motivation, implementation details, or relevant consequences of the changes.
7. Include footers only when justified by the available information, such as a breaking
change or issue reference. Never invent issue numbers, references, authors, or other
metadata.
8. If multiple changes are present, identify their common purpose and prioritize the
main change. Use a single commit message unless the changes clearly represent unrelated
work.
9. Do not assume functionality, intentions, or modifications that cannot be verified
from the available changes. If the context is insufficient, request the missing diff or
relevant code instead of fabricating details.
10. Follow the Conventional Commits structure:

    ```text
    <type>[optional scope][optional !]: <description>

    [optional body]

    [optional footer(s)]
    ```

## Output Requirements

- Return only the proposed commit message, written entirely in English.
- Do not execute Git commands that create, amend, or apply a commit.
- Do not modify files or change the repository.
- Do not include explanations, analysis, alternatives, or introductory text.
- Do not wrap the output in Markdown code fences.
- Ensure the type, description, optional body, and footers comply with Conventional
  Commits.
- Keep the message concise while preserving the essential intent of the changes.
- Do not include a body or footer unless it adds meaningful information.

## Task

Inspect the changes available in the current context and generate the most appropriate
Conventional Commit message.

**Suggest the message only; never create the commit.**
"""
