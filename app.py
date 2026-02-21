import streamlit as st
import requests
from groq import Groq

# ၁။ UI ပိုင်း ပြင်ဆင်ခြင်း
st.set_page_config(page_title="AI Football Predictor", page_icon="⚽")
st.title("⚽ နေ့စဉ် ဘောလုံးပွဲ ခန့်မှန်းချက်")
st.write("AI က ဒီနေ့ပွဲစဉ်တွေကို ခွဲခြမ်းစိတ်ဖြာပေးပါလိမ့်မယ်။")

# ၂။ API Keys များ (မင်းရဲ့ Key တွေ ဒီမှာ ထည့်ပါ)
GROQ_API_KEY = "မင်းရဲ့_Groq_API_Key"
FOOTBALL_KEY = "မင်းရဲ့_Football_Data_Key"

client = Groq(api_key=GROQ_API_KEY)

def get_cleaned_data():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    try:
        response = requests.get(url, headers=headers).json()
        cleaned_matches = []
        for match in response.get('matches', []):
            match_info = {
                "homeTeam": match['homeTeam']['name'],
                "awayTeam": match['awayTeam']['name'],
                "competition": match['competition']['name']
            }
            cleaned_matches.append(match_info)
        return cleaned_matches
    except:
        return None

# ၃။ ခန့်မှန်းချက်ခလုတ်
if st.button('ဒီနေ့အတွက် ခန့်မှန်းချက်ထုတ်ရန်'):
    with st.spinner('AI က တွက်ချက်နေပါတယ်...'):
        matches = get_cleaned_data()
        if matches:
            matches_text = "\n".join([f"{m['homeTeam']} vs {m['awayTeam']} ({m['competition']})" for m in matches])
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "မင်းက ဘောလုံးကျွမ်းကျင်သူပါ။"},
                        {"role": "user", "content": f"ဒီနေ့ပွဲတွေထဲက နိုင်ခြေအရှိဆုံး ၅ ပွဲကို ရွေးပေးပါ။ မြန်မာလိုရှင်းပြပါ။\n\nMatches:\n{matches_text}"}
                    ]
                )
                st.success("ခန့်မှန်းချက် ထွက်လာပါပြီ!")
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Data ယူလို့ မရနိုင်သေးပါ။")
