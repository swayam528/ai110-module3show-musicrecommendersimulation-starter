# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 suggests the top 5 songs from a 20-song catalog that best match a user's stated taste preferences. It is designed for classroom exploration of how content-based recommender systems work — not for deployment with real users. The system assumes the user can describe their preferences in advance using labels like genre and mood, and a target energy level. It makes no use of listening history, skip data, or any behavioral signal.

---

## 3. How the Model Works

Think of the recommender as a judge scoring a competition. Every song in the catalog gets a score based on how closely it matches what the user said they want. The judge checks six things: whether the genre matches (worth the most points), whether the mood matches (worth slightly less), and then how close the song's energy, acoustic feel, brightness, and tempo are to what the user described. Each of those last four checks gives partial credit — a song that is *almost* the right energy still earns most of those points. All six scores are added together into a number out of 10. The songs are then ranked from highest to lowest and the top 5 are shown, along with a plain-English explanation of exactly which features contributed to each score.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. The original starter file had 10 songs covering pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Ten additional songs were added to broaden coverage: hip-hop, classical, country, r&b, metal, folk, electronic, reggae, blues, and latin. Moods represented include happy, chill, intense, relaxed, moody, focused, confident, melancholy, nostalgic, romantic, angry, sad, energetic, peaceful, longing, and uplifting. The catalog skews toward genres with Western pop-music roots and does not represent traditional music from most of the world. There is only one song per genre in most cases, which creates fragility — if a user's preferred genre has no match, they get a very different experience.

---

## 5. Strengths

The system works best when the user's preferred genre exists in the catalog and at least one song shares their mood. In those cases — as seen with the Lofi/Chill profile and the Rock/Intense profile — the top result earns a score above 9.0 and the reasoning is intuitive and accurate. The system is also fully transparent: every point in the score is labeled, so a user can see exactly why "Library Rain" ranked above "Midnight Coding." That transparency is harder to achieve in real-world systems that use neural networks or collaborative filtering. The scoring is also fast and deterministic — the same inputs always produce the same ranked list, which makes it easy to test and debug.

---

## 6. Limitations and Bias

The most significant weakness discovered during experiments is that the system has no fallback for unknown genres. When the "k-pop" profile was tested, no song in the catalog earned genre points, so the top results were determined entirely by mood and numeric similarity — producing a list of pop-adjacent songs that a k-pop listener might find reasonable, but for entirely the wrong reasons. The system is also biased toward users whose tastes match the most-represented genre in the catalog: lofi has three songs while most genres have only one, giving lofi listeners a consistently stronger top result. A second bias appears in the energy feature: because energy is scored as a raw absolute difference, a user who wants energy 0.5 gets penalized equally for a song at 0.3 and a song at 0.7, even though those two songs can feel completely different depending on genre and production style. Finally, the system treats all users as if they have the same priority ordering — genre always matters most, mood second — but some users genuinely care more about mood than genre, and the current design does not allow for that without manually overriding the weights dictionary.

---

## 7. Evaluation

Six user profiles were tested: Late-Night Study (lofi/chill), High-Energy Pop Fan, Deep Intense Rock, and three adversarial edge cases. 

The **lofi/chill** and **rock/intense** profiles both produced strong, intuitive top results — the #1 song in each case was an exact genre and mood match with a score above 9.5. This confirmed that the categorical weights are working as intended.

The **high-energy pop** profile surfaced a surprise: Gym Hero (pop/intense, energy 0.93) ranked #2 despite its mood being "intense" rather than "happy." It earned a genre match but lost the mood points, yet still beat every non-pop song. This is the correct behavior — a pop song that is slightly wrong in mood is still more relevant than a perfect-mood song in a completely different genre — but it explains why "Gym Hero keeps showing up" for happy-pop listeners: the genre match alone (worth 3 points) is more powerful than a mood mismatch can overcome.

The **conflicting profile** (metal/sad, energy 0.95) revealed that the system cannot satisfy both halves of a contradiction. Iron Cathedral won on genre and energy but is "angry," not "sad." Empty Porch is "sad" but its low energy (0.30) makes it a terrible match for an energy target of 0.95. The system returned the less-bad option rather than refusing to answer — which is honest, but the low scores (below 8.0 for #1, below 4.0 for #5) signal to the user that the catalog cannot serve this profile well.

The **unknown genre** profile (k-pop) confirmed the coverage gap: no song earned genre points, and all top-5 scores fell below 7.0. The fallback results were reasonable — pop and indie-pop songs with happy moods surfaced — but a real user would likely feel the recommendations were off.

The **extreme acoustic minimalist** profile (classical/melancholy, energy 0.10) produced the starkest cliff: Sonata in Grey scored 9.63 and the next best result scored 4.31. The catalog has only one classical song and one melancholy song, and they happen to be the same song. Remove it and the profile gets useless results.

---

## 8. Future Work

- **Catalog expansion**: At minimum, two songs per genre and mood combination would eliminate the cliff-edge problem.
- **Soft genre matching**: Instead of a binary genre match, group genres into families (e.g., rock/metal/punk score partial credit for each other) so unknown or adjacent genres degrade gracefully.
- **Per-user weight customization via UI**: Rather than requiring the user to edit a Python dictionary, expose a simple "what matters most to you?" prompt that adjusts the weights automatically.
- **Diversity enforcement**: The current system can return three lofi songs in a row. A diversity penalty (e.g., no more than 2 songs from the same genre in the top 5) would make the output feel more useful.
- **Listening history**: Even a simple "thumbs up / thumbs down" flag stored between sessions would let the system learn which features the user actually responds to, rather than relying entirely on their stated preferences.

---

## 9. Personal Reflection

Building this recommender made it clear that the hardest part of a recommendation system is not the math — it is deciding what the numbers mean. Choosing whether genre should be worth 3.0 points or 2.0 points is not a technical question; it is a judgment about human taste. The edge case experiments were the most instructive part: the "high energy + sad mood" profile produced a result that is technically correct (it followed the rules) but would feel wrong to a real user, because no real person listens to music by optimizing a weighted sum. Real recommenders deal with this by learning from behavior over time instead of trusting users to accurately describe themselves upfront. The biggest takeaway is that transparency and accuracy are in tension: this system can explain every recommendation in plain English, but real systems that actually predict what users want — like Spotify's neural collaborative filters — work in ways that cannot be explained at all.
