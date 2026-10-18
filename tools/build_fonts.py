#!/usr/bin/env python3
"""Regenerate engine/kit/fonts/{fonts.css,fonts.js,README.md} from the FONTS table below + the font files.
Usage: python3 tools/build_fonts.py   (run from repo root). Add a font: drop the .ttf in engine/kit/fonts and add a row."""
import os, json
from fontTools.ttLib import TTFont
D = 'engine/kit/fonts'
# family, files[(file, weight-or-range)], script, genre, role, mood (en | ar)
FONTS = [
 ('Amiri',[('Amiri-Bold.ttf','700'),('Amiri-Regular.ttf','400')],'ar','naskh','display/body','classical, scholarly, Quranic | كلاسيكي، علمي، تراثي'),
 ('Naskh',[('NotoNaskhArabic[wght].ttf','400 700')],'ar','naskh','body/subtitle','neutral modern naskh, highly legible | نسخ حديث محايد واضح جدًا'),
 ('Scheherazade',[('ScheherazadeNew-Bold.ttf','700')],'ar','naskh','body/quote','traditional naskh, generous vowels | نسخ تقليدي بتشكيل واسع'),
 ('Lateef',[('Lateef-Bold.ttf','700')],'ar','naskh (sindhi)','quote','soft, handwritten-naskh warmth | نسخ دافئ قريب من اليد'),
 ('Markazi',[('MarkaziText[wght].ttf','400 700')],'ar+lat','naskh/serif','body/editorial','editorial, newspaper serif | تحريري صحفي'),
 ('Mirza',[('Mirza-Bold.ttf','700')],'ar','naskh','display','bold calligraphic naskh, poster headlines | نسخ خطي عريض للعناوين'),
 ('Ruqaa',[('ArefRuqaa-Bold.ttf','700')],'ar','ruqaa','display','handwritten ruqʿa, personal/historic | رقعة يدوية، شخصي وتاريخي'),
 ('RuqaaInk',[('ArefRuqaaInk-Bold.ttf','700')],'ar','ruqaa (COLR colour)','display/hero','ruqʿa with two-tone ink & ornaments (colour font) | رقعة بحبر ملوّن (خط ملوّن)'),
 ('Nastaliq',[('NotoNastaliqUrdu[wght].ttf','400 700')],'ar','nastaʿlīq','display/poetry','Persian/Urdu poetic hanging script | نستعليق شعري فارسي'),
 ('Gulzar',[('Gulzar-Regular.ttf','400')],'ar','nastaʿlīq','display/poetry','refined nastaʿlīq, poetry & titles | نستعليق رفيع للشعر'),
 ('Qahiri',[('Qahiri-Regular.ttf','400')],'ar','kufi (Mamluk)','display','geometric Cairene kufi, monumental | كوفي قاهري هندسي أثري'),
 ('Kufi',[('NotoKufiArabic[wght].ttf','100 900')],'ar','kufi (modern)','UI/labels','clean modern kufi UI face | كوفي حديث للواجهات'),
 ('ReemKufi',[('ReemKufi[wght].ttf','400 700')],'ar','kufi (fatimid)','display','elegant fatimid-flavoured kufi | كوفي فاطمي أنيق'),
 ('ReemKufiFun',[('ReemKufiFun[wght].ttf','400 700')],'ar','kufi (playful)','display','playful kufi, kids/edu | كوفي مرح للأطفال والتعليم'),
 ('ReemKufiInk',[('ReemKufiInk-Regular.ttf','400')],'ar','kufi (COLR colour)','hero','gradient/colour kufi (colour font) | كوفي ملوّن متدرّج'),
 ('Kufam',[('Kufam[wght].ttf','400 900')],'ar+lat','kufi (display)','display','squared contemporary kufi | كوفي مربّع معاصر'),
 ('Blaka',[('Blaka-Regular.ttf','400')],'ar+lat','blackletter-kufi','display','gothic/blackletter fusion, dramatic | قوطي درامي'),
 ('Alexandria',[('Alexandria[wght].ttf','100 900')],'ar+lat','geometric sans','display/UI','geometric modern sans, tech | هندسي حديث تقني'),
 ('Cairo',[('Cairo[slnt,wght].ttf','200 1000')],'ar+lat','sans','UI/display','contemporary sans, news & explainers | حديث للأخبار والشروحات'),
 ('Tajawal',[('Tajawal-Regular.ttf','400'),('Tajawal-Bold.ttf','700'),('Tajawal-Black.ttf','900')],'ar+lat','sans','UI/captions','low-contrast sans, captions | بسيط للترجمات والشروح'),
 ('Almarai',[('Almarai-Regular.ttf','400'),('Almarai-Bold.ttf','700'),('Almarai-ExtraBold.ttf','800')],'ar+lat','sans','UI/captions','rounded friendly sans | ودود مستدير'),
 ('PlexArabic',[('IBMPlexSansArabic-Regular.ttf','400'),('IBMPlexSansArabic-Bold.ttf','700')],'ar+lat','grotesk','UI/data','corporate, data & charts | مؤسسي للبيانات والرسوم'),
 ('Readex',[('ReadexPro[HEXP,wght].ttf','160 700')],'ar+lat','sans (variable expansion)','UI/kinetic','variable width, kinetic type | عرض متغيّر للطباعة الحركية'),
 ('Changa',[('Changa[wght].ttf','200 800')],'ar+lat','condensed sans','display','condensed, sporty, loud | مضغوط رياضي صاخب'),
 ('Mada',[('Mada[wght].ttf','200 900')],'ar+lat','sans','UI/body','humanist, calm | إنساني هادئ'),
 ('ElMessiri',[('ElMessiri[wght].ttf','400 700')],'ar+lat','display sans','display','soft modern display, culture | عرض حديث ناعم للثقافة'),
 ('Lemonada',[('Lemonada[wght].ttf','300 700')],'ar+lat','rounded display','display','bubbly, friendly, food/kids | منتفخ ودود'),
 ('Baloo',[('BalooBhaijaan2[wght].ttf','400 800')],'ar+lat','rounded display','display','chunky rounded, cartoon/edu | سميك مستدير كرتوني'),
 ('Marhey',[('Marhey[wght].ttf','300 700')],'ar+lat','playful display','display','hand-cut playful | مرح مقصوص باليد'),
 ('Lalezar',[('Lalezar-Regular.ttf','400')],'ar+lat','heavy display','display','heavy poster/impact headlines | ثقيل للملصقات'),
 ('Rakkas',[('Rakkas-Regular.ttf','400')],'ar+lat','vintage display','display','retro cinema/poster | سينمائي قديم'),
 ('Jomhuria',[('Jomhuria-Regular.ttf','400')],'ar+lat','ultra-heavy display','display','ultra-bold condensed slogans | أسود عريض للشعارات'),
 ('Katibeh',[('Katibeh-Regular.ttf','400')],'ar+lat','calligraphic display','display','reed-pen brushy display | قلم قصب فرشاتي'),
 ('Vibes',[('Vibes-Regular.ttf','400')],'ar','decorative display','display','decorative ornamental, festive | زخرفي احتفالي'),
 ('Harmattan',[('Harmattan-Bold.ttf','700')],'ar','west-african naskh','body/display','Warsh/Maghrebi-friendly naskh | نسخ مغاربي/إفريقي'),
 ('Handjet',[('Handjet[ELGR,ELSH,wght].ttf','100 900')],'ar+lat','pixel/modular','display/tech','modular dot-matrix, LED boards, retro tech | نقطي مصفوفي، لوحات LED'),
 ('Inter',[('Inter[opsz,wght].ttf','100 900')],'lat','grotesk','UI','Latin UI workhorse | واجهات لاتينية'),
 ('SpaceGrotesk',[('SpaceGrotesk[wght].ttf','300 700')],'lat','grotesk','display/UI','techy grotesk | تقني'),
 ('Fraunces',[('Fraunces[SOFT,WONK,opsz,wght].ttf','100 900')],'lat','soft serif','display','expressive old-style serif | سيرف معبّر'),
 ('JetBrains',[('JetBrainsMono[wght].ttf','100 800')],'lat','mono','code/data','code & numbers | أكواد وأرقام'),
 ('Mono',[('IBMPlexMono-Medium.ttf','500')],'lat','mono','code/data','numbers, timestamps | أرقام وطوابع زمنية'),
]
SAMPLE_AR = 'الخطّ العربي ١٢٣٤'
css = ['/* GENERATED by tools/build_fonts.py — all fonts SIL OFL-1.1, local files (no network). */']
reg, rows = [], []
for fam, files, script, genre, role, mood in FONTS:
    for f, w in files:
        assert os.path.exists(f'{D}/{f}'), f
        css.append(f'@font-face{{font-family:"{fam}";src:url("{f}");font-weight:{w};font-display:block}}')
        t = TTFont(f'{D}/{f}', lazy=True); n = t['name']
        cpy = (n.getDebugName(0) or '').split('\n')[0][:110]
        rows.append(f'| `{fam}` | {f} | {w} | {script} | {genre} | {role} | {mood} | {cpy} |')
    reg.append(dict(family=fam, files=[f for f, _ in files], weights=[w for _, w in files], script=script, genre=genre, role=role, mood=mood))
