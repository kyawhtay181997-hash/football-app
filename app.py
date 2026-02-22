import streamlit as st
import requests
from groq import Groq
from datetime import datetime

# ၁။ API KEYS (မင်းရဲ့ Key အစစ်တွေ ပြန်ထည့်ပါ)
GROQ_API_KEY = "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"
FOOTBALL_KEY = "5da489c665e54c44a227d7826b02134a"

# Page Settings
st.set_page_config(page_title="AI Smart Advisor V3", page_icon="🎯", layout="centered")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .match-card { background: white; padding: 15px; border-radius: 12px; border-left: 6px solid #007bff; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .time-badge { background: #007bff; color: white; padding: 4px 12px; border-radius: 15px; font-size: 13px; font-weight: bold; }
    .league-label { color: #6c757d; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .tip-box { background: #e9f7ef; color: #1e7e34; padding: 8px; border-radius: 6px; font-weight: bold; margin-top: 8px; border: 1px dashed #28a745; }
    .reason-text { font-size: 13px; color: #495057; margin-top: 5px; }
    </style>
    """, unsafe_content_safe=True)

st.title("🎯 AI Football Smart Advisor")
st.caption("Llama 3.3-70B စွမ်းအင်သုံး ထိပ်သီးလိဂ်များ အထူးခွဲခြမ်းစိတ်ဖြာချက်")

client = Groq(api_key=GROQ_API_KEY)

def get_top_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    try:
        res = requests.get(url, headers=headers).json()
        # Top 5 Leagues: PL, LaLiga, Serie A, Bundesliga, Ligue 1
        top_codes = ['PL', 'PD', 'SA', 'BL1', 'FL1']
        matches = [m for m in res.get('matches', []) if m['competition']['code'] in top_codes]
        return matches
    except: return None

if st.button('🚀 ပွဲစဉ်များအား Analysis လုပ်ရန်'):
    with st.spinner('AI က နောက်ဆုံးရ အချက်အလက်များကို တွက်ချက်နေပါသည်...'):
        matches = get_top_matches()
        if matches:
            # အချိန်အလိုက် ပွဲစဉ်များကို Group ဖွဲ့ခြင်း
            grouped = {}
            for m in matches:
                time = m['utcDate'][11:16] # Extract HH:MM
                if time not in grouped: grouped[time] = []
                grouped[time].append(m)
            
            # Sorted Time Slots
            for time in sorted(grouped.keys()):
                st.markdown(f"<span class='time-badge'>🕓 {time} (UTC)</span>", unsafe_content_safe=True)
                
                for m in grouped[time]:
                    home, away = m['homeTeam']['name'], m['awayTeam']['name']
                    league = m['competition']['name']
                    
                    # AI Reasoning Logic
                    prompt = f"""
                    You are a world-class football betting analyst. 
                    Analyze {home} vs {away} in {league}.
                    Consider: Latest team news, lineups, key injuries, and tactical form.
                    Pick the SINGLE BEST high-probability betting tip from 1xbet markets.
                    
                    Provide response in this exact format:
                    Best Tip: [Market Name] ([Probability %])
                    Reason: [Brief 1-sentence tactical reason in Burmese]
                    """
                    
                    try:
                        completion = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        ai_output = completion.choices[0].message.content
                        lines = ai_output.split('\n')
                        tip = next((l for l in lines if "Best Tip:" in l), "Tip: N/A")
                        reason = next((l for l in lines if "Reason:" in l), "Reason: N/A")

                        # UI Display Card
                        st.markdown(f"""
                        <div class='match-card'>
                            <div class='league-label'>{league}</div>
                            <div style='font-size: 16px; font-weight: bold;'>{home} vs {away}</div>
                            <div class='tip-box'>💎 {tip.replace("Best Tip: ", "")}</div>
                            <div class='reason-text'>💡 {reason.replace("Reason: ", "")}</div>
                        </div>
                        """, unsafe_content_safe=True)
                    except: continue
        else:
            st.warning("ယနေ့အတွက် ထိပ်သီးလိဂ်ပွဲစဉ်များ မရှိသေးပါ။")

st.markdown("---")
st.caption("မှတ်ချက်။ ။ ပွဲမစမီ ၁ နာရီအလိုတွင် ကြည့်ရှုခြင်းသည် အတိကျဆုံး ခန့်မှန်းချက်ကို ရရှိစေပါသည်။")
