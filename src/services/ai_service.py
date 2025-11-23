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

    def analyze_matchup(self, p1_name, p1_data, p1_moves, p1_item, p1_stats, p1_nature, p2_name, p2_data, p2_moves, p2_item, p2_stats, p2_nature):
        """
        Analyze battle matchup between two Pokemon with Moves, Items, and Real Stats
        """
        # Helper to format stats
        def format_stats(data, moves, item, real_stats, nature):
            types = [t['type']['name'] for t in data.get('types', [])]
            abilities = [a['ability']['name'] for a in data.get('abilities', [])]
            
            moves_str = ", ".join(moves) if moves else "Standard Competitive Set (AI Prediction)"
            item_str = item if item and item != "None" else "Standard Competitive Item (AI Prediction)"
            
            return f"""
            Types: {', '.join(types)}
            Abilities: {', '.join(abilities)}
            Base Stats: HP={data['stats'][0]['base_stat']}, Atk={data['stats'][1]['base_stat']}, Def={data['stats'][2]['base_stat']}, ...
            REAL STATS (Lv 50): HP={real_stats.get('hp')}, Atk={real_stats.get('attack')}, Def={real_stats.get('defense')}, 
                                SpA={real_stats.get('special-attack')}, SpD={real_stats.get('special-defense')}, Spd={real_stats.get('speed')}
            Nature: {nature}
            Held Item: {item_str}
            Moveset: {moves_str}
            """

        context = f"""
        POKEMON 1 (USER): {p1_name.upper()}
        {format_stats(p1_data, p1_moves, p1_item, p1_stats, p1_nature)}

        POKEMON 2 (OPPONENT): {p2_name.upper()}
        {format_stats(p2_data, p2_moves, p2_item, p2_stats, p2_nature)}
        """

        system_prompt = f"""You are a world-class Competitive Pokemon VGC/Smogon Analyst.
        Analyze the matchup between {p1_name} and {p2_name} in extreme detail.
        
        CRITICAL: Use the provided REAL STATS (at Level 50) for all calculations, NOT the Base Stats.
        Consider the Moves, Items, and Nature provided.
        
        DATA:
        {context}
        
        OUTPUT FORMAT (Use Markdown):
        
        ### 1. 📊 Matchup Overview
        Briefly describe the dynamic. Mention how the **Nature/EVs** and **Items** affect the matchup.
        
        ### 2. ⚡ Speed & Turn Order
        - Who moves first? (Compare REAL Speed stats: {p1_stats.get('speed')} vs {p2_stats.get('speed')}).
        - Does the Item (e.g. Choice Scarf) change this?
        
        ### 3. 🛡️ Type Interaction
        - Analyze Weaknesses/Resistances.
        
        ### 4. ⚔️ Damage Potential
        - Analyze the specific moves provided.
        - Can {p1_name} OHKO {p2_name} given the Real Attack/SpA vs Real Def/SpD?
        
        ### 5. 🧠 Strategy for {p1_name} (User)
        - How to use the selected moveset effectively.
        - Win Condition based on the current loadout.
        
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
