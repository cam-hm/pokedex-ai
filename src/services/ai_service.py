"""
AI Service - Pokemon Chatbot
Powered by Groq API (Fast & Free)
"""
import streamlit as st
from groq import Groq


class PokemonChatbot:
    """AI-powered Pokemon assistant using Groq"""
    
    def __init__(self):
        """Initialize Groq client with API key from secrets"""
        self.client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    def chat(self, pokemon_name, pokemon_data, user_message, chat_history=[]):
        """
        Chat about a Pokemon with AI context
        
        Args:
            pokemon_name (str): Name of current Pokemon
            pokemon_data (dict): Full Pokemon data from API
            user_message (str): User's question
            chat_history (list): Previous conversation messages
            
        Returns:
            str: AI response
        """
        # Build Pokemon context
        types = [t['type']['name'] for t in pokemon_data.get('types', [])]
        abilities = [a['ability']['name'] for a in pokemon_data.get('abilities', [])]
        stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data.get('stats', [])}
        
        context = f"""
Pokemon: {pokemon_name.title()}
Types: {', '.join(types)}
Abilities: {', '.join(abilities)}
Base Stats: HP={stats.get('hp')}, Atk={stats.get('attack')}, Def={stats.get('defense')}, 
           SpA={stats.get('special-attack')}, SpD={stats.get('special-defense')}, Spd={stats.get('speed')}
Height: {pokemon_data.get('height', 0)/10}m
Weight: {pokemon_data.get('weight', 0)/10}kg
"""
        
        # Build conversation messages
        messages = [
            {
                "role": "system",
                "content": f"""You are an expert Pokemon assistant helping users understand Pokemon.

Current Pokemon data:
{context}

Guidelines:
- Be friendly, concise, and use emojis where appropriate
- Answer based on Pokemon data provided and general Pokemon knowledge
- If asked about battles, suggest strategies based on types and stats
- For evolution questions, provide helpful evolution tips
- Keep responses under 150 words unless specifically asked for detailed explanation
- Use bullet points for lists"""
            }
        ]
        
        # Add chat history (last 4 messages for context)
        for msg in chat_history[-8:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response with Groq
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Latest stable model (Dec 2024)
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "authentication" in error_msg.lower():
                return f"⚠️ AI service authentication failed. Please check the Groq API key in settings."
            return f"Sorry, I encountered an error: {error_msg}. Please try again!"

    def analyze_matchup(self, p1_name, p1_data, p2_name, p2_data):
        """
        Analyze battle matchup between two Pokemon
        """
        # Helper to format stats
        def format_stats(data):
            stats = {s['stat']['name']: s['base_stat'] for s in data.get('stats', [])}
            types = [t['type']['name'] for t in data.get('types', [])]
            abilities = [a['ability']['name'] for a in data.get('abilities', [])]
            return f"""
            Types: {', '.join(types)}
            Abilities: {', '.join(abilities)}
            Stats: HP={stats.get('hp')}, Atk={stats.get('attack')}, Def={stats.get('defense')}, 
                   SpA={stats.get('special-attack')}, SpD={stats.get('special-defense')}, Spd={stats.get('speed')}
            """

        context = f"""
        POKEMON 1 (USER): {p1_name.upper()}
        {format_stats(p1_data)}

        POKEMON 2 (OPPONENT): {p2_name.upper()}
        {format_stats(p2_data)}
        """

        system_prompt = f"""You are a world-class Competitive Pokemon VGC/Smogon Analyst.
        Analyze the matchup between {p1_name} and {p2_name} in extreme detail.
        
        DATA:
        {context}
        
        OUTPUT FORMAT (Use Markdown):
        
        ### 1. 📊 Matchup Overview
        Briefly describe the dynamic (e.g., "Glass Cannon vs Wall", "Speed Tie", "Type Mismatch").
        
        ### 2. ⚡ Speed & Turn Order
        - Who moves first? (Compare Speed stats).
        - Does the slower Pokemon need a **Choice Scarf** or **Tailwind** to outspeed?
        
        ### 3. 🛡️ Type Interaction
        - Analyze Weaknesses/Resistances.
        - Mention any 4x weaknesses or Immunities.
        
        ### 4. ⚔️ Damage Potential (Hypothetical)
        - Can {p1_name} **OHKO** (One-Hit KO) {p2_name}?
        - Is {p2_name} bulky enough to survive and counter-attack?
        - Which stat should {p1_name} target (Defense or Sp. Def)?
        
        ### 5. 🧠 Strategy for {p1_name} (User)
        - **Recommended Moves:** List 2-3 best moves to use.
        - **Ideal Held Item:** Suggest an item (e.g., Focus Sash, Life Orb, Leftovers).
        - **Win Condition:** What needs to happen for {p1_name} to win?
        
        ### 6. 🔮 Final Verdict
        - **Winning Probability:** {p1_name}'s win chance %.
        - **Winner Prediction:** Who wins 1v1?
        
        Keep the tone professional but engaging. Use bolding for key terms."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}],
                temperature=0.5,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error analyzing matchup: {str(e)}"
