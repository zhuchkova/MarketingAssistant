# RAG Seed Data

This folder stores editable knowledge cards for ChromaDB.

Each JSON file maps to one Chroma collection. Large collections can also be split into a folder of JSON files, like `positioning_knowledge/`. Add new records with this shape:

```json
{
  "id": "unique_stable_id",
  "document": "Short reusable knowledge card. Keep it specific, practical, and written as guidance for the agent.",
  "metadata": {
    "type": "voice_of_customer",
    "platform": "instagram",
    "angle": "objection",
    "agent": "idea_agent"
  }
}
```

Good documents to add:

* Voice-of-customer snippets from comments, DMs, reviews, calls, FAQs, Reddit threads, and YouTube comments.
* Audience pains, desires, objections, failed alternatives, and trigger moments.
* Proven hook patterns with examples.
* LinkedIn and Instagram post frameworks.
* CTA examples by goal: comment, DM keyword, save, follow, download.
* ManyChat flow examples with first message, qualification question, and follow-up.

The `positioning_knowledge/` collection is split into smaller files:

* `base.json`: core positioning principles.
* `niches_001_025.json`, `niches_026_050.json`, `niches_051_075.json`, `niches_076_100.json`: voice-of-customer cards for the 100 included niches.

The `idea_knowledge.json` collection includes 60 audience-led hook patterns:

* 10 pain-led hooks for frustrations, stuck moments, bad advice fatigue, and failed DIY cycles.
* 10 desire-led hooks for identity, relief, visible progress, small wins, and future pacing.
* 10 objection-led hooks for fit, price, DIY hesitation, trust, bad past experiences, and fear of judgment.
* 10 trigger-led hooks for deadlines, failed attempts, decision moments, seasonal shifts, and visibility moments.
* 10 proof-led hooks for process proof, before-after specificity, risk reduction, measurable wins, and method transparency.
* 10 audience-language hooks for exact customer phrases, plain-language objections, buying signals, and search-style questions.

These hook cards are designed to work with the audience-analysis fields `pains`, `desires`, `objections`, `trigger_moments`, `proof_points`, and `audience_language`.

Avoid adding full copyrighted articles or long copied posts. Instead, turn each source into a short original summary card.

To seed all collections:

```bash
python scripts/seed_chroma_all.py
```

## Included Popular Niches

1. Fitness trainer
2. Nutrition coach
3. Bakery
4. Flower shop
5. Yoga instructor
6. Therapist or counselor
7. Life coach
8. Business coach
9. Real estate agent
10. Interior designer
11. Wedding photographer
12. Hair stylist or salon
13. Skincare specialist or esthetician
14. Makeup artist
15. Personal stylist
16. Handmade jewelry brand
17. Candle or soap maker
18. Coffee shop
19. Restaurant or cafe
20. Pet groomer
21. Dog trainer
22. Childcare or daycare
23. Tutor or test prep coach
24. Language teacher
25. Career coach or resume writer
26. Financial coach or bookkeeper
27. Social media manager or marketing consultant
28. Web designer
29. Virtual assistant
30. Online course creator
31. Nail artist
32. AI consultant
33. Brand designer
34. Copywriter
35. Podcast coach
36. Videographer
37. Event planner
38. Massage therapist
39. Pilates instructor
40. Chiropractor or physical therapist
41. Dentist
42. Med spa or aesthetics clinic
43. Cleaning service
44. Home organizer
45. Landscaper or gardener
46. Travel advisor
47. Accountant or tax preparer
48. Lawyer or legal consultant
49. HR consultant or recruiter
50. Ecommerce boutique
51. Longevity coach
52. Startup coach
53. Business angel or startup investor
54. UI/UX designer
55. 3D print shop
56. Swimming teacher
57. Driving school
58. Day spa
59. Cooking school
60. Programming school
61. Dance teacher
62. Cat breeder
63. Dog breeder
64. Horse riding school
65. Gardener
66. Bar
67. Ceramics shop or pottery courses
68. Lifestyle blog
69. Yacht club
70. Golf club
71. Charity organization
72. Boat or SUP renting
73. Ice cream cafe
74. Winery
75. Hotel
76. Anime artist
77. Painter or fine artist
78. Tattoo artist
79. Music teacher
80. Bookstore
81. Coworking space
82. Translator or localization specialist
83. Architect
84. Home builder or renovation contractor
85. Car detailing service
86. Car repair shop
87. Bike shop
88. Plant shop
89. Personal chef
90. Private school
91. Summer camp
92. Language school
93. Photography studio
94. Wedding officiant or ceremony celebrant
95. Escape room
96. Museum or art gallery
97. Gym or fitness studio
98. Martial arts school
99. Surf school
100. Influencer or creator coach

## Positioning Voice-Of-Customer Card Types

Each included niche has 50 voice-of-customer cards across these 10 groups:

1. Pain cards: frustrations, overwhelm, embarrassment, and the cost of staying stuck.
2. Desire cards: outcomes, confidence, relief, pride, and decision simplicity.
3. Objection cards: hesitation around fit, price, trust, pressure, and whether support will work.
4. Trigger cards: moments when the audience starts actively looking for help.
5. Comparison cards: how the audience compares paid help with DIY, cheaper alternatives, delaying, or asking friends.
6. Proof cards: what kinds of evidence, examples, before-after details, and process explanations reduce risk.
7. Emotion cards: the deeper emotional reason the audience wants the result.
8. Content angle cards: reusable post angles like mistakes, readiness signs, behind the scenes, and choosing well.
9. Language cards: plain-language guidance so posts sound like the audience's real thoughts instead of expert jargon.
10. Positioning cards: ways to connect audience, problem, first step, transformation, and offer.
