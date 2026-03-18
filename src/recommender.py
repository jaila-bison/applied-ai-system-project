from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for col in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[col] = float(row[col])
            songs.append(row)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    def score(song: Dict) -> float:
        """Return a 0–1 weighted similarity score between a song and the user's preferences."""
        return (
            (1.0 if song["genre"] == user_prefs.get("genre") else 0.0) * 0.30
            + (1.0 if song["mood"] == user_prefs.get("mood") else 0.0) * 0.25
            + (1.0 - abs(song["energy"] - user_prefs.get("energy", 0.5))) * 0.20
            + (1.0 - abs(song["valence"] - user_prefs.get("target_valence", 0.5))) * 0.15
            + (1.0 - abs(song["danceability"] - user_prefs.get("target_danceability", 0.5))) * 0.10
        )

    def explain(song: Dict) -> str:
        """Build a human-readable string listing which features matched the user's preferences."""
        reasons = []
        if song["genre"] == user_prefs.get("genre"):
            reasons.append(f"genre ({song['genre']})")
        if song["mood"] == user_prefs.get("mood"):
            reasons.append(f"mood ({song['mood']})")
        if abs(song["energy"] - user_prefs.get("energy", 0.5)) <= 0.15:
            reasons.append(f"energy ({song['energy']:.2f} ≈ target {user_prefs.get('energy', 0.5):.2f})")
        if not reasons:
            reasons.append(f"closest overall match (score {score(song):.2f})")
        return "Matched your " + ", ".join(reasons) + "."

    scored = [(song, score(song), explain(song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
