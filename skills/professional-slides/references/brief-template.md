# Brief template

Only the first four lines are required; leave the rest out and the agent decides.

```text
/professional-slides
Audience: [enterprise / government agency / investors / teachers / ...; listener role if known]
Slide language: [English / Vietnamese / bilingual English–Vietnamese / ...]
Presentation type and goal: [solution proposal / sales / report / training / ...; what the audience should understand or decide]
Content: [description plus attached files, or file paths the agent can read]

Brand: [logo, brand guideline, slide template if any]
Slide count: [e.g. 12 slides in total, or let the agent choose]
Delivery: [live presentation / read-ahead / webinar]
Preferred style: [auto / formal / modern / minimal / storytelling / ...]
AI images: [auto when useful / on / off / supplied assets only]
AI image style: [auto from content and brand / photographic / illustration / vector / isometric]
Object animation: [auto / minimal / progressive reveal / none]
Slide transitions: [auto / subtle fade / a specific supported effect / none]
Output: [editable PPTX; PDF if export is available]
Must-haves or things to avoid: [...]

Analyze the material, then choose the theme, brand-aligned colors, layout,
charts, illustrations, and motion. Build the complete deck, check every slide,
and report what was done and what was limited by the tools.
Do not invent figures, commitments, or unsourced claims.
```

## Example: government agency

```text
/professional-slides Create a presentation for the leadership of a city
department proposing an operations platform, from the attached Proposal.docx
and Appendix.pdf. Goal: approval for a pilot; live delivery, 12 slides in total.
Use the attached logo, a formal, clear, modern direction, and restrained
motion. Produce an editable PPTX with speaker notes, and a PDF if possible.
```

## Example: enterprise

```text
/professional-slides From the attached Q3Report.pptx and Figures.xlsx, build a
bilingual English–Vietnamese board report, 15 slides in total.
Goal: present results, risks, and the decisions that need approval.
Keep figures and logo exact; choose layout, colors, charts, and illustrations.
Clearly separate actuals from plan. Export an editable PPTX.
```

Natural language works too: "Use the professional-slides skill to build a deck
from the attached files..." with no slash command. In a web chat, attach the
real files; local paths only work when the agent can read that path.
