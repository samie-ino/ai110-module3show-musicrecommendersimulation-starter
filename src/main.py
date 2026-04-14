"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

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

    # ------------------------------------------------------------------ #
    # Profile 1 — High-Energy Pop                                         #
    # A workout listener who wants loud, fast, non-acoustic pop music.    #
    # ------------------------------------------------------------------ #
    high_energy_pop = {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.90,
        "tempo_bpm":    130,
        "valence":      0.85,
        "danceability": 0.88,
        "acousticness": 0.10,   # strongly prefers produced/electronic sound
    }

    # ------------------------------------------------------------------ #
    # Profile 2 — Chill Lofi                                              #
    # A late-night study session listener who wants slow, acoustic beats. #
    # ------------------------------------------------------------------ #
    chill_lofi = {
        "genre":        "lofi",
        "mood":         "chill",
        "energy":       0.40,
        "tempo_bpm":    76,
        "valence":      0.60,
        "danceability": 0.60,
        "acousticness": 0.75,   # prefers acoustic/organic sound
    }

    # ------------------------------------------------------------------ #
    # Profile 3 — Deep Intense Rock                                       #
    # A headbanger who wants high-energy, aggressive, electric guitar.    #
    # ------------------------------------------------------------------ #
    deep_intense_rock = {
        "genre":        "rock",
        "mood":         "intense",
        "energy":       0.92,
        "tempo_bpm":    155,
        "valence":      0.45,
        "danceability": 0.65,
        "acousticness": 0.08,   # strongly prefers electric/distorted sound
    }

    # ------------------------------------------------------------------ #
    # ADVERSARIAL / EDGE CASE PROFILES                                    #
    # Designed to expose unexpected scoring behaviour.                    #
    # ------------------------------------------------------------------ #

    # Edge Case A — Conflicting Energy vs. Mood                           #
    # energy=0.9 screams "club banger" but mood=sad points to low-energy  #
    # ballads. The scoring function scores energy numerically but treats  #
    # mood as an exact string match — so this user will get high-energy   #
    # songs even though "sad" implies something slow.                     #
    conflicting_energy_sad = {
        "genre":        "pop",
        "mood":         "sad",          # no song in catalog has mood="sad"
        "energy":       0.90,           # wants high energy
        "tempo_bpm":    130,
        "valence":      0.20,           # low valence (dark/sad feeling)
        "danceability": 0.70,
        "acousticness": 0.15,
    }

    # Edge Case B — Genre Not In Catalog                                  #
    # The user wants "jazz-pop" which doesn't exist. Genre bonus never    #
    # fires, so every song starts from 0. Ranking falls back entirely on  #
    # mood+energy+acousticness — the weakest signals.                     #
    missing_genre = {
        "genre":        "jazz-pop",     # not in catalog
        "mood":         "happy",
        "energy":       0.65,
        "tempo_bpm":    110,
        "valence":      0.80,
        "danceability": 0.75,
        "acousticness": 0.40,
    }

    # Edge Case C — Perfectly Neutral (all mid-range values)              #
    # No strong signal in any dimension. Every song is roughly equal.     #
    # The tie-breaking falls to tiny energy differences — top 5 could     #
    # feel random or arbitrary to the listener.                           #
    perfectly_neutral = {
        "genre":        "ambient",      # only 1 ambient song in catalog
        "mood":         "chill",
        "energy":       0.50,           # dead-center energy target
        "tempo_bpm":    90,
        "valence":      0.50,
        "danceability": 0.50,
        "acousticness": 0.50,           # right on the acoustic threshold (0.6)
    }

    # ------------------------------------------------------------------ #
    # Run all profiles                                                     #
    # ------------------------------------------------------------------ #
    profiles = [
        (high_energy_pop,         "Profile 1 — High-Energy Pop"),
        (chill_lofi,              "Profile 2 — Chill Lofi"),
        (deep_intense_rock,       "Profile 3 — Deep Intense Rock"),
        (conflicting_energy_sad,  "Edge Case A — Conflicting Energy vs. Sad Mood"),
        (missing_genre,           "Edge Case B — Genre Not In Catalog (jazz-pop)"),
        (perfectly_neutral,       "Edge Case C — Perfectly Neutral / All Mid-Range"),
    ]

    for prefs, title in profiles:
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(recommendations, title=title)


if __name__ == "__main__":
    main()
