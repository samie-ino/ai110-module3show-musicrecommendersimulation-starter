# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

GrooveFit 1.0 is a rule-based music recommender that scores every song in an 18-song catalog against a user's taste profile and returns the top 5 matches. It uses four signals — genre, mood, energy level, and acoustic preference — to assign each song a score out of 4.5. Every recommendation includes a plain-English breakdown showing exactly which signals fired and how many points each one contributed. The project was built to explore how simple scoring rules can produce realistic-feeling recommendations, and to make the biases in those rules easy to observe and explain.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Each song in the system uses genre, mood, energy, and acousticness. The user profile stores their favorite genre, favorite mood, target energy level, and whether they prefer acoustic music.

- **Genre** — an exact match earns full points. A mismatch earns nothing.
- **Mood** — same rule as genre. An exact match earns full points. A mismatch earns nothing.
- **Energy** — measures the gap between the song's energy and the user's preferred energy. The smaller the gap, the more points it earns (up to 1.0).
- **Acousticness** — a bonus is awarded when the song's acoustic character matches the user's preference (threshold: acousticness ≥ 0.6).

Note: valence is stored on each song but is not yet part of the scoring formula. It is listed as a future improvement in the Limitations section.

We never pick songs by hand. Instead, we let the scores do the deciding automatically. After every song in the catalog has been scored, we line them all up from highest score to lowest. The songs at the top earned their spot purely by how well they matched what the user told us they want. We then take however many top songs the user asked for, and those become the recommendations. Because the score is built from the user's own profile, the result is personal to them. Two different users running the same system against the same catalog will get different recommendations, because their profiles are different and so their scores will be different.

The scoring function (`score_song`) returns both a numeric score and a list of human-readable reasons that explain each point contribution, for example:

```
genre match (+2.0)
mood match (+1.0)
energy similarity (+0.98) (song=0.42, target=0.40)
acoustic match (+0.5) (acousticness=0.90)
```

This means the system is:
1. Automatic — no human decides what gets recommended
2. Consistent — the same user with the same profile always gets the same result
3. Explainable — we can always point to exactly why a song ranked where it did, because every score is traceable back to the four checks we ran

---

### Algorithm Recipe

Each song receives a score built from four weighted checks, applied in this order:

- **Genre match — +2.0 points**
  Exact match only. Partial credit is not given.

- **Mood match — +1.0 points**
  Exact match only. Partial credit is not given.

- **Energy similarity — +0.0 to 1.0 points**
  Calculated as `1.0 − |song.energy − target_energy|`. Rewards closeness continuously — the nearer the song's energy is to the user's target, the higher the score.

- **Acousticness preference — +0.5 points**
  Bonus awarded if the user prefers acoustic music and the song is acoustic (acousticness ≥ 0.6), or if the user prefers non-acoustic and the song is not.

- **Maximum possible score — 4.5 points**
  Earned when all four signals align perfectly.

A song that matches the user's genre and mood, sits at the exact target energy level, and matches their production-style preference will score 4.5. A song that misses on all four checks will score near 0.

---

### Potential Biases

- **Genre dominance.** At +2.0, genre carries twice the weight of mood and more than twice the max energy points. A great song from a slightly different genre (e.g., "indie pop" vs. "pop") scores at most 2.5 even if it matches every other preference perfectly — while a poor energy match in the right genre still scores 2.0+ automatically. The system may bury cross-genre gems.

- **Mood is all-or-nothing.** A "chill" user and a song tagged "relaxed" are arguably very close, but the system treats them as a complete miss (+0.0). Any labeling inconsistency in the catalog punishes the user.

- **Small catalog amplifies genre bias.** With only 18 songs across 15 genres, several genres have just one representative. A user whose favorite genre appears once will have that single song boosted to the top regardless of how well its other features match.

