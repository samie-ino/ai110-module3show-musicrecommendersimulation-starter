# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The most significant weakness discovered during experimentation is a **genre filter bubble**: the genre match bonus (+2.0 out of a maximum 4.5 points) accounts for 44% of the total possible score, which means the top recommendations almost always come from a single genre regardless of how well a song fits in other dimensions. This is compounded by the small, genre-diverse dataset — with 18 songs spread across 15 distinct genres, most users receive only one or two genre-matched songs before the algorithm begins surfacing poor-fit alternatives. The scoring also treats related genres as completely unrelated: a user who prefers "pop" receives zero genre credit for "indie pop" or "electronic," creating hard walls between musically similar styles that real listeners would likely enjoy together. Three song attributes — `tempo_bpm`, `valence`, and `danceability` — are loaded from the dataset but never factored into scoring, so the system cannot distinguish between a user who wants high-energy dance music and one who wants high-energy background music, even though their ideal playlists would look very different. Finally, the acousticness preference uses a binary 0.6 threshold, meaning a song at 0.59 acousticness is treated identically to a fully electric track, introducing a sharp and arbitrary cutoff that does not reflect how listeners actually perceive acoustic character on a spectrum.

---

## 7. Evaluation

Six user profiles were run against the full 18-song catalog: three listener personas designed to represent realistic use cases, and three adversarial edge cases designed to push the system into difficult territory.

**Profiles tested:**

| Profile | Genre | Mood | Energy | Acoustic |
|---|---|---|---|---|
| 1 — High-Energy Pop | pop | happy | 0.90 | no |
| 2 — Chill Lofi | lofi | chill | 0.40 | yes |
| 3 — Deep Intense Rock | rock | intense | 0.92 | no |
| Edge A — Conflicting Sad | pop | sad | 0.90 | no |
| Edge B — Missing Genre | jazz-pop | happy | 0.65 | no |
| Edge C — Perfectly Neutral | ambient | chill | 0.50 | 0.50 (on threshold) |

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

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
