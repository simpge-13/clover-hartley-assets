#!/usr/bin/env python3
"""Clover Hartley social — Week 2 (Fri 6 – Thu 12 Nov 2026), theme "Show it in use".
Builds IG posts (1080x1350) + Pinterest pins (1000x1500) into out/, plus week2.json and week2_metricool.csv."""
import csv, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

B = os.path.dirname(os.path.abspath(__file__))
GEN, SRC, OUT = f"{B}/gen", f"{B}/src", f"{B}/out"
REPO_IMG = "/home/claude/clover-hartley-assets/images"
os.makedirs(OUT, exist_ok=True)
RAW = "https://raw.githubusercontent.com/simpge-13/clover-hartley-assets/main/social/week2/"

LD = dict(bg="#FFF3DC", band="#2F7D4F", ink="#1B3358", acc="#F26A21", font="Fredoka", tag="Little Dinkums")
LW = dict(bg="#F6EFE3", band="#3F5E4A", ink="#3B3A36", acc="#C4663F", font="Lora", tag="Long Weekend")

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

# ---------------- IG templates (1080x1350) ----------------
def ig_photo(photo, label, S, out):
    """Full-bleed lifestyle photo with a small product pill bottom-left."""
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
    n = len(paths); w = 430 if n == 2 else 300; gap = 60
    x = (1080 - (n*w + (n-1)*gap))//2
    for p in paths:
        c = Image.open(p).convert("RGB"); c = c.resize((w, round(w*c.height/c.width)), Image.LANCZOS)
        y = 380 + (560 - c.height)//2
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((x+8, y+14, x+w+8, y+c.height+14), fill=(0, 0, 0, 60))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); im.paste(c, (x, y)); x += w + gap
    d = ImageDraw.Draw(im); text_block(d, 60, 1130, foot, F(S["font"], 34, "Medium"), S["ink"], 960, 48)
    im.convert("RGB").save(out, quality=90)

def ig_offer(head, S, out):
    im = Image.new("RGBA", (1080, 1350), S["bg"]); d = ImageDraw.Draw(im)
    y = text_block(d, 60, 110, head, F(S["font"], 70), S["ink"], 960, 86)
    c = Image.open(f"{REPO_IMG}/lw-christmas-cover.jpg").convert("RGB"); c = c.resize((440, round(440*c.height/c.width)), Image.LANCZOS)
    x, yy = (1080-440)//2, 250
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((x+8, yy+14, x+448, yy+c.height+14), fill=(0, 0, 0, 60))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); im.paste(c, (x, yy)); d = ImageDraw.Draw(im)
    d.text((60, 900), "15% off printable PDFs with code", font=F(S["font"], 38, "Medium"), fill=S["ink"])
    d.text((60, 960), "LAUNCH15", font=F(S["font"], 120), fill=S["band"])
    d.text((60, 1120), "cloverhartley.com  ·  until 30 Nov", font=F(S["font"], 34, "Medium"), fill=S["acc"])
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
    d = ImageDraw.Draw(im)
    pill(d, 965, 30 if mode != "split" else 30, S["tag"], F(S["font"], 24, "SemiBold"), S["acc"], right=True, h=44)
    d.rectangle((0, 1040, 1000, 1500), fill=S["band"])
    y = text_block(d, 50, 1080, title, F(S["font"], 52), "white", 900, 64) + 8
    text_block(d, 50, y, sub, F(S["font"], 30, "Medium" if S is LD else "Regular"), "#FFFFFF", 900, 40)
    d.text((50, 1440), "Printable PDF  ·  cloverhartley.com", font=F(S["font"], 28, "SemiBold" if S is LD else "Medium"), fill="#FFFFFF")
    im.convert("RGB").save(out, quality=90)

