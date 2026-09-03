# podcast-clips — extracting Ramona's questions from long-form episodes

## The problem

Ramona has appeared in many podcast episodes and Lunch & Learn sessions, often as
the person asking questions. She wants those moments collated. The interesting
part is not the cutting — it is **identifying which turns are hers** in a
multi-speaker recording where the transcript carries no speaker labels.

That is a modelling and evaluation problem with a buildable ground truth, which
is why it is worth doing as a study rather than a script.

## Hard constraint: do not download the media

Ramona halted a previous project (`podcast-rag`) after review found its ingestion
breached platform terms. Do not repeat that.

**Work from captions, not audio.** Pull transcripts through YouTube's caption
track, identify her segments, and emit **timestamped YouTube links**
(`?v=ID&t=1234s`). No download, no re-hosting, no terms problem — and the output
plays in context on the original creator's video, which is fairer to the hosts.

If a caption track is unavailable for an episode, drop that episode rather than
falling back to audio.

## The actual research question

Given an unlabelled transcript with timestamps, which turns belong to a specific
speaker?

Signals available without audio:
- turn boundaries (caption cue gaps, punctuation, speaker-change heuristics)
- utterance shape — questions vs. exposition
- her known lexical patterns (she asks layered, analogy-driven questions)
- host/guest structure — who introduces, who answers at length
- cross-episode consistency: the same person across nine recordings

Success is measurable. Hand-label two episodes as ground truth, then report
precision and recall on the rest. Do not claim it works without that.

## Method to evaluate, not assume

1. Fetch caption tracks + timestamps for the nine episodes below
2. Segment into turns
3. Hand-label 2 episodes (ground truth)
4. Try approaches in increasing cost order and measure each:
   - rules (question marks, turn length, position after a long turn)
   - embedding similarity against her labelled turns
   - LLM classification per turn
5. Report precision/recall per approach. Cheapest sufficient method wins.
6. Emit timestamped links for the winner

Ramona's standing rule: cheapest model that clears the bar, and the bar is
measured, not assumed.

## Corpus

| Date | Show | Episode | URL |
|---|---|---|---|
| 2026-03-26 | Super Data Show | AI Agent Memory is BROKEN | https://www.youtube.com/watch?v=gUekOnPsahI |
| 2025-10-02 | The Data Engineering Channel | The Truth About The Medallion Architecture | https://www.youtube.com/live/1HUCUU5G_Ns |
| 2025-08-15 | The Data Engineering Channel | AI That Actually Helps Data Professionals | https://www.youtube.com/live/9d_k-uS2LcA |
| 2025-08-04 | LEIT Data Podcast | Staying Human in the AI Era | https://www.youtube.com/watch?v=MFor0EJ7DyI |
| 2025-07-18 | Christopher Gambill | Learn These 10 AI Skills! | https://www.youtube.com/watch?v=fK_75G-s77w |
| 2025-06-27 | Christopher Gambill | Data Architecture Principles That Skyrocket Your Career! | https://www.youtube.com/watch?v=RKsm8-RyeeY |
| 2025-06-04 | Agile Data Podcast #64 | The pattern of writing a data book (**she interviews Shane Gibson**) | https://youtu.be/9VBus8KtyfI |
| 2025-04-28 | LEIT Data Podcast | Dashboard for the Human Spirit | https://youtu.be/AfeOP7GYFW0 |
| 2024-08-05 | LEIT Data Podcast | Data With Heart: The Human Connection in Data Value | https://youtu.be/DfGq3cH2kAc |

Plus: Joe Reis Lunch & Learn sessions — Ramona has the list, these are the
original motivation. Ask her for them.

The Agile Data episode is the useful outlier: she is the *interviewer* there, so
her turns dominate. Good for building the labelled set.

## Deliverable

A page or file of timestamped links, grouped by theme, each playing her question
in context. Plus the measurement write-up — which method, what precision, what it
missed.

## Before starting

Read `~/.claude/skills/working-with-ramona/SKILL.md`.
