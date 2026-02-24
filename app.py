import streamlit as st
import google.generativeai as genai
import requests

# --- SETUP ---
GEMINI_API_KEY = "AIzaSyA4-9LZdhqavOcjmJ2W0yDAVJNNOoFsICQ"
FOOTBALL_KEY = "5da489c665e54c44a227d7826b02134a "

genai.configure(api_key=GEMINI_API_KEY)

# Google Search Tool ကို Gemini ထဲ ထည့်သွင်းခြင်း (ဒါက အဓိက အသက်ပါ)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=[{"google_search_retrieval": {}}] 
)

st.set_page_config(page_title="One-Click AI Pro", layout="wide")
st.title("⚡ One-Click Football Expert")
st.caption("ခလုတ်နှိပ်ရုံဖြင့် Gemini မှ Google တွင် ရှာဖွေပြီး အပိုင်ပွဲများကို တွက်ချက်ပေးမည်။")

# ပွဲစဉ်ဒေတာယူရန်
def get_today_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    res = requests.get(url, headers=headers).json()
    return res.get('matches', [])

if st.button('🚀 ပွဲစဉ်အားလုံးကို AI ဖြင့် ခြုံငုံသုံးသပ်ရန်'):
    matches = get_today_matches()
    
    for m in matches:
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        league = m['competition']['name']
        
        with st.container():
            st.subheader(f"🏟️ {home} vs {away} ({league})")
            
            # ငါ့ဆီမှာ မေးသလိုမျိုး မေးခွန်းကို AI ဆီ တန်းပို့လိုက်ခြင်း
            prompt = f"""
            Search Google for the following for {home} vs {away} on today's date:
            1. Official Lineups and key injuries.
            2. Market sentiment (Betting volume %).
            3. Tactical analysis (How they will play).
            4. Final Verdict: Give a high-confidence tip with logic.
            Answer in Burmese, be very concise and direct for someone with no time.
            """
            
            try:
                # Gemini က Google မှာ ကိုယ်တိုင်ရှာပြီး အဖြေထုတ်ပေးမည်
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.divider()
            except Exception as e:
                st.error(f"Error analyzing {home}: {e}")
