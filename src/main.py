"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
from recommender import load_songs, recommend_songs

# Resolve data path relative to this file so the script works from any directory.
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_HERE, "..", "data", "songs.csv")


def main() -> None:
    songs = load_songs(DATA_PATH)
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: late-night study listener
    # Prefers mellow, acoustic-leaning tracks to stay focused without distraction.
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_tempo": 80,
        "target_valence": 0.60,
        "likes_acoustic": True,
        "weights": {
            "genre":       3.0,   # genre match is the strongest signal
            "mood":        2.5,   # mood is nearly as important
            "energy":      2.0,   # low-energy tracks are strongly preferred
            "acousticness": 1.5,  # acoustic texture matters but is secondary
            "valence":     1.0,   # mild positivity is fine; not a dealbreaker
            "tempo":       1.0,   # slow tempo preferred but flexible
        },
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 52)
    print("  TOP RECOMMENDATIONS")
    print(f"  Genre: {user_prefs['favorite_genre']}  |  Mood: {user_prefs['favorite_mood']}  |  Energy: {user_prefs['target_energy']}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score: {score:.2f} / 10.0")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print("       Why:")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")
        print("  " + "-" * 50)

    print()


if __name__ == "__main__":
    main()
