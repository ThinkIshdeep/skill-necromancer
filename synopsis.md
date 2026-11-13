# Synopsis — Skill Necromancer

**Ishdeep Singh · 12 November 2026**

## V2 interface release

A focused learning studio.

- Concept path and mastery estimates with one adaptive question
- Worked feedback, hints and one-word recall triggers
- Separate exact-arithmetic row-operation studio
- Editable matrix entries and attempt journal

BKT mastery is a model estimate, not proof of exam readiness or learning gains. The underlying domain scope and research-extension boundaries below remain explicit.

## Implemented release

Runnable source: `lab/tutor.py`. Interface and backend are included. Tests and benchmark outputs accompany this distribution.

## Limits of the implemented release

Small authored question generator, BKT estimates, exact row checks. No measured human learning gains or semester-sized item bank.

## Measured evaluation

```json
{
  "checks": {
    "correct_answer_raises_posterior": true,
    "exact_row_check": true,
    "rational_values_preserved": true
  },
  "note": "Mathematical/BKT regression checks. Synthetic histories do not prove learning gains."
}
```

## Original specification and proposed extensions

The material below preserves the design ambitions. Future-tense features and anticipated challenges are not completed-development claims.

Skill Necromancer

**Tagline:** The student knows the chapter. The minus sign has other plans.

### Concept, problem, and users

Skill Necromancer is a tutor that tries to identify the misconception behind repeated errors. It begins with Gaussian elimination because row operations can be represented and checked step by step. A final wrong answer alone cannot reveal whether the student misunderstood elimination, made an arithmetic slip, or guessed.

Target users are learners and teachers in one narrowly defined course. The research question is whether misconception-aware question selection improves delayed retention compared with fixed practice and difficulty-only adaptation.

### Proposed product and workflow

The learner completes a short diagnostic, enters row-operation steps, receives a focused explanation, and attempts a small follow-up question. A concept map shows prerequisites, while a review queue revisits concepts after time gaps.

Screens: diagnostic, worked-step editor, misconception explanation, concept map, practice history, and review schedule. Explanations should use simple language and optionally include one-word recall cues. The tutor must allow valid alternative solution paths. “Your answer is different from my stored answer” is not a mathematical check.

### Data and system design

Records: `Learner`, `Concept`, `PrerequisiteEdge`, `Item`, `AllowedTransformation`, `AttemptStep`, `MisconceptionHypothesis`, and `ReviewEvent`. Each item needs a concept map, difficulty annotation, correct mathematical constraints, and known error patterns.

Synthetic learners test the pipeline only. Learning-effect claims require consented real responses and an appropriate study. Split predictive evaluation by learner; use a separate delayed assessment for retention. Prevent near-identical generated questions from appearing as both practice and supposed transfer tests.

### Algorithms and experiments

Baseline: fixed question order and ordinary spaced review. Next: an interpretable knowledge-tracing or item-response model, plus rule-based diagnosis of sign, scaling, and row-update errors. A contextual bandit may later select questions using mastery uncertainty and learning objectives. Any experimental policy needs reasonable coverage rather than repeatedly serving the same easiest item.

For Gaussian elimination, validate the stated row operation against the next matrix. Use exact rational arithmetic where possible. Separate an invalid operation from an arithmetic mistake within a valid operation. Update a misconception hypothesis after several pieces of evidence rather than treating one slip as a permanent identity.

Metrics: next-response log loss or Brier score, diagnosis agreement on labelled steps, questions to demonstrated mastery, and delayed retention. A prospective comparison should predefine groups, assessment intervals, and the analysis. Predicting answers accurately is not the same as causing students to learn more.

### Anticipated problems, in my voice

| What could go wrong | My likely reaction | Engineering response |
|---|---|---|
| One careless mistake becomes a diagnosis | “I dropped a sign once and the app wrote my biography.” | Maintain uncertainty and test competing explanations |
| A guessed answer looks like mastery | “Correct by luck, promoted by statistics.” | Use follow-up evidence and varied equivalent items |
| The checker rejects another valid row sequence | “Apparently maths now has a preferred writing style.” | Validate transformations, not a single solution script |

### Demo, milestones, and limits

Enter repeated sign errors during row operations, inspect the inferred misconception, and complete a focused follow-up. Milestones: verified item bank; step validator; diagnostic rules; adaptive selection; learner study. Deliver a small reliable tutor and an interpretable learning history. A semester-wide tutor is a later expansion; no improvement in exam marks should be claimed before a real study.




## Problems actually encountered during the makeover

| The problem | In my voice | What changed |
|---|---|---|
| Sample B overwrote the file used by sample A | “Bro, this is an A/B test, why did B steal A’s identity?” | Recordings now get unique file names; a regression test checks both files remain distinct and unchanged. |
| A duplicate highlight followed row positions instead of duplicate evidence | “Apparently every third row had been arrested on vibes.” | Duplicate highlights now use exact record content and jump to a real duplicate. |
| The table displayed a rounded number that search did not match | “I copied the number from your own screen, my guy.” | Search checks both raw values and the formatted values visible in the table. |
| Graph labels became tiny on a phone | “Causal inference, now available to ants.” | Graph workspaces keep readable node widths and scroll within their own viewport. |
| Robot movement and the play button disagreed about whether it was running | “Gordon left the parking spot while the button was still contemplating life.” | The live flag is synchronized after accepted commands and remains off after rejected commands. |
| Fast screenshots caught an interface between renders | “The UI took a smoke break precisely when the camera arrived.” | Captures were inspected, incomplete frames replaced, and videos labelled as edited screenshots. |

These are observed build issues. Proposed research challenges in the original specifications remain proposed; this log does not invent months of model training or real deployments.
