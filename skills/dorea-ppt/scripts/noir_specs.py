"""design_spec.md e spec_lock.md genéricos para o ppt-master (estilo noir editorial)."""
import datetime, os

FONT_ROWS = """| Title | Geometric sans, same as the reference template | Open Sauce | Open Sauce | Arial |
| Body | Geometric sans, same as the reference template | Open Sauce | Open Sauce | Arial |
| Annotation | Technical monospace captions, same as the reference template | Space Mono | Space Mono | Courier New |
| Display | Light weight for the parenthesis glyphs | Open Sauce Light | Open Sauce Light | Arial |"""


def design_spec(meta, roster, images, accent):
    name = meta.get("title", "Apresentação"); n = len(roster)
    lang = meta.get("lang", "pt-BR"); org = meta.get("org", "")
    aud = meta.get("audience", "Público da apresentação"); intent = meta.get("intent", "Comunicar o conteúdo com clareza e impacto visual.")
    core = meta.get("core", name)
    img_rows = ""
    for fn, purpose, kind in images:
        img_rows += f"\n| {fn} | auto | auto | {purpose} | {kind} | Centered behind the title or inside a panel | no-crop | user | Existing | Supplied or generated for this deck | none | hero |"
    s = f"""<!-- ppt-master-schema: design-spec/v1 -->
# {name} - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | {name} |
| Canvas Format | PPT 16:9 (1280 × 720) |
| Page Count | {n} |
| Primary Language | {lang} |
| Target Audience | {aud} |
| Communication Intent | {intent} |
| Desired Audience Outcome | The audience grasps the key message of every slide at a glance. |
| Core Message / Ask / Action | {core} |
| Delivery Context | Meeting on screen and offline reading as PPTX |
| Artifact Afterlife | Shared as a PPTX file |
| Reading Mode | balanced |
| Content Strategy | Balanced default: facts come only from the source content supplied by the user. |
| Design Style | Editorial noir: pure black, hairline charts, 3D objects, one accent color |
| AI Image Acquisition Path | not applicable |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | disabled — workflow default |
| Custom Animations | enabled — object fade-in, parentheses opening, title and caption reveal, fade page transitions (reference template rhythm) |
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
- **Mode Behavior**: Conclusion-first: cover, then one message per slide, dividers between sections, closing slide.
- **Visual style**: custom
- **Visual Style Behavior**: Pure-black editorial like the reference template: no cards, hairline rules, Open Sauce numerals and parenthesis-wrapped titles with real Open Sauce Light parenthesis glyphs, Space Mono captions, thin-line charts, one accent color, 3D objects on cover/dividers/closing.
- **Theme**: Editorial noir presentation.
- **Tone**: Authoritative, precise, calm under data density.

### Color Scheme

| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #000000 | Slide field, pure black like the reference template |
| Secondary background | #0D0D0D | Subtle fields (rare) |
| Primary | #F2F5F9 | Headlines and key numerals |
| Accent | {accent} | Leaders, hero numerals, kickers |
| Secondary accent | #FFFFFF | Thin chart lines and dots |
| Body text | #F2F5F9 | Primary reading text on dark |
| Secondary text | #9A9A9A | Mono captions, axis text |
| Divider | #2A2A2A | Hairlines |

## IV. Typography System

### Font Plan

| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
{FONT_ROWS}

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
| Display medium | 96 |
| Display small | 72 |
| Display extra small | 56 |
| Hero | 140 |
| Paren | 220 |

## V. Layout Principles

### Deck-wide Direction

- **Hierarchy direction**: Kicker, then action title, then KPI row, then panels; hero numeral first, label second.
- **Composition tendency**: Hairline-separated panels on a 56 px grid; no cards.
- **Cross-page continuity**: Same header position, logo top-left, footer rule with page number.
- **Spacing posture**: dense data pages, open cover and dividers.
- **Spacing anchors**: 56 page margin, 24 block gap, 40 column gutter, 0 corner radius, 1.4 body leading

## VI. Icon Usage Specification

- **Primary bundled library**: none

| Icon Path | Suitable Scenarios |
| --- | --- |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |{img_rows}

## IX. Content Outline
"""
    for i, (num, fn, title) in enumerate(roster, 1):
        s += f"""
#### Slide {i:02d} - {title}

- **Audience move**: from not knowing this slide's content to seeing the conclusion at a glance
- **Relationships**: page units belong to one page job; no cross-page dependency
- **Title**: {title}
- **Core message**: {title}
- **Content**: Content of slide {i} from the user's source material
"""
    s += """
## X. Speaker Notes Requirements

- **Generation**: disabled
"""
    return s


def spec_lock(meta, n, images, accent):
    rhythm = "\n".join(f"- P{i:02d}: {'anchor' if i in (1, n) else 'dense'}" for i in range(1, n + 1))
    imgs = "\n".join(f"- {os.path.splitext(fn)[0].replace('.', '_')}: images/{fn} | source=user | crop=no-crop" for fn, _, _ in images)
    return f"""<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: {meta.get('lang', 'pt-BR')}
- audience: {meta.get('audience', 'Público da apresentação')}
- objective: {meta.get('intent', 'Comunicar o conteúdo com clareza e impacto visual.')}
- core_message: {meta.get('core', meta.get('title', 'Apresentação'))}
- consumption_mode: balanced

## mode
- mode: custom
- mode_behavior: Conclusion-first: cover, then one message per slide, dividers between sections, closing slide.

## visual_style
- visual_style: custom
- visual_style_behavior: Pure-black editorial, no cards, hairline rules, Open Sauce numerals and parenthesis titles, Space Mono captions, thin-line charts, one accent color, 3D objects on cover/dividers/closing.

## colors
- background: #000000
- secondary_bg: #0D0D0D
- primary: #F2F5F9
- accent: {accent}
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
- display_medium: 96
- display_small: 72
- display_xsmall: 56
- hero: 140
- paren: 220

## icons
- library: none
- inventory: none

## images
{imgs}

## page_rhythm
{rhythm}

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
"""
