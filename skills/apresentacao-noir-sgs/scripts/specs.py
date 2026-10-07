import sys,os,datetime
sys.path.insert(0,os.path.dirname(__file__))

COMMON_COLORS="""| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #000000 | Slide field, pure black like the reference template |
| Secondary background | #0D0D0D | Subtle fields (rare) |
| Primary | #F2F5F9 | Headlines and key numerals |
| Accent | #F7941D | SGS orange: leaders, hero numerals, kickers |
| Secondary accent | #FFFFFF | Thin chart lines and dots |
| Body text | #F2F5F9 | Primary reading text on dark |
| Secondary text | #9A9A9A | Mono captions, axis text |
| Divider | #2A2A2A | Hairlines |"""

HR={'hero_tower':'| hero_tower.png | 960 × 1000 | 0.8 | Black chrome 3D transmission tower (Canva AI) | Illustration | Centered behind the title, dimmed to 62%, title overlaps | no-crop | user | Existing | Generated in Canva, exported 1920x1080, cropped with alpha | none | hero |',
'hero_tower_fx':'| hero_tower_fx.png | 960 × 1000 | 0.8 | Iridescent entrance layer of the same object, fades out after the entrance | Illustration | Same box as the object | no-crop | user | Existing | Derived from hero_tower.png (hue map plus chromatic split) | none | hero |',
'hero_trafo':'| hero_trafo.png | 960 × 1000 | 0.8 | Black chrome 3D power transformer (Canva AI) | Illustration | Centered behind the title, dimmed to 62%, title overlaps | no-crop | user | Existing | Generated in Canva, exported 1920x1080, cropped with alpha | none | hero |',
'hero_trafo_fx':'| hero_trafo_fx.png | 960 × 1000 | 0.8 | Iridescent entrance layer of the same object, fades out after the entrance | Illustration | Same box as the object | no-crop | user | Existing | Derived from hero_trafo.png (hue map plus chromatic split) | none | hero |',
'hero_breaker':'| hero_breaker.png | 960 × 1000 | 0.8 | Black chrome 3D substation circuit breaker (Canva AI) | Illustration | Centered behind the title, dimmed to 62%, title overlaps | no-crop | user | Existing | Generated in Canva, exported 1920x1080, cropped with alpha | none | hero |',
'hero_breaker_fx':'| hero_breaker_fx.png | 960 × 1000 | 0.8 | Iridescent entrance layer of the same object, fades out after the entrance | Illustration | Same box as the object | no-crop | user | Existing | Derived from hero_breaker.png (hue map plus chromatic split) | none | hero |',
'hero_insul':'| hero_insul.png | 960 × 1000 | 0.8 | Black glass 3D insulator string (Canva AI) | Illustration | Centered behind the title, dimmed to 62%, title overlaps | no-crop | user | Existing | Generated in Canva, exported 1920x1080, cropped with alpha | none | hero |',
'hero_insul_fx':'| hero_insul_fx.png | 960 × 1000 | 0.8 | Iridescent entrance layer of the same object, fades out after the entrance | Illustration | Same box as the object | no-crop | user | Existing | Derived from hero_insul.png (hue map plus chromatic split) | none | hero |',
'hero_hat':'| hero_hat.png | 960 × 1000 | 0.8 | Glossy black 3D safety hard hat (Canva AI) | Illustration | Centered behind the title, dimmed to 62%, title overlaps | no-crop | user | Existing | Generated in Canva, exported 1920x1080, cropped with alpha | none | hero |',
'hero_hat_fx':'| hero_hat_fx.png | 960 × 1000 | 0.8 | Iridescent entrance layer of the same object, fades out after the entrance | Illustration | Same box as the object | no-crop | user | Existing | Derived from hero_hat.png (hue map plus chromatic split) | none | hero |'}
def design_spec(name,pages,core,intent,outcome,style_theme,afterlife,deliv,audience,mode_name,mode_beh,used=()):
    n=len(pages)
    HEROROWS=''.join(chr(10)+HR[h] for h in sorted(used))
    s=f"""<!-- ppt-master-schema: design-spec/v1 -->
# {name} - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | {name} |
| Canvas Format | PPT 16:9 (1280 × 720) |
| Page Count | {n} |
| Primary Language | pt-BR |
| Target Audience | {audience} |
| Communication Intent | {intent} |
| Desired Audience Outcome | {outcome} |
| Core Message / Ask / Action | {core} |
| Delivery Context | {deliv} |
| Artifact Afterlife | {afterlife} |
| Reading Mode | balanced |
| Content Strategy | Balanced default: every figure comes from the weekly SGI export; no invented values. |
| Design Style | {style_theme} |
| AI Image Acquisition Path | not applicable |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | disabled — delegated Stage-2 decision, the deck is data-led and self-explanatory |
| Custom Animations | enabled — explicit user request (object fade-in, parentheses opening, title and caption reveal, fade-through page transitions, like the reference template) |
| Narration Audio | disabled — workflow default |
| Created Date | {datetime.date.today().isoformat()} |

## II. Canvas Specification

| Property | Value |
| --- | --- |
| Format | PPT 16:9 |
| Dimensions | 1280 × 720 |
| viewBox | `0 0 1280 720` |
| Margins | 56 px left/right, 40 px top, 48 px bottom footer band |
| Content Area | x 56–1224, y 170–664 |

## III. Visual Theme

### Theme Style

- **Mode**: custom
- **Mode Behavior**: {mode_beh}
- **Visual style**: custom
- **Visual Style Behavior**: Pure-black editorial like the reference template: no cards, hairline rules, Open Sauce numerals and parenthesis-wrapped titles with real Open Sauce Light parenthesis glyphs, Space Mono captions, thin-line lollipop and line charts, one SGS-orange accent, chrome 3D hero objects on cover, dividers and closing. Semaphore colors appear only as status dots.
- **Theme**: Engineering control-room dashboard for transmission-line and substation inspection.
- **Tone**: Authoritative, precise, calm under data density.

### Color Scheme

{COMMON_COLORS}

## IV. Typography System

### Font Plan

| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | Geometric sans, same as the reference template | Open Sauce | Open Sauce | Arial |
| Body | Geometric sans, same as the reference template | Open Sauce | Open Sauce | Arial |
| Annotation | Technical monospace captions, same as the reference template | Space Mono | Space Mono | Courier New |
| Display | Light weight for the parenthesis glyphs | Open Sauce Light | Open Sauce Light | Arial |

- **Title stack**: Open Sauce, Arial
- **Body stack**: Open Sauce, Arial
- **Annotation stack**: Space Mono, Courier New
- **Display stack**: Open Sauce Light, Arial

### Font Size Hierarchy

| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 18 |
| Title | 40 |
| Annotation | 13 |
| KPI numeral | 64 |
| Meta | 26 |
| Display | 120 |
| Hero | 140 |
| Paren | 220 |

## V. Layout Principles

### Deck-wide Direction

- **Hierarchy direction**: Kicker, then action title, then KPI row, then charts; hero numeral first, label second.
- **Composition tendency**: Rounded cards on a 56 px grid; chart panels share one outline treatment.
- **Cross-page continuity**: Same header position, SGS logo plate top-right, footer rule with page number.
- **Spacing posture**: dense data pages, open cover and dividers.
- **Spacing anchors**: 56 page margin, 14 block gap, 16 column gutter, 14 corner radius, 1.4 body leading

## VI. Icon Usage Specification

- **Primary bundled library**: none

| Icon Path | Suitable Scenarios |
| --- | --- |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sgs_logo.png | 637 × 313 | 2.03 | SGS brand mark, reversed to white on the navy field, no plate, every page | Photograph | Top-left on every page | no-crop | user | Existing | Supplied by user | none | brand |{HEROROWS}

## IX. Content Outline
"""
    part=None
    for i,(fn,title,msg,content,rel) in enumerate(pages,1):
        s+=f"""
#### Slide {i:02d} - {title}

- **Audience move**: from not knowing this page's facts to seeing the conclusion at a glance
- **Relationships**: {rel}
- **Title**: {title}
- **Core message**: {msg}
- **Content**: {content}
"""
    s+="""
## X. Speaker Notes Requirements

- **Generation**: disabled
"""
    return s

