# Motion-design glossary — قاموس مصطلحات الموشن جرافيك (EN ⇄ AR)

A working dictionary: each term → Arabic → one-line meaning → **where it lives in this repo** (so a word in a brief maps straight to code).
Related dictionaries: [motion_recipes.md](motion_recipes.md) (84 named moves) · [motion_vocabulary.md](motion_vocabulary.md) (camera & editorial phrasing) · [transitions.md](transitions.md) + [gl_transitions.md](gl_transitions.md) · [style_catalog.md](style_catalog.md) · [effects_dictionary.md](effects_dictionary.md) · vendored glossary: [resources/skills/emilkowalski/animation-vocabulary](../resources/skills/emilkowalski/animation-vocabulary/SKILL.md).

## 1 · Timing, easing, physics — التوقيت والتسارع والفيزياء
| term | العربية | meaning | in repo |
|---|---|---|---|
| Keyframe | إطار مفتاحي | a defined value at a defined time; the engine interpolates between | `kf()` fx.js §1 |
| Tween / interpolation | استيفاء / تحريك بيني | generating in-between values | `tw()`, `lerp()` |
| Easing | منحنى التسارع | how speed changes across a move | `E.*`, `CURVE.*` |
| Ease-out (decelerate) | تباطؤ في النهاية | fast start, soft landing; default for entrances | `E.cubicOut`, `CURVE.signature` |
| Ease-in (accelerate) | تسارع في البداية | slow start, fast leave; for exits | `E.cubicIn`, `CURVE.md3Accel` |
| Ease-in-out | تسارع ثم تباطؤ | camera moves, position swaps | `CURVE.camera` |
| Cubic-bezier | منحنى بيزييه | 4-number curve definition (CSS/AE) | `bezier(x1,y1,x2,y2)` |
| Overshoot | تجاوز ثم ارتداد | passes the target then settles | `CURVE.overshoot`, `popIn` |
| Anticipation | تمهيد / استعداد | small opposite move before the main move | `CURVE.anticipate`, `stretch` |
| Follow-through | استمرار الحركة | parts keep moving after the body stops | `springIn`, `swing` |
| Overlapping action | تداخل الحركات | parts move at different times/rates | `staggerMove` |
| Spring | نابض | physical motion with stiffness/damping | `spring()`, `spr()`, `SPRINGS` |
| Stiffness / damping | الصلابة / التخميد | how strong / how quickly a spring stops wobbling | `SPRINGS.wobbly=[180,12]` |
| Squash & stretch | الانضغاط والتمدد | volume-preserving deformation that shows weight | `squash`, `stretch`, `dropIn` |
| Arc | القوس | natural motion paths curve, not straight | `orbit`, `camKeys` |
| Slow-in / slow-out | بطء الدخول والخروج | Disney principle = easing | `E.*` |
| Hold | ثبات | frames with no change so the eye can read | rules/motion_rules.md |
| Stagger / cascade | تتابع متدرّج | same move offset per item | `staggerMove`, `staggerIn` |
| Orchestration | تنسيق الحركة | multiple moves timed as one gesture | recipes table |
| Beat / on-beat | نبضة / على الإيقاع | cut or hit exactly on a music/VO accent | `punch`, workflow/05_build.md |
| Speed ramp | تغيير السرعة | time remapped: fast → slow → fast | shotcraft `speed-ramp-freeze` |
| Frame rate (fps) | معدل الإطارات | 30 fps house standard; integer-frame boundaries | `tools/render_seg.py` |
| On twos / on threes | كل إطارين / ثلاثة | hold each drawing 2–3 frames (stop-motion feel) | `jitter` (fps 12) |
| Motion blur | ضبابية الحركة | smear along movement direction | `smearDraw`, `whipIn` |
| Wiggle | اهتزاز عشوائي | seeded noise offset (AE `wiggle()`) | `wiggle()`, `drift` |
| Persona (motion personality) | شخصية الحركة | one set of durations/curves for the film | `PERSONA` |

