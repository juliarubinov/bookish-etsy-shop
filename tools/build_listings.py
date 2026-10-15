#!/usr/bin/env python3
"""Listing drafts: single source of truth -> listings/<slug>.md, with Etsy limit checks.

    python3 tools/build_listings.py

Fails loudly if a title is > 140 chars, there are > 13 tags, a tag is > 20 chars,
or a tag/title contains a phrase on the avoid list.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

AVOID = ["booktok", "book boyfriend", "bridgerton", "acotar", "fourth wing", "romantasy",
         "taylor", "spicy book club", "smut"]

PRICES = {}
with open(ROOT / "pricing" / "pricing.csv") as f:
    for r in csv.DictReader(f):
        if r["scenario"] == "Full price":
            PRICES[r["slug"]] = (float(r["buyer_pays"]), float(r["profit"]), float(r["margin"]))

POD_DISCLOSURE = (
    "**Made to order:** this item is printed on demand by our production partner, Printify, "
    "through one of its print providers ([PROVIDER NAME — add once chosen]). "
    "Designed by Julia's Bookish World; the wording and artwork are original to this shop.")
AI_DISCLOSURE = (
    "**AI disclosure:** this design was created with the help of an AI assistant (it laid out "
    "the typography and drew the simple shapes in code, using open-license fonts). No images from "
    "other artists were used.")
POD_POLICY = (
    "**Processing & returns:** every piece is made for you after you order, so processing usually "
    "takes a few business days before shipping [confirm provider's time]. Because items are made to order, "
    "we can't accept returns for size or change of mind, but if your item arrives damaged, misprinted or "
    "defective, message us within 30 days with a photo and we'll replace it or refund you.")

LISTINGS = [
    dict(
        slug="ruined-by-chapter-twelve-tee",
        title="Ruined by Chapter Twelve Romance Reader Shirt, Bookish Garment Dyed Tee, Funny Book Lover Gift, Cozy Reading T-Shirt for Women",
        tags=["romance reader shirt", "bookish tshirt", "romance book lover", "reader gift",
              "book lover gift", "romance novel shirt", "bookworm shirt", "reading shirt",
              "book club shirt", "literary tee", "chapter shirt", "gift for readers", "romance reader gift"],
        category="Clothing › Gender-Neutral Adult Clothing › Tops & Tees › T-shirts",
        attributes={"Primary color": "Pink / Beige / Purple (per variant)", "Secondary color": "Red",
                    "Sleeve length": "Short sleeve", "Neckline": "Crew neck", "Fabric": "Cotton",
                    "Style": "Casual", "Occasion": "Birthday", "Holiday": "Valentine's Day",
                    "Who made it": "I did (designed by me, made by a production partner)",
                    "What is it": "A finished product", "When was it made": "Made to order"},
        variants="Colours: Ivory, Blossom, Orchid · Sizes: S–3XL (confirm provider range; larger sizes may cost more)",
        opening="For every reader whose book got them at chapter twelve. A soft, garment-dyed tee with original serif lettering in wine and deep plum.",
        details=["Unisex relaxed fit (Comfort Colors 1717 heavyweight garment-dyed tee). Women may want one size down for a closer fit.",
                 "100% ring-spun cotton [confirm on Printify listing]",
                 "Front print, about 12 in wide (same print size on every shirt size); direct-to-garment printed",
                 "Garment dyeing means every shirt's colour varies slightly; that's part of the charm"],
        care="Machine wash cold inside out, tumble dry low, do not iron directly on the print.",
        photos=["Printify flat-lay mockup, Blossom (thumbnail)", "Model mockup, Ivory", "Close-up of lettering",
                "Lifestyle: folded tee with a stack of paperbacks (no readable covers)", "All three colours", "Size chart"],
    ),
    dict(
        slug="yearning-night-shift-sweatshirt",
        title="Department of Yearning Night Shift Sweatshirt, Romance Reader Crewneck, Bookish Gift, Late Night Reading Sweater, Moon Book Lover",
        tags=["romance reader gift", "bookish sweatshirt", "night reader", "book lover crewneck",
              "reading sweatshirt", "yearning sweatshirt", "romance book merch", "bookworm sweater",
              "cozy reading top", "book club gift", "gift for book lover", "slow burn reader", "moon and books"],
        category="Clothing › Gender-Neutral Adult Clothing › Hoodies & Sweatshirts › Sweatshirts",
        attributes={"Primary color": "Beige / Pink / White (per variant)", "Secondary color": "Red",
                    "Sleeve length": "Long sleeve", "Neckline": "Crew neck", "Fabric": "Cotton blend",
                    "Style": "Casual", "Holiday": "Christmas", "Occasion": "Birthday",
                    "Who made it": "I did (designed by me, made by a production partner)",
                    "What is it": "A finished product", "When was it made": "Made to order"},
        variants="Colours: Sand, Light Pink, White · Sizes: S–3XL (confirm)",
        opening="Official issue for readers on the night shift: still up, still turning pages, still yearning. A cozy crewneck with an original Department of Yearning seal.",
        details=["Unisex classic fit (Gildan 18000 Heavy Blend crewneck)",
                 "50% cotton / 50% polyester [confirm on Printify listing]",
                 "Front print, about 11.5 in wide (same on every size)",
                 "Original seal artwork: crescent moon, stars and two tiny hearts"],
        care="Machine wash cold inside out, tumble dry low, do not iron the print.",
        photos=["Printify mockup, Sand (thumbnail)", "Model mockup, Light Pink", "Close-up of seal",
                "Lifestyle: sweatshirt with a reading lamp and an open book", "Colour options", "Size chart"],
    ),
    dict(
        slug="yearning-morning-shift-mug",
        shelved=True,
        title="Coffee First Then Yearning Mug, Romance Reader Coffee Mug, Bookish Gift for Book Lovers, Department of Yearning 11oz Ceramic Cup",
        tags=["romance reader mug", "bookish mug", "book lover mug", "reading coffee mug",
              "gift for readers", "book club gift", "romance book gift", "bookworm mug",
              "yearning mug", "book lover gift", "funny reader mug", "coffee and books", "reader coffee cup"],
        category="Home & Living › Kitchen & Dining › Drink & Barware › Drinkware › Mugs",
        attributes={"Primary color": "White", "Secondary color": "Red", "Material": "Ceramic",
                    "Capacity": "11 fl oz", "Occasion": "Birthday", "Holiday": "Valentine's Day",
                    "Who made it": "I did (designed by me, made by a production partner)",
                    "What is it": "A finished product", "When was it made": "Made to order"},
        variants="11oz (add 15oz later only after checking that the artwork fits its wrap)",
        opening="Morning shift at the Department of Yearning: coffee first, then back to the book. Printed on both sides, so it reads right in either hand.",
        details=["11 oz white ceramic mug [confirm provider]",
                 "Side one: Department of Yearning, Morning Shift seal. Side two: \"Coffee first. Then yearning.\"",
                 "Sublimation printed in wine and deep plum",
                 "Microwave & dishwasher safe [confirm for chosen provider]"],
        care="Hand washing keeps the print bright longest.",
        photos=["Printify mockup, wording side (thumbnail)", "Seal side", "Both sides together",
                "Lifestyle: mug beside an open paperback", "Size reference in hand"],
    ),
    dict(
        slug="contents-tote",
        shelved=True,
        title="Contents Books Snacks Unresolved Tension Tote Bag, Romance Reader Canvas Book Bag, Funny Bookish Gift, Library Tote for Book Lovers",
        tags=["bookish tote bag", "library tote", "romance reader tote", "book lover tote",
              "canvas book bag", "reader gift", "book club tote", "funny tote bag", "bookstore tote",
              "gift for readers", "romance book gift", "bookworm bag", "book haul bag"],
        category="Bags & Purses › Totes",
        attributes={"Primary color": "Beige", "Secondary color": "Red", "Material": "Cotton canvas",
                    "Occasion": "Birthday", "Holiday": "Christmas",
                    "Who made it": "I did (designed by me, made by a production partner)",
                    "What is it": "A finished product", "When was it made": "Made to order"},
        variants="One size, 15 × 16 in, natural canvas",
        opening="An honest inventory for library runs and bookstore hauls: books (too many), snacks, and unresolved tension.",
        details=["Natural cotton canvas tote, 15 × 16 in [confirm provider]",
                 "Front print, about 8 × 10 in",
                 "Long handles for the shoulder",
                 "Original checklist design in wine and deep plum"],
        care="Spot clean or hand wash cold; air dry.",
        photos=["Printify mockup (thumbnail)", "Lifestyle: tote with books peeking out", "Close-up of print",
                "Size reference on shoulder"],
    ),
    dict(
        slug="will-they-tee",
        title="Will They They Will Romance Reader Shirt, Funny Bookish Tee, Garment Dyed Book Lover Gift, Subtle Romance Novel T-Shirt for Readers",
        tags=["romance reader shirt", "funny bookish shirt", "book lover gift", "romance novel shirt",
              "reader gift", "bookworm shirt", "book club shirt", "subtle book shirt", "reading tshirt",
              "gift for readers", "romance trope shirt", "happy ending shirt", "literary tee"],
        category="Clothing › Gender-Neutral Adult Clothing › Tops & Tees › T-shirts",
        attributes={"Primary color": "Beige / Pink / Purple (per variant)", "Secondary color": "Red",
                    "Sleeve length": "Short sleeve", "Neckline": "Crew neck", "Fabric": "Cotton",
                    "Style": "Minimalist", "Occasion": "Birthday", "Holiday": "Valentine's Day",
                    "Who made it": "I did (designed by me, made by a production partner)",
                    "What is it": "A finished product", "When was it made": "Made to order"},
        variants="Colours: Ivory, Blossom, Orchid · Sizes: S–3XL (confirm provider range; larger sizes may cost more)",
        opening="For readers who already know how it ends and read every page anyway. Two lines of original lettering: the question, then the answer, in wine italic.",
        details=["Unisex relaxed fit (Comfort Colors 1717 heavyweight garment-dyed tee). Women may want one size down for a closer fit.",
                 "100% ring-spun cotton [confirm on Printify listing]",
                 "Front print, about 12 in wide (same print size on every shirt size); direct-to-garment printed",
                 "Garment dyeing means every shirt's colour varies slightly; that's part of the charm"],
        care="Machine wash cold inside out, tumble dry low, do not iron directly on the print.",
        photos=["Printify flat-lay mockup, Ivory (thumbnail)", "Model mockup, Blossom", "Close-up of lettering",
                "Lifestyle: tee with a paperback (no readable covers)", "All three colours", "Size chart"],
    ),
    dict(
        slug="pining-professionally-sweatshirt",
        title="Pining Professionally Sweatshirt, Romance Reader Crewneck, Funny Bookish Gift, Cozy Book Lover Sweater, Subtle Romance Novel Pullover",
        tags=["romance reader gift", "bookish sweatshirt", "book lover crewneck", "reading sweatshirt",
              "pining sweatshirt", "romance book merch", "bookworm sweater", "cozy reading top",
              "book club gift", "gift for book lover", "funny book sweater", "slow burn reader", "pine tree sweater"],
        category="Clothing › Gender-Neutral Adult Clothing › Hoodies & Sweatshirts › Sweatshirts",
        attributes={"Primary color": "Beige / Pink / White (per variant)", "Secondary color": "Red",
                    "Sleeve length": "Long sleeve", "Neckline": "Crew neck", "Fabric": "Cotton blend",
                    "Style": "Minimalist", "Holiday": "Christmas", "Occasion": "Birthday",
                    "Who made it": "I did (designed by me, made by a production partner)",
                    "What is it": "A finished product", "When was it made": "Made to order"},
        variants="Colours: Sand, Light Pink, White · Sizes: S–3XL (confirm)",
        opening="Some people pine for the weekend. You pine for two fictional people to finally say it. An original pine-sprig design, with a tiny heart, for the professionally yearning.",
        details=["Unisex classic fit (Gildan 18000 Heavy Blend crewneck)",
                 "50% cotton / 50% polyester [confirm on Printify listing]",
                 "Front print, about 11 in wide (same on every size)",
                 "Original artwork: a drawn pine sprig ending in a tiny heart, with serif and italic lettering"],
        care="Machine wash cold inside out, tumble dry low, do not iron the print.",
        photos=["Printify mockup, Sand (thumbnail)", "Model mockup, Light Pink", "Close-up of pine sprig",
                "Lifestyle: crewneck with a stack of books and a mug", "Colour options", "Size chart"],
    ),
    dict(
        slug="yearning-log-printable",
        title="Romance Reading Journal Printable, Book Tracker and Trope Tracker PDF, Reading Log for Book Lovers, TBR List, Instant Download",
        tags=["reading journal", "romance reading log", "book tracker", "printable book log",
              "trope tracker", "reading tracker pdf", "book review template", "tbr list printable",
              "bookish printable", "reading planner", "book journal pdf", "romance reader gift", "reading challenge"],
        category="Paper & Party Supplies › Paper › Calendars & Planners",
        attributes={"Primary color": "Pink", "Secondary color": "Red", "Occasion": "New Year",
                    "Who made it": "I did", "What is it": "A finished product",
                    "When was it made": "2020-2026", "Type": "Digital download"},
        variants="Instant download: US Letter + A4 PDFs, 9 pages each",
        opening="The Yearning Log is a printable reading journal made for romance readers. Rate the yearning, the spice and the ending, and track every trope you can't resist.",
        details=["2 PDFs: US Letter (8.5 × 11 in) and A4, 9 pages each",
                 "Includes: cover, how-to page, Book Record (print as many as you like), Trope Tracker (16 tropes + 4 of your own), Spine Shelf (52 books), TBR & Wishlist",
                 "Print at home or at a print shop at 100% / actual size",
                 "For personal use only; please don't resell or share the files",
                 "This is a digital file. Nothing physical will be shipped."],
        care="",
        photos=["Cover + 3 inner pages fanned (thumbnail)", "Book Record page", "Trope Tracker",
                "Spine Shelf partly coloured in", "What's included list", "Printed and on a clipboard (photo after printing)"],
        digital=True,
    ),
]


def check(L):
    errs = []
    if len(L["title"]) > 140:
        errs.append(f"title {len(L['title'])} chars")
    if len(L["tags"]) > 13:
        errs.append(f"{len(L['tags'])} tags")
    if len(set(L["tags"])) != len(L["tags"]):
        errs.append("duplicate tags")
    for t in L["tags"]:
        if len(t) > 20:
            errs.append(f"tag too long: {t} ({len(t)})")
    blob = (L["title"] + " " + " ".join(L["tags"])).lower()
    for a in AVOID:
        if a in blob:
            errs.append(f"avoid-list phrase: {a}")
    return errs


def render(L):
    price, profit, margin = PRICES[L["slug"]]
    digital = L.get("digital")
    out = [f"# Listing — {L['slug']}", "",
           f"- **Product file:** `products/{L['slug']}/README.md`",
           "- **Status:** draft (not published; needs owner approval)",
           f"- **Category:** {L['category']}",
           f"- **Price:** ${price:.2f}{'' if digital else ' with free US shipping'} · est. profit ${profit:.2f} ({margin * 100:.0f}%), see `pricing/pricing.md`",
           f"- **Variations:** {L['variants']}", "",
           f"## Title ({len(L['title'])}/140)", "", L["title"], "",
           f"## Tags ({len(L['tags'])}/13)", ""]
    out += [f"{i}. {t} ({len(t)})" for i, t in enumerate(L["tags"], 1)]
    out += ["", "## Attributes", ""] + [f"- **{k}:** {v}" for k, v in L["attributes"].items()]
    out += ["", "## Description", "", L["opening"], "", "**Details**", ""]
    out += [f"- {d}" for d in L["details"]]
    if L["care"]:
        out += ["", f"**Care:** {L['care']}"]
    out += [""]
    if digital:
        out += ["**Instant download:** your files are ready right after purchase from Purchases & Reviews on Etsy. "
                "Because it's a digital file, all sales are final, but if a file won't open, message us and we'll help.",
                "", AI_DISCLOSURE.replace("this design", "this printable's layout")]
    else:
        out += [POD_POLICY, "", POD_DISCLOSURE, "", AI_DISCLOSURE]
    out += ["", "Every word and drawing here is original. There are no book quotes, characters or series references.",
            "", "## Photos (in order)", ""]
    out += [f"{i}. {p}" for i, p in enumerate(L["photos"], 1)]
    if not digital:
        out += ["", "_Use Printify's mockup generator for photos 1–3 once the file is uploaded. The previews in "
                "`products/<slug>/previews/` are illustrative only and should not be used as listing photos._"]
    return "\n".join(out) + "\n"


def main():
    bad = False
    for L in LISTINGS:
        errs = check(L)
        if errs:
            bad = True
            print(L["slug"], "FAIL:", errs)
        else:
            print(L["slug"], f"OK title {len(L['title'])}/140, {len(L['tags'])} tags, longest tag "
                  f"{max(len(t) for t in L['tags'])}/20")
        folder = ROOT / "listings" / ("shelved" if L.get("shelved") else "")
        folder.mkdir(exist_ok=True)
        (folder / f"{L['slug']}.md").write_text(render(L))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
