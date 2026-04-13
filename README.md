# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version builds a content-based music recommender that matches songs to a user's stated preferences using a weighted scoring system. Each song is represented by a set of descriptive features (genre, mood, energy, tempo, and valence), and each user profile stores the features they care about most along with how much weight to give each one. The recommender scores every song in the catalog against the user's profile and returns the top matches. The goal is to make the scoring logic transparent and easy to inspect, so it is clear exactly why a song was or was not recommended.

---

## Data Flow

```mermaid
flowchart TD
    A([🧑 User Preferences\nfavorite_genre · favorite_mood\ntarget_energy · target_tempo\ntarget_valence · likes_acoustic]) --> B

    B[(📄 songs.csv\n20 songs)] --> C

    C[🔁 For each song in catalog]

    C --> D1[Genre match?\n+3.0 or +0.0]
    C --> D2[Mood match?\n+2.0 or +0.0]
    C --> D3[Energy similarity\n2.0 × 1 - diff]
    C --> D4[Acousticness similarity\n1.5 × 1 - diff]
    C --> D5[Valence similarity\n1.0 × 1 - diff]
    C --> D6[Tempo similarity\n0.5 × 1 - norm_diff]

    D1 & D2 & D3 & D4 & D5 & D6 --> E[🧮 Sum all terms\nScore out of 10.0]

    E --> F[📋 Scored song list\nsong + score + reasons]

    F --> G[⬇️ Sort descending by score]

    G --> H[✂️ Slice top K results]

    H --> I([🎵 Top K Recommendations\ntitle · artist · score · explanation])
```

---

## How The System Works

Real-world recommenders like Spotify or YouTube Music typically combine two strategies: collaborative filtering (recommending what similar users liked) and content-based filtering (recommending songs that share features with songs you already enjoy). In practice, large platforms layer both on top of vast behavioral data — play counts, skips, replays, and playlist adds — to continuously refine what "you" means to the system. This simulation focuses on content-based filtering only, which means it will never surprise a user with something unexpected, but it also means every recommendation is fully explainable. The system will prioritize matching the features a user explicitly cares about — especially genre and mood — and use energy, tempo, and valence as tiebreakers.

---

## Algorithm Recipe

### Scoring formula

Each song receives a score out of **10.0**. The score is the sum of six weighted terms:

```
score = genre_points + mood_points + energy_points
      + acousticness_points + valence_points + tempo_points
```

### Step-by-step rules

**Step 1 — Genre match (categorical, max 3.0 pts)**

```
if song.genre == user.favorite_genre:
    genre_points = 3.0
else:
    genre_points = 0.0
```

*Why 3.0?* The catalog has 13 distinct genres. A random song has only an ~8% chance of matching. Genre defines the entire sonic landscape (instrumentation, production, rhythm), so a match is the strongest signal available.

---

**Step 2 — Mood match (categorical, max 2.0 pts)**

```
if song.mood == user.favorite_mood:
    mood_points = 2.0
else:
    mood_points = 0.0
```

*Why 2.0, not 3.0?* Mood is important but more porous than genre. A "chill" classical piece and a "chill" lofi track share a mood label but sound completely different. Genre narrows the sonic world first; mood refines within it.

---

**Step 3 — Energy similarity (continuous, max 2.0 pts)**

```
energy_points = 2.0 × (1 − |song.energy − user.target_energy|)
```

Energy spans 0.22–0.97 in the catalog — the widest numeric spread of any feature. It captures both tempo and intensity in one number, making it the best single proxy for "how this song feels."

---

**Step 4 — Acousticness similarity (continuous, max 1.5 pts)**

```
acousticness_points = 1.5 × (1 − |song.acousticness − user.target_acousticness|)
```

Acousticness cleanly separates organic-sounding tracks (folk, jazz, classical, all ≥ 0.72) from produced ones (electronic, synthwave, hip-hop, all ≤ 0.22). Users tend to have a stable organic-vs-produced preference, so this feature earns more weight than valence.

---

**Step 5 — Valence similarity (continuous, max 1.0 pts)**

```
valence_points = 1.0 × (1 − |song.valence − user.target_valence|)
```

Valence measures musical brightness (0 = dark, 1 = bright). Users tolerate more variation here — someone who wants "chill" music is fine with valence 0.55–0.75 — so the weight is lower.

---

**Step 6 — Tempo similarity (continuous, max 0.5 pts)**

```
normalized_song_tempo  = song.tempo_bpm / 200
normalized_user_tempo  = user.target_tempo / 200
tempo_points = 0.5 × (1 − |normalized_song_tempo − normalized_user_tempo|)
```

Tempo is divided by 200 to convert BPM to the same 0–1 scale as the other features. It gets the lowest weight because energy already encodes much of what tempo communicates about intensity.

---

### Weight summary

| Feature | Type | Max points | Why this weight |
|---|---|---|---|
| Genre | categorical match | 3.0 | Rarest match (~8% chance), strongest sonic constraint |
| Mood | categorical match | 2.0 | Strong signal but less precise than genre |
| Energy | continuous similarity | 2.0 | Widest numeric range; best single feel proxy |
| Acousticness | continuous similarity | 1.5 | Cleanly separates organic vs produced |
| Valence | continuous similarity | 1.0 | Users tolerate wider variation |
| Tempo | continuous similarity | 0.5 | Redundant with energy; needs BPM normalization |
| **Total** | | **10.0** | |

---

### `Song` features

| Feature   | Type      | Description                               |
| --------- | --------- | ----------------------------------------- |
| `title`   | string    | Song name                                 |
| `artist`  | string    | Artist name                               |
| `genre`   | string    | e.g. pop, hip-hop, indie, classical       |
| `mood`    | string    | e.g. happy, melancholy, hype, chill       |
| `energy`  | float 0–1 | How intense or active the track feels     |
| `tempo`   | int (BPM) | Beats per minute                          |
| `valence` | float 0–1 | Musical positivity (0 = dark, 1 = bright) |

### `UserProfile` features

| Feature           | Type      | Description                                                                 |
| ----------------- | --------- | --------------------------------------------------------------------------- |
| `name`            | string    | User identifier                                                             |
| `preferred_genre` | string    | The genre the user wants to hear                                            |
| `preferred_mood`  | string    | The mood the user is in                                                     |
| `energy_target`   | float 0–1 | How energetic the user wants songs to be                                    |
| `weights`         | dict      | How much each feature matters (e.g. `{"genre": 3, "mood": 2, "energy": 1}`) |

## Sample Output

![Recommendation output](recommendationOutput.png)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

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

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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
```
