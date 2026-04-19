import os
from litellm import completion 
from recommender import (
    load_songs, 
    recommend_songs, 
    get_knowledge_context, 
    verify_song_in_library
)

_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

def get_local_reasoning(user_prefs: dict, songs: list) -> str:
    """
    Simulates an AI recommendation by using local RAG logic 
    instead of an external API call.
    """
    # 1. RAG STEP: Get the context from your text files
    query = f"{user_prefs.get('mood')} {user_prefs.get('genre')}"
    context = get_knowledge_context(query)
    
    # 2. MATH STEP: Get the best song from your existing logic
    math_recs = recommend_songs(user_prefs, songs, k=1)
    song_obj = math_recs[0][0]
    
    # 3. GENERATION STEP: Create a "templated" response
    # This mimics what an LLM would do by combining data and context
    explanation = (
        f"Expert Insight: {context.strip()}\n"
        f"Recommendation: Based on your request for a {user_prefs.get('mood')} vibe, "
        f"I suggest '{song_obj['title']}' by {song_obj['artist']}. "
        f"This matches your target energy of {user_prefs.get('energy')}."
    )

    # 4. GUARDRAIL STEP: Still check if the song is valid!
    if verify_song_in_library(song_obj['title'], songs):
        return f"--- Verified Local AI Output ---\n{explanation}"
    else:
        return "Guardrail Triggered: Recommendation not found in library."

def main() -> None:
    songs = load_songs(_CSV_PATH)
    print(f"--- Music Discovery System Initialized ---")
    print(f"Knowledge Base Loaded. {len(songs)} verified tracks in library.")

    # Let's just test one profile for your video walkthrough
    test_profile = {"genre": "lofi", "mood": "focused", "energy": 0.40}
    
    print("\n[User Request]: I'm coding my CS project and need to focus.")
    result = get_local_reasoning(test_profile, songs)
    print("-" * 50)
    print(result)
    print("-" * 50)

if __name__ == "__main__":
    main()