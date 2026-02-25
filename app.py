import streamlit as st
import google.generativeai as genai
import requests

# --- CONFIGURATION (မင်းရဲ့ အချက်အလက်များ ထည့်ရန်) ---
GEMINI_API_KEY = "AIzaSyA4-9LZdhqavOcjmJ2W0yDAVJNNOoFsICQ"
FOOTBALL_KEY = "85888e2858904e578f14f40f0c058c4f"
TELEGRAM_TOKEN = "8259077848:AAEbVOoEVc36sZBaMNxQ4J7qkL6b6rZEK7A" # <--- ဒီမှာ Token ထည့်ပါ
CHAT_ID = "5236506026"      # <--- ဒီမှာ ID ထည့်ပါ

genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model with Google Search
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    tools=[{"google_search_retrieval": {}}]
)

# Telegram သို့ စာပို့သည့် Function
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

st.set_page_config(page_title="Phone A - AI Analyst", page_icon="🛡️")
st.title("🛡️ Phone A: Smart AI Analyst")
st.write("အလုပ်ထဲတွင် ဖုန်းကြည့်စရာမလိုဘဲ Smart Watch မှတစ်ဆင့် Alert ရယူပါ။")

if st.button('🚀 ပွဲစဉ်များကို စတင်ခွဲမ်းစိတ်ပြီး Telegram ပို့ရန်'):
    with st.spinner('Gemini မှ Google တွင် ရှာဖွေနေသည်...'):
        # ယနေ့ပွဲစဉ်များရယူခြင်း
        match_url = "https://api.football-data.org/v4/matches"
        headers = {'X-Auth-Token': FOOTBALL_KEY}
        res = requests.get(match_url, headers=headers).json()
        matches = res.get('matches', [])

        if not matches:
            st.warning("ယနေ့အတွက် ပွဲစဉ်များ မတွေ့ရှိပါ။")
        else:
            for m in matches:
                home = m['homeTeam']['name']
                away = m['awayTeam']['name']
                league = m['competition']['name']
                
                # Gemini ကို Google Search ဖြင့် အသေးစိတ်ခိုင်းစေခြင်း
                prompt = f"""
                Search Google for the match {home} vs {away} on Feb 26, 2026.
                1. Check official lineups and injury news.
                2. Look for betting market traps (where public bets are going vs odds movement).
                3. Provide a high-confidence tip in Burmese.
                
                If the match is very risky, say 'SKIP'.
                If it's high confidence, format as:
                ⚽ Match: {home} vs {away} ({league})
                🔥 Tip: [Your Result]
                📊 Confidence: [90%+]
                💡 Reason: [Short tactical reason]
                ⚠️ Warning: [Any trap detected]
                """
                
                try:
                    response = model.generate_content(prompt)
                    analysis = response.text
                    
                    if "SKIP" not in analysis.upper():
                        # Telegram သို့ ပို့မည်
                        send_to_telegram(f"🔔 *AI CONFIRMED TIP*\n\n{analysis}")
                        st.success(f"Sent: {home} vs {away}")
                    else:
                        st.info(f"Skipped: {home} vs {away} (Risky)")
                except Exception as e:
                    st.error(f"Error analyzing {home}: {str(e)}")

st.divider()
st.caption("ဒူဘိုင်းရှိ မင်းရဲ့အောင်မြင်မှုအတွက် Gemini မှ အစွမ်းကုန် ကူညီပေးနေပါတယ်။")
