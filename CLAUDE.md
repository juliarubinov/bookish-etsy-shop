# Department of Yearning (Etsy shop): Working Notes for Claude

## Start here
1. `TASKS.md`: what's done, what's waiting, what's next
2. `decision-log.md`: decisions made and decisions pending
3. `shop-brief.md`: concept and collection
4. `research/verification-needed.md`: unverified numbers

## Folder map
- `research/`: sourced observations (with links and dates), hypotheses, verification list
- `brand/`: identity, voice, shop copy, trademark review
- `products/<slug>/`: README (spec + QC), `art/` print files, `previews/`, `files/` (digital)
- `listings/<slug>.md`: generated listing drafts (edit `tools/build_listings.py`, not the .md)
- `pricing/`: generated margins (edit inputs in `tools/pricing.py`)
- `qc/qc-report.md`: generated QC
- `tools/`: build scripts and fonts

## Rebuild everything
```
python3 tools/build_art.py && python3 tools/qc.py && python3 tools/build_previews.py
python3 tools/build_journal.py
python3 tools/pricing.py && python3 tools/build_listings.py
```
Needs Python 3 with Pillow, numpy, reportlab; `pdftoppm` for journal previews.

## Rules
- Owner's instructions: make routine reversible decisions yourself; ask before spending money, ordering samples,
  publishing listings or sending messages. Confirm budget before any cost. Never store passwords or API keys here.
- Never invent search volume, sales, revenue or trends. Label estimates. Separate observations from assumptions.
- Original wording and art only: no book quotes, characters, authors, series or franchise elements.
  Flag phrases for trademark review; never claim clearance.
- Etsy: title ≤ 140 chars, ≤ 13 tags, each ≤ 20 chars (the listing build checks this).
- Changing a print-area size: edit `SPECS` in `tools/build_art.py` and re-run. Never upscale or just change the DPI tag.
- Disclose AI assistance and Printify production in every listing.
- Update `TASKS.md`, `decision-log.md` and `launch-checklist.md` when work is done.