- **Valence is not yet scored.** The system description above lists valence as a preference signal, but the current recipe does not include it. Songs with emotionally mismatched valence (e.g., a dark, low-valence song recommended to a "happy" user) can still rank highly if genre and mood labels align.

---

## Multi-Profile Evaluation — Six User Profiles

The recommender was run against three distinct listener types and three adversarial edge cases. Terminal output for each is captured below.

---

### Profile 1 — High-Energy Pop

A workout listener who wants loud, fast, non-acoustic pop.

```
============================================================
  Profile 1 — High-Energy Pop
============================================================

  #1  Sunrise City  —  Neon Echo
       Genre: pop  |  Mood: happy
       Score: 4.42 / 4.5  [####################]
       Why this song:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.92) (song=0.82, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.18)

  #2  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense
       Score: 3.47 / 4.5  [###############-----]
       Why this song:
         • genre match (+2.0)
         • energy similarity (+0.97) (song=0.93, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.05)

  #3  Rooftop Lights  —  Indigo Parade
       Genre: indie pop  |  Mood: happy
       Score: 2.36 / 4.5  [##########----------]
       Why this song:
         • mood match (+1.0)
         • energy similarity (+0.86) (song=0.76, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.35)

  #4  Storm Runner  —  Voltline
       Genre: rock  |  Mood: intense
       Score: 1.49 / 4.5  [#######-------------]
       Why this song:
         • energy similarity (+0.99) (song=0.91, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.10)

  #5  Neon Pulse  —  Greywave
       Genre: electronic  |  Mood: energetic
       Score: 1.48 / 4.5  [#######-------------]
       Why this song:
         • energy similarity (+0.98) (song=0.88, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.08)

============================================================
```