## 2 · Entrances, exits, emphasis — الدخول والخروج والتأكيد
| term | العربية | meaning | in repo |
|---|---|---|---|
| Entrance / build-in | دخول | how an element appears | `MOVES` type `in` |
| Exit / build-out | خروج | how it leaves | type `out` |
| Emphasis | تأكيد | motion on an element already on screen | type `emph` |
| Pop-in | ظهور قافز | scale with overshoot | `popIn` |
| Reveal | كشف | uncover with a mask or clip | `riseIn`, `maskReveal` |
| Wipe | مسح | hard-edge mask sweeping across | `wipeOut`, `TRANS.band` |
| Draw-on / write-on | رسم تدريجي | stroke appears along its path | `icon({k})`, `pathDraw`, `writeOn` |
| Typewriter | آلة كاتبة | characters/words appear in sequence | `typeIn`, `drawWords('type')` |
| Morph | تحوّل الشكل | one shape becomes another | `gl:morph`, `blurSwap` |
| Shared-element transition | انتقال العنصر المشترك | an element travels from shot A into shot B | motion_vocabulary.md |
| Hinge | المفصلة | swings off a corner and falls | `hinge` |
| Idle / ambient loop | حركة خاملة | small continuous life on secondary items | type `loop` |

## 3 · Camera — الكاميرا
| term | العربية | meaning | in repo |
|---|---|---|---|
| Dolly in/out | دفع / سحب الكاميرا | camera moves toward/away (parallax changes) | `cam({z})` |
| Zoom | تقريب بالعدسة | lens change, no parallax | `cam({z})` flat |
| Truck / pan | تحريك جانبي / بانورامي | sideways move / rotate | `cam({x})` |
| Pedestal / tilt | رفع-خفض / إمالة | vertical move / rotate | `cam({y})` |
| Roll / Dutch angle | دوران / زاوية مائلة | rotation around the lens axis | `cam({r})` |
| Orbit / arc shot | دوران حول الهدف | camera circles the subject | `cam({ox})` |
| Dolly-zoom (vertigo) | زوم هيتشكوك | background warps while subject stays | `cam({vz})` |
| Rack focus | تحويل البؤرة | focus pulls between depth planes | `cam({fd, ap})` |
| Handheld | محمولة باليد | organic camera noise | `handheld()` |
| Crash zoom | زوم صادم | very fast push into a detail | `TRANS.zoom`, shotcraft `crash-zoom-punch` |
| Parallax | اختلاف المنظر | layers at different depths move at different speeds | `layer(depth, fn)` |
| Establishing shot | لقطة تأسيسية | wide shot that shows where we are | camera_language.md |
| Close-up / insert | لقطة قريبة / إدراج | detail shot | camera_language.md |
| Rule of thirds | قاعدة الأثلاث | key points on the 1/3 grid lines | shot-composition skill |
| Headroom / lead room | فراغ الرأس / فراغ الاتجاه | space above / in front of the subject | `resources/skills/iart-motion-design/shot-composition` |
| Safe area | المنطقة الآمنة | 5% (action) / 10% (title) margins | rules/design_rules.md |

## 4 · Editing & transitions — المونتاج والانتقالات
| term | العربية | meaning | in repo |
|---|---|---|---|
| Hard cut | قطع مباشر | instant switch | `tin:'cut'` |
| Match cut | قطع متطابق | shape/motion continues across the cut | transitions.md |
| J-cut / L-cut | قطع J / L | audio leads / trails the picture | workflow/05_build.md |
| Whip pan | التفاف سريع | blurred sideways rush between shots | `TRANS.whip` |
| Dip to black | تلاشي للأسود | fade through a colour | `TRANS.dip` |
| Iris | فتحة دائرية | circle open/close | `TRANS.iris`, `gl:circleopen` |
| Luma wipe | مسح بالإضاءة | dissolve driven by a grayscale map | `TRANS.luma`, `gl:luma` |
| Glitch | خلل رقمي | slice offsets + RGB split | `TRANS.glitch`, `gl:GlitchMemories` |
| Hidden cut | قطع مخفي | cut hidden behind a foreground wipe/flash | shotcraft `transition-hidden-cut` |
| Jump cut | قطع قافز | same framing, time skips | shotcraft `rhythm-interrupt-moves` |
| Montage | مونتاج متتابع | sequence of shots that compress time | workflow/02_treatment.md |
| Pacing | الإيقاع | rate of new information (house: something new every 2–4 s) | rules/motion_rules.md |
| Hook | خطّاف | the first 2 s that earn attention | workflow/02_treatment.md |
| Bumper / sting | فاصل قصير | 1–3 s branded interstitial | recipes |

