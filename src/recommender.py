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
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(song: Dict, user_prefs: Dict) -> float:
    """Return a 0.0–7.5 match score: +2.0 genre, +1.0 mood, up to +4.5 numeric similarity."""
    score = 0.0

    # Categorical bonuses
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0

    # Numeric similarity — each term is weight × (1 − absolute difference)
    score += 1.50 * (1 - abs(song["energy"]       - user_prefs["target_energy"]))
    score += 1.00 * (1 - abs(song["danceability"]  - user_prefs["target_danceability"]))
    score += 0.75 * (1 - abs(song["valence"]       - user_prefs["target_valence"]))
    score += 0.75 * (1 - abs(song["acousticness"]  - user_prefs["target_acousticness"]))

    # Normalize tempo to 0–1 before differencing (cap assumed at 200 BPM)
    tempo_norm   = song["tempo_bpm"]              / 200
    target_tempo = user_prefs["target_tempo_bpm"] / 200
    score += 0.50 * (1 - abs(tempo_norm - target_tempo))

    return round(score, 4)


def _build_explanation(song: Dict, user_prefs: Dict) -> str:
    """Build a human-readable reason string listing categorical matches and key numeric targets."""
    parts = []
    if song["genre"] == user_prefs["favorite_genre"]:
        parts.append(f"genre match ({song['genre']})")
    if song["mood"] == user_prefs["favorite_mood"]:
        parts.append(f"mood match ({song['mood']})")
    parts.append(f"energy {song['energy']} vs target {user_prefs['target_energy']}")
    parts.append(f"danceability {song['danceability']} vs target {user_prefs['target_danceability']}")
    return " · ".join(parts)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    # Score every song with a list comprehension — Pythonic single-pass loop
    scored = [
        (song, score_song(song, user_prefs))
        for song in songs
    ]

    # sorted() returns a NEW list sorted by score descending.
    # We use this instead of .sort() to avoid mutating the original songs list.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    # Slice the top k, then attach an explanation string to each result
    return [
        (song, score, _build_explanation(song, user_prefs))
        for song, score in ranked[:k]
    ]
