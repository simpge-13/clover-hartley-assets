#!/usr/bin/env python3
"""Clover Hartley social — Week 3 (Fri 13 – Thu 19 Nov 2026), theme "Gift & plan".
Builds IG posts (1080x1350) + Pinterest pins (1000x1500) into out/, plus week3.json and the three Metricool CSVs.
Templates carried over from week2.py (ig_photo / ig_before / ig_text / ig_covers / ig_offer / pin photo|page|split)
plus ig_list (numbered gift list) and pin mode "covers".
Needs: ./fonts/Fredoka.ttf + Lora.ttf, ./gen/c_*.jpg (Playground coloured-in mockups), ./src/*.jpg (page crops)."""
import csv, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

B = os.path.dirname(os.path.abspath(__file__))
GEN, SRC, OUT = f"{B}/gen", f"{B}/src", f"{B}/out"
REPO_IMG = os.path.abspath(f"{B}/../../images")
os.makedirs(OUT, exist_ok=True)
RAW = "https://raw.githubusercontent.com/simpge-13/clover-hartley-assets/main/social/week3/"

LD = dict(bg="#FFF3DC", band="#2F7D4F", ink="#1B3358", acc="#F26A21", font="Fredoka", tag="Little Dinkums")
LW = dict(bg="#F6EFE3", band="#3F5E4A", ink="#3B3A36", acc="#C4663F", font="Lora", tag="Long Weekend")
CH = dict(bg="#FFF3DC", band="#1B3358", ink="#1B3358", acc="#F26A21", font="Fredoka", tag="Clover Hartley")  # whole-range posts

def F(name, size, w="Bold"):
    f = ImageFont.truetype(f"{B}/fonts/{name}.ttf", size)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f

def wrap(d, text, f, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split(" "):
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
    return lines

def text_block(d, x, y, text, f, fill, maxw, lh):
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill); y += lh
    return y

def cover(im, W, H):
    return ImageOps.fit(im.convert("RGB"), (W, H), Image.LANCZOS, centering=(0.5, 0.5))

