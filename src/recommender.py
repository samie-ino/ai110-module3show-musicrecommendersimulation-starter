import csv
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


def score_song_oop(song: Song, user: UserProfile) -> Tuple[float, List[str]]:
    """
    Scoring recipe:
      +2.0  genre match      (broadest preference — highest weight)
      +1.0  mood match       (contextual preference)
      +0.0–1.0  energy similarity  (1.0 - |song.energy - target_energy|)
      +0.5  acousticness bonus  (if user.likes_acoustic and song is acoustic,
                                 or user dislikes acoustic and song is not)
    Max possible score: 4.5
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song.genre == user.favorite_genre:
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match: +1.0
    if song.mood == user.favorite_mood:
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Energy similarity: +0.0 to +1.0
    # Formula: 1.0 - |song.energy - target_energy|
    energy_diff = abs(song.energy - user.target_energy)
    energy_points = round(1.0 - energy_diff, 3)
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f}) (song={song.energy:.2f}, target={user.target_energy:.2f})")

    # Acousticness preference: +0.5
    is_acoustic = song.acousticness >= 0.6
    if user.likes_acoustic and is_acoustic:
        score += 0.5
        reasons.append(f"acoustic match (+0.5) (acousticness={song.acousticness:.2f})")
    elif not user.likes_acoustic and not is_acoustic:
        score += 0.5
        reasons.append(f"non-acoustic match (+0.5) (acousticness={song.acousticness:.2f})")

    return round(score, 3), reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user profile."""
        scored = [(song, score_song_oop(song, user)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended to a user."""
        _, reasons = score_song_oop(song, user)
        if not reasons:
            return f"'{song.title}' is a general match for your taste."
        return f"'{song.title}' recommended because: " + "; ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
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


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song against a user preference dictionary.

    Algorithm Recipe (max 4.5 points):
      +2.0        genre match      — exact match only, no partial credit
      +1.0        mood match       — exact match only, no partial credit
      +0.0–1.0    energy similarity — 1.0 − |song.energy − target_energy|
      +0.5        acousticness     — bonus when song's acoustic character
                                     matches the user's preference
                                     (threshold: acousticness ≥ 0.6)

    Returns:
        (score, reasons) where reasons is a list of human-readable strings
        that explain each point contribution, e.g. "genre match (+2.0)".
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match: +1.0
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Energy similarity: +0.0 to +1.0
    # Formula: 1.0 - |song.energy - target_energy|
    target_energy = user_prefs.get("energy", 0.5)
    energy_diff = abs(song["energy"] - target_energy)
    energy_points = round(1.0 - energy_diff, 3)
    score += energy_points
    reasons.append(
        f"energy similarity (+{energy_points:.2f}) "
        f"(song={song['energy']:.2f}, target={target_energy:.2f})"
    )

    # Acousticness preference: +0.5
    target_acousticness = user_prefs.get("acousticness", 0.5)
    likes_acoustic = target_acousticness >= 0.6
    is_acoustic = song["acousticness"] >= 0.6
    if likes_acoustic and is_acoustic:
        score += 0.5
        reasons.append(f"acoustic match (+0.5) (acousticness={song['acousticness']:.2f})")
    elif not likes_acoustic and not is_acoustic:
        score += 0.5
        reasons.append(f"non-acoustic match (+0.5) (acousticness={song['acousticness']:.2f})")

    return round(score, 3), reasons


def _score_song_dict(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    """Thin wrapper kept for internal backwards-compatibility; delegates to score_song."""
    return score_song(user_prefs, song)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Returns: list of (song_dict, score, explanation) tuples, sorted by score descending.

    Pythonic approach:
    - List comprehension scores every song in one expression (no manual append loop)
    - score_song is called once per song and acts as the ranking "judge"
    - sorted() returns a NEW ranked list without mutating the original songs list
      (contrast with .sort(), which sorts in-place and returns None)
    - [:k] slices off the top-k results after sorting
    """
    scored = [
        (song, score, "; ".join(reasons) if reasons else "general match")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]   # unpack once per song
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
