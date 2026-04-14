"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

# Max possible score from score_song (genre+mood+energy+acousticness)
MAX_SCORE = 4.5
BAR_WIDTH = 20


def score_bar(score: float) -> str:
    """Return a visual ASCII bar proportional to score out of MAX_SCORE."""
    filled = round((score / MAX_SCORE) * BAR_WIDTH)
    return "[" + "#" * filled + "-" * (BAR_WIDTH - filled) + "]"


def print_recommendations(recommendations, title: str = "Top Recommendations") -> None:
    """Print a ranked list of (song, score, explanation) tuples in a readable layout."""
    width = 60
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"       Score: {score:.2f} / {MAX_SCORE}  {score_bar(score)}")
        print(f"       Why this song:")
        # explanation is a "; "-joined string — split into individual bullet lines
        for reason in explanation.split("; "):
            print(f"         • {reason}")

    print()
    print("=" * width)
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.")

    # Taste profile — target values for each song feature
    user_prefs = {
        "genre":        "lofi",   # preferred genre
        "mood":         "chill",  # preferred mood
        "energy":       0.4,      # low-energy, background listening
        "tempo_bpm":    76,       # slow, relaxed tempo
        "valence":      0.6,      # moderately positive
        "danceability": 0.6,      # somewhat groovy but not club-ready
        "acousticness": 0.75,     # prefers acoustic/organic sound
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