## 5 · Typography — الطباعة الحركية
| term | العربية | meaning | in repo |
|---|---|---|---|
| Kinetic typography | الطباعة الحركية | text as the moving subject | kinetic_typography.md, `drawWords` |
| Display face / UI face | خط العرض / خط الواجهة | headline font / caption font (1 each) | fonts.md |
| Variable font | خط متغيّر | continuous weight/width axes → weight morph | `Cairo`, `Readex`, `_wm` |
| Kerning / tracking | تقنين المسافات / التباعد | letter-space between pairs / all letters | (Latin only, not Arabic) |
| Leading (line height) | تباعد الأسطر | vertical distance between lines | fonts.md §4 |
| Kashida / tatweel | الكشيدة / التطويل | Arabic elongation stroke ـ | fonts.md §4 |
| Tashkeel | التشكيل | Arabic vowel marks | fonts.md §4 |
| Karaoke highlight | تظليل متزامن | words light up with the VO | `voTimes`, `activeIndex` |
| Marker sweep | تظليل بالقلم | highlighter bar behind a word | `marker()` |
| Lower third | الثلث السفلي | name/title strip at the bottom | style_presets.md |
| Callout | تعليق توضيحي | leader line + label pointing at a detail | `callout()` |
| Text mask | قناع النص | image/video visible through letters | shotcraft `text-as-mask` |

## 6 · Compositing & FX — التركيب والمؤثرات
| term | العربية | meaning | in repo |
|---|---|---|---|
| Layer / precomp | طبقة / تركيب مسبق | stacked drawing units / nested group | `layer()`, offscreen `mk()` |
| Mask / matte | قناع | defines visible area | `g.clip()`, `maskReveal` |
| Blend mode | وضع الدمج | multiply/screen/overlay compositing | `globalCompositeOperation` |
| Grain | حبيبات الفيلم | animated noise texture | `fxGrain` |
| Vignette | تعتيم الأطراف | darkened edges | `fxVignette` |
| Bloom / halation | توهّج / هالة | light spills from bright areas (film halo = red) | `fxBloom`, `fxHalation` |
| Chromatic aberration | زيغ لوني | RGB channel offset | `fxChroma`, `rgbSplit` |
| Light leak | تسرّب ضوئي | warm film light washes | `fxLeak` |
| Colour grade / LUT | تدريج لوني | global colour transform | `fxGrade`, `LOOKS` |
| Lift / gamma / gain | الظلال / المتوسطات / الإضاءات | 3-way grade controls | `fxGrade({lift,gamma,gain})` |
| Halftone | نقاط طباعية | tone as dot size | `pattern('halftone')` |
| Duotone | ثنائي اللون | image mapped to two inks | `tint()`, effects_dictionary.md |
| Cut-out / sticker | قصاصة / ملصق | subject isolated with an outline | `cutout`, `outline()`, `sticker()` |
| Extrude | بروز ثلاثي | fake depth by stacked offsets | `extrude()` |
| Drop shadow / contact shadow | ظل ساقط / ظل تلامس | separation from background / sense of touching the surface | `card()`, `hover` loop |

## 7 · Colour — اللون
| term | العربية | meaning | in repo |
|---|---|---|---|
| Palette roles | أدوار الألوان | bg / ink / paper / accent / accent2 / muted | `paletteRoles()` |
| Accent colour | لون التمييز | the ONE colour that points at meaning | rules/design_rules.md |
| Contrast ratio | نسبة التباين | WCAG: ≥4.5 text, ≥3 display | `contrast()` |
| OKLCH | فضاء OKLCH | perceptual lightness/chroma/hue; mixes never go muddy | `oklch()`, `mixOK()` |
| Value / lightness | القيمة / الإضاءة | light-dark structure (read it in grayscale) | color_systems.md |
| Saturation / chroma | التشبّع | colour intensity | `palettesBy({minChroma})` |
| Complementary / analogous | متكامل / متجاور | opposite / neighbouring hues | color_systems.md |
| Colour script | سيناريو الألوان | colour arc across the film's acts | color_systems.md |

