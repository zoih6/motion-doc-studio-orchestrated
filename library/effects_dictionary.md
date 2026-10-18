# Effects dictionary — قاموس المؤثرات (effect → engine call → reference card)

Look up an effect by name (as a user or a reference video would say it), then build it with the listed engine calls.
Detailed theory: [compositing_fx.md](compositing_fx.md) · moves: [motion_recipes.md](motion_recipes.md) · transitions: [transitions.md](transitions.md), [gl_transitions.md](gl_transitions.md).
**Card** = a vendored shot card in `resources/skills/shotcraft-shot-cards/shots/<path>.md` (Apache-2.0, Chinese, with timing numbers; English index in [shot_cards_index.md](shot_cards_index.md)).

## Light & optics — الضوء والعدسة
| effect | العربية | build it with | card |
|---|---|---|---|
| Film grain | حبيبات | `fxGrain(t, .06)` (every look includes it) | — |
| Vignette | تعتيم الأطراف | `fxVignette(.5)` | — |
| Bloom on highlights | توهج الإضاءات | `fxBloom(.35)`. Only on light sources, never on UI | effects/light-play-moves |
| Halation (film red halo) | هالة الفيلم | `fxHalation()` | — |
| Light leak | تسرّب ضوئي | `fxLeak(t, …)` or `gl:Overexposure` as a transition | transition/transition-hidden-cut |
| God rays / volumetric beam | أشعة ضوئية | `rays()` (core) | opening/spotlight-hero-card |
| Spotlight sweep | مسح بالضوء | radial gradient mask moving with `kf()`, `globalCompositeOperation='multiply'` | effects/spotlight-sweep-moves |
| Sheen / specular sweep | لمعة عابرة | diagonal white gradient clipped to the shape, `tw()` across | effects/light-play-moves |
| Rack focus | تحويل البؤرة | `cam({fd, ap})` + `layer()` | camera/depth-layer-moves |
| Chromatic aberration | زيغ لوني | `fxChroma(2)` / `rgbSplit(img, 6)` | effects/riso-print-hits |
| Lens flash / white flash | وميض | `TRANS.flash`, or a 2-frame white `fillRect` at an impact | transition/white-flash-logo-simplify-cut |

## Texture & print — الملمس والطباعة
| effect | العربية | build it with | card |
|---|---|---|---|
| Paper texture | ملمس الورق | `kit/textures/paper_cream.jpg` + `paper()` | typography/paper-title-card |
| Torn paper edge | حافة ممزقة | `tornPoly()` + `drawTear` / `tin:'tear'` | — |
| Halftone | نقاط طباعية | `pattern('halftone', t, {tone:(x,y)=>…})` | effects/riso-print-hits |
| Riso misregistration | إزاحة الطباعة | draw twice with `tint()` in two inks, offset 3–6 px, snap together with `shakeX` | effects/riso-print-hits |
| Duotone photo | صورة ثنائية اللون | `tint(img, PAL.accent)` over a grayscale copy, `multiply` | — |
| Ink bleed reveal | انتشار الحبر | `TRANS.luma` / `gl:luma` / `gl:perlin` | transition/print-texture-transitions |
| Film burn | احتراق الفيلم | `gl:FilmBurn`, `gl:burn` | — |
| VHS / CRT | شريط فيديو قديم | `fxLook(t,'vhs')`, `pattern('lines')` scanlines at 4% | effects/scanline-annotate-focus |
| Stop-motion boil | ارتجاف الإيقاف | `move('jitter', …, {fps:12})` + `breathe()` | rhythm/sakuga-timing-shift |
| Grain dissolve | تلاشي حبيبي | `gl:StaticFade` / `TRANS.luma` with fine noise | outro/grain-dissolve |

