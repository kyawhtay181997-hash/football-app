import streamlit as st
import requests
from groq import Groq

# ၁။ API KEYS (မင်းရဲ့ Key အစစ်တွေ ဒီမှာ ပြန်ထည့်ပါ)
GROQ_API_KEY = "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"
FOOTBALL_KEY = "5da489c665e54c44a227d7826b02134a"

st.set_page_config(page_title="AI Smart Advisor V3", page_icon="🎯")

# UI အလှဆင်ခြင်း
st.markdown("""
    <style>
    .match-card { background: white; padding: 15px; border-radius: 12px; border-left: 6px solid #007bff; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .tip-box { background: #e9f7ef; color: #1e7e34; padding: 8px; border-radius: 6px; font-weight: bold; margin-top: 5px; }
    .percent { color: #d9534f; font-weight: bold; }
    </style>
    """, unsafe_content_safe=True)

st.title("🎯 AI Football Smart Advisor (V3)")

client = Groq(api_key=GROQ_API_KEY)

def get_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    try:
        res = requests.get(url, headers=headers).json()
        top_codes = ['PL', 'PD', 'SA', 'BL1', 'FL1'] # ထိပ်သီး ၅ လိဂ်
        return [m for m in res.get('matches', []) if m['competition']['code'] in top_codes]
    except: return None

if st.button('🚀 Analysis စတင်ရန်'):
    with st.spinner('AI က % များနှင့် တိကျသော Tips များကို တွက်ချက်နေသည်...'):
        matches = get_matches()
        if matches:
            for m in matches:
                home, away = m['homeTeam']['name'], m['awayTeam']['name']
                league = m['competition']['name']
                time = m['utcDate'][11:16]

                # AI ကို % ပါအောင် အတင်းအကျပ် ခိုင်းစေခြင်း
                prompt = f"""
                Analyze {home} vs {away} ({league}). 
                Give me ONLY ONE best betting tip with its probability percentage (%).
                Format: Tip: [Market] | Probability: [%] | Reason: [Short Burmese Reason]
                """
                
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    res_text = completion.choices[0].message.content
                    
                    # ကတ်ပြားပုံစံဖြင့် ပြသခြင်း
                    st.markdown(f"""
                    <div class='match-card'>
                        <small>{league} | 🕓 {time} UTC</small><br>
                        <b>{home} vs {away}</b><br>
                        <div class='tip-box'>💎 {res_text}</div>
                    </div>
                    """, unsafe_content_safe=True)
                except: continue
        else:
            st.warning("ယနေ့အတွက် ထိပ်သီးလိဂ်ပွဲစဉ်များ မရှိသေးပါ။")