open(f'{D}/fonts.css', 'w').write('\n'.join(css) + '\n')
open(f'{D}/fonts.js', 'w').write('// GENERATED by tools/build_fonts.py — font registry (see kit/fonts/README.md)\n'
  'window.FONT_REGISTRY = ' + json.dumps(reg, ensure_ascii=False, indent=0) + ';\n'
  '// fontsBy("kufi") / fontsBy("display") → registry rows matching genre/role/mood text\n'
  'window.fontsBy = q => FONT_REGISTRY.filter(f => (f.genre + " " + f.role + " " + f.mood + " " + f.family).toLowerCase().includes(q.toLowerCase()));\n'
  '// preload strings for FILM.fonts: fontLoads(["Cairo","Amiri"]) → ["700 60px Cairo", ...]\n'
  'window.fontLoads = fams => fams.flatMap(fam => { const f = FONT_REGISTRY.find(r => r.family === fam); if (!f) return []; return f.weights.map(w => `${w.split(" ").pop()} 60px "${fam}"`); });\n')
hdr = ('# Font kit — %d families / %d files, all **SIL Open Font License 1.1**\n\n'
 'Generated by `tools/build_fonts.py`. Include `<link rel="stylesheet" href="kit/fonts/fonts.css">` and '
 '`<script src="kit/fonts/fonts.js"></script>` (registry: `FONT_REGISTRY`, `fontsBy(q)`, `fontLoads(fams)`).\n'
 'Choosing fonts: [`library/fonts.md`](../../../library/fonts.md) · visual specimen: [`library/specimens/fonts.jpg`](../../../library/specimens/fonts.jpg).\n\n'
 'OFL-1.1 lets you use, embed, bundle and redistribute the fonts (also commercially); they may not be sold on their own, '
 'and modified versions must not use the Reserved Font Name. Full licence text: [`OFL.txt`](OFL.txt). Sources: github.com/google/fonts (ofl/*).\n\n'
 '| CSS family | file | weight | script | genre | role | mood (en / ar) | copyright |\n|---|---|---|---|---|---|---|---|\n') % (len(FONTS), sum(len(f[1]) for f in FONTS))
open(f'{D}/README.md', 'w').write(hdr + '\n'.join(rows) + '\n')
print(len(FONTS), 'families')
