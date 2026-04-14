# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

Each song in the system will use energy, mood, genre, acousticness, and valence. What will be stored in the user profile will be thier energy level, favorite mood, favorite genre, and whether they prefer acoustic music or not.

• Energy (most important) — measure the gap between the song's energy and   the user's preferred energy. The smaller the gap, the more points it earns.
Mood — if the song's mood exactly matches the user's favorite mood, it earns full points. If not, it earns nothing.
• Genre — same rule as mood. An exact match earns full points, a mismatch earns nothing.
• Acousticness — if the user likes acoustic music, songs that are more acoustic earn more points. If the user prefers non-acoustic, the opposite applies.
• Valence (least important) — we infer how emotionally positive the user probably wants a song to be based on their mood preference. A happy mood preference expects a bright, positive song. A moody preference expects something darker. The closer the song is to that expectation, the more points it earns.

We never pick songs by hand. Instead, we let the scores do the deciding automatically.After every song in the catalog has been scored, we line them all up from highest score to lowest. The songs at the top earned their spot purely by how well they matched what the user told us they want. We then take however many top songs the user asked for and those become the recommendations.Because the score is built from the user's own profile, the result is personal to them. Two different users running the same system against the same catalog will get different recommendations, because their profiles are different and so their scores will be different.

This means the system is:
1. Automatic — no human decides what gets recommended
2. Consistent — the same user with the same profile always gets the same result
3. Explainable — we can always point to exactly why a song ranked where it did, because every score is traceable back to the five checks we ran

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

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

