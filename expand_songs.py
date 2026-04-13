import anthropic

client = anthropic.Anthropic()

prompt = """Generate 8 additional songs in CSV format to extend a music dataset.
Use ONLY the data rows (no headers, no markdown, no extra text).
The columns are: id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness

Rules:
- id starts at 11 and increments
- energy, valence, danceability, acousticness are floats between 0.0 and 1.0
- tempo_bpm is an integer
- Include diverse genres NOT in this list: pop, lofi, rock, ambient, jazz, synthwave, indie pop
- Include diverse moods NOT in this list: happy, chill, intense, relaxed, moody, focused
- Aim for genres like: classical, hip-hop, metal, reggae, country, r&b, electronic, folk, blues
- Aim for moods like: melancholic, energetic, romantic, angry, peaceful, nostalgic, uplifting"""

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

new_rows = response.content[0].text.strip()
print("Generated rows:\n", new_rows)

with open("data/songs.csv", "a") as f:
    f.write("\n" + new_rows + "\n")

print("\nSuccessfully appended to data/songs.csv")
