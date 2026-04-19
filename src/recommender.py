from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import os


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

    def _score(self, user: UserProfile, song: Song) -> float:
        """
        Weighted similarity score in [0, 1].
        Weights: genre 0.35 + mood 0.25 + energy 0.25 + acousticness 0.15 = 1.00
        """
        acoustic_score = song.acousticness if user.likes_acoustic else (1.0 - song.acousticness)
        return (
            (1.0 if song.genre == user.favorite_genre else 0.0) * 0.35
            + (1.0 if song.mood == user.favorite_mood else 0.0) * 0.25
            + max(0.0, 1.0 - abs(song.energy - user.target_energy)) * 0.25
            + max(0.0, acoustic_score) * 0.15
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood ({song.mood})")
        if abs(song.energy - user.target_energy) <= 0.15:
            reasons.append(f"energy ({song.energy:.2f} ≈ target {user.target_energy:.2f})")
        acoustic_label = "acoustic" if user.likes_acoustic else "non-acoustic"
        if user.likes_acoustic and song.acousticness >= 0.70:
            reasons.append(f"{acoustic_label} feel (acousticness {song.acousticness:.2f})")
        elif not user.likes_acoustic and song.acousticness <= 0.30:
            reasons.append(f"{acoustic_label} feel (acousticness {song.acousticness:.2f})")
        if not reasons:
            reasons.append(f"closest overall match (score {self._score(user, song):.2f})")
        return "Matched your " + ", ".join(reasons) + "."

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
    def _get(key: str, default: float) -> float:
        """Return user_prefs[key], falling back to default if absent or None."""
        v = user_prefs.get(key)
        return default if v is None else v

    def score(song: Dict) -> float:
        """
        Weighted similarity score in [0, 1].
        Weights: genre 0.30 + mood 0.25 + energy 0.20 + valence 0.15 + danceability 0.10 = 1.00
        Continuous terms are clamped to [0, 1] to guard against out-of-range inputs.
        """
        return (
            (1.0 if song["genre"] == user_prefs.get("genre") else 0.0) * 0.30
            + (1.0 if song["mood"] == user_prefs.get("mood") else 0.0) * 0.25
            + max(0.0, 1.0 - abs(song["energy"] - _get("energy", 0.5))) * 0.20
            + max(0.0, 1.0 - abs(song["valence"] - _get("target_valence", 0.5))) * 0.15
            + max(0.0, 1.0 - abs(song["danceability"] - _get("target_danceability", 0.5))) * 0.10
        )

    def explain(song: Dict) -> str:
        """Build a human-readable string listing which features matched the user's preferences."""
        reasons = []
        if song["genre"] == user_prefs.get("genre"):
            reasons.append(f"genre ({song['genre']})")
        if song["mood"] == user_prefs.get("mood"):
            reasons.append(f"mood ({song['mood']})")
        if abs(song["energy"] - _get("energy", 0.5)) <= 0.15:
            reasons.append(f"energy ({song['energy']:.2f} ≈ target {_get('energy', 0.5):.2f})")
        if abs(song["valence"] - _get("target_valence", 0.5)) <= 0.15:
            reasons.append(f"valence ({song['valence']:.2f} ≈ target {_get('target_valence', 0.5):.2f})")
        if abs(song["danceability"] - _get("target_danceability", 0.5)) <= 0.15:
            reasons.append(f"danceability ({song['danceability']:.2f} ≈ target {_get('target_danceability', 0.5):.2f})")
        if not reasons:
            reasons.append(f"closest overall match (score {score(song):.2f})")
        return "Matched your " + ", ".join(reasons) + "."

    scored = [(song, score(song), explain(song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_knowledge_context(user_query: str) -> str:
    query_lower = user_query.lower()
    
    # Keyword check
    if any(w in query_lower for w in ["coding", "study", "focus", "project"]):
        target_file = "studyjams.txt"
    elif any(w in query_lower for w in ["workout", "gym", "energy"]):
        target_file = "workoutjams.txt"
    else:
        target_file = "feelthefeels.txt"
        
    # Build the absolute path to the knowledge folder at root
    file_path = os.path.join(BASE_DIR, "knowledge", target_file)
    
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        # Debugging tip: print the path if it fails so you can see where it's looking
        return f"Error: Could not find file at {file_path}"
def verify_song_in_library(song_title: str, songs: List[Dict]) -> bool:
    """
    GUARDRAIL STEP:  ensures the AI doesn't hallucinate a song 
    that isn't in CSV.
    """
    # Create a list of all titles in your CSV (lowercased for easy matching)
    valid_titles = [s["title"].lower().strip() for s in songs]
    return song_title.lower().strip() in valid_titles