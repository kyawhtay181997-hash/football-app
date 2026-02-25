import streamlit as st
import google.generativeai as genai
import requests

# --- CONFIGURATION (မင်းရဲ့ အချက်အလက်များ) ---
# API Keys များကို Screenshot (12) အရ ထည့်သွင်းထားသည်
GEMINI_API_KEY = "AIzaSyA4-9LZdhqavOcjmJ2W0yDAVJNNOoFsICQ"
FOOTBALL_KEY = "85888e2858904e578f14f40f0c058c4f"
TELEGRAM_TOKEN = "8259077848:AAEbVOoEVc36sZBaMNxQ4J7qkL6b6rZEK7A" #
CHAT_ID = "5236506026" #

genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model with Google Search
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
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
st.write("အလုပ်ထဲတွင် ဖုန်းကြည့်စရာမလိုဘဲ Smart Watch မှတစ်ဆင့် Alert ရယူပါ။")

if st.button('🚀 ပွဲစဉ်များကို စတင်ခွဲမ်းစိတ်ပြီး Telegram ပို့ရန်'):
    # အဆင့် (၁) - ချိတ်ဆက်မှု အောင်မြင်ကြောင်း Telegram ဆီ အရင်စာပို့မည်
    send_to_telegram("🛠️ *Phone A System Check:* Checking for high-confidence matches...")
    
    with st.spinner('Gemini မှ Google တွင် ရှာဖွေနေသည်...'):
        # API Limit မကျော်စေရန် ရက်စွဲကို ၃ ရက်စာသာ သတ်မှတ်သည်
        match_url = "https://api.football-data.org/v4/matches?dateFrom=2026-02-26&dateTo=2026-03-01"
        headers = {'X-Auth-Token': FOOTBALL_KEY}
        
        try:
            res = requests.get(match_url, headers=headers).json()
            matches = res.get('matches', [])

            if not matches:
                st.warning("ယနေ့အတွက် ပွဲစဉ်များ မတွေ့ရှိပါ။")
                send_to_telegram("⚠️ No major matches found in the current date range.")
            else:
                send_to_telegram(f"✅ Found {len(matches)} matches. Analyzing traps now...")
                for m in matches:
                    home = m['homeTeam']['name']
                    away = m['awayTeam']['name']
                    league = m['competition']['name']
                    
                    # Gemini Analysis Logic
                    prompt = f"""
                    Search Google for the match {home} vs {away}.
                    1. Check injury news, team form and market traps.
                    2. Provide a high-confidence tip in Burmese (မြန်မာဘာသာဖြင့်).
                    If it's too risky, say SKIP.
                    """
                    
                    response = model.generate_content(prompt)
                    analysis = response.text
                    
                    if "SKIP" not in analysis.upper():
                        # Telegram သို့ အပိုင် Tip ပို့မည်
                        send_to_telegram(f"⚽ *{home} vs {away}*\n\n{analysis}")
                        st.success(f"Sent: {home} vs {away}")
                    else:
                        st.info(f"Skipped: {home} vs {away} (Too Risky)")
                        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            send_to_telegram(f"❌ Error occurred: {str(e)}")

st.divider()
st.caption("ဒူဘိုင်းရှိ မင်းရဲ့အောင်မြင်မှုအတွက် Gemini မှ အစွမ်းကုန် ကူညီပေးနေပါတယ်။")
