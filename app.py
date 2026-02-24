import streamlit as st
import google.generativeai as genai
import requests

# --- CONFIGURATION ---
# မင်းရဲ့ API Keys များ
GEMINI_API_KEY = "AIzaSyA4-9LZdhqavOcjmJ2W0yDAVJNNOoFsICQ"
FOOTBALL_KEY = "85888e2858904e578f14f40f0c058c4f"

genai.configure(api_key=GEMINI_API_KEY)

# Screenshot ထဲက Error ကို ဖြေရှင်းရန် model_name ကို 'models/' ထည့်ထားသည်
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash', 
    tools=[{"google_search_retrieval": {}}] 
)

st.set_page_config(page_title="AI Expert (One-Click)", layout="wide")
st.title("⚡ One-Click Football Expert")
st.info("ခလုတ်နှိပ်ရုံဖြင့် Gemini မှ Google တွင် ရှာဖွေပြီး အပိုင်ပွဲများကို ခြုံငုံသုံးသပ်ပေးမည်။")

# ပွဲစဉ်ဒေတာယူရန် Function
def get_today_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    try:
        res = requests.get(url, headers=headers).json()
        return res.get('matches', [])
    except:
        return []

# ခလုတ်နှိပ်သည့်အခါ အလုပ်လုပ်မည့်အပိုင်း
if st.button('🚀 ပွဲစဉ်အားလုံးကို AI ဖြင့် အပိုင်တွက်ချက်ရန်'):
    matches = get_today_matches()
    
    if not matches:
        st.warning("ယနေ့အတွက် ပွဲစဉ်များ မရှိသေးပါ။")
    else:
        for m in matches:
            home = m['homeTeam']['name']
            away = m['awayTeam']['name']
            league = m['competition']['name']
            
            # ပွဲစဉ်တစ်ခုချင်းစီကို Expander ထဲတွင် ပြသမည်
            with st.expander(f"🏟️ {home} vs {away} ({league})", expanded=True):
                # Google Search ကို အသုံးပြုပြီး ပိုမိုတိကျသော သုံးသပ်ချက်ရယူရန် Prompt
                prompt = f"""
                Today is February 25, 2026. Search Google for the match between {home} and {away}. 
                Please analyze: 
                1. Official starting lineups and recent injuries.
                2. Market sentiment (what percentage of bettors are picking which team).
                3. Tactical match-up and any 'traps' in the odds.
                
                Provide the output in Burmese:
                - **အပိုင် Tip**: (90% ကျော်သေချာသော ရလဒ်ကို တိုက်ရိုက်ပြောပါ)
                - **သုံးသပ်ချက်**: (ဘာကြောင့် နိုင်မှာလဲဆိုတာကို ကျွမ်းကျင်သူတစ်ယောက်လို ရှင်းပြပါ)
                - **သတိပေးချက်**: (ကြေးမှားနေတာမျိုး သို့မဟုတ် သတိထားရမည့်အချက်များ)
                """
                
                try:
                    # Gemini မှ Google Search သုံးပြီး အဖြေထုတ်ပေးမည်
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    # Error တစ်ခုခုရှိလျှင် ပြသရန်
                    st.error(f"Error analyzing {home}: {str(e)}")