def card(base, art, box, shadow=True):
    x0, y0, x1, y1 = box
    if shadow:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x0+6, y0+12, x1+6, y1+12), 18, fill=(0, 0, 0, 55))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(base).rounded_rectangle(box, 18, fill="white")
    pad = 26; a = ImageOps.contain(art.convert('RGB'), (x1-x0-2*pad, y1-y0-2*pad), Image.LANCZOS)
    base.paste(a, (x0+(x1-x0-a.width)//2, y0+(y1-y0-a.height)//2))

def pill(d, x, y, text, f, fill, color="white", right=False, padx=22, h=None):
    w = d.textlength(text, font=f); h = h or int(f.size*1.75)
    if right: x = x - w - 2*padx
    d.rounded_rectangle((x, y, x+w+2*padx, y+h), h//2, fill=fill); d.text((x+padx, y+(h-f.size)/2-f.size*0.12), text, font=f, fill=color)

def book_shadowed(im, path, x, y, w):
    c = Image.open(path).convert("RGB"); c = c.resize((w, round(w*c.height/c.width)), Image.LANCZOS)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((x+8, y+14, x+w+8, y+c.height+14), fill=(0, 0, 0, 60))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); im.paste(c, (x, y)); return c.height

# ---------------- IG templates (1080x1350) ----------------
def ig_photo(photo, label, S, out):
    im = cover(Image.open(photo), 1080, 1350).convert("RGBA"); d = ImageDraw.Draw(im)
    f = F(S["font"], 30, "SemiBold"); pill(d, 40, 1350-40-54, label, f, S["band"], h=54)
    im.convert("RGB").save(out, quality=90)

def ig_before(art, head, sub, S, out):
    im = Image.new("RGBA", (1080, 1350), S["bg"]); d = ImageDraw.Draw(im)
    pill(d, 60, 56, S["tag"], F(S["font"], 26, "SemiBold"), S["band"], h=46)
    d.text((60, 122), head, font=F(S["font"], 58), fill=S["ink"])
    card(im, Image.open(art), (150, 230, 930, 1190)); d = ImageDraw.Draw(im)
    d.text((60, 1236), sub, font=F(S["font"], 30, "Medium"), fill=S["ink"])
    t = "cloverhartley.com"; f = F(S["font"], 28, "Medium"); d.text((1020-d.textlength(t, font=f), 1240), t, font=f, fill=S["acc"])
    im.convert("RGB").save(out, quality=90)

def ig_text(head, body, S, out, art=None, num=None):
    im = Image.new("RGBA", (1080, 1350), S["band"]); d = ImageDraw.Draw(im)
    y = 90
    if num: pill(d, 60, y, num, F(S["font"], 30, "SemiBold"), S["acc"], h=56); y += 96
    fh = F(S["font"], 84); y = text_block(d, 60, y, head, fh, "white", 960, 100) + 40
    fb = F(S["font"], 46, "Regular" if S is LW else "Medium"); y = text_block(d, 60, y, body, fb, "#FFFFFF", 960, 66)
    if art:
        a = ImageOps.contain(Image.open(art).convert("RGB"), (330, 410), Image.LANCZOS)
        card(im, a, (1020-a.width-40, 1350-80-a.height-40, 1020, 1350-80), shadow=False); d = ImageDraw.Draw(im)
    d.text((60, 1350-80), "@cloverhartley  ·  cloverhartley.com", font=F(S["font"], 28, "Medium"), fill="#FFFFFF")
    im.convert("RGB").save(out, quality=90)

def ig_covers(paths, head, head2, foot, S, out):
    im = Image.new("RGBA", (1080, 1350), S["bg"]); d = ImageDraw.Draw(im)
    d.text((60, 90), head, font=F(S["font"], 72), fill=S["ink"]); d.text((60, 175), head2, font=F(S["font"], 72), fill=S["acc"])
    n = len(paths); w = {2: 430, 3: 300}.get(n, 180); gap = 60 if n <= 3 else 24
    x = (1080 - (n*w + (n-1)*gap))//2
    for p in paths:
        c = Image.open(p).convert("RGB"); hh = round(w*c.height/c.width)
        y = 380 + (560 - hh)//2
        book_shadowed(im, p, x, y, w); x += w + gap
    d = ImageDraw.Draw(im); text_block(d, 60, 1130, foot, F(S["font"], 34, "Medium"), S["ink"], 960, 48)
    im.convert("RGB").save(out, quality=90)

def ig_offer(head, S, out, cover_path=None):
    im = Image.new("RGBA", (1080, 1350), S["bg"]); d = ImageDraw.Draw(im)
    text_block(d, 60, 110, head, F(S["font"], 70), S["ink"], 960, 86)
    book_shadowed(im, cover_path or f"{REPO_IMG}/lw-christmas-cover.jpg", (1080-440)//2, 250, 440); d = ImageDraw.Draw(im)
    d.text((60, 900), "15% off printable PDFs with code", font=F(S["font"], 38, "Medium"), fill=S["ink"])
    d.text((60, 960), "LAUNCH15", font=F(S["font"], 120), fill=S["band"])
    d.text((60, 1120), "cloverhartley.com  ·  until 30 Nov", font=F(S["font"], 34, "Medium"), fill=S["acc"])
    im.convert("RGB").save(out, quality=90)

def ig_list(head, items, S, out):
    """Gift list: heading + rows of (cover, who, what)."""
    im = Image.new("RGBA", (1080, 1350), S["bg"]); d = ImageDraw.Draw(im)
    d.text((60, 70), head, font=F(S["font"], 64), fill=S["ink"])
    y = 175; rowh = 262
    for cov, who, what in items:
        h = book_shadowed(im, cov, 70, y, 190); d = ImageDraw.Draw(im)
        d.text((300, y+44), who, font=F(S["font"], 44), fill=S["acc"])
        text_block(d, 300, y+108, what, F(S["font"], 34, "Medium"), S["ink"], 700, 46)
        y += rowh
    d.text((60, 1350-90), "All five at cloverhartley.com  ·  LAUNCH15 = 15% off until 30 Nov", font=F(S["font"], 28, "Medium"), fill=S["ink"])
    im.convert("RGB").save(out, quality=90)

# ---------------- Pin templates (1000x1500) ----------------
def pin(img, title, sub, S, out, mode="photo", img2=None):
    im = Image.new("RGBA", (1000, 1500), S["bg"])
    if mode == "photo":
        im.paste(cover(Image.open(img), 1000, 1040), (0, 0))
    elif mode == "page":
        card(im, Image.open(img), (110, 70, 890, 1000))
    elif mode == "split":   # before | after
        a = Image.open(img).convert("RGB"); b = cover(Image.open(img2), 470, 880)
        card(im, a, (20, 140, 490, 1020), shadow=False); im.paste(b, (510, 140))
        d = ImageDraw.Draw(im); fl = F(S["font"], 40, "SemiBold")
        d.text((30, 70), "Before", font=fl, fill=S["ink"]); d.text((520, 70), "After", font=fl, fill=S["acc"])
    elif mode == "covers":
        paths = img; n = len(paths); w = 184 if n == 5 else 260; gap = 14 if n == 5 else 40
        x = (1000 - (n*w + (n-1)*gap))//2
        for p in paths:
            c = Image.open(p); hh = round(w*c.height/c.width); y = 120 + (820-hh)//2
            book_shadowed(im, p, x, y, w); x += w + gap
    d = ImageDraw.Draw(im)
    pill(d, 965, 30, S["tag"], F(S["font"], 24, "SemiBold"), S["acc"], right=True, h=44)
    d.rectangle((0, 1040, 1000, 1500), fill=S["band"])
    y = text_block(d, 50, 1080, title, F(S["font"], 52), "white", 900, 64) + 8
    text_block(d, 50, y, sub, F(S["font"], 30, "Medium" if S is not LW else "Regular"), "#FFFFFF", 900, 40)
    d.text((50, 1440), "Printable PDF  ·  cloverhartley.com", font=F(S["font"], 28, "SemiBold" if S is not LW else "Medium"), fill="#FFFFFF")
    im.convert("RGB").save(out, quality=90)

# ---------------- links ----------------
P = "https://cloverhartley.com/products/"
LINK = {
    "ld_xmas": P + "little-dinkums-christmas-colouring-book-printable-pdf-a4-us-letter",
    "ld_aussie": P + "little-dinkums-aussie-christmas-colouring-book-printable-pdf-a4-us-letter",
    "ld_animals": P + "little-dinkums-aussie-animals-colouring-book-printable-pdf-a4-us-letter",
    "lw_xmas": P + "long-weekend-christmas-a-calm-cosy-colouring-book-printable-pdf-a4-us-letter",
    "lw_beach": P + "long-weekend-the-beach-a-calm-cosy-colouring-book-printable-pdf-a4-us-letter",
    "ld_coll": "https://cloverhartley.com/collections/little-dinkums-ages-2-8",
    "lw_coll": "https://cloverhartley.com/collections/long-weekend-adults",
    "all": "https://cloverhartley.com/collections/all",
}
def utm(k, n): return f"{LINK[k]}?utm_source=pinterest&utm_medium=social&utm_campaign=launch&utm_content=w3pin{n:02d}"

g = lambda n: f"{GEN}/c_{n}.jpg"; s = lambda n: f"{SRC}/{n}.jpg"; cv = lambda n: f"{REPO_IMG}/{n}-cover.jpg"
LD_COVERS = [cv("ld-christmas"), cv("ld-aussie-christmas"), cv("ld-aussie-animals")]
ALL_COVERS = LD_COVERS + [cv("lw-christmas"), cv("lw-beach")]

# ---------------- Instagram posts ----------------
IG = [
 dict(day=15, date="2026-11-13", time="12:30", kind="Carousel · 3", theme="Teachers & classrooms",
  caption="""Teachers: the last few weeks of term, sorted. 🖍️

One PDF, printed as many times as you need — a page for every kid in the room, spares for the ones who finish first, and nothing to pack away at 3:30.

The Aussie Animals pages are the quiet ones: big, thick lines so Preps can manage them, and a kookaburra, a wombat and a platypus to talk about while they colour.

Little Dinkums printables: Christmas, Aussie Christmas and Aussie Animals. A4 and US Letter, single-sided. Link in bio.

#teachersofinstagram #aussieteachers #primaryteacher #earlychildhoodeducation #kindyteacher #classroomactivities #endofyear #endofterm #christmasintheclassroom #oshc #homeschoolaustralia #printables #cloverhartley #littledinkums""",
  slides=[("photo", g("class"), "Little Dinkums: Aussie Animals", LD),
          ("text", "One PDF. The whole class.", "•  Print a page per kid, plus spares\n•  A4 + US Letter in every book\n•  Single-sided — textas don't bleed through\n•  Thick lines made for little hands\n\nBuy once, print all term.", LD, s("aa_wombat"), "For teachers"),
          ("before", s("aa_kook"), "Meet the kookaburra.", "Little Dinkums: Aussie Animals · 50 pages", LD)]),
 dict(day=16, date="2026-11-14", time="19:30", kind="Carousel · 3", theme="Stocking stuffers",
  caption="""Stocking stuffers that aren't lollies, batteries or tiny plastic things. 🎄

A Little Dinkums paperback is flat, light and keeps a small person busy on Christmas afternoon — which is roughly when you'll need it most.

Three to choose from: Christmas, Aussie Christmas and the new Aussie Animals. Paperbacks on Amazon; printable PDFs on cloverhartley.com if you'd rather print the pages yourself. Link in bio.

#stockingstuffers #stockingfillers #christmasgiftideas #giftsforkids #toddlergifts #kidschristmas #aussiechristmas #colouringbook #christmasshopping #giftguide #australianmum #cloverhartley #littledinkums""",
  slides=[("photo", g("stocking"), "Little Dinkums: Christmas", LD),
          ("covers", LD_COVERS, "Stocking stuffers,", "sorted.", "Little Dinkums paperbacks — big & easy colouring for ages 2–8. Christmas · Aussie Christmas · Aussie Animals. Paperbacks on Amazon, printable PDFs at cloverhartley.com", LD),
          ("before", s("ldx_ginger"), "Gingerbread, obviously.", "Little Dinkums: Christmas · 50 pages", LD)]),
 dict(day=17, date="2026-11-15", time="19:30", kind="Carousel · 3", theme="A gift for mum",
  caption="""For the mum who says she doesn't want anything. 🌿

Print the pages, tie them with a ribbon, add a tin of pencils. That's a gift that gives her an excuse to sit down — and nobody has to pretend to like a candle.

Long Weekend: The Beach is 42 pages of the Australian coast: beach boxes, rock pools, a pelican on a pier, a hammock at sunset. Bold botanical lines, medium detail, no fiddly bits.

Printable PDF at cloverhartley.com — and LAUNCH15 takes 15% off until 30 Nov. Link in bio.

#giftsformum #christmasgiftsforher #giftsforher #adultcolouring #colouringforadults #mindfulcolouring #selfcaregifts #thoughtfulgifts #beachvibes #australianbeach #slowliving #cloverhartley #longweekend""",
  slides=[("photo", g("gift"), "Long Weekend: The Beach", LW),
          ("covers", [cv("lw-christmas"), cv("lw-beach")], "For mum.", "Or for you.", "Long Weekend — calm & cosy colouring for grown-ups. Christmas (42 pages) · The Beach (42 pages). Printable PDFs at cloverhartley.com", LW),
          ("before", s("bch_hammock"), "The hammock page.", "Long Weekend: The Beach · 42 pages", LW)]),
 dict(day=18, date="2026-11-16", time="19:30", kind="Carousel · 4", theme="Aussie Animals poll",
  caption="""Settle this for us: which one gets coloured first? 👇

1️⃣ The quokka taking a selfie
2️⃣ The koala asleep in the gum tree
3️⃣ The wombat coming out of the burrow
4️⃣ The platypus in the creek

All four are in Little Dinkums: Aussie Animals — 50 big & easy pages of the animals Aussie kids actually see (or at least hear about at kindy). Ages 2–8. Printable PDF, link in bio.

#aussieanimals #australiananimals #quokka #koala #wombat #platypus #kidscolouring #colouringpages #toddleractivities #preschoolactivities #australiankids #cloverhartley #littledinkums""",
  slides=[("photo", g("quokka"), "Little Dinkums: Aussie Animals", LD),
          ("before", s("aa_koala"), "2. The koala.", "Little Dinkums: Aussie Animals", LD),
          ("before", s("aa_wombat"), "3. The wombat.", "Little Dinkums: Aussie Animals", LD),
          ("before", s("aa_platypus"), "4. The platypus.", "Little Dinkums: Aussie Animals", LD)]),
 dict(day=19, date="2026-11-17", time="19:30", kind="Carousel · 4", theme="School holidays plan",
  caption="""Six weeks of school holidays. One printer. Here's the plan. 📋

1. Print a stack now, while you've got ink and patience
2. Keep it in a folder with a pencil case — one grab on the way out the door
3. Ration it: a page for the café, a page for the car, a page for Christmas Day while the prawns go round

Little Dinkums Christmas, Aussie Christmas and Aussie Animals, all printable at home. Buy once, print all summer. Link in bio.

#schoolholidays #summerholidays #schoolholidayactivities #holidayactivities #kidsactivities #roadtripwithkids #mumhacks #parentinghacks #printables #printablecolouring #australianmum #cloverhartley #littledinkums""",
  slides=[("photo", g("kit"), "Little Dinkums printables", LD),
          ("text", "1. Print the stack now", "Open the PDF, hit \"Fit to page\", print 20 or 30 pages in one go.\n\nMix the books — a few animals, a few Christmas ones.", LD, s("aa_roo"), "Step 1"),
          ("text", "2. Folder + pencil case", "Keep the stack in a manila folder with a zip case of pencils.\n\nIt lives in the car or the tote bag. One grab, no packing.", LD, None, "Step 2"),
          ("text", "3. Ration it", "•  A page for the café\n•  A page for the car\n•  A page for the cousins\n•  A page for Christmas Day\n\nRun out? Print it again.", LD, s("ldx_penguin"), "Step 3")]),
 dict(day=20, date="2026-11-18", time="19:30", kind="Single", theme="The Beach in use",
  caption="""Beach boxes, a cup of tea, and absolutely nowhere to be. 🌊

Half a page in, pencils everywhere. This one's from Long Weekend: The Beach — 42 pages of the Australian coast drawn in bold botanical lines: banksia, pandanus, pelicans, rock pools and a very Melbourne row of beach boxes.

Medium detail. Enough to lose an hour in; never so much it turns into homework.

Printable PDF. Link in bio.

#adultcolouring #colouringforadults #mindfulcolouring #beachboxes #brightonbeach #australianbeach #coastalliving #colouredpencils #slowliving #selfcare #botanicalcolouring #cloverhartley #longweekend""",
  slides=[("photo", g("boxes"), "Long Weekend: The Beach", LW)]),
 dict(day=21, date="2026-11-19", time="19:30", kind="Carousel · 3", theme="Gift list + LAUNCH15",
  caption="""The Clover Hartley gift list, one line each: 🎁

🦘 For the toddler — Little Dinkums: Aussie Animals
🎄 For the kid who's counting sleeps — Little Dinkums: Christmas (or Aussie Christmas, if the North Pole feels a long way from the beach)
🌿 For mum, nan or the friend who's had a year — Long Weekend: The Beach or Christmas
🖍️ For the teacher — a printable they can use for the whole class

Printable PDFs on cloverhartley.com; Little Dinkums paperbacks on Amazon. Code LAUNCH15 takes 15% off every printable until 30 Nov. Link in bio.

#giftguide #christmasgiftguide #christmasgiftideas #giftsforkids #giftsformum #teachergifts #colouringbook #adultcolouring #kidscolouring #aussiechristmas #shopsmallaustralia #cloverhartley #littledinkums #longweekend""",
  slides=[("list", "The gift list.", [(cv("ld-aussie-animals"), "For the toddler", "Little Dinkums: Aussie Animals — 50 big & easy pages, ages 2–8"),
                                      (cv("ld-christmas"), "For the sleep-counter", "Little Dinkums: Christmas, or Aussie Christmas for a hot one"),
                                      (cv("lw-beach"), "For mum (or nan)", "Long Weekend: The Beach — 42 calm, cosy pages of the coast"),
                                      (cv("ld-aussie-christmas"), "For the teacher", "Any printable — buy once, print for the whole class")], CH),
          ("offer", "Colour their Christmas in.", LW, cv("lw-beach")),
          ("covers", ALL_COVERS, "All five.", "Printable at home.", "Little Dinkums (ages 2–8): Christmas · Aussie Christmas · Aussie Animals. Long Weekend (grown-ups): Christmas · The Beach. cloverhartley.com", CH)]),
]

# ---------------- Pins ----------------
PINS = [
 (1, "2026-11-13", "10:00", "photo", g("class"), None, LD, "Printable Activities for Kids", "ld_animals",
  "Colouring pages for the classroom — print one per kid", "Little Dinkums: Aussie Animals · ages 2–8",
  "Printable colouring pages for the classroom: buy one PDF and print a page for every child, with spares. Little Dinkums: Aussie Animals — 50 big, easy Australian animal pages for ages 2–8, A4 and US Letter, single-sided."),
 (2, "2026-11-13", "19:00", "page", s("aa_koala"), None, LD, "Printable Activities for Kids", "ld_animals",
  "Koala colouring page for kids", "Little Dinkums: Aussie Animals · 50 pages",
  "A sleepy koala hugging a gum tree — a big, easy colouring page for toddlers and preschoolers from Little Dinkums: Aussie Animals. 50 printable Australian animal pages, ages 2–8."),
 (3, "2026-11-14", "10:00", "photo", g("stocking"), None, LD, "Christmas Colouring Pages for Kids", "ld_xmas",
  "Stocking stuffer idea: a Christmas colouring book", "Little Dinkums: Christmas · paperback or printable",
  "Stocking stuffer idea for kids: a flat, light Christmas colouring book with 50 big, easy pages. Little Dinkums: Christmas — paperback on Amazon or printable PDF at cloverhartley.com."),
 (4, "2026-11-14", "19:00", "page", s("ldx_ginger"), None, LD, "Christmas Colouring Pages for Kids", "ld_xmas",
  "Gingerbread house colouring page for kids", "Little Dinkums: Christmas · ages 2–8",
  "A gingerbread man outside his gingerbread house — a simple, bold Christmas colouring page for ages 2–8 from Little Dinkums: Christmas. 50 printable pages, A4 and US Letter."),
 (5, "2026-11-15", "10:00", "photo", g("gift"), None, LW, "Colouring Pages for Adults", "lw_beach",
  "Gift idea for mum: printed colouring pages + a tin of pencils", "Long Weekend: The Beach · for grown-ups",
  "A thoughtful Christmas gift for mum: print the pages of Long Weekend: The Beach, tie them with a ribbon and add a tin of coloured pencils. 42 calm, cosy Australian coast colouring pages, printable PDF."),
 (6, "2026-11-15", "19:00", "page", s("bch_hammock"), None, LW, "Colouring Pages for Adults", "lw_beach",
  "Hammock at sunset — beach colouring page for adults", "Long Weekend: The Beach · 42 pages",
  "A hammock strung between pandanus palms at sunset, frangipani in the foreground — a calm adult colouring page from Long Weekend: The Beach. 42 printable pages of the Australian coast."),
 (7, "2026-11-16", "10:00", "photo", g("quokka"), None, LD, "Printable Activities for Kids", "ld_animals",
  "Quokka selfie colouring page — coloured in!", "Little Dinkums: Aussie Animals · ages 2–8",
  "A quokka taking a selfie, coloured in with crayons. One of 50 big, easy Australian animal colouring pages for kids in Little Dinkums: Aussie Animals. Printable PDF, A4 and US Letter."),
 (8, "2026-11-16", "19:00", "page", s("bch_pelican"), None, LW, "Colouring Pages for Adults", "lw_beach",
  "Pelican on the pier — coastal colouring page for adults", "Long Weekend: The Beach",
  "A pelican on a pier post with fishing boats and a lighthouse behind — an adult colouring page from Long Weekend: The Beach, 42 calm pages of the Australian coast in bold botanical lines. Printable PDF."),
 (9, "2026-11-17", "10:00", "photo", g("kit"), None, LD, "Printable Activities for Kids", "ld_coll",
  "School holiday boredom buster: print a colouring stack", "Folder + pencil case = one grab on the way out",
  "School holiday activity idea: print a stack of colouring pages, keep them in a folder with a pencil case, and grab it for the café, the car and Christmas Day. Little Dinkums printable colouring books, ages 2–8."),
 (10, "2026-11-17", "19:00", "page", s("aa_wombat"), None, LD, "Printable Activities for Kids", "ld_animals",
  "Wombat colouring page for toddlers", "Little Dinkums: Aussie Animals · big & easy",
  "A wombat coming out of its burrow with a butterfly — a thick-lined, easy colouring page for toddlers from Little Dinkums: Aussie Animals. 50 printable Australian animal pages, ages 2–8."),
 (11, "2026-11-18", "10:00", "photo", g("boxes"), None, LW, "Colouring Pages for Adults", "lw_beach",
  "Beach boxes colouring page for adults, in progress", "Long Weekend: The Beach · coloured pencil",
  "A row of beach boxes with banksia and pandanus, half coloured in pencil over a cup of tea. From Long Weekend: The Beach — 42 calm, cosy adult colouring pages of the Australian coast. Printable PDF."),
 (12, "2026-11-18", "19:00", "page", s("bch_rockpool"), None, LW, "Australian Native Flowers Colouring", "lw_beach",
  "Rock pool colouring page — starfish, shells & crab", "Long Weekend: The Beach · for grown-ups",
  "Starfish, shells, a crab and sea anemones in a rock pool — a detailed-but-calm adult colouring page from Long Weekend: The Beach. 42 printable pages of the Australian coast, A4 and US Letter."),
 (13, "2026-11-19", "10:00", "split", s("aa_quokka"), g("quokka"), LD, "Printable Activities for Kids", "ld_animals",
  "Before & after: quokka colouring page", "Little Dinkums: Aussie Animals · ages 2–8",
  "Before and after: the quokka selfie page from Little Dinkums: Aussie Animals, printed in black and white and coloured in with crayons. 50 big, easy Australian animal colouring pages for kids, printable PDF."),
 (14, "2026-11-19", "19:00", "covers", ALL_COVERS, None, CH, "Christmas Colouring Pages for Kids", "all",
  "Christmas gift guide: colouring books for kids & grown-ups", "15% off printables with LAUNCH15 · until 30 Nov",
  "Christmas gift guide from Clover Hartley: Little Dinkums colouring books for ages 2–8 (Christmas, Aussie Christmas, Aussie Animals) and Long Weekend for grown-ups (Christmas, The Beach). Printable PDFs — code LAUNCH15 takes 15% off until 30 Nov."),
]

def build():
    rows, data = [], {"ig": [], "pins": []}
    for p in IG:
        files = []
        for i, sl in enumerate(p["slides"], 1):
            fn = f"d{p['day']}_{i}.jpg"; out = f"{OUT}/{fn}"; k = sl[0]
            if k == "photo": ig_photo(sl[1], sl[2], sl[3], out)
            elif k == "before": ig_before(sl[1], sl[2], sl[3], sl[4], out)
            elif k == "text": ig_text(sl[1], sl[2], sl[3], out, art=sl[4], num=sl[5])
            elif k == "covers": ig_covers(sl[1], sl[2], sl[3], sl[4], sl[5], out)
            elif k == "offer": ig_offer(sl[1], sl[2], out, cover_path=sl[3] if len(sl) > 3 else None)
            elif k == "list": ig_list(sl[1], sl[2], sl[3], out)
            files.append(fn)
        data["ig"].append({**{k: v for k, v in p.items() if k != "slides"}, "files": files})
        rows.append(dict(Text=p["caption"], Date=p["date"], Time=p["time"] + ":00", Instagram="true", **{"Instagram Post Type": "POST"},
                         **{f"Picture Url {i}": RAW + f for i, f in enumerate(files, 1)},
                         **{f"Alt text picture {i}": f"Clover Hartley colouring page — {p['theme']}" for i in range(1, len(files)+1)}))
    for (n, date, time, mode, img, img2, S, board, lk, title, sub, desc) in PINS:
        fn = f"pin{n:02d}.jpg"; pin(img, title, sub, S, f"{OUT}/{fn}", mode, img2)
        link = utm(lk, n)
        data["pins"].append(dict(n=n, date=date, time=time, board=board, title=title, description=desc, link=link, file=fn))
        rows.append({"Text": desc, "Date": date, "Time": time + ":00", "Pinterest": "true", "Picture Url 1": RAW + fn,
                     "Alt text picture 1": title, "Pinterest Board": board, "Pinterest Pin Title": title, "Pinterest Pin Link": link})
    hdr = next(csv.reader(open(f"{B}/../week1/week1_metricool.csv")))
    bools = {"Draft", "Facebook", "Twitter/X", "LinkedIn", "GBP", "Instagram", "Pinterest", "TikTok", "Youtube", "Threads", "Bluesky", "Shortener"}
    def write(name, rs):
        with open(f"{OUT}/{name}", "w", newline="") as fh:
            w = csv.writer(fh, quoting=csv.QUOTE_ALL); w.writerow(hdr)
            for r in rs: w.writerow([r.get(h, "false" if h in bools else "") for h in hdr])
    write("week3_metricool.csv", rows)
    write("week3_instagram_metricool.csv", [r for r in rows if r.get("Instagram") == "true"])
    write("week3_pins_metricool.csv", [r for r in rows if r.get("Pinterest") == "true"])
    json.dump(data, open(f"{OUT}/week3.json", "w"), indent=1, ensure_ascii=False)
    print(len(data["ig"]), "IG posts,", sum(len(x["files"]) for x in data["ig"]), "IG images,", len(data["pins"]), "pins")

if __name__ == "__main__":
    build()