## Shape & graphics — الأشكال
| effect | العربية | build it with | card |
|---|---|---|---|
| Path draw-on | رسم المسار | `pathDraw()`, `icon(..,{k})`, `pattern(..,{k})` | ui-entrance/draw-svg-trace |
| Hand-drawn circle | دائرة يدوية | `handCircle()` | typography/marker-underline-title |
| Marker underline | تسطير بالقلم | `marker()` | typography/marker-underline-title |
| Burst / impact lines | انفجار خطوط | `burst()` + `impact()` | effects/slam-entrance-moves, effects/impact-feedback |
| Sparkles | لمعات | `sparkles()`. Only on discrete wins, never as ambient particles (banned) | — |
| Ring pulse / ripple | تموّج دائري | `ring()`, `ripple()` | effects/radial-ripple-phone-chips |
| Reticle lock-on | تصويب وتثبيت | 4 L-corners `move('popIn')` inward + `shakeX` | effects/fui-hud-moves |
| Scan bracket | إطار المسح | corner brackets + moving gradient bar | effects/scan-bracket-sweep |
| Connection lines (red string) | خطوط الربط | `line()` with draw-on + `pulse` on nodes | effects/glow-flyline-moves |
| Islamic star lattice | نجمة هندسية | `pattern('star8'/'star12'/'girihNet', t, {k})` | — |
| Arabesque scroll | توريق | spiral `pathDraw` (log spiral) + leaf `icon('leaf')` stamped along with `staggerMove('popIn')` | — |
| Topographic lines | خطوط كنتورية | `pattern('topo', t)` (animated) | opening/dataviz-landscape-open |
| Counter / number roll | عدّاد | `counter()` (helpers) + `heartBeat` at the end | data/gauge-readout-moves |
| Chart draw | رسم بياني | bars `staggerMove('riseIn',{clip})`, lines `pathDraw` | data/chart-live-moves |
| Timeline travel | خط زمني | `camKeys` along x + ticks `popIn` | data/timeline-travel |
| Before/after slider | قبل/بعد | two layers + `clip()` at `kf(t,…)` | data/before-after-slider-scrub |

## Depth & 3D-ish — العمق
| effect | العربية | build it with | card |
|---|---|---|---|
| Parallax layers | اختلاف المنظر | `cam()` + `layer(depth, fn)` | camera/depth-layer-moves |
| Card flip | قلب البطاقة | `flipInY`/`flipCoin` + `st.shade` | transition/card-flip-reveal |
| Exploded view | عرض مفكك | parts `move('backInUp')` along their normals, reverse to assemble | camera/space-camera-moves |
| Extrude / 3D type | نص بارز | `extrude(img, depth)` | — |
| Cloner echo | صدى مستنسخ | `echo(img, n, dx, dy)` | ui-entrance/cloner-depth-echo |
| Crash zoom | زوم صادم | `TRANS.zoom` or `cam({z})` 6 frames `E.expoIn` + `impact()` | camera/crash-zoom-punch |
| Cube / doorway switch | انتقال مكعب | `gl:cube`, `gl:doorway` | transition/wipe-transitions |
| Contact shadow lift | رفع الظل | `hover` loop → scale the shadow with `st.shadow` | ui-entrance/element-body-moves |

## Text-specific — النص
| effect | العربية | build it with | card |
|---|---|---|---|
| Word pop / slam | ظهور الكلمة بقوة | `drawWords(…,'pop'|'slam')` | effects/slam-entrance-moves |
| Blur-slide words | انزلاق ضبابي | `drawWords(…,'blur')` | typography/blur-slide |
| Weight pump | نبض السماكة | variable font weight `_wm()` on beat | typography/type-rhythm-sync |
| Karaoke fill | تعبئة متزامنة | `voTimes()` + `activeIndex()` | typography/type-rhythm-sync |
| Word slot cycle | تبديل كلمة | `blurSwap()` / vertical roll with `slideInUp` + `fadeOutUp` | typography/pill-slot-cycle |
| Text as window | نص كنافذة | `g.clip()` on the text path, draw video/image inside | opening/text-as-mask |
| Title demote to label | العنوان يصبح وسمًا | `kf()` on scale + position to a corner, then hold | typography/title-demote-to-label |
| Typewriter with retype | كتابة وتصحيح | `typeIn` + backspace by reversing `reveal` | typography/typewriter-moves |
| Glitch text cycle | نص مشوّش | random glyph swap for Latin; for Arabic swap whole words + `rgbSplit` | typography/glitch-cycle |
