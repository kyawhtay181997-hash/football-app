import streamlit as st
import requests
from groq import Groq
import pandas as pd

# ၁။ API KEYS
GROQ_API_KEY = "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"
FOOTBALL_KEY = "5da489c665e54c44a227d7826b02134a"

st.set_page_config(page_title="AI Football Advisor V3", layout="wide")

st.title("⚽ AI Football Smart Advisor (V3)")

client = Groq(api_key=GROQ_API_KEY)

def get_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    try:
        res = requests.get(url, headers=headers).json()
        top_codes = ['PL', 'PD', 'SA', 'BL1', 'FL1']
        return [m for m in res.get('matches', []) if m['competition']['code'] in top_codes]
    except: return None

if st.button('🚀 Analysis စတင်ရန်'):
    with st.spinner('AI က ပွဲစဉ်များကို ခွဲခြားတွက်ချက်နေပါသည်...'):
        matches = get_matches()
        if matches:
            # အချိန်အလိုက် ပွဲများကို ခွဲထုတ်ခြင်း
            # ပထမ ၅ ပွဲကို AI Analysis လုပ်ပြီး အပေါ်ဇယားမှာ ပြမယ်
            analyzed_data = []
            upcoming_data = []
            
            for i, m in enumerate(matches):
                home, away = m['homeTeam']['name'], m['awayTeam']['name']
                league = m['competition']['name']
                time = m['utcDate'][11:16]
                
                if i < 5: # ထိပ်ဆုံး ၅ ပွဲကို AI နဲ့ စစ်မယ်
                    prompt = f"Analyze {home} vs {away} ({league}). Give ONLY one best tip with % and 1-sentence Burmese reason. Format: [Tip] ([%]) | [Reason]"
                    try:
                        completion = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        ai_res = completion.choices[0].message.content
                        analyzed_data.append([time, league, f"{home} vs {away}", ai_res])
                    except: analyzed_data.append([time, league, f"{home} vs {away}", "AI Error"])
                else: # ကျန်တဲ့ပွဲတွေကို အောက်ဇယားမှာပြမယ်
                    upcoming_data.append([time, league, f"{home} vs {away}"])

            # --- အပေါ်ဇယား (AI Confirmed Tips) ---
            st.subheader("💎 AI အပိုင်တွက်ချက်ထားသော ပွဲစဉ်များ")
            df1 = pd.DataFrame(analyzed_data, columns=['အချိန် (UTC)', 'လိဂ်', 'ပွဲစဉ်', 'AI ခန့်မှန်းချက် နှင့် အကြောင်းပြချက်'])
            st.table(df1) # st.table က ဖုန်းမှာ ဇယားကွက်အပြည့် မြင်ရစေတယ်

            st.markdown("---")

            # --- အောက်ဇယား (Other Upcoming Matches) ---
            st.subheader("📅 နောက်ထပ် ကစားမည့် ပွဲစဉ်များ")
            if upcoming_data:
                df2 = pd.DataFrame(upcoming_data, columns=['အချိန် (UTC)', 'လိဂ်', 'ပွဲစဉ်'])
                st.dataframe(df2, use_container_width=True)
            else:
                st.write("နောက်ထပ် ပွဲစဉ်များ မရှိသေးပါ။")
        else:
            st.warning("ယနေ့အတွက် ထိပ်သီးလိဂ်ပွဲစဉ်များ မရှိသေးပါ။")
