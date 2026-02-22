import streamlit as st
import requests
from groq import Groq

# ==========================================
# ၁။ မင်းရဲ့ API KEYS တွေကို ဒီအောက်မှာ အသေထည့်ပါ
# ==========================================
# (မျက်တောင်ဖွင့် ပိတ် " " ထဲမှာ မင်းရဲ့ Key အစစ်တွေကို ထည့်ပေးရမှာပါ)

GROQ_API_KEY = "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"
FOOTBALL_KEY = "5da489c665e54c44a227d7826b02134a"

# ==========================================

# ၂။ UI ပိုင်း ပြင်ဆင်ခြင်း
st.set_page_config(page_title="AI Football Predictor", page_icon="⚽")
st.title("⚽ နေ့စဉ် ဘောလုံးပွဲ ခန့်မှန်းချက်")
st.write("AI က ဒီနေ့ပွဲစဉ်တွေကို ခွဲခြမ်းစိတ်ဖြာပြီး နိုင်ခြေရှိတာတွေ ရွေးပေးပါလိမ့်မယ်။")

# AI Client ကို ချိတ်ဆက်ခြင်း
client = Groq(api_key=GROQ_API_KEY)

# ၃။ Football Data ယူတဲ့ Function
def get_cleaned_data():
    url = "https://api.football-data.org/v4/matches"
    headers = {'X-Auth-Token': FOOTBALL_KEY}
    try:
        response = requests.get(url, headers=headers).json()
        cleaned_matches = []
        if 'matches' in response:
            for match in response['matches']:
                match_info = {
                    "homeTeam": match['homeTeam']['name'],
                    "awayTeam": match['awayTeam']['name'],
                    "competition": match['competition']['name']
                }
                cleaned_matches.append(match_info)
        return cleaned_matches
    except:
        return None

# ၄။ ခန့်မှန်းချက်ခလုတ်
if st.button('ဒီနေ့အတွက် ခန့်မှန်းချက်ထုတ်ရန်'):
    # Key မထည့်ရသေးရင် သတိပေးမယ်
    if "ထည့်ပါ" in GROQ_API_KEY or "ထည့်ပါ" in FOOTBALL_KEY:
        st.error("⚠️ အမှားအယွင်းရှိနေပါသည်- API Keys များ ထည့်သွင်းပေးရန် လိုအပ်ပါသည်။")
    else:
        with st.spinner('AI က ပွဲစဉ်တွေကို တွက်ချက်နေပါတယ်... ခဏစောင့်ပေးပါ...'):
            matches = get_cleaned_data()
            
            if matches:
                # ပွဲစဉ်စာရင်းကို စာသားအဖြစ်ပြောင်း
                matches_text = "\n".join([f"{m['homeTeam']} vs {m['awayTeam']} ({m['competition']})" for m in matches])
                
                try:
                    # AI ဆီက အဖြေတောင်းခြင်း
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "မင်းက ကမ္ဘာကျော် ဘောလုံးပွဲ ကျွမ်းကျင်သူ ခွဲခြမ်းစိတ်ဖြာသူပါ။"},
                            {"role": "user", "content": f"ဒီနေ့ပွဲစဉ်တွေထဲက နိုင်ခြေအရှိဆုံး ၅ ပွဲကို ရွေးပေးပါ။ အသင်းတစ်သင်းချင်းစီရဲ့ အားသာချက်ကို မြန်မာလို အကျဉ်းချုပ် ရှင်းပြပေးပါ။\n\nဒီနေ့ပွဲစဉ်များ-\n{matches_text}"}
                        ]
                    )
                    st.success("✅ ခန့်မှန်းချက် ထွက်လာပါပြီ!")
                    st.markdown("---")
                    st.markdown(completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"AI Error: {e}")
            else:
                st.warning("⚠️ ယနေ့အတွက် ပွဲစဉ်ဒေတာ မရှိသေးပါ (သို့မဟုတ်) API Limit ပြည့်နေပါသည်။")

# အောက်ခြေစာသား
st.markdown("---")
st.caption("Developed by AI Assistant for Football Fans")