# ---------------- links ----------------
P = "https://cloverhartley.com/products/"
LINK = {
    "ld_xmas": P + "little-dinkums-christmas-colouring-book-printable-pdf-a4-us-letter",
    "ld_aussie": P + "little-dinkums-aussie-christmas-colouring-book-printable-pdf-a4-us-letter",
    "lw_xmas": P + "long-weekend-christmas-a-calm-cosy-colouring-book-printable-pdf-a4-us-letter",
    "ld_coll": "https://cloverhartley.com/collections/little-dinkums-ages-2-8",
    "lw_coll": "https://cloverhartley.com/collections/long-weekend-adults",
}
def utm(k, n): return f"{LINK[k]}?utm_source=pinterest&utm_medium=social&utm_campaign=launch&utm_content=w2pin{n:02d}"

g = lambda n: f"{GEN}/c_{n}.jpg"; s = lambda n: f"{SRC}/p{n:02d}.png"

# ---------------- Instagram posts ----------------
IG = [
 dict(day=8, date="2026-11-06", kind="Carousel · 3", theme="Before & after",
  caption="""Same page. One box of crayons later. 🖍️

Santa on his paddleboard from Little Dinkums: Aussie Christmas — black-and-white when it comes out of the printer, and very much not by the time it's done. Swipe for the before, plus a kangaroo sleigh in full texta.

Every page is drawn with thick, simple outlines so little hands can stay (mostly) inside the lines.

Printable PDF, A4 + US Letter. Print it as many times as you like. Link in bio.

#aussiechristmas #christmascolouring #colouringpages #beforeandafter #kidsactivities #crayons #toddleractivities #preschoolactivities #summerchristmas #australiankids #printablecolouring #cloverhartley #littledinkums""",
  slides=[("photo", g("surf"), "Little Dinkums: Aussie Christmas", LD),
          ("before", s(2), "Before.", "Page 32 · Little Dinkums: Aussie Christmas", LD),
          ("photo", g("sleigh"), "Kangaroos > reindeer", LD)]),
 dict(day=9, date="2026-11-07", kind="Carousel · 4", theme="How to print at home",
  caption="""How to print your colouring pages at home (save this one 📌)

1. Buy once on cloverhartley.com — the download link arrives straight away, and in your email.
2. Open the PDF and choose A4 (Australia, UK) or US Letter.
3. Print with "Fit to page" on, single-sided.
4. Plain copy paper for pencils and crayons; 120gsm or light card if textas are involved.

Then print it again. And again. Your PDF never runs out — siblings, cousins, the whole class.

#printables #printablecolouring #colouringpages #kidsactivities #homeschoolaustralia #teachersofinstagram #christmasactivities #rainydayactivities #mumhacks #cloverhartley #littledinkums #longweekend""",
  slides=[("photo", g("printer"), "Print at home", LD),
          ("text", "1. Buy once, download straight away", "Checkout on cloverhartley.com and your download link appears on the order page — and lands in your inbox, so it's there when you need it.\n\nEach book comes as two PDFs: A4 and US Letter.", LD, None, "Step 1"),
          ("text", "2. Print settings", "Open the PDF that matches your paper.\n\n•  Scale: \"Fit to page\"\n•  Single-sided (blank backs = no bleed-through)\n•  Print just the pages you want, or the lot", LD, s(10), "Step 2"),
          ("text", "3. Pick your paper", "•  Copy paper (80gsm): pencils & crayons\n•  120gsm+ or light card: textas & markers\n•  Card stock: anything going on the fridge\n\nRun out? Print it again. It never runs out.", LD, None, "Step 3")]),
 dict(day=10, date="2026-11-08", kind="Single", theme="Long Weekend in use",
  caption="""Sunday arvo, sorted. ☕

Two kookaburras in a flowering gum, a few baubles hanging off the branches — a page from Long Weekend: Christmas, part-way through with a tin of pencils and a cuppa.

Medium detail, bold lines, no fiddly bits. Enough for an afternoon; never so much it feels like homework.

Printable PDF or paperback. Link in bio.

#adultcolouring #colouringforadults #mindfulcolouring #sundayvibes #slowliving #kookaburra #australianbirds #botanicalcolouring #colouredpencils #selfcaresunday #christmascolouring #cloverhartley #longweekend""",
  slides=[("photo", g("kook"), "Long Weekend: Christmas", LW)]),
 dict(day=11, date="2026-11-09", kind="Carousel · 3", theme="Aussie Christmas spotlight",
  caption="""Things on an Aussie Christmas colouring page that would confuse the North Pole: 🦘

• A kookaburra in a Santa hat, guarding the stockings on the Hills Hoist
• Three kangaroos pulling the sleigh (they do the job in half the time)
• A koala and a kangaroo building a sandcastle on Christmas Day

All three are in Little Dinkums: Aussie Christmas — 50 pages of the Christmas our kids actually have: hot, sandy and loud.

Which one's going on your fridge? 👇

#aussiechristmas #australianchristmas #hillshoist #kookaburra #kangaroo #koala #christmascolouring #colouringpages #kidsactivities #summerchristmas #australiankids #cloverhartley #littledinkums""",
  slides=[("photo", g("hoist"), "Little Dinkums: Aussie Christmas", LD),
          ("before", s(5), "Kangaroo power.", "Little Dinkums: Aussie Christmas", LD),
          ("before", s(11), "Sandcastles, obviously.", "Little Dinkums: Aussie Christmas", LD)]),
 dict(day=12, date="2026-11-10", kind="Single", theme="Christmas Day kids' table",
  caption="""The kids' table plan for Christmas lunch:

1. Print a few pages (one per kid, plus spares for the cousins who turn up)
2. Small jar of crayons at each spot
3. Bonbons, cherries, done

Buys you a solid stretch while the prawns go round — and the finished ones make handy place cards for next year.

Little Dinkums Christmas and Aussie Christmas, printable at home. Link in bio.

#christmaslunch #kidstable #christmaswithkids #aussiechristmas #christmasactivities #kidsactivities #printables #christmashacks #mumlife #australianmum #partyideas #cloverhartley #littledinkums""",
  slides=[("photo", g("table"), "Little Dinkums printables", LD)]),
 dict(day=13, date="2026-11-11", kind="Carousel · 3", theme="New books: Aussie Animals + The Beach",
  caption="""Two new books — and neither of them is about Christmas. 🌊

🦘 Little Dinkums: Aussie Animals — 50 big & easy pages of kangaroos, koalas, wombats, platypus, quokkas and more, for ages 2–8. (Yes, the kangaroo surfs.)

🌿 Long Weekend: The Beach — 42 calm, cosy pages of the Australian coast for grown-ups: beach boxes, rock pools, pelicans, banksia and pandanus.

Both out now as printable PDFs. Link in bio.

#newrelease #aussieanimals #australiananimals #kidscolouring #adultcolouring #beachvibes #australianbeach #colouringbook #printables #summerholidays #schoolholidays #cloverhartley #littledinkums #longweekend""",
  slides=[("photo", g("roo"), "Little Dinkums: Aussie Animals", LD),
          ("covers", [f"{REPO_IMG}/ld-aussie-animals-cover.jpg", f"{REPO_IMG}/lw-beach-cover.jpg"], "Two new books.", "Not a Santa in sight.", "Little Dinkums: Aussie Animals (ages 2–8)  ·  Long Weekend: The Beach (grown-ups). Printable PDFs at cloverhartley.com", LD),
          ("before", f"{SRC}/lwbeach_p2.png", "Inside The Beach.", "Long Weekend: The Beach · 42 pages", LW)]),
 dict(day=14, date="2026-11-12", kind="Carousel · 3", theme="The grown-up version + LAUNCH15",
  caption="""Christmas, the grown-up version. 🌿

Sunset on the sand with a hat and towel, and a pavlova piled with mango, passionfruit and strawberries, framed by gum blossom. Two pages from Long Weekend: Christmas, coloured in pencil.

42 pages, bold botanical lines, one calm evening at a time. A nice one to tuck in with a gift for mum, too.

Code LAUNCH15 still takes 15% off every printable on cloverhartley.com until 30 Nov. Link in bio.

#adultcolouring #colouringforadults #mindfulcolouring #giftsformum #christmasgiftideas #pavlova #australianchristmas #botanicalart #colouredpencils #slowliving #cloverhartley #longweekend""",
  slides=[("photo", g("beach"), "Long Weekend: Christmas", LW),
          ("photo", g("pav"), "Long Weekend: Christmas", LW),
          ("offer", "Colour the long weekend in.", LW)]),
]

