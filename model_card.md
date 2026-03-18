# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
MixPix
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
MixPix generates ranked song recommendations based on a user's stated genre, mood, and audio feature preferences.
- What assumptions does it make about the user  
It assumes the user can describe their taste with a single favorite genre, mood, and target energy/valence/danceability level.
- Is this for real users or classroom exploration 
 This is built for classroom exploration, not production use.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
Each song is scored using five features: genre, mood, energy level, emotional positivity (valence), and danceability.
- What user preferences are considered 
 The user's favorite genre, mood, target energy, target valence, and target danceability are all considered.
- How does the model turn those into a score  
Each feature is compared to the user's preference and given a weighted score (genre 30%, mood 25%, energy 20%, valence 15%, danceability 10%), then summed to produce a final score between 0 and 1.
- What changes did you make from the starter logic  
Two explicit user preference fields (target_valence and target_danceability) were added to the starter profile to make all five features directly comparable.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
The catalog contains 15 songs.
- What genres or moods are represented  
It covers 12 genres (lofi, pop, rock, hip-hop, classical, r&b, metal, folk, ambient, jazz, synthwave, indie pop) and 11 moods (happy, chill, intense, relaxed, moody, focused, energetic, melancholic, romantic, angry, nostalgic).
- Did you add or remove data  
5 songs were added to the original 10-song starter set to broaden genre and mood coverage.
- Are there parts of musical taste missing in the dataset  
Tempo preferences, lyrics/language, cultural background, and listening context (e.g. commute vs. sleep) are not represented.


---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
The system works best for users with a clear, single-genre preference like lofi/focused or pop/happy.
- Any patterns you think your scoring captures correctly  
The genre + mood combination correctly dominates the score, keeping contextually irrelevant songs ranked low.
- Cases where the recommendations matched your intuition  
A pop/happy/high-energy user consistently gets "Sunrise City" and "Gym Hero" ranked first, which matches intuition.


---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The greatest weakness is the binary genre/mood lock-in controlling 55% of the score. Because genre and mood are exact-match booleans, a song is either in or completely out, there's no concept of "close enough." This means a lofi user will never discover ambient or jazz even though those genres are sonically indistinguishable from lofi on every continuous dimension. A single genre match (0.30) is so dominant that it can outweigh near-perfect alignment on energy, valence, and danceability combined (max 0.45). The fix would be replacing the binary with a soft similarity, a genre affinity matrix or embedding distance, so adjacent genres can surface instead of the same narrow slice repeating forever.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Eleven profiles were tested — three standard users and eight adversarial cases designed to expose edge cases in the scoring logic.
Standard profiles (lofi/focused, gym/energetic, folk/nostalgic) all returned the expected #1 result, confirming the formula behaves correctly under normal conditions.
The most surprising adversarial finding was that a "Metal but Happy" user receives a pop song at #1, because mood alignment plus strong continuous feature matches outweighs the genre bonus going to the only metal song in the catalog.
Profiles with nonexistent genres ("country") or moods ("sad") silently wasted up to 55% of the score with no warning, and a `None` energy value previously caused a crash that was only caught after testing with the `_get()` guard.
The out-of-range energy profile (1.5) confirmed that the `max(0.0, …)` clamping fix successfully prevents negative sub-scores and keeps all rankings valid.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Adding tempo_bpm range preferences and likes_acoustic as a scored feature (not just stored) would improve accuracy.
Explanations could show the numeric contribution of each feature rather than just which ones matched.
A diversity penalty could prevent all top-5 results from being the same genre.
Supporting a list of favorite genres and moods (instead of just one each) would handle mixed-taste users much better.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this made it clear that recommendation is fundamentally a design problem — choosing what to measure matters far more than the math itself.
The most surprising discovery was how a 15-song dataset with simple weights already produces results that feel reasonable and explainable.
It reframes apps like Spotify from "magic AI" to a system of deliberate tradeoffs — what to measure, how much to weight it, and what to deliberately leave out.