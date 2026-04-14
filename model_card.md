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

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
