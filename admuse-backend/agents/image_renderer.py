from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def _font(size: int):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

SIZES = {
    "banner": (1200, 300),
    "interstitial": (1080, 1920),
    "rewarded": (1280, 720),
}

def render(creative: dict, out_dir: Path) -> Path:
    fmt = creative.get("format", "banner")
    w, h = SIZES.get(fmt, (1200, 300))

    img = Image.new("RGB", (w, h), (26, 28, 34))
    d = ImageDraw.Draw(img)

    # gradient background
    for y in range(h):
        shade = int(26 + (y / max(h-1,1)) * 40)
        d.line([(0,y),(w,y)], fill=(shade,shade,shade+10))

    pad = int(min(w,h)*0.05)
    headline = creative.get("headline","Your Headline")
    body     = creative.get("body","Your value prop goes here.")
    cta      = creative.get("cta","Install Now")

    head_font = _font(max(20, int(h*0.12)))
    body_font = _font(max(16, int(h*0.06)))
    cta_font  = _font(max(18, int(h*0.07)))

    def wrap(text, font, maxw):
        words, line, lines = text.split(), "", []
        for w0 in words:
            t = (line + " " + w0).strip()
            if d.textlength(t, font=font) <= maxw: line = t
            else:
                if line: lines.append(line)
                line = w0
        if line: lines.append(line)
        return lines

    maxw = w - 2*pad
    y = pad
    for ln in wrap(headline, head_font, maxw):
        d.text((pad,y), ln, font=head_font, fill=(255,255,255)); y += head_font.size + int(h*0.01)
    y += int(h*0.01)
    for ln in wrap(body, body_font, maxw)[:3]:
        d.text((pad,y), ln, font=body_font, fill=(210,210,210)); y += body_font.size + int(h*0.005)

    # CTA pill
    hexcol = creative.get("brand_color") or "#00c882"
    try:
        rgb = tuple(int(hexcol.lstrip("#")[i:i+2],16) for i in (0,2,4))
    except Exception:
        rgb = (0,200,130)

    cta_text = cta.upper()
    tw = d.textlength(cta_text, font=cta_font)
    th = cta_font.size
    pill_w = int(tw + pad*1.2)
    pill_h = int(th + pad*0.6)
    pill_x = pad
    pill_y = min(h - pill_h - pad, y + int(h*0.04))

    d.rounded_rectangle([pill_x,pill_y,pill_x+pill_w,pill_y+pill_h], radius=int(pill_h/2), fill=rgb)
    d.text((pill_x+(pill_w - tw)/2, pill_y+(pill_h - th)/2), cta_text, font=cta_font, fill=(20,28,32))

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{creative['id']}.png"
    img.save(out_path, format="PNG", optimize=True)
    return out_path
