# Data Flow: Music Recommender Simulation

This diagram traces the path of a single song from the CSV catalog through the
scoring loop to its place in the final ranked output.

```mermaid
---
id: 4980b655-68a4-4eb9-b04c-36839ac4d8b2
---
flowchart TD
    A[/"data/songs.csv"/] -->|"load_songs()"| B["List of 18 Song Dicts"]
    C[/"User Preferences\ngenre · mood · energy · acousticness"/] --> F

    B --> E["For Each Song in List"]
    E --> F["score = 0.0\nreasons = []"]

    F --> G{"song.genre ==\nuser genre?"}
    G -->|"Yes — +2.0"| H["score += 2.0\nadd 'genre match'"]
    G -->|"No"| I["no change"]
    H --> J{"song.mood ==\nuser mood?"}
    I --> J

    J -->|"Yes — +1.0"| K["score += 1.0\nadd 'mood match'"]
    J -->|"No"| L["no change"]
    K --> M["energy_pts = 1.0 − |song.energy − target|\nscore += energy_pts  (0.0 – 1.0)\nadd 'energy similarity'"]
    L --> M

    M --> N{"acousticness\npreference aligns?"}
    N -->|"Yes — +0.5"| O["score += 0.5\nadd 'acoustic match'"]
    N -->|"No"| P["no change"]
    O --> Q["Append\n(song, score, explanation)"]
    P --> Q

    Q --> R{"More songs\nin list?"}
    R -->|"Yes"| E
    R -->|"No — loop complete"| S["Sort all results\nby score descending"]
    S --> T[/"Top K Results\n song · score · explanation"/]
```

## Scoring weights at a glance

| Step | Signal | Points |
|------|--------|--------|
| 1 | Genre exact match | +2.0 |
| 2 | Mood exact match | +1.0 |
| 3 | Energy closeness | +0.0 – 1.0 |
| 4 | Acousticness preference | +0.5 |
| | **Max possible score** | **4.5** |

## How a single song moves through the system

1. `load_songs("data/songs.csv")` reads the file into a plain Python list of dicts.
2. `recommend_songs(user_prefs, songs, k)` iterates over every song.
3. Each song enters `_score_song_dict()`, collecting points at each of the four
   scoring steps; each step also appends a human-readable reason string.
4. The `(song, score, explanation)` tuple is stored in a results list.
5. After the loop, results are sorted by `score` descending.
6. The top `k` tuples are returned and printed by `main.py`.