## 8 · Islamic & Arabic visual arts — الفنون الإسلامية والعربية (for style and asset briefs)
| term | العربية | meaning | in repo |
|---|---|---|---|
| Khatt | الخط | calligraphy; main scripts below | fonts.md |
| Kufi | الكوفي | angular early script; square kufi in architecture | `Qahiri`, `ReemKufi`, `Kufi` |
| Naskh | النسخ | standard book hand | `Naskh`, `Amiri`, `Scheherazade` |
| Thuluth | الثلث | monumental cursive for titles and inscriptions | examples/thuluth film |
| Ruqʿa | الرقعة | quick everyday hand | `Ruqaa` |
| Nastaʿlīq | النستعليق | hanging Persian script | `Nastaliq`, `Gulzar` |
| Diwani | الديواني | Ottoman chancery script (dense, curvy) | asset_sourcing.md (no OFL font) |
| Maghribi | المغربي | North-African/Andalusian script | `Harmattan` (nearest) |
| Tughra | الطغراء | Ottoman calligraphic monogram/seal | `stampIn` recipe |
| Zakhrafa | الزخرفة | ornament in general | `pattern()` |
| Arabesque / tawrīq | الأرابيسك / التوريق | endless vegetal scroll | effects_dictionary.md |
| Girih | الكريه (عقدة) | strapwork of 5/10-fold stars | `pattern('girihNet')` |
| Khatam (8-point star) | الخاتم / النجمة الثمانية | 8-fold star lattice | `pattern('star8')` |
| Rosette (shamsa) | الشمسة / الوردة | radial star medallion | `pattern('rosette')` |
| Muqarnas | المقرنصات | stalactite vaulting | asset_sourcing.md |
| Mashrabiya | المشربية | turned-wood lattice screen | `pattern('mashrabiya')` |
| Zellige | الزليج | Moroccan cut-tile mosaic | `HERITAGE.andalusZellige` |
| Iznik | إزنيق | Ottoman cobalt/tomato/turquoise ceramics | `HERITAGE.iznikTile` |
| Tazhib / illumination | التذهيب | gold manuscript ornament | `HERITAGE.mamlukGold`, `goldify()` |
| ʿUnwān / sarlawh | العنوان / السرلوح | illuminated headpiece of a manuscript | style_catalog.md |
| Ebru | الإبرو (الرخامي) | marbled paper | `gl:Swirl`, `gl:ripple` |
| Qamariya | القمرية | Yemeni stained-glass half-moon window | `HERITAGE.sanaaOldCity` |
| Mihrab | المحراب | prayer niche (arch frame) | composition motif |

## 9 · Production — الإنتاج
| term | العربية | meaning | in repo |
|---|---|---|---|
| Brief | موجز الطلب | goals, audience, tone, length | workflow/00_intake.md |
| Script / VO | النص / التعليق الصوتي | narration that drives the timeline | workflow/01_setup_and_vo.md |
| Storyboard / animatic | لوحة القصة / الأنيماتك | key frames / timed rough cut | workflow/02_treatment.md |
| Style frame | إطار الأسلوب | one finished still that sets the look | workflow/03_style_bible.md |
| Contact sheet | ورقة المعاينة | grid of frames for critique | `tools/cs.sh` |
| Render | التصيير | turning the timeline into frames/video | `tools/render.mjs` |
| Loudness (LUFS) | الجهارة | perceived audio level; house −14 LUFS (calm −18) | `sound-layer/scripts/mix.py` + `qa.py` |
| Ducking | خفض الموسيقى | music dips under VO | mix.py `duck_db` (qa.py `voice`) |
| SFX / foley | المؤثرات الصوتية | whooshes, hits, paper, ink: real CC0 recordings only | `sfx.py kit/browse` · `engine/cues.js` |
| Sound cue | نقطة صوت | a sound tied to a frame: cut · move · land · appear · hero | `cue.*` → `tools/export_cues.mjs` |
| Hero hit | الضربة البطلة | one per ~4 s on a logo/reveal: thump+tap, dead stop + build | `cue.hero` |
| Deliverables | المخرجات | final.mp4, contact.png, poster.png | workflow/07_render_deliver.md |
