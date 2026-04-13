"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

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

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
