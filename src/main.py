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

_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

def main() -> None:
    songs = load_songs(_CSV_PATH)
    print(f"Loaded {len(songs)} songs")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 40)
    print(f"  Top {len(recommendations)} Recommendations")
    print("=" * 40)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']}  —  {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Why   : {explanation}")
    print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
