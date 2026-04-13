# Reflection: Profile Comparison Notes

These notes compare what happened when I ran the recommender for different user profiles.
Written in plain language for a non-programmer audience.

---

## Lofi/Chill vs. High-Energy Pop

The lofi listener and the pop listener are almost mirror images of each other.
The lofi profile wants slow, quiet, acoustic tracks and gets Library Rain and Midnight Coding
at the top — both perfect matches. The pop profile wants loud, fast, produced tracks and gets
Sunrise City first. The interesting case is Gym Hero: it shows up #2 for the pop profile
even though the user said they want "happy" music and Gym Hero is tagged as "intense."
The reason is that Gym Hero is still a pop song, so it earns the genre bonus (3 points),
and its energy is very close to what the user asked for. That 3-point genre bonus is hard to
beat — it is worth more than a perfect mood match. So if you are a pop fan, you will keep
seeing Gym Hero near the top of your list even if the mood is not quite right.
This makes sense musically — pop fans generally prefer pop songs even imperfect ones —
but it shows that genre is doing a lot of heavy lifting in the score.

---

## High-Energy Pop vs. Deep Intense Rock

Both profiles want high energy, but they land in very different places.
The pop fan gets bright, danceable songs (Sunrise City, Rooftop Lights).
The rock fan gets Storm Runner first by a wide margin — it is the only rock song in the catalog,
so it earns the full genre bonus. The #2 result for rock is Gym Hero, which shows up again
because it has a matching mood ("intense") even though it is a pop song.
The takeaway: mood can pull a song across genre lines when the genre bonus is already lost.
For the pop fan, mood mattered less than expected because genre dominated.
For the rock fan, mood became the tiebreaker once Storm Runner was set aside.

---

## Deep Intense Rock vs. Conflicting (High Energy + Sad Mood)

This comparison is the most instructive. The rock profile has consistent preferences —
high energy and an intense mood go together naturally — so the top result is clear and scores 9.74.
The conflicting profile asks for high energy AND a sad mood, which almost never go together in real music.
The system's response is honest: Iron Cathedral wins because it is the only metal song (genre match)
and has the right energy, but it is "angry" not "sad." The system cannot find a song that does both.
The score drops to 7.81 for #1, and then falls sharply to 4.42 for #2.
In a real app you would want to tell the user "we could not find a good match" rather than
silently returning a mediocre list. This recommender does not do that — it always returns k results
no matter how poor the fit.

---

## Unknown Genre (k-pop) vs. Extreme Acoustic Minimalist

Both profiles expose the same root problem: the catalog is too small.
The k-pop listener gets zero genre matches. The system falls back to mood + numeric features
and returns pop-adjacent songs, which are close but not the same thing.
The scores all land between 4.5 and 6.7 — the system is visibly reaching.
The classical minimalist has the opposite problem: there is exactly one classical song,
so the #1 result is perfect (9.63) and then everything else is a steep drop to 4.31.
One song serves this profile well; zero songs serve the k-pop profile at all.
Both cases point to the same fix: more data. A real recommender would have millions of songs
and would rarely face a true coverage gap. At 20 songs, the gaps are everywhere.

---

## General Observation: Why "Gym Hero" Keeps Showing Up

A non-programmer asked why Gym Hero appears in so many different profiles.
Here is the plain-language answer: Gym Hero is a pop song with very high energy (0.93),
high danceability, and almost no acoustic instruments. That combination of features
makes it numerically close to a lot of different user targets.
If you want high energy, Gym Hero scores well on energy.
If you want pop, it earns the genre bonus.
If you want low acousticness, it scores well there too.
It is basically a "safe" song for the scoring formula — it sits in the middle of many features
at an extreme value, so it gets pulled into many different top-5 lists.
This is a known problem in content-based recommenders called the "popularity trap":
a small number of songs with broad feature coverage dominate the rankings
across many different user types, while niche songs (like Sonata in Grey or Empty Porch)
only appear for one very specific profile.
