# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder 1.0 tries to predict which songs from a small catalog a user would most enjoy, based on preferences they describe in advance. Given a user's favorite genre, mood, energy level, tempo, and acoustic texture, the system scores every song and returns the top 5 ranked from best to worst match. It does not learn over time — every run starts fresh from the same rules.

---

## 3. Data Used

- **Size**: 20 songs in `data/songs.csv`
- **Features per song**: id, title, artist, genre, mood, energy (0–1), tempo in BPM, valence (0–1), danceability (0–1), acousticness (0–1)
- **Genres covered**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, country, r&b, metal, folk, electronic, reggae, blues, latin
- **Moods covered**: happy, chill, intense, relaxed, moody, focused, confident, melancholy, nostalgic, romantic, angry, sad, energetic, peaceful, longing, uplifting
- **Limits**: Most genres have only one song. The catalog has no non-Western music. All songs are fictional. There is no listening history, artist popularity data, or lyric content.

---

## 4. Algorithm Summary

The recommender works like a scorecard. For each song, it checks six things and adds up the points:

1. **Genre match** — worth 3 points if the song's genre matches what the user asked for, 0 if not. Genre gets the most weight because it defines the whole sound of a song.
2. **Mood match** — worth 2 points for a match, 0 for a miss. Mood matters a lot but is slightly less reliable than genre as a signal.
3. **Energy similarity** — worth up to 2 points. A song that is very close to the user's target energy scores almost full points; one that is far away scores close to 0.
4. **Acoustic texture similarity** — worth up to 1.5 points. This captures whether the user wants organic instruments or produced sounds.
5. **Valence (brightness) similarity** — worth up to 1 point. How positive or dark the music feels.
6. **Tempo similarity** — worth up to 0.5 points. The BPM is converted to a 0–1 scale before comparing.

All six are added into a final score out of 10. The songs are sorted from highest to lowest and the top 5 are returned with a bullet-point breakdown of every term.

---

## 5. Observed Behavior / Biases

**What works well:** When the user's preferred genre and mood both exist in the catalog, the system reliably returns the right songs at the top. The Lofi/Chill and Rock/Intense profiles both produced a clear #1 with a score above 9.5, matching what a human would expect.

**Bias 1 — Catalog size imbalance.** Lofi has three songs; most genres have one. A lofi listener always gets a strong top result. A blues listener or a reggae listener has exactly one song that can earn genre points, so any variation in the other features pushes them down the list quickly.

**Bias 2 — Unknown genre cliff.** When a user's genre is not in the catalog (tested with k-pop), no song earns genre points. The system silently falls back to mood and numeric features and returns a list that is "close but wrong." Scores cap out below 7.0, but the system does not warn the user.

**Bias 3 — Energy is direction-blind.** The energy gap is calculated as an absolute difference. A user who wants energy 0.5 is penalized the same whether a song is at 0.2 (too calm) or 0.8 (too intense), even though those feel very different. For users near the middle of the scale, this can pull in songs from both extremes.

**Bias 4 — Genre outweighs mood at 3:2.** A song with the right genre but wrong mood will almost always beat a song with the wrong genre but right mood. This is usually correct, but it means that users who care more about mood than genre will get results that feel off, with no way to change it short of editing the Python code.

---

## 6. Evaluation Process

Six profiles were run and their top-5 results were inspected manually:

| Profile | Result |
|---|---|
| Late-Night Study (lofi/chill) | Strong — Library Rain at 9.67 was exactly right |
| High-Energy Pop Fan | Good — Sunrise City at 9.53, but Gym Hero (#2) appeared despite wrong mood |
| Deep Intense Rock | Strong — Storm Runner at 9.74 was a clear winner |
| Conflicting: High Energy + Sad (metal) | Exposed contradiction — no song could satisfy both preferences |
| Unknown Genre (k-pop) | Exposed coverage gap — zero genre matches, all scores below 7.0 |
| Extreme Acoustic Minimalist (classical) | Exposed single-song cliff — #1 at 9.63, #2 dropped to 4.31 |

The most surprising finding was the "Gym Hero problem": a pop song with the wrong mood kept appearing in the top 3 for the pop profile because the genre bonus (3.0 pts) is too powerful to be overcome by a mood mismatch (losing 2.0 pts). That is technically correct given the weights, but it felt like a bug until the math was checked.

No numeric accuracy metric was used. Evaluation was judgment-based: does the top result feel right for this profile, and does the score gap between #1 and #5 reflect how well the catalog serves the user?

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Classroom demonstration of how content-based filtering works
- Learning how features, weights, and scoring interact to produce a ranked list
- Exploring bias and limitation analysis in a simple, inspectable system

**Not intended for:**
- Real music discovery — the catalog is 20 fictional songs
- Personalization — the system has no memory and cannot learn from feedback
- Any user-facing product — there is no input validation, no error handling for edge cases, and no way for a user to indicate that a recommendation was bad
- Comparing artists, predicting popularity, or making any claim about real music

---

## 8. Ideas for Improvement

1. **Soft genre matching**: Instead of a binary genre/no-genre check, group related genres (rock, metal, punk) so they give each other partial credit. This would fix the cliff-edge problem for users whose exact genre is missing from the catalog.

2. **Diversity enforcement**: Add a rule that no more than 2 songs from the same genre can appear in the top 5. Right now a lofi listener can get 3 lofi songs in a row, which is boring even if technically correct.

3. **Confidence signal**: When no song earns genre points, or when the top score is below 6.0, print a message like "No strong matches found — showing closest alternatives." This tells the user the system is uncertain rather than presenting a weak result as if it were confident.

---

## 9. Personal Reflection

**Biggest learning moment:** The hardest part of building this was not writing the code — it was deciding what the numbers should be. Choosing whether genre should be worth 3.0 or 2.0 points is not a programming question; it is a judgment call about how humans actually experience music. Every weight in the system encodes a hidden assumption about taste, and those assumptions shape every result the system ever produces. That was not obvious before building it.

**How AI tools helped, and when I had to check them:** AI assistance was most useful for generating the initial song catalog with diverse genres and moods, and for suggesting the weight structure. But the edge case analysis required running the system and reading the actual output — no amount of upfront planning predicted the "Gym Hero problem" or the classical cliff until the numbers appeared in the terminal. The AI could suggest what the weights should be in theory; only running the code revealed whether they worked in practice.

**What surprised me about simple algorithms:** A weighted sum of six features is about as simple as machine learning gets, yet the output genuinely felt like recommendations. When Library Rain appeared at the top for the lofi/chill profile with a score of 9.67 and a full explanation, it felt surprisingly convincing — even though the "intelligence" behind it was six additions and a sort. That gap between how simple the logic is and how reasonable the output feels is probably why recommender systems are so easy to over-trust in real products.

**What I would try next:** The single most valuable extension would be a feedback loop — even just a yes/no flag after each recommendation that adjusts the weights slightly over time. That would turn this from a static rule-follower into something that actually learns what the user means, rather than just what they said.