# ---------------- Pins ----------------
PINS = [
 (1, "2026-11-06", "10:00", "photo", g("surf"), None, LD, "Aussie Christmas Colouring", "ld_aussie",
  "Beach Santa colouring page — coloured in!", "Little Dinkums: Aussie Christmas · ages 2–8",
  "Santa on a paddleboard with two dolphins, coloured in with crayons. From Little Dinkums: Aussie Christmas — 50 printable Australian Christmas colouring pages for kids aged 2–8."),
 (2, "2026-11-06", "19:00", "photo", g("kook"), None, LW, "Colouring Pages for Adults", "lw_xmas",
  "Kookaburra Christmas colouring page in coloured pencil", "Long Weekend: Christmas · for grown-ups",
  "Two kookaburras in a flowering gum with Christmas baubles, part-coloured in pencil. A calm adult colouring page from Long Weekend: Christmas — 42 printable pages."),
 (3, "2026-11-07", "10:00", "photo", g("printer"), None, LD, "Printable Activities for Kids", "ld_xmas",
  "How to print colouring pages at home", "Fit to page · single-sided · print again any time",
  "Printing colouring pages at home: choose A4 or US Letter, set 'Fit to page', print single-sided, use 120gsm paper for textas. Little Dinkums printable PDFs — print as many times as you like."),
 (4, "2026-11-07", "19:00", "photo", g("sleigh"), None, LD, "Aussie Christmas Colouring", "ld_aussie",
  "Kangaroos pulling Santa's sleigh — Aussie Christmas colouring", "Coloured in with textas",
  "Three kangaroos pulling Santa's sleigh under the stars, coloured with markers. One of 50 Australian Christmas colouring pages for kids in Little Dinkums: Aussie Christmas."),
 (5, "2026-11-08", "10:00", "photo", g("pav"), None, LW, "Australian Native Flowers Colouring", "lw_xmas",
  "Pavlova & gum blossom — botanical colouring page", "Long Weekend: Christmas · 42 calm pages",
  "A pavlova piled with mango, passionfruit and strawberries, framed with gum blossom, coloured in pencil. Australian native flower colouring page for adults from Long Weekend: Christmas."),
 (6, "2026-11-08", "19:00", "photo", g("table"), None, LD, "Printable Activities for Kids", "ld_coll",
  "Christmas lunch kids' table activity idea", "Printable colouring pages + a jar of crayons",
  "Easy Christmas kids' table idea: a printed colouring page and a jar of crayons at each place, with bonbons and cherries. Little Dinkums printable Christmas colouring pages for ages 2–8."),
 (7, "2026-11-09", "10:00", "photo", g("hoist"), None, LD, "Aussie Christmas Colouring", "ld_aussie",
  "Kookaburra on the Hills Hoist — Aussie Christmas colouring page", "Coloured in with crayons",
  "A kookaburra in a Santa hat next to stockings on the Hills Hoist, coloured in with crayons. From Little Dinkums: Aussie Christmas, 50 printable pages for kids."),
 (8, "2026-11-09", "19:00", "photo", g("beach"), None, LW, "Colouring Pages for Adults", "lw_xmas",
  "Christmas sunset at the beach — adult colouring, coloured in", "Long Weekend: Christmas",
  "A sunset beach with pandanus, straw hat and striped towel, coloured in pencil. Calm Australian Christmas colouring page for adults from Long Weekend: Christmas."),
 (9, "2026-11-10", "10:00", "photo", g("roo"), None, LD, "Printable Activities for Kids", "ld_coll",
  "Surfing kangaroo colouring page for kids", "New: Little Dinkums: Aussie Animals · ages 2–8",
  "A kangaroo in sunnies surfing a wave, coloured in with crayons. From Little Dinkums: Aussie Animals — 50 big & easy Australian animal colouring pages for kids, printable PDF."),
 (10, "2026-11-10", "19:00", "page", f"{REPO_IMG}/lw-beach-preview.jpg", None, LW, "Colouring Pages for Adults", "lw_coll",
  "Australian beach colouring pages for adults", "New: Long Weekend: The Beach · 42 pages",
  "Beach boxes, rock pools, pelicans, sea turtles and banksia — Long Weekend: The Beach is 42 calm, cosy colouring pages of the Australian coast for grown-ups. Printable PDF."),
 (11, "2026-11-11", "10:00", "page", f"{REPO_IMG}/ld-aussie-animals-preview.jpg", None, LD, "Printable Activities for Kids", "ld_coll",
  "50 Aussie animal colouring pages for kids", "Kangaroos, koalas, wombats & more · ages 2–8",
  "Kangaroos, koalas, wombats, platypus, quokkas and more — 50 big, easy Australian animal colouring pages for ages 2–8 in Little Dinkums: Aussie Animals. Printable PDF."),
 (12, "2026-11-11", "19:00", "split", s(2), g("surf"), LD, "Aussie Christmas Colouring", "ld_aussie",
  "Before & after: beach Santa colouring page", "Little Dinkums: Aussie Christmas",
  "Before and after: the paddleboarding Santa page from Little Dinkums: Aussie Christmas, printed in black and white and coloured in with crayons. 50 printable pages for kids."),
 (13, "2026-11-12", "10:00", "split", s(6), g("kook"), LW, "Australian Native Flowers Colouring", "lw_xmas",
  "Before & after: kookaburra & gum blossom colouring", "Long Weekend: Christmas · for grown-ups",
  "Before and after: two kookaburras in a flowering gum, from line art to coloured pencil. Australian native flower colouring for adults in Long Weekend: Christmas."),
 (14, "2026-11-12", "19:00", "split", s(5), g("sleigh"), LD, "Christmas Colouring Pages for Kids", "ld_aussie",
  "Before & after: kangaroo sleigh colouring page", "Christmas colouring for ages 2–8",
  "Before and after: kangaroos pulling Santa's sleigh, coloured in with textas. Big, easy Christmas colouring pages for kids from Little Dinkums: Aussie Christmas."),
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
            elif k == "offer": ig_offer(sl[1], sl[2], out)
            files.append(fn)
        data["ig"].append({**{k: v for k, v in p.items() if k != "slides"}, "time": "19:30", "files": files})
        rows.append(dict(Text=p["caption"], Date=p["date"], Time="19:30:00", Instagram="true", **{"Instagram Post Type": "POST"},
                         **{f"Picture Url {i}": RAW + f for i, f in enumerate(files, 1)},
                         **{f"Alt text picture {i}": f"Clover Hartley colouring page — {p['theme']}" for i in range(1, len(files)+1)}))
    for (n, date, time, mode, img, img2, S, board, lk, title, sub, desc) in PINS:
        fn = f"pin{n:02d}.jpg"; pin(img, title, sub, S, f"{OUT}/{fn}", mode, img2)
        link = utm(lk, n)
        data["pins"].append(dict(n=n, date=date, time=time, board=board, title=title, description=desc, link=link, file=fn))
        rows.append({"Text": desc, "Date": date, "Time": time + ":00", "Pinterest": "true", "Picture Url 1": RAW + fn,
                     "Alt text picture 1": title, "Pinterest Board": board, "Pinterest Pin Title": title, "Pinterest Pin Link": link})
    hdr = next(csv.reader(open("/home/claude/clover-hartley-assets/social/week1/week1_metricool.csv")))
    bools = {"Draft", "Facebook", "Twitter/X", "LinkedIn", "GBP", "Instagram", "Pinterest", "TikTok", "Youtube", "Threads", "Bluesky", "Shortener"}
    with open(f"{OUT}/week2_metricool.csv", "w", newline="") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_ALL); w.writerow(hdr)
        for r in rows: w.writerow([r.get(h, "false" if h in bools else "") for h in hdr])
    json.dump(data, open(f"{OUT}/week2.json", "w"), indent=1, ensure_ascii=False)
    print(len(data["ig"]), "IG posts,", sum(len(x["files"]) for x in data["ig"]), "IG images,", len(data["pins"]), "pins")

if __name__ == "__main__":
    build()
