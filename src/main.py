"""
Command line runner for the Music Recommender Simulation.

Run with:  python src/main.py
"""

import os
from recommender import load_songs, recommend_songs

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_HERE, "..", "data", "songs.csv")

# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

# Standard profiles
PROFILES = {
    "Late-Night Study (Lofi / Chill)": {
        "favorite_genre": "lofi",
        "favorite_mood":  "chill",
        "target_energy":  0.40,
        "target_tempo":   80,
        "target_valence": 0.60,
        "likes_acoustic": True,
        "weights": {"genre": 3.0, "mood": 2.0, "energy": 2.0,
                    "acousticness": 1.5, "valence": 1.0, "tempo": 0.5},
    },
    "High-Energy Pop Fan": {
        "favorite_genre": "pop",
        "favorite_mood":  "happy",
        "target_energy":  0.90,
        "target_tempo":   128,
        "target_valence": 0.85,
        "likes_acoustic": False,
        "weights": {"genre": 3.0, "mood": 2.0, "energy": 2.0,
                    "acousticness": 1.5, "valence": 1.0, "tempo": 0.5},
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood":  "intense",
        "target_energy":  0.92,
        "target_tempo":   150,
        "target_valence": 0.40,
        "likes_acoustic": False,
        "weights": {"genre": 3.0, "mood": 2.0, "energy": 2.0,
                    "acousticness": 1.5, "valence": 1.0, "tempo": 0.5},
    },
    # -------------------------------------------------------------------
    # Adversarial / edge-case profiles
    # -------------------------------------------------------------------
    # EDGE CASE 1: Conflicting energy + mood
    # energy: 0.95 (mosh-pit intensity) but mood: sad
    # Tests whether high energy rescues a dark-mood song or if mood weight wins.
    "Conflicting: High Energy + Sad Mood": {
        "favorite_genre": "metal",
        "favorite_mood":  "sad",
        "target_energy":  0.95,
        "target_tempo":   160,
        "target_valence": 0.15,
        "likes_acoustic": False,
        "weights": {"genre": 3.0, "mood": 2.0, "energy": 2.0,
                    "acousticness": 1.5, "valence": 1.0, "tempo": 0.5},
    },
    # EDGE CASE 2: Genre that does not exist in the catalog
    # No song will earn genre points — forces the system to rank entirely
    # on continuous features.  Exposes whether numeric scores alone
    # produce a "sensible" fallback or just noise.
    "Unknown Genre (k-pop)": {
        "favorite_genre": "k-pop",
        "favorite_mood":  "happy",
        "target_energy":  0.80,
        "target_tempo":   120,
        "target_valence": 0.85,
        "likes_acoustic": False,
        "weights": {"genre": 3.0, "mood": 2.0, "energy": 2.0,
                    "acousticness": 1.5, "valence": 1.0, "tempo": 0.5},
    },
    # EDGE CASE 3: Extreme acoustic + low energy preference
    # Targets the very bottom of the energy/tempo range.
    # Should surface classical/folk; tests whether the system over-favors
    # lofi (which is close but not the extreme).
    "Extreme Acoustic Minimalist": {
        "favorite_genre": "classical",
        "favorite_mood":  "melancholy",
        "target_energy":  0.10,
        "target_tempo":   50,
        "target_valence": 0.10,
        "likes_acoustic": True,
        "weights": {"genre": 3.0, "mood": 2.0, "energy": 2.0,
                    "acousticness": 1.5, "valence": 1.0, "tempo": 0.5},
    },
}

# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    """Print a formatted leaderboard for one user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 60)
    print(f"  PROFILE: {profile_name}")
    print(f"  Genre: {user_prefs['favorite_genre']}  |  "
          f"Mood: {user_prefs['favorite_mood']}  |  "
          f"Energy: {user_prefs['target_energy']}")
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  --  {song['artist']}")
        print(f"       Score : {score:.2f} / 10.0")
        print(f"       Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print("       Why   :")
        for reason in explanation.split(" | "):
            print(f"         * {reason}")
        print("  " + "-" * 58)

    print()


def main() -> None:
    songs = load_songs(DATA_PATH)
    print(f"Loaded songs: {len(songs)}\n")

    for profile_name, user_prefs in PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()
