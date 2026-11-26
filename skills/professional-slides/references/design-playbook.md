# Presentation design decisions

## Audience and objective

| Context | Narrative emphasis | Suitable visual direction | Watch for |
|---|---|---|---|
| Enterprise leadership | Decision, business impact, evidence, investment, risks, next action | Restrained brand palette, strong numbers, comparisons and roadmaps | Unsupported ROI, jargon, crowded dashboards |
| Government/public institution | Mandate and context, evidence, options, feasibility, responsibilities, decision requested | Formal hierarchy, clear diagrams, legible tables, restrained motion | Invented seals, legal authority, missing source dates; do not assume red/gold is mandatory |
| Sales/customer proposal | Customer situation, value, credible proof, fit, delivery, next step | Brand-led imagery, focused comparisons, realistic scenarios | Invented customer logos, testimonials, pricing or promises |
| Investor/startup | Market evidence, differentiated proposition, traction, economics, team, ask | Confident typography, clean charts, controlled visual energy | Confusing projections with actual results |
| Training/education | Learning outcome, explanation, example, practice, recap | Chunked concepts, progressive diagrams, meaningful illustrations | Too much text, decorative animation, no practice |
| Technical/scientific | Question, method/system, evidence, tradeoffs, limitations | Precise diagrams and charts, annotations, appendices | Distorted plots, unlabeled units, unreadable architecture |

Combine these when audiences overlap. Respect an explicit template or established brand before choosing a new direction.

## Composition and visual system

Choose one core visual metaphor appropriate to the subject (e.g. connected service journey, geographic coverage, layered platform, measurable progress). Use it selectively to connect sections; avoid repeating the same motif on every slide.

Set generous safe margins (roughly 5–7% of slide width) and a consistent alignment grid. Establish a type scale and use one or two compatible font families supporting every requested script. Suitable fallback candidates include Aptos, Arial, and Noto Sans when installed; verify availability and licensing before embedding. Reuse the user's font when supplied and usable.

Use a small palette: a background, primary text, one brand accent, and semantic colors as needed. A neutral canvas plus brand accent often works; do not default all clients to dark backgrounds or purple/blue gradients. Use light/dark sections intentionally, with adequate contrast and consistent meaning.

Choose visual form by information relationship:
- Difference: aligned comparison or a chart with a shared scale.
- Sequence: step process, journey, timeline, or staged reveal.
- Hierarchy: tree, layers, or nested structure.
- System relationships: labeled nodes and connectors; simplify to the audience's level.
- Distribution/trend: appropriate quantitative chart with actual data.
- Qualitative importance: typographic hierarchy, not fabricated numeric charts.
- Context: authentic image with concise annotation, or a clearly illustrative scene.

Do not use a pie chart for a non-additive whole, 3D charts for decoration, or an illustration in place of factual evidence. Large tables belong in appendices unless the audience must compare their values during the talk.

## Language and density

For speaker-led decks, use brief supporting points; move detail into notes. For send-ahead reports, provide sufficient standalone context with an executive summary and more explicit captions. For bilingual decks, use separate paired sections or a restrained secondary language line; split slides when readability suffers. Do not mechanically duplicate every sentence.

## Motion

| Mode | Recommended behavior |
|---|---|
| Formal/public-sector briefing | Mostly static; subtle fade for section changes, occasional staged process reveal |
| Executive/sales live talk | Restrained transition; reveal comparisons or evidence in the speaker's sequence |
| Training | Stepwise diagram build, example then answer, controlled learner pacing |
| Read-ahead/PDF | Fully meaningful static slides; no information dependent on animation |

Use short durations (approximately 0.2–0.5 s) as a starting point. Prefer click-triggered reveals when a presenter controls pacing. Avoid gratuitous spinning, bouncing, flashing, sound effects, and auto-advance. Provide reduced-motion/static equivalents for essential explanations.

If exporting to PDF, ensure the final visible state contains all essential content and that overlapping animated objects do not hide information. For supported animation authoring, verify the actual player behavior; a motion plan is not an implementation.