def spec_lock(n,core,audience,objective,mode_beh,used=()):
    HEROLOCK=chr(10).join(f"- {h}: images/{h}.png | source=user | crop=no-crop" for h in sorted(used))
    rhythm="\n".join(f"- P{i:02d}: {'anchor' if i in (1,n) else 'dense'}" for i in range(1,n+1))
    return f"""<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: pt-BR
- audience: {audience}
- objective: {objective}
- core_message: {core}
- consumption_mode: balanced

## mode
- mode: custom
- mode_behavior: {mode_beh}

## visual_style
- visual_style: custom
- visual_style_behavior: Pure-black editorial, no cards, hairline rules, Open Sauce numerals and parenthesis titles, Space Mono captions, thin-line charts, one SGS-orange accent, chrome 3D hero objects on cover/dividers/closing, semaphore colors only as status dots.

## colors
- background: #000000
- secondary_bg: #0D0D0D
- primary: #F2F5F9
- accent: #F7941D
- secondary_accent: #FFFFFF
- body_text: #F2F5F9
- secondary_text: #9A9A9A
- divider: #2A2A2A
- positive: #34D399
- warning: #FACC15
- caution: #FB923C
- negative: #F43F5E

## typography
- font_family: Open Sauce, Arial
- title_family: Open Sauce, Arial
- body_family: Open Sauce, Arial
- annotation_family: Space Mono, Courier New
- display_family: Open Sauce Light, Arial
- body: 18
- title: 40
- annotation: 13
- kpi: 64
- meta: 26
- display: 120
- hero: 140
- paren: 220

## icons
- library: none
- inventory: none

## images
- logo: images/sgs_logo.png | source=user | crop=no-crop
{HEROLOCK}

## page_rhythm
{rhythm}

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
"""
