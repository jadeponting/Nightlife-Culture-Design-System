# Rowan's local design skill — review and connection

Reviewed 14 October 2026 against the local checkout. The declared source is read from
`foundations/tokens.json`, rather than pinned in the local skill.

## What the review found

- The historical root `nightlife-culture-design.skill` declared v1.4.1. At review, 24 of its 28
  files differed from the current generated skill folder. The package in `dist/` matched that
  folder and declared v1.5.1. The builder now refreshes both download locations together.
- The portable entrypoint repeated a hand-written palette and type table. Its accent text
  column said black where the current tokens say ink. Those repeated values have been removed
  in favour of the generated token reference.
- Portable skill freshness was only partly covered by HTML/CSS stamps. It now records a
  source-and-bundle manifest covering instructions, voice, patterns, reference images and fonts.
  Changes are detected even when the guide version is not bumped.
- The v1.5.1 guide and voice reference distinguish cultural value from cultural contribution.
  An older token and component-reference sentence instead banned the latter term. Those
  summaries now match the existing guide; this is an editorial correction, not a new decision.
- The README and AGENTS caps summaries omitted the small-role exceptions already recorded
  in NC-TYP-04. Those exceptions are now explicit.
- Word and Excel support is partial. The Word adapter builds an Operating Plan using some
  older hard-coded sizes; the Excel adapter restyles a particular budget workbook and sets
  Inter 11. Neither is a universal template generated from current roles. Their inspectors
  test limited presentation properties; passing them does not establish full compliance.
- The build's Python Playwright dependency is unavailable in the current interpreters.
  Rendered contrast and slide fit therefore need separate confirmation; a skipped check
  must not be reported as passed. See the current build output when using the system.

## How the connection works

`adapters/skill/local/nightlife-culture-design/` is the maintained entrypoint. Its personal
installation links to this folder, so editing the entrypoint does not create another copy.
`scripts/current_system.py` resolves the link to the repo and reads the current guide version,
source hashes, portable bundle manifest and generated-artifact stamps. It performs no writes.

Every branded task reads the live sources. Before handing over an asset, the skill checks the
sources again and compares its fingerprint, then records which version informed the output.
Changes in the local checkout are visible without reinstalling. Changes made only in remote
Git become visible after the local checkout is synced; the skill does not pull automatically.

The design repo supplies style. The output belongs in the user's requested project or destination.
Brand sources remain private and are not uploaded by this connection. Another computer or cloud
environment needs its own access to the repo or an explicitly versioned portable package.

## Using it

In a local Codex chat, request a Nightlife Culture or Vibe Map branded asset. For explicit use:

> Use $nightlife-culture-design to create an editable Word briefing from this content.

> Use $nightlife-culture-design to format this Excel workbook; preserve its formulas and values.

The skill is available for automatic matching too. If the host has not refreshed its skill
list, open a fresh chat or restart the app. Confirm the skill appears before relying on it.

A new format can use the existing foundations without waiting for a universal template. Where
format-specific rules are missing, follow NC-SYS-08, mark the adaptation provisional and log
the gap. Building an asset does not adopt a new brand rule.

The existing voice reference applies when drafting branded copy. Formatting supplied text
does not authorise rewriting it. A separate voice-learning workflow is outside this connection.

## Verification on 14 October 2026

- Installed a personal folder link at `/Users/carly/.codex/skills/nightlife-culture-design`.
  The local Codex app server's `skills/list` returned exactly one enabled user skill, with no
  discovery errors, from the design repo, `nightlife-culture-organisational-framework` and
  `vibe-map-ukdf-scope`.
- Both the local entrypoint and generated portable skill passed Skill Creator validation.
- In temporary copies, token and voice edits without version bumps, changes to bundled CSS,
  and an added source asset all produced `needs-attention`. A changed guide version was
  discovered dynamically; restoring the originals returned `current`.
- Both portable archives were compared byte for byte with their generated files; the root
  archive and `dist/` archive now match. The live check reports current sources and stamps.
- The repo build reported zero files with Fixed breaches, complete component coverage and
  zero stamp divergences. It also emitted existing warnings. Rendered contrast/slide fit was
  skipped because Python Playwright is missing; it has not passed. The skip currently also
  prints a misleading `3 rendered contrast failure(s)` line, but exits with its documented
  skipped-check code, 3. No new Word, Excel or other asset has been rendered in this task.

The connection and freshness behaviour are verified. Output quality still needs the asset's
own applicable checks and visual inspection whenever an actual deliverable is produced.

## First Word test — 14 October 2026

The supplied `Nightlife_Culture_Vibe_Map_Partner_Deck_Content.docx` was used to produce a
separate editable reading copy. All 155 non-empty source paragraphs were preserved verbatim
and in order, including speaker notes, optional slides and editorial notes. The provisional
Word composition is recorded against gap 19 and marked in the footer.

The copy uses the current role sizes, blue masthead, placed outlined SVG wordmark with a PNG
fallback, native named styles and seven embedded font faces derived from the supplied assets.
The first LibreOffice render substituted serif fonts despite correct XML declarations and
font embedding. A task-local Fontconfig configuration exposing private converted TTF copies
resolved this; no system fonts were installed. Stock Word Title borders were also removed.

All 15 pages of the final render were inspected. The repo DOCX inspector and structural
accessibility audit passed; measured rendered text contrast was at least 8.59:1. Archivo and
Inter are used for the text; the six arrow symbols in the method note use a symbol fallback
because those glyphs are absent from the supplied subset fonts. The source guide and source
fingerprint were unchanged between authoring and handoff. The repo's broader HTML contrast
check remains unavailable in its current Python environment.

The final DOCX and a private QA build record are in the current chat's `word-brand-test`
output directory. This test does not adopt a universal Word template or prove identical
rendering in every Word installation. The local skill now requires checking rendered font
use and removing inherited Title borders when authoring future Word assets.
