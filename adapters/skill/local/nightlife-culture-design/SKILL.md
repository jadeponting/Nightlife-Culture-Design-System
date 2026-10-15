---
name: nightlife-culture-design
description: Create, edit or review Nightlife Culture and Vibe Map branded assets using the current local design-system repo. Applies across documents, spreadsheets, presentations, websites, graphics and new formats; also use for Nightlife Culture brand questions. Read live styles before building. Does not apply to unrelated Carly projects or ordinary chat replies.
---

# Nightlife Culture design — local, current source

This is the local entrypoint to the maintained design system, not a second style guide.
Do not remember a palette, a version number or a type scale from an earlier task.

## Read the current system

Before each new branded task, run `scripts/current_system.py` with Python, resolving the
script relative to this skill's installed path. It follows the installation link to the
repo and returns its absolute path, current guide, source fingerprint and freshness checks.
The current installation is `/Users/carly/.codex/skills/nightlife-culture-design`.

“Current” means the local checkout, including current uncommitted source edits. It does not
mean the latest remote Git commit. Do not pull, publish or change brand decisions merely
to create an asset. If the repo is inaccessible, explain the missing access; do not silently
fall back to remembered styles or a packaged snapshot.

Read the live `AGENTS.md`, `foundations/tokens.json`, `foundations/rules.json` and
`docs/gaps.md`. Read the current guide sections relevant to the requested output. Prefer
specific current roles and rules over older summaries; flag any unresolved conflict.
For example, NC-TYP-04 has small-role exceptions to the heading caps floor.

If freshness checks fail, inspect the reason. For stale generated assets, run `python3
build.py` in the design repo to regenerate and check them, without changing source decisions.
If the build fails or a required check cannot run, report that limitation and do not call the
output fully verified. Use the user's chosen destination for the asset; the design repo is
a reference and generator, not the default home for every project output.

## Choose the format, then read its live guidance

Paths below are relative to the repo returned by the script. Search the current repo for new
format guidance too; this table is a starting point, not a closed list.

| Output | Read and reuse |
|---|---|
| HTML, reports, tables, panels | `adapters/skill/src/references/components.md`, `components/library.body.html`, current `foundations/nightlife-culture.css` and `foundations/fonts.css`; the checked portable template can be a starting point |
| Slides and PowerPoint | `foundations/patterns.json`, `layouts/slide-patterns.html`, relevant images in `reference/`, `decks/*.json`; the current deck route is `adapters/powerpoint/build_deck_pptx.py` |
| Charts and statistics, in any format | `adapters/skill/src/references/charts.md`, chart tokens, evidence rules and the project's own methodology |
| Word | Current document rules and `type.roles` / `type.voices` / `type.steps`, including each role's `word` mapping; inspect `adapters/word/` before reusing it |
| Excel | Current tokens and table/chart/evidence rules; inspect `adapters/excel/` and `checks/inspect_xlsx.py` before reusing them |
| PDF | The appropriate structured source above, then export and inspect the pages |
| Social images or another new format | Relevant current guide sections and existing components/assets; search for a maintained adapter or template, then identify any missing format-specific decisions |

Use the available document, spreadsheet, presentation, PDF or image workflow when appropriate
for authoring and rendering; this skill supplies the brand rules. Honour the requested native
format, editability and existing content. Do not substitute HTML for a requested Word or Excel file.

The Word and Excel adapters are examples for particular documents, not universal templates.
They contain older hard-coded sizes; do not copy them unquestioningly. Map the live roles into
native document styles or spreadsheet styles. Preserve formulas, values, number formats and
evidence. Use the real wordmark and fonts. HTML uses the embedded font stylesheet; Office font
delivery depends on the format and available tools. Say when substitution or missing font
delivery remains, and inspect its effect. Do not promise identical layout without rendering it.

## Apply rules; handle gaps explicitly

Read actual colour/text pairings, type roles, sizes, line weights and spacing from the live
sources. Reuse assets and components; never retype the wordmark or choose substitute design
values because a tool's defaults are convenient. Protect evidence and accessibility.

A new asset type can use established brand foundations even when it lacks a dedicated template.
Identify the precise missing decision, follow NC-SYS-08 using the nearest existing components,
and mark the result provisional with the cost or limitation. Log the gap in `docs/gaps.md` as
the repo requires. An interim output does not settle a design decision; Carly does.

Read `adapters/skill/src/references/voice.md` when writing or editing branded copy. When the
request is formatting only, preserve the supplied words. This task does not establish a
separate voice-learning agent or authorise gathering new writing samples.

## Check the actual deliverable

Run `python3 build.py` in the design repo before delivery as its instructions require, then
check the created asset itself. A repo build passing does not validate an external asset.
Use applicable `checks/validate.py`, `checks/inspect_docx.py`, `checks/inspect_pptx.py` or
`checks/inspect_xlsx.py`. Office inspectors cover limited properties; also compare the actual
styles with current roles, check contrast, chart colours, wordmark, font delivery and layout.
Check fonts actually used in the rendered output, not just declared in the DOCX XML. The bundled
LibreOffice renderer may not discover embedded fonts. For a Word preview, convert private copies
of the supplied WOFF2 files to correctly named Office TTF faces and expose that temporary font
directory through a task-local `FONTCONFIG_FILE`; do not install or change system fonts. Remove
stock Word Title borders and theme overrides before applying the brand's own styles.
For Excel, verify calculation health as well as appearance. Render and inspect the output.

Run `scripts/current_system.py` again before delivery and compare its source fingerprint with
the one used when building. If sources changed, reassess the output against them. Record the
guide version and fingerprint in artifact metadata or a companion build record, and state the
version used in the handoff. Distinguish passed, failed and unavailable checks.
