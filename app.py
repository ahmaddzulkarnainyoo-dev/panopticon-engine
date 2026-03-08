import sys
import streamlit as st
from groq import Groq
from gnews import GNews
import base64

# API Key Hardcoded
API_KEY = 
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="The Panopticon Engine", layout="wide")

# --- IMPROVED SCRAPER WITH SOCIAL MEDIA DORKING ---
def fetch_intelligence_data(query):
    google_news = GNews(language='id', country='ID', max_results=10)
    
    # Teknik Dorking: Mencari narasi di X dan TikTok lewat Google News
    queries = [
        query, 
        f"site:twitter.com {query}", 
        f"site:tiktok.com {query}"
    ]
    
    combined_text = ""
    for q in queries:
        results = google_news.get_news(q)
        for article in results:
            combined_text += f"\n[SUMBER: {article['publisher']['title']}] \nJudul: {article['title']}\nDesc: {article['description']}\n"
    
    return combined_text

# --- UI & DOWNLOAD LOGIC (Sama seperti sebelumnya) ---
def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.txt" style="text-decoration:none;"><button style="width:100%; background-color:#2ecc71; color:white; border-radius:5px; border:none; padding:10px; font-weight:bold;">💾 SIMPAN LAPORAN INTELIJEN</button></a>'
    return href

def analyze_ai(system_prompt, user_msg):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
        temperature=0.4
    )
    return completion.choices[0].message.content

# UI Style
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #e63946; color: white; border-radius: 5px; font-weight: bold; }
    .stTextArea textarea { background-color: #1a1c23; color: white; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.title("⚖️ Panopticon Engine")
    mode = st.radio("Operasi:", ["Private War Room", "Public Intelligence Radar"])
    st.markdown("---")
    st.info("Isu publik adalah medan perang persepsi.")

# --- MODE 1: PRIVATE WAR ROOM ---
if mode == "Private War Room":
    st.header("🌑 Private Strategic War Room")
    col1, col2 = st.columns([1, 1])
    with col1:
        target = st.text_input("Identitas Target:", "Si X")
        archetype = st.selectbox("Archetype:", ["Narcissist", "Tyrant", "Seducer", "Shadow Player", "Weak Leader"])
        insecurity = st.text_input("The Thumbscrew (Kelemahan):")
        dynamic = st.select_slider("Power Dynamic:", options=["Dia Dominan", "Seimbang", "User Dominan"])
        goal = st.radio("Tujuan Strategis:", ["Pedang (Win)", "Tameng (Protect)"])
        evidence = st.text_area("Bukti/Kronologi Kejadian:", height=200)

    with col2:
        if st.button("EXECUTE ANALYSIS"):
            sys_msg = "Kamu adalah Penasihat Strategis rahasia. Bedah shadow dan berikan langkah taktis Greene/Machiavelli."
            user_msg = f"Target: {target}, Archetype: {archetype}, Kelemahan: {insecurity}, Goal: {goal}, Evidence: {evidence}"
            result = analyze_ai(sys_msg, user_msg)
            st.markdown(result)
            st.markdown(get_binary_file_downloader_html(result, f"Analisis_{target}"), unsafe_allow_html=True)

# --- MODE 2: PUBLIC INTELLIGENCE RADAR (INTEGRASI MEDSOS) ---
else:
    st.header("🌐 Public Intelligence Radar")
    tab1, tab2 = st.tabs(["🕵️ Social Narrative Scanner", "🔍 Framing Forensic"])

    with tab1:
        st.subheader("Automated Cross-Platform Scan")
        query = st.text_input("Masukkan Nama Tokoh / Isu Viral:", placeholder="Misal: @PolitisiX atau #KasusY")
        if st.button("Deep Scan Medsos & Berita"):
            if query:
                with st.spinner(f"Menjelajah X, TikTok, dan Portal Berita untuk '{query}'..."):
                    raw_intelligence = fetch_intelligence_data(query)
                    if raw_intelligence:
                        sys_msg = """
                        Kamu adalah Pakar Intelijen Digital. 
                        Bedah data dari berbagai platform ini. 
                        Pisahkan mana narasi ORGANIK dari rakyat dan mana narasi BUATAN (Buzzer/Bot). 
                        Identifikasi pola manipulasi tokoh terkait.
                        """
                        analysis = analyze_ai(sys_msg, raw_intelligence)
                        st.markdown(analysis)
                        st.markdown(get_binary_file_downloader_html(analysis, f"Radar_{query}"), unsafe_allow_html=True)
                    else: st.warning("Radar tidak menemukan data yang cukup.")
            else: st.error("Input query-nya dulu, dher.")

    with tab2:
        st.subheader("Manual Framing Forensic")
        news_text = st.text_area("Tempel Teks Narasi yang Mau Dibedah:", height=300)
        if st.button("Detect Manipulation"):
            analysis = analyze_ai("Bedah framing, bias, dan agenda tersembunyi.", news_text)
            st.markdown(analysis)
            st.markdown(get_binary_file_downloader_html(analysis, "Framing_Report"), unsafe_allow_html=True)
