import streamlit as st
import google.generativeai as genai
import requests

# --- CONFIGURATION (မင်းရဲ့ အချက်အလက်များ) ---
GEMINI_API_KEY = "AIzaSyA4-9LZdhqavOcjmJ2W0yDAVJNNOoFsICQ"
FOOTBALL_KEY = "85888e2858904e578f14f40f0c058c4f"
TELEGRAM_TOKEN = "8259077848:AAEbVOoEVc36sZBaMNxQ4J7qkL6b6rZEK7A" #
CHAT_ID = "5236506026" #

genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model with Google Search
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', #
    tools=[{"google_search_retrieval": {}}]
)

# Telegram သို့ စာပို့သည့် Function
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        st.error(f"Telegram Error: {str(e)}")

st.set_page_config(page_title="Phone A - AI Analyst", page_icon="🛡️")
st.title("🛡️ Phone A: Smart AI Analyst")
st.write("အလုပ်ထဲတွင် ဖုန်းကြည့်စရာမလိုဘဲ Smart Watch မှတစ်ဆင့် အပိုင်ပွဲစဉ်များကို သိနိုင်ပါပြီ။")

if st.button('🚀 ပွဲစဉ်များကို စတင်ခွဲမ်းစိတ်ပြီး Telegram ပို့ရန်'):
    # စနစ်စတင်ကြောင်း အချက်ပေးခြင်း
    send_to_telegram("🔍 *Phone A:* Analyzing upcoming high-confidence matches...")
    
    with st.spinner('Gemini မှ အချက်အလက်များကို ရှာဖွေနေသည်...'):
        # ရက်စွဲကို API Limit အတွင်းဖြစ်စေရန် ၅ ရက်စာသာ သတ်မှတ်သည်
        match_url = "https://api.football-data.org/v4/matches?dateFrom=2026-02-26&dateTo=2026-03-03"
        headers = {'X-Auth-Token': FOOTBALL_KEY}
        
        try:
            res = requests.get(match_url, headers=headers).json()
            matches = res.get('matches', [])

            if not matches:
                st.warning("လက်ရှိတွင် ထိပ်တန်းလိဂ်ပွဲစဉ်များ မတွေ့ရှိသေးပါ။")
                send_to_telegram("⚠️ No major matches found for the next few days.")
            else:
                send_to_telegram(f"✅ Found {len(matches)} matches. Filtering for the best tips...")
                for m in matches:
                    home = m['homeTeam']['name']
                    away = m['awayTeam']['name']
                    league = m['competition']['name']
                    
                    # Gemini Analysis for Smart Watch
                    prompt = f"""
                    Search for {home} vs {away} match in {league}.
                    1. Check lineups and key injuries.
                    2. Provide a 90% confidence tip in Burmese (short for smartwatch).
                    3. If it's a trap or too risky, start the response with 'SKIP'.
                    """
                    
                    response = model.generate_content(prompt)
                    analysis = response.text
                    
                    if not analysis.upper().startswith("SKIP"):
                        # Smart Watch အတွက် အတိုဆုံးနှင့် အလိုရှင်းဆုံး format ချခြင်း
                        formatted_msg = (
                            f"⚽ *{home} vs {away}*\n"
                            f"🏆 {league}\n\n"
                            f"{analysis}"
                        )
                        send_to_telegram(formatted_msg)
                        st.success(f"Sent Tip: {home} vs {away}")
                    else:
                        st.info(f"Skipped: {home} vs {away} (Risky)")
                        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            send_to_telegram(f"❌ Error: {str(e)}")

st.divider()
st.caption("ဒူဘိုင်းရှိ မင်းရဲ့ အောင်မြင်မှုအတွက် Gemini AI က အမြဲရှိနေပါတယ်။")
