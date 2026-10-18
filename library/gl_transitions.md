# GPU transitions pack — 125 gl-transitions (MIT/BSD)

**Data:** [`engine/kit/data/gl_transitions.js`](../engine/kit/data/gl_transitions.js) (all GLSL sources, author + licence header kept) · **Runner:** [`engine/gl.js`](../engine/gl.js) · **Licence:** [`resources/licenses/gl-transitions.txt`](../resources/licenses/gl-transitions.txt) · **Upstream:** github.com/gl-transitions/gl-transitions
**Hand-made canvas transitions (16):** [transitions.md](transitions.md) (`whip`, `zoom`, `iris`, `band`…) — prefer those for VOX-style graphic cuts; use the GL pack for organic/optical/3D effects.

## Use
```html
<script src="kit/data/gl_transitions.js"></script>   <!-- after fx.js -->
<script src="gl.js"></script>
```
```js
SHOTS.push({ a: 12, b: 20, draw: s05, tin: 'gl:Dreamy', tdur: .9 });
SHOTS.push({ a: 20, b: 26, draw: s06, tin: 'gl:directionalwarp', glParams: { direction: [-1, 0] } });   // RTL: travel right→left
SHOTS.push({ a: 26, b: 31, draw: s07, tin: 'gl:ripple', glEase: 'linear' });
// direct use anywhere (e.g. a morph inside one shot): g.drawImage(GLT.frame('cube', canvasA, canvasB, k, {persp: .7}), 0, 0)
```
Headless rendering: chromium needs WebGL. Default headless Chromium provides it (v2.1 no longer forces SwiftShader for 2D; if WebGL is missing on your machine run with `RENDER_GL=swiftshader` / `render.mjs --gl swiftshader`). Cost ≈ 15–40 ms per transition frame at 1080p.

## Curated picks by intent (documentary / explainer)

| intent | pick | why |
|---|---|---|
| time passes / memory | `gl:Dreamy`, `gl:ripple`, `gl:luminance_melt`, `gl:morph` | soft, liquid, no hard edge |
| archive / old film | `gl:FilmBurn`, `gl:burn`, `gl:fadegrayscale`, `gl:Overexposure` | optical film artefacts |
| ink / calligraphy | `gl:luma` (fbm map), `gl:perlin`, `gl:undulatingBurnOut`, `gl:displacement` | ink-bleed reveals |
| geometry / Islamic art | `gl:hexagonalize`, `gl:powerKaleido`, `gl:kaleidoscope`, `gl:polar_function`, `gl:pinwheel` | tessellation & symmetry |
| page / document | `gl:BookFlip`, `gl:InvertedPageCurl` (BSD-3), `gl:Swirl` | turning pages |
| 3D / space | `gl:cube`, `gl:doorway`, `gl:swap`, `gl:GridFlip`, `gl:Rolls` | volumetric switch |
| digital / modern | `gl:GlitchMemories`, `gl:glitch` (canvas), `gl:DoomScreenTransition`, `gl:StaticFade`, `gl:TVStatic` | tech contrast |
| directional travel (RTL) | `gl:directionalwarp`, `gl:wind`, `gl:directional-easing`, `gl:CrossZoom` | motivated movement |
| graphic wipes | `gl:circleopen`, `gl:heart`, `gl:StarWipe`, `gl:windowslice`, `gl:squareswire`, `gl:angular` | shape cuts (prefer canvas `iris/band` for VOX) |
| impact / punch | `gl:CrossZoom`, `gl:ZoomInCircles`, `gl:SimpleZoom`, `gl:flyeye` | energy spikes |

**Rules:** max 1 GL transition per 20–30 s in documentary pacing; never two different GL looks back-to-back; match the motivation (what moves in shot A continues into shot B); hard cuts stay the default (see [transitions.md](transitions.md)).

<!-- AUTO -->
## Catalogue (generated from engine/kit/data/gl_transitions.js — 125 transitions)
Contact sheet at progress .5: [specimens/gl_transitions.jpg](specimens/gl_transitions.jpg)