**Observation:** Sunrise City (#1) is a near-perfect match at 4.42. The genre bonus (+2.0) dominates — Gym Hero (#2) scores only 3.47 despite a nearly identical energy match because it tagged "intense" instead of "happy." The bottom three results (#3-5) all miss the genre bonus, so despite strong energy alignment they cannot climb higher.

---

### Profile 2 — Chill Lofi

A late-night study listener who wants slow, acoustic beats.

```
============================================================
  Profile 2 — Chill Lofi
============================================================

  #1  Midnight Coding  —  LoRoom
       Genre: lofi  |  Mood: chill
       Score: 4.48 / 4.5  [####################]
       Why this song:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.98) (song=0.42, target=0.40)
         • acoustic match (+0.5) (acousticness=0.71)

  #2  Library Rain  —  Paper Lanterns
       Genre: lofi  |  Mood: chill
       Score: 4.45 / 4.5  [####################]
       Why this song:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.95) (song=0.35, target=0.40)
         • acoustic match (+0.5) (acousticness=0.86)

  #3  Focus Flow  —  LoRoom
       Genre: lofi  |  Mood: focused
       Score: 3.50 / 4.5  [################----]
       Why this song:
         • genre match (+2.0)
         • energy similarity (+1.00) (song=0.40, target=0.40)
         • acoustic match (+0.5) (acousticness=0.78)

  #4  Spacewalk Thoughts  —  Orbit Bloom
       Genre: ambient  |  Mood: chill
       Score: 2.38 / 4.5  [###########---------]
       Why this song:
         • mood match (+1.0)
         • energy similarity (+0.88) (song=0.28, target=0.40)
         • acoustic match (+0.5) (acousticness=0.92)

  #5  Coffee Shop Stories  —  Slow Stereo
       Genre: jazz  |  Mood: relaxed
       Score: 1.47 / 4.5  [#######-------------]
       Why this song:
         • energy similarity (+0.97) (song=0.37, target=0.40)
         • acoustic match (+0.5) (acousticness=0.89)

============================================================
```

**Observation:** Both lofi/chill songs hit near-perfect scores. The clear drop from #3 (3.50) to #4 (2.38) shows the mood bonus is the deciding separator once genre is established.

---

### Profile 3 — Deep Intense Rock

A headbanger who wants aggressive, electric guitar at high energy.

```
============================================================
  Profile 3 — Deep Intense Rock
============================================================

  #1  Storm Runner  —  Voltline
       Genre: rock  |  Mood: intense
       Score: 4.49 / 4.5  [####################]
       Why this song:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.99) (song=0.91, target=0.92)
         • non-acoustic match (+0.5) (acousticness=0.10)

  #2  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense
       Score: 2.49 / 4.5  [###########---------]
       Why this song:
         • mood match (+1.0)
         • energy similarity (+0.99) (song=0.93, target=0.92)
         • non-acoustic match (+0.5) (acousticness=0.05)

  #3  Crown of Thunder  —  Ironveil
       Genre: metal  |  Mood: angry
       Score: 1.46 / 4.5  [######--------------]
       Why this song:
         • energy similarity (+0.96) (song=0.96, target=0.92)
         • non-acoustic match (+0.5) (acousticness=0.04)

  #4  Neon Pulse  —  Greywave
       Genre: electronic  |  Mood: energetic
       Score: 1.46 / 4.5  [######--------------]
       Why this song:
         • energy similarity (+0.96) (song=0.88, target=0.92)
         • non-acoustic match (+0.5) (acousticness=0.08)

  #5  Sunrise City  —  Neon Echo
       Genre: pop  |  Mood: happy
       Score: 1.40 / 4.5  [######--------------]
       Why this song:
         • energy similarity (+0.90) (song=0.82, target=0.92)
         • non-acoustic match (+0.5) (acousticness=0.18)

============================================================
```

**Observation:** Storm Runner is the only rock/intense song, so it scores a near-perfect 4.49 and then there is a huge cliff — #2 drops to 2.49. The bottom three slots (#3-5) are essentially tied around 1.46, showing the catalog has only one true rock song and the system cannot differentiate much below #1.

---

### Edge Case A — Conflicting Energy vs. Sad Mood

**Design intent:** energy=0.9 implies a club banger; mood="sad" implies a slow ballad. No song in the catalog is tagged "sad." This tests whether the system honors the emotional intent or ignores it in favor of numeric energy.

```
============================================================
  Edge Case A — Conflicting Energy vs. Sad Mood
============================================================

  #1  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense
       Score: 3.47 / 4.5  [###############-----]
       Why this song:
         • genre match (+2.0)
         • energy similarity (+0.97) (song=0.93, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.05)

  #2  Sunrise City  —  Neon Echo
       Genre: pop  |  Mood: happy
       Score: 3.42 / 4.5  [###############-----]
       Why this song:
         • genre match (+2.0)
         • energy similarity (+0.92) (song=0.82, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.18)

  #3  Storm Runner  —  Voltline
       Genre: rock  |  Mood: intense
       Score: 1.49 / 4.5  [#######-------------]
       Why this song:
         • energy similarity (+0.99) (song=0.91, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.10)

  #4  Neon Pulse  —  Greywave
       Genre: electronic  |  Mood: energetic
       Score: 1.48 / 4.5  [#######-------------]
       Why this song:
         • energy similarity (+0.98) (song=0.88, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.08)

  #5  Crown of Thunder  —  Ironveil
       Genre: metal  |  Mood: angry
       Score: 1.44 / 4.5  [######--------------]
       Why this song:
         • energy similarity (+0.94) (song=0.96, target=0.90)
         • non-acoustic match (+0.5) (acousticness=0.04)

============================================================
```

**What this reveals:** The system was "tricked." A user who says they want sad music gets Gym Hero and Sunrise City — upbeat, high-energy pop — because energy=0.9 fires strongly and mood="sad" never matches anything (it earns 0 mood points for every song). The mood label is silently ignored, and the numeric energy score takes over. This is a real-world failure mode: the system optimizes what it can measure (energy as a float) and discards what it cannot match (a mood label not in the catalog).

---

### Edge Case B — Genre Not In Catalog (jazz-pop)

**Design intent:** The user wants "jazz-pop," which does not exist as a genre in `songs.csv`. The genre bonus (+2.0) never fires, capping every song's max score at 2.5.

```
============================================================
  Edge Case B — Genre Not In Catalog (jazz-pop)
============================================================

  #1  Rooftop Lights  —  Indigo Parade
       Genre: indie pop  |  Mood: happy
       Score: 2.39 / 4.5  [###########---------]
       Why this song:
         • mood match (+1.0)
         • energy similarity (+0.89) (song=0.76, target=0.65)
         • non-acoustic match (+0.5) (acousticness=0.35)

  #2  Sunrise City  —  Neon Echo
       Genre: pop  |  Mood: happy
       Score: 2.33 / 4.5  [##########----------]
       Why this song:
         • mood match (+1.0)
         • energy similarity (+0.83) (song=0.82, target=0.65)
         • non-acoustic match (+0.5) (acousticness=0.18)

  #3  Mango Sunset  —  Coral Tide
       Genre: reggae  |  Mood: uplifting
       Score: 1.47 / 4.5  [#######-------------]
       Why this song:
         • energy similarity (+0.97) (song=0.62, target=0.65)
         • non-acoustic match (+0.5) (acousticness=0.58)

  #4  Concrete Gospel  —  MadLib Jones
       Genre: hip-hop  |  Mood: nostalgic
       Score: 1.42 / 4.5  [######--------------]
       Why this song:
         • energy similarity (+0.92) (song=0.73, target=0.65)
         • non-acoustic match (+0.5) (acousticness=0.15)

  #5  Night Drive Loop  —  Neon Echo
       Genre: synthwave  |  Mood: moody
       Score: 1.40 / 4.5  [######--------------]
       Why this song:
         • energy similarity (+0.90) (song=0.75, target=0.65)
         • non-acoustic match (+0.5) (acousticness=0.22)

============================================================
```

**What this reveals:** With no genre match available, the system silently falls back on mood+energy+acousticness. The top two results (2.39 and 2.33) are reasonable happy/pop-adjacent picks, but the margin over #3 (1.47) is tiny. Tiny energy differences are now deciding the ranking. A catalog gap directly weakens recommendation confidence and the results feel arbitrary below #2.

---

### Edge Case C — Perfectly Neutral / All Mid-Range

**Design intent:** Every preference is set to the middle value (energy=0.5, acousticness=0.5 — right on the threshold). The genre is "ambient" (only one song in the catalog). This tests whether the system surfaces a reasonable list or collapses into a near-random ranking.

```
============================================================
  Edge Case C — Perfectly Neutral / All Mid-Range
============================================================

  #1  Spacewalk Thoughts  —  Orbit Bloom
       Genre: ambient  |  Mood: chill
       Score: 3.78 / 4.5  [#################---]
       Why this song:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.78) (song=0.28, target=0.50)

  #2  Midnight Coding  —  LoRoom
       Genre: lofi  |  Mood: chill
       Score: 1.92 / 4.5  [#########-----------]
       Why this song:
         • mood match (+1.0)
         • energy similarity (+0.92) (song=0.42, target=0.50)

  #3  Library Rain  —  Paper Lanterns
       Genre: lofi  |  Mood: chill
       Score: 1.85 / 4.5  [########------------]
       Why this song:
         • mood match (+1.0)
         • energy similarity (+0.85) (song=0.35, target=0.50)

  #4  Mango Sunset  —  Coral Tide
       Genre: reggae  |  Mood: uplifting
       Score: 1.38 / 4.5  [######--------------]
       Why this song:
         • energy similarity (+0.88) (song=0.62, target=0.50)
         • non-acoustic match (+0.5) (acousticness=0.58)

  #5  Concrete Gospel  —  MadLib Jones
       Genre: hip-hop  |  Mood: nostalgic
       Score: 1.27 / 4.5  [######--------------]
       Why this song:
         • energy similarity (+0.77) (song=0.73, target=0.50)
         • non-acoustic match (+0.5) (acousticness=0.15)

============================================================
```

**What this reveals:** Spacewalk Thoughts scores 3.78 and wins by a wide margin simply because it is the only ambient song — it collects the genre bonus (+2.0) and mood bonus (+1.0) while its low energy (0.28 vs target 0.50) only costs 0.22 points. The acousticness=0.50 profile sits exactly on the threshold (0.6), so the acoustic/non-acoustic bonus never fires for Spacewalk Thoughts. Below #1, the list devolves to whatever songs happened to land closest to energy=0.50 — mood labels do the remaining sorting. The system produces a coherent-looking top result but the bottom four are essentially noise for this user.

---

## Sample Output — Default Pop/Happy Profile

Terminal output from running `python -m src.main` with the default lofi/chill user profile (energy 0.4, acousticness 0.75):

```
Loaded 18 songs from catalog.

============================================================
  Top Recommendations
============================================================

  #1  Midnight Coding  —  LoRoom
       Genre: lofi  |  Mood: chill
       Score: 4.48 / 4.5  [####################]
       Why this song:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.98) (song=0.42, target=0.40)
         • acoustic match (+0.5) (acousticness=0.71)

  #2  Library Rain  —  Paper Lanterns
       Genre: lofi  |  Mood: chill
       Score: 4.45 / 4.5  [####################]
       Why this song:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.95) (song=0.35, target=0.40)
         • acoustic match (+0.5) (acousticness=0.86)

  #3  Focus Flow  —  LoRoom
       Genre: lofi  |  Mood: focused
       Score: 3.50 / 4.5  [################----]
       Why this song:
         • genre match (+2.0)
         • energy similarity (+1.00) (song=0.40, target=0.40)
         • acoustic match (+0.5) (acousticness=0.78)

  #4  Spacewalk Thoughts  —  Orbit Bloom
       Genre: ambient  |  Mood: chill
       Score: 2.38 / 4.5  [###########---------]
       Why this song:
         • mood match (+1.0)
         • energy similarity (+0.88) (song=0.28, target=0.40)
         • acoustic match (+0.5) (acousticness=0.92)

  #5  Coffee Shop Stories  —  Slow Stereo
       Genre: jazz  |  Mood: relaxed
       Score: 1.47 / 4.5  [#######-------------]
       Why this song:
         • energy similarity (+0.97) (song=0.37, target=0.40)
         • acoustic match (+0.5) (acousticness=0.89)

============================================================
```

The results match expectations: the two lofi/chill songs rank 1st and 2nd with near-perfect scores (4.48 and 4.45). The third slot goes to another lofi song that lost the mood-match bonus. The ASCII score bar makes it easy to spot the large gap between the top three and the rest.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

**Experiment 1 — Baseline: lofi / chill user (energy 0.4, prefers acoustic)**

The system ranked both lofi-chill songs at the top with scores of 4.48 and 4.45, well clear of everything else. The third result, Focus Flow, was still lofi but tagged "focused" instead of "chill" — it scored 3.50 because the mood bonus was missing. This confirmed the recipe was working as intended.

**Experiment 2 — Dropping the genre weight from +2.0 to +0.5**

With the same lofi / chill user, lowering the genre weight closed the gap significantly. The two lofi-chill songs still led (2.98 and 2.95), but Spacewalk Thoughts — an ambient-chill song with no genre match — jumped to third place at 2.38, nearly tied with Focus Flow at 2.00. This showed that genre is the main separator in the current design. Reducing its weight lets mood and energy do more work, which can surface good cross-genre matches but also makes the results feel less targeted.

**Experiment 3 — High-energy metal / angry user (energy 0.95, non-acoustic)**

Crown of Thunder scored 4.49 — nearly a perfect score — and the second-place song (Gym Hero, pop/intense) was all the way back at 1.48. This revealed a concentration problem: when a user has a very specific genre, all the points pile onto one song and the rest of the list is essentially random. The catalog only has one metal song, so the ranking below first place is not meaningful for this user type.

**Experiment 4 — User whose favorite genre does not exist in the catalog (jazz-pop)**

With no genre match available, the genre bonus never fired and the maximum any song could score was 2.5. The top result was Rooftop Lights (indie pop / happy) at 2.44, followed closely by Sunrise City (pop / happy) at 2.38. The system fell back on mood and energy similarity, which produced a reasonable result — but every song in the top five was within 1 point of each other, meaning small differences in energy level were deciding the ranking. A catalog gap directly weakened the system's confidence.

**Experiment 5 — Weight shift: double energy importance, halve genre importance (not applied to code)**

This was a hypothetical test run without changing the main scoring code. The question: what if energy similarity was worth +0.0–2.0 (doubled) and genre was only worth +1.0 (halved), while keeping the max score at 4.5?

Simulated results showed:
- Songs without a genre match climbed significantly — Rooftop Lights (indie pop) rose from 2.36 to 3.22 for a pop user, nearly matching Gym Hero.
- The "huge cliff" effect in Profile 3 (rock) shrank — Gym Hero jumped from 2.49 to 3.48 purely on energy proximity.
- The conflicting energy/mood edge case got worse: with energy worth twice as much, the numeric signal drowned out mood even more completely.

**Conclusion:** The change made recommendations more "vibe-accurate" (rewarding songs that feel right energetically) but less genre-loyal. For users with niche genres or mood-driven preferences, halving genre made the results feel less targeted. The original weights — where genre anchors the recommendation — produce more consistent and expected results for this small catalog.

---

## Limitations and Risks

- **Tiny catalog.** With 18 songs across 15 genres, most genres have exactly one representative. The system cannot recommend diverse results for users with niche tastes — it runs out of genre matches almost immediately.
- **No understanding of meaning.** The system matches labels exactly. It does not know that "relaxed" and "chill" describe similar feelings, or that "indie pop" is a subgenre of "pop." Musically similar songs and genres are treated as completely unrelated.
- **Genre dominates everything.** The genre bonus (+2.0) is 44% of the maximum score. A song with the wrong genre can never beat a mediocre song with the right genre, no matter how well it fits in energy or mood.
- **Silent failures.** When a mood or genre is not in the catalog, the system does not warn the user. It quietly ignores the signal and returns results that look confident but may be emotionally wrong (see Edge Case A).
- **Three features are loaded but never scored.** Tempo, valence, and danceability are stored on every song but have no effect on recommendations. The system cannot tell the difference between a user who wants fast dance music and one who wants slow background music at the same energy level.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

This project made one thing very clear: a recommender system is only as good as its data. The scoring logic is simple and consistent, but the quality of its output depends entirely on whether the catalog covers the user's taste. When lofi/chill was the genre, the results were clean and confident. When rock was the genre, the system had one correct answer and four guesses. When the genre did not exist at all, everything felt arbitrary. The algorithm did not change between those cases — the catalog did. That is a lesson that carries over directly to real AI systems: collecting diverse, representative data is not less important than designing a good model. It is usually more important.

The bias question was the most eye-opening part. The genre weight (+2.0 out of 4.5) was not a deliberate design choice to favor certain users — it was a practical decision to make genre the primary signal. But that decision has a side effect: users whose favorite genre is well-represented in the catalog get noticeably better recommendations than users whose genre is rare or missing. The system does not intend to treat those users differently. It just does, as a consequence of a weight that seemed reasonable in isolation. That is what makes bias in AI systems hard to catch: it is often not the result of a bad intention, it is the result of a reasonable-seeming decision that interacts badly with uneven data.