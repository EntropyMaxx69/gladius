# Erzeugt das Gladius-App-Symbol: pompejanisches Rot, goldener Rahmen mit Mäander (römisch), Gladius + Funkelstern
import asyncio, base64, io, re
from playwright.async_api import async_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/e093d6d0-2bf4-5709-94ea-79f68d58b872/scratchpad/'
G='/home/claude/gladius-desktop/'
SWORD='''<path d="M3 0.5 L17 0.5 L16 4.2 L12.6 5.4 L12.6 7.4 L7.4 7.4 L7.4 5.4 L4 4.2 Z" fill="url(#hilt)"/>
    <rect x="7.6" y="7" width="4.8" height="12.6" rx="1" fill="url(#hilt)"/>
    <path d="M7.6 10.2h4.8M7.6 16.4h4.8" stroke="#1a1f26" stroke-width=".9"/>
    <circle cx="10" cy="13.3" r="1.5" fill="#e8b04a"/>
    <path d="M3.6 19.4 L16.4 19.4 L15.4 23.4 L4.6 23.4 Z" fill="url(#hilt)"/>
    <path d="M6.4 23.4 L13.6 23.4 L12.7 33.5 L14.4 50 L10 66 L5.6 50 L7.3 33.5 Z" fill="url(#blade)"/>
    <path d="M8 24.2 L12 24.2 L11.4 33.5 L12.8 49.6 L10 59.5 L7.2 49.6 L8.6 33.5 Z" fill="#8f9aa8"/>
    <path d="M10 24.2 L10 59.5" stroke="#d3dae2" stroke-width=".5"/>'''
def star(x,y,r):
    a,b=r*0.16,r
    return f'''<g transform="translate({x} {y})"><circle r="{r*0.55}" fill="url(#halo)"/>
    <path d="M0 {-b} L{a} {-a} L{b} 0 L{a} {a} L0 {b} L{-a} {a} L{-b} 0 L{-a} {-a} Z" fill="#fff"/>
    <path d="M0 {-b*.55} L{a*.6} {-a*.6} L{b*.55} 0 L{a*.6} {a*.6} L0 {b*.55} L{-a*.6} {a*.6} L{-b*.55} 0 L{-a*.6} {-a*.6} Z" fill="#fff" transform="rotate(45)"/></g>'''
def meander(side_len, start, y0, h=22, tile=30):
    # Mäander-Band entlang einer geraden Kante (oben), wird für die anderen Seiten gedreht
    n=int(side_len//tile); off=start+(side_len-n*tile)/2; d=''
    for i in range(n):
        x=off+i*tile
        d+=f'M{x:.1f} {y0+h} V{y0} H{x+tile-6:.1f} V{y0+h-6} H{x+8:.1f} V{y0+8} H{x+tile-14:.1f} '
    return f'<path d="{d}" fill="none" stroke="url(#gold)" stroke-width="4" stroke-linecap="square"/><path d="M{off:.1f} {y0+h} H{off+n*tile:.1f}" stroke="url(#gold)" stroke-width="4"/>'
def svg(full=True):
    defs='''<defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9c1f2e"/><stop offset=".55" stop-color="#861826"/><stop offset="1" stop-color="#5e0f1a"/></linearGradient>
    <radialGradient id="glow" cx=".45" cy=".4" r=".6"><stop offset="0" stop-color="#ffb3a0" stop-opacity=".22"/><stop offset="1" stop-color="#ffb3a0" stop-opacity="0"/></radialGradient>
    <linearGradient id="blade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#dfe5eb"/><stop offset="1" stop-color="#9aa6b4"/></linearGradient>
    <linearGradient id="hilt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f6f8"/><stop offset="1" stop-color="#b9c2cc"/></linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff0b0"/><stop offset=".3" stop-color="#e9c25a"/><stop offset=".6" stop-color="#b8862a"/><stop offset=".85" stop-color="#f1d27a"/><stop offset="1" stop-color="#8f6216"/></linearGradient>
    <radialGradient id="halo"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".4" stop-color="#fff3d6" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  </defs>'''
    body=f'<rect x="16" y="16" width="480" height="480" rx="108" fill="url(#bg)"/><rect x="16" y="16" width="480" height="480" rx="108" fill="url(#glow)"/>'
    if full:
        # Goldrahmen: dicke Aussenkante, Mäanderband, feine Innenlinie
        body+='<rect x="22" y="22" width="468" height="468" rx="102" fill="none" stroke="url(#gold)" stroke-width="12"/>'
        band=meander(512-2*112, 112, 38)
        body+=''.join(f'<g transform="rotate({r} 256 256)">{band}</g>' for r in (0,90,180,270))
        # Eckrosetten
        for cx,cy in ((70,70),(442,70),(70,442),(442,442)):
            body+=f'<circle cx="{cx}" cy="{cy}" r="9" fill="url(#gold)"/><circle cx="{cx}" cy="{cy}" r="3.5" fill="#6a121d"/>'
        body+='<rect x="68" y="68" width="376" height="376" rx="60" fill="none" stroke="url(#gold)" stroke-width="4"/>'
        sc, st = 5.0, (372, 140, 68)
    else:
        body+='<rect x="23" y="23" width="466" height="466" rx="101" fill="none" stroke="url(#gold)" stroke-width="14"/>'
        sc, st = 6.6, (409, 103, 38)
    body+=f'<g transform="translate(256 256) rotate(225) scale({sc}) translate(-10 -33)">{SWORD}</g>'+star(*st)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">{defs}{body}</svg>'
async def render(s, out):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':512,'height':512})
        await pg.set_content(f"<html><body style='margin:0;background:transparent'>{s}</body></html>")
        await pg.screenshot(path=out, omit_background=True); await b.close()
full = simple = svg(False)
asyncio.run(render(simple, S+'icon-simple.png')); import shutil; shutil.copy(S+'icon-simple.png', S+'icon-full.png')
F=Image.open(S+'icon-full.png').convert('RGBA'); P=Image.open(S+'icon-simple.png').convert('RGBA')
open(G+'build/icon.svg','w').write(full)
F.save(G+'build/icon.png'); F.resize((256,256),Image.LANCZOS).save(G+'app/icon.png')
# ICO: grosse Grössen mit Mäander, kleine (≤48 px) mit schlichtem Goldrand und grösserem Gladius
imgs=[(P if s<=48 else F).resize((s,s),Image.LANCZOS) for s in (16,24,32,48,64,128,256)]
imgs[-1].save(G+'build/icon.ico', format='ICO', sizes=[(i.width,i.height) for i in imgs], append_images=imgs[:-1])
sheet=Image.new('RGBA',(760,560),(32,32,36,255))
for row,bg in ((0,(32,32,36,255)),(280,(240,240,240,255))):
    band=Image.new('RGBA',(760,280),bg); x=20
    for s in (256,128,64,32,16):
        r=(P if s<=48 else F).resize((s,s),Image.LANCZOS); band.paste(r,(x,12+(256-s)//2),r); x+=s+30
    sheet.paste(band,(0,row))
sheet.save(S+'icon-sheet.png')
buf=io.BytesIO(); P.resize((64,64),Image.LANCZOS).save(buf,'PNG')
h=open(G+'app/index.html').read(); h=re.sub(r'<link rel="icon"[^>]*>', '<link rel="icon" href="data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()+'">', h); open(G+'app/index.html','w').write(h)
print('ok')