| shot.tin | description | author | licence | uniforms (= default) → shot.glParams |
|---|---|---|---|---|
| `gl:AdvancedMosaic` | Both images break into large blocks that blend, then sharpen into the incoming image | Sergey Kosarevsky | MIT | pixelSize=50.0 |
| `gl:BlockDissolve` | The incoming image appears in small random blocks | nwoeanhinnogaehr | MIT | blocksize=0.02 |
| `gl:BookFlip` | The outgoing image turns like a book page from right to left, revealing the incoming one | hong | MIT | — |
| `gl:Bounce` | The outgoing image drops out of the frame with a few bounces, revealing the incoming one | Adrian Purser | MIT | shadow_colour=vec4(0.,0.,0.,.6), shadow_height=0.075, bounces=3.0 |
| `gl:BowTieHorizontal` | Two triangles grow from the left and right edges into a bow tie that reveals the incoming image | huynx | MIT | — |
| `gl:BowTieVertical` | Two triangles grow from the top and bottom edges into a bow tie that reveals the incoming image | huynx | MIT | — |
| `gl:BowTieWithParameter` | A bow-tie wipe with an adjustable shape that can run in reverse | KMojek | MIT | adjust=0.5, reverse=false |
| `gl:Box` | The outgoing image shrinks into a box, toward the center or a corner, revealing the incoming one | lql | MIT | rectIn=1, location=0 |
| `gl:ButterflyWaveScrawler` | Wavy, color-separated ripples scramble the outgoing image into the incoming one | mandubian | MIT | amplitude=1.0, waves=30.0, colorSeparation=0.3 |
| `gl:CircleCrop` | The outgoing image closes into a circle over a background color, then the incoming one opens from it | fkuteken | MIT | bgcolor=vec4(0.0, 0.0, 0.0, 1.0) |
| `gl:ColourDistance` | Pixels switch to the incoming image in order of how close their colors are | P-Seebauer | MIT | power=5.0 |
| `gl:CrazyParametricFun` | The outgoing image is pulled along a parametric curve into a psychedelic swirl | mandubian | MIT | a=4, b=1, amplitude=120, smoothness=0.1 |
| `gl:CrossZoom` | A crossfade through a strong zoom blur | rectalogic | MIT | strength=0.4 |
| `gl:DefocusBlur` | A crossfade through an out-of-focus blur | Sergey Kosarevsky | MIT | blurSize=0.02 |
| `gl:Directional` | The incoming image pushes the outgoing one out in a given direction | Gaëtan Renaudeau | MIT | direction=vec2(0.0, 1.0) |
| `gl:DirectionalScaled` | Like Directional, with both images scaled down while they slide | Thibaut Foussard | MIT | direction=vec2(0.0, 1.0), scale=.7 |
| `gl:DoomScreenTransition` | The outgoing image melts down in uneven columns, like the Doom screen wipe | Zeh Fernando | MIT | bars=30, amplitude=2, noise=0.1, frequency=0.5, dripScale=0.5 |
| `gl:Dreamy` | A crossfade with a gentle wavy distortion | mikolalysenko | MIT | — |
| `gl:DreamyZoom` | Zooms and rotates into a bright flash, then out to the incoming image | Zeh Fernando | MIT | rotation=6, scale=1.2 |
| `gl:Drop_Zone_Flicker` | A flickering glitch with RGB offset, ghosting and scanlines that flashes back to the outgoing image | bread | MIT | frameRate=24.0, rgbOffset=0.014, blockAmount=0.72, ghostAmount=0.62, redCyan=0.58, scanline=0.075 |
| `gl:EdgeTransition` | Both images fade through black with their edges glowing | Woohyun Kim | MIT | edge_thickness=0.001, edge_brightness=8.0 |
| `gl:FilmBurn` | Glowing film-burn light leaks wash over the image and reveal the incoming one | Anastasia Dunbar | MIT | Seed=2.31 |
| `gl:Fold` | The incoming image unfolds from the left while the outgoing one folds away to the right | nwoeanhinnogaehr | MIT | — |
| `gl:GlitchDisplace` | Blocks of the image are displaced in a glitch that flashes into the incoming image | Matt DesLauriers | MIT | — |
| `gl:GlitchMemories` | A crossfade with glitchy, color-shifted blocks | Gunnar Roth | MIT | — |
| `gl:GridFlip` | The image splits into a grid of tiles that flip one by one to the incoming image | TimDonselaar | MIT | size=ivec2(4), pause=0.1, dividerWidth=0.05, bgcolor=vec4(0.0, 0.0, 0.0, 1.0), randomness=0.1 |
| `gl:HSVfade` | A crossfade through the HSV color space that cycles through hues | nwoeanhinnogaehr | MIT | — |
| `gl:HorizontalClose` | The incoming image closes in from the top and bottom edges toward the middle | martiniti | MIT | — |
| `gl:HorizontalOpen` | The incoming image opens from a line in the middle toward the top and bottom edges | martiniti | MIT | — |
| `gl:InvertedPageCurl` | The outgoing image curls away like a page, revealing the incoming one | Hewlett-Packard | BSD 3 Clause | — |
| `gl:LeftRight` | The outgoing image shrinks away to the left while the incoming one slides in from the right | zhmy | MIT | — |
| `gl:LinearBlur` | A crossfade through a blur | gre | MIT | intensity=0.1 |
| `gl:Mosaic` | The view pans across a mosaic of rotated tiles from both images and settles on the incoming one | Xaychru | MIT | endx=2, endy=-1 |
| `gl:Overexposure` | A crossfade through a washed-out, overexposed white | Ben Zhang | MIT | strength=0.6 |
| `gl:PolkaDotsCurtain` | The incoming image appears through growing polka dots | bobylito | MIT | dots=20.0, center=vec2(0, 0) |
| `gl:PuzzleRight` | The image splits into a grid of tiles that flip one by one to the incoming image | JustKirillS | MIT | size=ivec2(4, 4), pause=0.1, dividerWidth=0.005 |
| `gl:Radial` | A radial wipe that sweeps around the center like a clock hand | Xaychru | MIT | smoothness=1.0 |
| `gl:Rectangle` | A rectangle grows from the center to cover the outgoing image, then shrinks to reveal the incoming one | martiniti | MIT | bgcolor=vec4(0.0, 0.0, 0.0, 1.0) |
| `gl:RectangleCrop` | The outgoing image shrinks into a small rectangle over a background color, then the incoming one grows from it | martiniti | MIT | bgcolor=vec4(0.0, 0.0, 0.0, 1.0) |
| `gl:Revolve_Left` | The outgoing image swirls and zooms with motion blur into the incoming one | bread | MIT | center=vec2(0.46, 0.52), direction=-1.0, maxRotation=1.95, peakZoom=2.22, swirl=2.85, barrel=0.38, motionBlur=1.0, switchStart=0.30, switchEnd=0.50, shadow=0.16 |
| `gl:Rolls` | The outgoing image rolls away around a corner, revealing the incoming one | Mark Craig | MIT | type=0, RotDown=false |
| `gl:RotateScaleVanish` | The outgoing image spins and shrinks away over the incoming one | Mark Craig | MIT | FadeInSecond=true, ReverseEffect=false, ReverseRotation=false |
| `gl:SimpleFlip` | The outgoing image flips around the vertical axis into the incoming one | nwoeanhinnogaehr | MIT | — |
| `gl:SimpleZoom` | Zooms into the outgoing image, then fades to the incoming one | 0gust1 | MIT | zoom_quickness=0.8 |
| `gl:SimpleZoomOut` | The incoming image zooms out into place while fading in | Tianshuo | MIT | zoom_quickness=0.8, fade=true |
| `gl:Slides` | The outgoing image slides out, or the incoming one slides in, toward an edge, a corner or the center | Mark Craig | MIT | type=0, In=false |
| `gl:StarWipe` | A growing star reveals the incoming image | Ben Lucas | MIT | border_thickness=0.01, star_rotation=0.75, border_color=vec4(1.0), star_center=vec2(0.5) |
| `gl:StaticFade` | Cuts to the incoming image halfway, hidden behind a burst of TV static | Ben Lucas | MIT | n_noise_pixels=200.0, static_luminosity=0.8 |
| `gl:StereoViewer` | Both images shrink into rounded cards that swap, like a stereo viewer toy | Ted Schundler | BSD 2 Clause | zoom=0.88, corner_radius=0.22 |
| `gl:StripDatamoshGlitch` | A datamosh glitch: torn strips, chroma shifts and scan noise drag the outgoing image into the incoming one | bread | MIT | strength=1.0, horizontalBars=42.0, verticalSlits=18.0, tear=0.18, chroma=0.032, residue=0.62, noiseAmount=0.16, scanAmount=0.13, flashAmount=0.20 |
| `gl:Swirl` | Both images swirl around the center while crossfading | Sergey Kosarevsky | MIT | — |
| `gl:TVStatic` | Cuts to full-screen TV static, then to the incoming image | Brandon Anzaldi | MIT | offset=0.05 |
| `gl:TilesWave` | The incoming image is revealed tile by tile in a diagonal wave | numb3r23 | MIT | tileCount=ivec2(8, 8), flipX=true, flipY=false |
| `gl:TopBottom` | The outgoing image shrinks away upward while the incoming one slides in from the bottom | zhmy | MIT | — |
| `gl:VerticalClose` | The incoming image closes in from the left and right edges toward the middle | martiniti | MIT | — |
| `gl:VerticalOpen` | The incoming image opens from a line in the middle toward the left and right edges | martiniti | MIT | — |
| `gl:WaterDrop` | Ripples spread from the center like a drop falling into water, crossfading to the incoming image | Paweł Płóciennik | MIT | amplitude=30, speed=30 |
| `gl:ZoomInCircles` | Concentric rings of the outgoing image zoom at different speeds before revealing the incoming one | dycm8009 | MIT | — |
| `gl:ZoomLeftWipe` | Zooms into the outgoing image, then the incoming one wipes in from right to left | Handk | MIT | zoom_quickness=0.8 |
| `gl:ZoomRigthWipe` | Zooms into the outgoing image, then the incoming one wipes in from left to right | Handk | MIT | zoom_quickness=0.8 |
| `gl:angular` | A wipe that sweeps around the center from a starting angle | Fernando Kuteken | MIT | startingAngle=90 |
| `gl:burn` | A crossfade that brightens toward a color in the middle | gre | MIT | color=vec3(0.9, 0.4, 0.2) |
| `gl:burn0` | The outgoing image burns away in noisy, glowing patches | liubailin2020@gmail.com | MIT | burnColor=vec3(1.0, 0.5, 0.0) |
| `gl:cannabisleaf` | A cannabis-leaf shape grows from the center to reveal the incoming image | @Flexi23 | MIT | — |
| `gl:chessboard` | A chessboard pattern of squares reveals the incoming image | lql | MIT | grid_num=10.0 |
| `gl:circle` | The outgoing image closes into a circle over a background color, then the incoming one opens from it | Fernando Kuteken | MIT | center=vec2(0.5, 0.5), backColor=vec3(0.1, 0.1, 0.1) |
| `gl:circleopen` | A soft-edged circle opens from the center to reveal the incoming image | gre | MIT | smoothness=0.3, opening=true |
| `gl:colorphase` | A crossfade in which each color channel changes at a different time | gre | MIT | fromStep=vec4(0.0, 0.2, 0.4, 0.0), toStep=vec4(0.6, 0.8, 1.0, 1.0) |
| `gl:coord-from-in` | A crossfade in which the colors of one image displace the other | haiyoucuv | MIT | — |
| `gl:crosshatch` | The incoming image appears through a crosshatch of lines spreading from the center | pthrasher | MIT | center=vec2(0.5), threshold=3.0, fadeEdge=0.1 |
| `gl:crosswarp` | The outgoing image zooms in while the incoming one zooms out into place, sweeping from right to left | Eke Péter <peterekepeter@gmail.com> | MIT | — |
| `gl:cube` | The two images are faces of a rotating 3D cube, with a floor reflection | gre | MIT | persp=0.7, unzoom=0.3, reflection=0.4, floating=3.0 |
| `gl:directional-easing` | Like Directional, with an eased movement | Max Plotnikov | MIT | direction=vec2(0.0, 1.0) |
| `gl:directionalwarp` | A diagonal wipe with a warped, smeared edge | pschroen | MIT | smoothness=0.1, direction=vec2(-1.0, 1.0) |
| `gl:directionalwipe` | A soft-edged diagonal wipe | gre | MIT | direction=vec2(1.0, -1.0), smoothness=0.5 |
| `gl:displacement` | A crossfade in which a displacement map (an extra grayscale texture) warps both images | Travis Fischer | MIT | displacementMap, strength=0.5 |
| `gl:dissolve` | The incoming image spreads over the outgoing one with a hot, glowing edge | hjm1fb | MIT | uLineWidth=0.1, uSpreadClr=vec3(1.0, 0.0, 0.0), uHotClr=vec3(0.9, 0.9, 0.2), uPow=5.0, uIntensity=1.0 |
| `gl:doorway` | The outgoing image opens like double doors as the incoming one comes forward, with a floor reflection | gre | MIT | reflection=0.4, perspective=0.4, depth=3 |
| `gl:fade` | A linear crossfade between the two images | gre | MIT | — |
| `gl:fadecolor` | A fade through a solid color, black by default | gre | MIT | color=vec3(0.0), colorPhase=0.4 |
| `gl:fadegrayscale` | A crossfade through grayscale | gre | MIT | intensity=0.3 |
| `gl:flyeye` | The image breaks into a fly's-eye grid of lenses with color separation | gre | MIT | size=0.04, zoom=50.0, colorSeparation=0.3 |
| `gl:fragment` | The outgoing image shatters into fragments that fly away | lbl | MIT | — |
| `gl:heart` | A heart shape grows from the center to reveal the incoming image | gre | MIT | — |
| `gl:hexagonalize` | Both images turn into hexagons, crossfade, then sharpen again | Fernando Kuteken | MIT | steps=50, horizontalHexagons=20 |
| `gl:kaleidoscope` | A crossfade through a spinning kaleidoscope | nwoeanhinnogaehr | MIT | speed=1.0, angle=1.0, power=1.5 |
| `gl:luma` | A wipe that follows the brightness of a grayscale mask (the luma texture) | gre | MIT | luma |
| `gl:luminance_melt` | The outgoing image melts away in noisy vertical streaks, depending on its brightness | 0gust1 | MIT | direction=true, l_threshold=0.8, above=false |
| `gl:morph` | A crossfade in which each image is displaced by the other's colors, like a morph | paniq | MIT | strength=0.1 |
| `gl:mosaic_transition` | Both images break into mosaic blocks that blend, then sharpen into the incoming image | YueDev | MIT | mosaicNum=10.0 |
| `gl:multiply_blend` | A crossfade through the multiplied blend of both images | Fernando Kuteken | MIT | — |
| `gl:old_tv_lost_signal` | A crossfade with drifting tracking lines and tearing, like a TV losing its signal | mernking (gitlab.com/Godswork) | MIT | — |
| `gl:parametric_glitch` | A crossfade with glitchy horizontal bands and color shifts | Yoni Maltsman @friendlyspinach | MIT | ampx=1.0, ampy=1.0 |
| `gl:perlin` | The incoming image appears through blobs of Perlin noise | Rich Harris | MIT | scale=4.0, smoothness=0.01, seed=12.9898 |
| `gl:pinwheel` | A spinning pinwheel reveals the incoming image | Mr Speaker | MIT | speed=2.0 |
| `gl:pixelize` | Both images pixelate, crossfade, then sharpen again | gre | MIT | squaresMin=ivec2(20), steps=50 |
| `gl:polar_function` | A flower shape with several petals grows to reveal the incoming image | Fernando Kuteken | MIT | segments=5 |
| `gl:powerKaleido` | The image folds into an animated kaleidoscope before revealing the incoming one | Boundless | MIT | scale=2.0, z=1.5, speed=5. |
| `gl:randomNoisex` | The incoming image appears pixel by pixel in random noise | towrabbit | MIT | — |
| `gl:randomsquares` | The incoming image appears in random squares | gre | MIT | size=ivec2(10, 10), smoothness=0.5 |
| `gl:ripple` | Ripples spread from the center while crossfading | gre | MIT | amplitude=100.0, speed=50.0 |
| `gl:rotateTransition` | The images spin around the center while crossfading | haiyoucuv | MIT | — |
| `gl:rotate_scale_fade` | The outgoing image spins and zooms while fading to the incoming one, over a background color | Fernando Kuteken | MIT | center=vec2(0.5, 0.5), rotations=1, scale=8, backColor=vec4(0.15, 0.15, 0.15, 1.0) |
| `gl:scale-in` | The incoming image scales in from the center while fading in | haiyoucuv | MIT | — |
| `gl:splitSlideInHorizontal` | The incoming image slides in as two halves moving horizontally in opposite directions | OllyOllyOlly | MIT | reverse=false |
| `gl:splitSlideInOutHorizontal` | The halves of both images slide horizontally in opposite directions, out and in at once | OllyOllyOlly | MIT | reverse=false |
| `gl:splitSlideInOutVertical` | The halves of both images slide vertically in opposite directions, out and in at once | OllyOllyOlly | MIT | reverse=false |
| `gl:splitSlideInVertical` | The incoming image slides in as two halves moving vertically in opposite directions | OllyOllyOlly | MIT | reverse=false |
| `gl:splitSlideOutHorizontal` | The outgoing image slides out as two halves moving horizontally in opposite directions | OllyOllyOlly | MIT | reverse=false |
| `gl:splitSlideOutVertical` | The outgoing image slides out as two halves moving vertically in opposite directions | OllyOllyOlly | MIT | reverse=false |
| `gl:squareswire` | Squares grow along a diagonal sweep to reveal the incoming image | gre | MIT | squares=ivec2(10,10), direction=vec2(1.0, -0.5), smoothness=1.6 |
| `gl:squeeze` | The outgoing image is squeezed into a line with color separation, revealing the incoming one | gre | MIT | colorSeparation=0.04 |
| `gl:static_wipe` | A wipe from top to bottom with a band of TV static at its edge | Ben Lucas | MIT | u_transitionUpToDown=true, u_max_static_span=0.5 |
| `gl:swap` | The two images swap places in 3D, with a floor reflection | gre | MIT | reflection=0.4, perspective=0.2, depth=3.0 |
| `gl:tangentMotionBlur` | The outgoing image is flung away along a curve with motion blur | chenkai | MIT | — |
| `gl:undulatingBurnOut` | A circle with a wavy edge burns out from the center to reveal the incoming image | pthrasher | MIT | smoothness=0.03, center=vec2(0.5), color=vec3(0.0) |
| `gl:wind` | A ragged left-to-right wipe, as if the image was blown away by the wind | gre | MIT | size=0.2, reversed=false |
| `gl:windowblinds` | A crossfade through horizontal window blinds | Fabien Benetou | MIT | — |
| `gl:windowslice` | The incoming image appears through vertical slices that widen | gre | MIT | count=10.0, smoothness=0.5 |
| `gl:wipeDown` | A hard-edged wipe from top to bottom | Jake Nelson | MIT | — |
| `gl:wipeLeft` | A hard-edged wipe from right to left | Jake Nelson | MIT | — |
| `gl:wipeRight` | A hard-edged wipe from left to right | Jake Nelson | MIT | — |
| `gl:wipeUp` | A hard-edged wipe from bottom to top | Jake Nelson | MIT | — |
| `gl:x_axis_translation` | The outgoing image slides to the right, uncovering a crossfade to the incoming one | lizhongjian | MIT | — |
| `gl:zoomInOut` | Zooms into the outgoing image until it blurs into a flat color, then out to the incoming one | OllyOllyOlly | MIT | — |
