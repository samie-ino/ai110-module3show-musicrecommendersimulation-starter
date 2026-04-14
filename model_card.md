# Model Card: Music Recommender Simulation

## 1. Model Name

**GrooveFit 1.0**

---

## 2. Intended Use

GrooveFit suggests songs based on a listener's genre, mood, energy level, and acoustic preference.

It assumes the user can describe their taste with a single genre label, a single mood word, a number between 0 and 1 for energy, and a yes/no answer about liking acoustic music.

This is a classroom simulation. It is meant to help students understand how simple scoring rules produce real-world recommendation patterns. It is not designed for a live music app.

**What it should NOT be used for:** Production music services, personalization at scale, or any situation where a wrong recommendation has real consequences for a user.

---

## 3. How the Model Works

Every song in the catalog gets a score out of 4.5 points. The top five scores become the recommendations.

Here is how points are awarded:

- **Genre match (+2.0):** If the song's genre exactly matches your favorite genre, it earns 2 points. No partial credit — "indie pop" and "pop" are treated as completely different.
- **Mood match (+1.0):** If the song's mood tag exactly matches your preferred mood, it earns 1 point.
- **Energy similarity (+0.0 to +1.0):** The closer the song's energy is to your target energy, the more points it earns. A perfect energy match gives +1.0; being 0.5 off gives +0.5.
- **Acoustic preference (+0.5):** If you like acoustic music and the song has high acousticness (above 0.6), it earns 0.5 points. Same bonus if you dislike acoustic music and the song is below 0.6.

The system prints a plain-English reason for every point, so you can see exactly why each song was recommended.

---

## 4. Data

The catalog has **18 songs** spread across **15 different genres**.

Each song has ten attributes: id, title, artist, genre, mood, energy, tempo (bpm), valence, danceability, and acousticness.

Only four of those attributes are actually used in scoring: genre, mood, energy, and acousticness. Tempo, valence, and danceability are loaded but ignored.

The catalog is small and uneven. Most genres have only one song. Lofi has three songs and pop has two — users who prefer those genres get the most reliable results. A user who prefers rock, blues, or reggae gets only one genre match in the entire catalog.

No real listener data was collected. All user profiles were hand-crafted for testing. The catalog does not cover subgenres, regional styles, or newer music trends.

---

## 5. Strengths

The system works best when a user's genre has several well-tagged songs in the catalog. Lofi/chill listeners, for example, see clean, high-confidence results because the catalog has three lofi songs and two of them also match mood=chill.

Every recommendation comes with a score breakdown. A developer or student can immediately see why a song ranked where it did, which makes debugging and learning straightforward.

For users whose preferences are well-represented, the top result is almost always an intuitive match. In six out of six test profiles, the #1 song was defensible given the user's stated preferences.

---

## 6. Limitations and Bias

The most significant weakness discovered during experimentation is a **genre filter bubble**: the genre match bonus (+2.0 out of a maximum 4.5 points) accounts for 44% of the total possible score, which means the top recommendations almost always come from a single genre regardless of how well a song fits in other dimensions. This is compounded by the small, genre-diverse dataset — with 18 songs spread across 15 distinct genres, most users receive only one or two genre-matched songs before the algorithm begins surfacing poor-fit alternatives. The scoring also treats related genres as completely unrelated: a user who prefers "pop" receives zero genre credit for "indie pop" or "electronic," creating hard walls between musically similar styles that real listeners would likely enjoy together. Three song attributes — `tempo_bpm`, `valence`, and `danceability` — are loaded from the dataset but never factored into scoring, so the system cannot distinguish between a user who wants high-energy dance music and one who wants high-energy background music, even though their ideal playlists would look very different. Finally, the acousticness preference uses a binary 0.6 threshold, meaning a song at 0.59 acousticness is treated identically to a fully electric track, introducing a sharp and arbitrary cutoff that does not reflect how listeners actually perceive acoustic character on a spectrum.

---

## 7. Evaluation

Six user profiles were run against the full 18-song catalog: three listener personas designed to represent realistic use cases, and three adversarial edge cases designed to push the system into difficult territory.

**Profiles tested:**

- **Profile 1 — High-Energy Pop:** genre=pop, mood=happy, energy=0.90, acoustic=no
- **Profile 2 — Chill Lofi:** genre=lofi, mood=chill, energy=0.40, acoustic=yes
- **Profile 3 — Deep Intense Rock:** genre=rock, mood=intense, energy=0.92, acoustic=no
- **Edge A — Conflicting Sad:** genre=pop, mood=sad, energy=0.90, acoustic=no
- **Edge B — Missing Genre:** genre=jazz-pop, mood=happy, energy=0.65, acoustic=no
- **Edge C — Perfectly Neutral:** genre=ambient, mood=chill, energy=0.50, acoustic=0.50 (on threshold)

