Music Discovery System: A Knowledge-Infused Recommender
1. Original Scope (Project 3)
My original project was a Music Recommender Simulation built during Module 3. Its primary goal was to use deterministic math—specifically weighted similarity scores—to recommend songs from a local CSV file based on a user's preferred genre, mood, and energy levels. While functional, it lacked the ability to explain why a song was a good fit beyond raw data points.

2. Project Summary
This evolved Applied AI System transforms the original "math-only" script into a Local Retrieval-Augmented Expert System. By integrating a custom knowledge base, the system now provides human-like "Expert Insights" alongside recommendations. It matters because it bridges the gap between cold data (BPM, valence) and real-world context (coding focus, workout motivation), making the AI a more helpful collaborator for the user.

3. Architecture Overview
The system follows a modular architecture designed for reliability and speed:

Knowledge Base: A collection of domain-specific text files (.txt) containing musicology insights.

Keyword Retriever: A logic layer that "retrieves" relevant context by matching user intent to the knowledge base.

Reasoning Engine: A local processor that synthesizes song data and retrieved context into a readable output.

Reliability Guardrail: A verification loop that cross-references all outputs against the verified songs.csv to prevent "hallucinations" or invalid suggestions.

4. Setup Instructions
To run this system locally, follow these steps:

Clone the Repository:

Bash
git clone https://github.com/your-username/applied-ai-system-project.git
cd applied-ai-system-project
Environment Setup: Ensure you have Python 3.x installed. No external heavy LLM libraries are required for the local version.

Run the System:

Bash
python src/main.py
5. Sample Interactions
Example 1: The "Deep Work" Request
User Input: "I'm coding my CS project and need to focus."
Expert Insight: Midnight Coding by LoRoom – This lofi song is perfect for studying because its chill and focused vibe helps maintain concentration and reduces distractions.
Recommendation: 'Focus Flow' by LoRoom (Energy: 0.4).

Example 2: The "Hype" Request
User Input: "I'm heading to the gym and need high energy."
Expert Insight: High-energy tracks with 120+ BPM are scientifically proven to increase motivation and maintain workout pacing.
Recommendation: 'Gym Hero' by Max Pulse (Energy: 0.93).

6. Design Decisions & Trade-offs
Local vs. Cloud AI: I chose to build a Local Reasoning Engine instead of using a Cloud API (like OpenAI).

Trade-off: While I lost the "natural" conversational flair of a massive LLM, I gained 100% reliability, zero latency, and improved privacy.

Keyword-Based Retrieval: I implemented a simple keyword-matching RAG.

Trade-off: It is less flexible than vector-based search but extremely efficient for small, curated datasets like my 15-song library.

7. Testing Summary
What Worked: The path-handling logic successfully connects the src scripts to the root knowledge folder, ensuring context is always retrieved.

What Didn't: Initially, the system would default to "general musicology" if a keyword wasn't an exact match. I improved this by adding more flexible keyword arrays.

The Guardrail: I tested the system by forcing a "fake" song title; the Verification Guardrail successfully caught the error and prevented the system from displaying invalid data.

10 out of 11 test profiles passed successfully. The system maintained 100% accuracy in song selection due to the verification guardrail. The single "failure" occurred during the "Ghost Genre" test, where the RAG system correctly identified the lack of context and provided a safe, generalized musicology fallback rather than making up data.

8. Reflection
Building this system taught me that "AI" doesn't always have to be a massive, expensive black box. By combining Deterministic Logic (my original math) with Contextual Knowledge (my new RAG feature), I created a tool that feels much smarter than its codebase suggests. It reinforced the importance of Responsible AI—specifically, that a system is only as good as the guardrails that keep it grounded in truth.