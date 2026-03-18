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

def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print("\n" + "=" * 50)
    print(f"  Profile : {label}")
    print(f"  Prefs   : {user_prefs}")
    print("=" * 50)
    try:
        recommendations = recommend_songs(user_prefs, songs, k=k)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n  #{i}  {song['title']}  —  {song['artist']}")
            print(f"       Score : {score:.2f}")
            print(f"       Why   : {explanation}")
    except Exception as e:
        print(f"\n  ERROR: {type(e).__name__}: {e}")
    print("=" * 50)


def main() -> None:
    songs = load_songs(_CSV_PATH)
    print(f"Loaded {len(songs)} songs")

    profiles = [
        # Standard profiles
        ("Lofi User",           {"genre": "lofi",    "mood": "focused",   "energy": 0.40, "target_valence": 0.58, "target_danceability": 0.60}),
        ("Gym User",            {"genre": "hip-hop", "mood": "energetic", "energy": 0.90, "target_valence": 0.72, "target_danceability": 0.91}),
        ("Folk User",           {"genre": "folk",    "mood": "nostalgic", "energy": 0.30, "target_valence": 0.62, "target_danceability": 0.38}),
        # Adversarial profiles
        ("Metal but Happy",     {"genre": "metal",   "mood": "happy",     "energy": 0.90, "target_valence": 0.80, "target_danceability": 0.80}),
        ("Chill but Intense",   {"genre": "lofi",    "mood": "chill",     "energy": 0.95, "target_valence": 0.60, "target_danceability": 0.60}),
        ("Phantom Mood (sad)",  {"genre": "hip-hop", "mood": "sad",       "energy": 0.85, "target_valence": 0.30, "target_danceability": 0.70}),
        ("Ghost Genre (country)",{"genre": "country","mood": "nostalgic", "energy": 0.35, "target_valence": 0.65, "target_danceability": 0.40}),
        ("Extremist (all zero)",{"genre": "classical","mood": "melancholic","energy": 0.0,"target_valence": 0.0,  "target_danceability": 0.0}),
        ("Out-of-Range Energy", {"genre": "pop",     "mood": "happy",     "energy": 1.5,  "target_valence": 0.5,  "target_danceability": 0.5}),
        ("Case Mismatch",       {"genre": "Lo-Fi",   "mood": "Chill",     "energy": 0.40, "target_valence": 0.58, "target_danceability": 0.60}),
        ("None Energy (crash)", {"genre": "lofi",    "mood": "focused",   "energy": None, "target_valence": 0.58, "target_danceability": 0.60}),
    ]

    for label, user_prefs in profiles:
        print_recommendations(label, user_prefs, songs)


if __name__ == "__main__":
    main()