**What I looked for:**

For each profile I checked three things: (1) whether the top-ranked song was a reasonable match for that listener, (2) whether the score distribution looked healthy — a clear winner with a meaningful gap below it — and (3) whether unexpected songs appeared where they should not have.

**What surprised me:**

The biggest surprise was how often "Gym Hero" (pop, mood=intense) appeared for users who never asked for intense music. Profile 1 wanted pop/happy, yet Gym Hero ranked #2 with 3.47 out of 4.5, just below the correct pop/happy song Sunrise City at 4.42. Gym Hero earned those points purely from genre match (+2.0) and a near-perfect energy score (+0.97) — even though it missed the mood bonus entirely. The genre weight is heavy enough that a wrong-mood pop song still outranks every song from a different genre, no matter how well those songs match in energy.

In Edge Case A (the user who said they wanted "sad" music), Gym Hero actually climbed to #1. Because no song in the catalog has mood="sad", the mood bonus was zero for every song. The system could not reward any song for being emotionally correct, so it fell back entirely on genre and energy — and Gym Hero's energy (0.93) happened to sit slightly closer to the target (0.90) than Sunrise City's (0.82). A user asking for slow, melancholy songs received a high-energy workout track. The system did not detect the contradiction; it just optimized the numbers it had.

The second surprise was the sharp cliff in Profile 3 (rock). Storm Runner scored 4.49 and the next song dropped all the way to 2.49 — a gap of exactly two points, which is the size of the genre bonus. The catalog has exactly one rock song. That made position #1 a foregone conclusion before the algorithm even ran. Positions #2 through #5 were decided by mood and energy among songs that shared no genre with the user, making those slots feel arbitrary.

The third surprise was Edge Case B (jazz-pop, a genre not in the catalog). With the genre bonus permanently at zero, the maximum any song could score was 2.5. The top five results clustered between 2.39 and 1.40 — all within one point of each other — with tiny energy differences deciding the order. The recommendations looked plausible on the surface but were fragile: shifting a song's energy by 0.05 could swap its position by two or three ranks.

**Comparisons and simple tests:**

A weight-reduction experiment (genre dropped from +2.0 to +0.5) confirmed that genre is the main separator in the current design. With lower genre weight, cross-genre songs with strong energy matches climbed significantly and the "Gym Hero problem" for Profile 1 shrank. However, results felt less targeted for users with niche taste profiles. The original weights produce more consistent and expected results for this catalog size.

The primary evaluation method was reading the reasoning bullets printed for each recommendation. Because every score is fully explained — for example, `genre match (+2.0); energy similarity (+0.97)` — mismatches like "this user wanted happy music but received intense" were immediately visible without any additional tooling.

---

## 8. Ideas for Improvement

**1. Add fuzzy genre matching.**
Right now "pop" and "indie pop" are treated as completely unrelated. A real listener who likes pop would probably enjoy indie pop too. Grouping similar genres into families (like pop → pop, indie pop, synth pop) and giving partial credit for close matches would make the recommendations feel less rigid.

**2. Use the ignored features.**
Tempo, valence, and danceability are already in every song record but never affect the score. Adding them — even with small weights — would let the system tell the difference between a user who wants fast, danceable music and one who wants slow, melancholy music at the same energy level.

**3. Expand the catalog.**
With 18 songs across 15 genres, most genres have exactly one representative. No matter how good the algorithm is, it cannot recommend diverse rock songs when only one rock song exists. Growing the catalog to at least five songs per genre would dramatically improve results for users with niche tastes.

---

## 9. Personal Reflection

Building this simulation made it clear how much a recommender system depends on what is in its catalog — not just how smart the scoring is. I expected the algorithm to be the interesting part, but the most revealing moments came from the edge cases: a user who asked for sad music and got a workout track, or a user whose favorite genre simply did not exist in the catalog. Those failures are not really bugs in the code. They are gaps between what the data covers and what real listeners want.

The thing that surprised me most was how confident the system looks even when it is wrong. The scores have decimal places, the explanations look detailed, and the top result is usually a song you could believe in. It is easy to trust the output without noticing that the mood signal was silently ignored or that the recommendations are basically tied. Real music apps have millions of songs and user feedback to smooth over these gaps. With 18 songs and no feedback loop, every weakness becomes very visible — which turned out to be the best thing about doing this as a classroom exercise.

I now think about recommendation engines differently. Every "because you liked X" suggestion from a real app is hiding decisions about weights, catalog coverage, and which signals to trust. This simulation showed me the skeleton underneath those decisions.
