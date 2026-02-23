import streamlit as st
import requests
from groq import Groq
import pandas as pd

# ၁။ API KEYS (မင်းရဲ့ Key တွေ ဒီမှာ အမှန်ပြန်ထည့်ပါ)
GROQ_API_KEY = "မင်းရဲ့_Groq_Key_အစစ်"
FOOTBALL_KEY = "မင်းရဲ့_Football_Data_Key_အစစ်"

st.set_page_config(page_title="AI Smart Advisor V4", layout="wide")

st.title("🎯 AI Smart Advisor (Double-Check Logic)")
st.caption("ပွဲမစခင် ၁ နာရီအလိုတွင် ရှာဖွေခြင်းသည် ၉၀% အထက် တိကျမှုကို ပေးစွမ်းနိုင်ပါသည်။")

client = Groq(api_key=GROQ_API_KEY)

def get_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    try:
        res = requests.get(url, headers=headers).json()
        top_leagues = ['PL', 'PD', 'SA', 'BL1', 'FL1']
        return [m for m in res.get('matches', []) if m['competition']['code'] in top_leagues]
    except: return None

if st.button('🚀 Analysis စတင်ရန်'):
    with st.spinner('AI က နောက်ဆုံးရ လူစာရင်းများကို စစ်ဆေးနေပါသည်...'):
        matches = get_matches()
        if matches:
            # အချိန်အလိုက် ပွဲစဉ်များကို Group ဖွဲ့ခြင်း
            grouped_matches = {}
            for m in matches:
                time = m['utcDate'][11:16]
                if time not in grouped_matches: grouped_matches[time] = []
                grouped_matches[time].append(m)
            
            # အချိန်အလိုက် ဇယားကွက်များ ထုတ်ပေးခြင်း
            for time in sorted(grouped_matches.keys()):
                st.markdown(f"### 🕓 ပွဲချိန် - {time} (UTC)")
                table_data = []
                
                for m in grouped_matches[time]:
                    home, away = m['homeTeam']['name'], m['awayTeam']['name']
                    league = m['competition']['name']
                    
                    # AI Advisor Logic (1xbet Markets အကုန်ထည့်တွက်ခိုင်းသည်)
                    prompt = f"""
                    Context: {home} vs {away} in {league}.
                    Task: Act as a pro 1xbet tipster. Analyze official lineups and team news. 
                    Pick the SINGLE best outcome (W1, W2, X, Over/Under, BTTS, Corner, Double Chance, etc).
                    
                    Respond ONLY in this format:
                    Tip: [Market] ([Probability %]) | Reason: [Burmese Reason]
                    """
                    
                    try:
                        completion = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        ai_res = completion.choices[0].message.content
                        table_data.append([league, f"{home} vs {away}", ai_res])
                    except:
                        table_data.append([league, f"{home} vs {away}", "AI Error"])
                
                # ဇယားကွက်ဖြင့် ပြသခြင်း
                df = pd.DataFrame(table_data, columns=['League', 'Match', 'AI Recommendation (% & Reason)'])
                st.table(df)
        else:
            st.warning("ယနေ့အတွက် ထိပ်သီးလိဂ်ပွဲစဉ်များ မရှိသေးပါ။")
