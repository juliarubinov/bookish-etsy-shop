# What I Can and Can't Do From This Workspace

_Checked 2026-10-15._

## Can do directly
| Capability | How | Notes |
|---|---|---|
| Web research with sources and dates | Web search | Results arrive as excerpts. Pages on etsy.com and printify.com can't be opened directly |
| Original typographic artwork at full print size | Python + Pillow, OFL fonts in `tools/fonts/` | Type, simple shapes, seals, icons. Rendered at real pixel size, never upscaled |
| Automated print QC | `tools/qc.py` | Size, real px/in, transparency, clipping, colours, text size, contrast |
| To-scale previews | `tools/build_previews.py` | Illustrative flat previews only, not photo mockups |
| Finished digital products (PDF) | reportlab | Printables with embedded fonts |
| Margin and cost models | `tools/pricing.py` | Inputs labeled with source or ESTIMATE |
| Listing drafts with Etsy limit checks | `tools/build_listings.py` | Title, tags, description, attributes, disclosures |
| Save and version everything | git → github.com/juliarubinov/bookish-etsy-shop | Pushes work |

## Needs an integration or network access (currently blocked)
| Need | Blocked by | Fix |
|---|---|---|
| Read Printify's real print areas, providers, costs, shipping | printify.com blocked by the environment's network policy; no Printify API token | Allow `printify.com` + `api.printify.com` in the environment's network settings, **or** you check them (see `verification-needed.md`). An API token would go in environment secrets, **never** in project files |
| Read Etsy fee page, rules, search results | etsy.com blocked | Allow `etsy.com`, or you check |
| USPTO trademark searches | tmsearch.uspto.gov blocked | Allow it, or you search (a trademark attorney for real clearance) |
| Photo-realistic mockups | No mockup tool | Printify's mockup generator after upload (you, or me with API access) |
| Illustrated (non-typographic) artwork | No image-generation tool here | Design briefs + editable layouts from me; illustration by you, a hired illustrator, or an image tool you choose (needs AI disclosure) |

## Needs you (manual, by design)
- Confirm budget; approve anything that costs money (samples, Etsy setup fee, ads, Printify Premium)
- Create the Etsy and Printify accounts, payments and taxes (credentials stay with you)
- Upload files to Printify and publish listings, or give me API access and approve each publish
- Order and review physical samples
- Final say on designs and shop name
