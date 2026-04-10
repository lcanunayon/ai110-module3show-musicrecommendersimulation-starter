"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Full taste profile — target values used for similarity scoring
    user_prefs = {
        # Categorical preferences (used for bonus matching, not distance math)
        "favorite_genre": "pop",
        "favorite_mood":  "happy",

        # Numeric targets (0.0 – 1.0 scale, used in score_song distance formula)
        "target_energy":       0.85,  # high energy — prefers upbeat, driving songs
        "target_valence":      0.75,  # mostly positive/happy emotional tone
        "target_acousticness": 0.10,  # prefers produced/electronic over acoustic
        "target_danceability": 0.88,  # strong preference for groovy, rhythmic tracks

        # Tempo stored in BPM — normalize to 0–1 inside score_song before scoring
        "target_tempo_bpm":    110,   # mid-to-fast tempo sweet spot
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print(f"  Top {len(recommendations)} Recommendations")
    print(f"  Genre: {user_prefs['favorite_genre']}  |  Mood: {user_prefs['favorite_mood']}")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Score  : {score:.2f} / 7.50")
        print(f"    Genre  : {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Why    : {explanation}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
