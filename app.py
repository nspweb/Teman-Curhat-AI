import os
import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime

# ----------------------------------------------------------------------------
# API KEY — diambil dari server (Streamlit Secrets / env var), TIDAK dari UI
# ----------------------------------------------------------------------------
# Cara pakai:
# 1) Lokal: buat file .streamlit/secrets.toml berisi:
#        GEMINI_API_KEY = "isi-api-key-kamu"
# 2) Saat deploy di Streamlit Community Cloud: buka menu app -> Settings -> Secrets,
#    lalu isi baris yang sama di sana. Key ini terenkripsi di server dan TIDAK
#    pernah dikirim ke browser/client, jadi tidak akan pernah muncul di sidebar
#    atau bisa dilihat lewat "View Page Source".
API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))


@st.cache_resource(show_spinner=False)
def get_client(key: str):
    """Client di-cache supaya tidak dibuat ulang di setiap pesan (lebih cepat)."""
    return genai.Client(api_key=key)

# ----------------------------------------------------------------------------
# KONFIGURASI HALAMAN
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Teman Curhat AI",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# CSS KUSTOM — TAMPILAN HANGAT & RAMAH
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* Background gradient lembut */
        .stApp {
            background: linear-gradient(160deg, #fff5f0 0%, #f0f4ff 50%, #f5f0ff 100%);
        }

        /* Header custom */
        .curhat-header {
            text-align: center;
            padding: 1.2rem 1rem 0.5rem 1rem;
        }
        .curhat-header h1 {
            font-size: 2.1rem;
            margin-bottom: 0.2rem;
            background: linear-gradient(90deg, #ff8a65, #7e57c2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .curhat-header p {
            color: #6b6b6b;
            font-size: 0.95rem;
            margin-top: 0;
        }

        /* Bubble chat */
        .stChatMessage {
            border-radius: 18px !important;
            padding: 0.4rem 0.2rem;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #fdf2f8 0%, #eef2ff 100%);
        }

        /* Tombol */
        .stButton>button {
            border-radius: 12px;
            border: none;
            background: linear-gradient(90deg, #ff8a65, #7e57c2);
            color: white;
            font-weight: 600;
            transition: 0.2s;
        }
        .stButton>button:hover {
            opacity: 0.85;
            transform: scale(1.02);
        }

        /* Kotak input chat */
        .stChatInputContainer {
            border-radius: 16px;
        }

        /* Footer kecil */
        .footer-note {
            text-align: center;
            color: #9a9a9a;
            font-size: 0.75rem;
            padding-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="curhat-header">
        <h1>💬 Teman Curhat</h1>
        <p>Cerita apa aja di sini, aku dengerin ✨</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SIDEBAR — PENGATURAN
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan")

    if API_KEY:
        st.success("🔐 Terhubung ke AI (key dikelola oleh server)")
    else:
        st.error(
            "⚠️ GEMINI_API_KEY belum di-set di server. Tambahkan lewat "
            "`.streamlit/secrets.toml` (lokal) atau menu Secrets di Streamlit "
            "Cloud (saat deploy)."
        )

    st.markdown("---")
    st.markdown("### 🎭 Kepribadian Teman")
    persona = st.selectbox(
        "Pilih gaya ngobrol",
        [
            "Hangat & Suportif",
            "Santai & Asik (bahasa gaul)",
            "Kalem & Reflektif",
            "Ceria & Semangat",
        ],
        index=0,
    )

    st.markdown("---")
    if st.button("🗑️ Mulai Obrolan Baru"):
        st.session_state["messages"] = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div class="footer-note">
        ⚠️ Ini bukan pengganti bantuan profesional.<br>
        Kalau kamu merasa dalam krisis, hubungi:<br>
        <b>119 ext. 8</b> (Kemenkes, 24 jam) atau<br>
        <b>Into The Light ID</b> untuk dukungan kesehatan jiwa.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# SYSTEM PROMPT SESUAI PERSONA
# ----------------------------------------------------------------------------
PERSONA_STYLES = {
    "Hangat & Suportif": (
        "Kamu berbicara dengan nada hangat, tenang, dan penuh empati. "
        "Gunakan bahasa Indonesia yang lembut dan suportif."
    ),
    "Santai & Asik (bahasa gaul)": (
        "Kamu ngobrol santai kayak temen deket, boleh pakai bahasa gaul sehari-hari "
        "(seperti 'gue-lo', 'anjir', 'wkwk' secukupnya), tapi tetap sopan dan peduli."
    ),
    "Kalem & Reflektif": (
        "Kamu berbicara pelan, reflektif, dan suka mengajak orang berpikir lebih dalam "
        "tentang perasaan mereka lewat pertanyaan yang lembut."
    ),
    "Ceria & Semangat": (
        "Kamu punya energi positif dan ceria, suka menyemangati, tapi tetap sensitif "
        "terhadap perasaan orang yang lagi cerita."
    ),
}

SYSTEM_PROMPT = f"""Kamu adalah teman curhat virtual berbahasa Indonesia. Peranmu adalah menjadi
pendengar yang hangat, tidak menghakimi, dan suportif — seperti sahabat dekat yang selalu
punya waktu untuk mendengarkan.

Gaya bicara: {PERSONA_STYLES[persona]}

Pedoman penting:
- Dengarkan dulu, jangan buru-buru kasih solusi kecuali diminta.
- Validasi perasaan orang yang cerita tanpa menghakimi.
- Ajukan pertanyaan lanjutan yang tulus untuk menunjukkan kamu benar-benar peduli, tapi jangan bertubi-tubi.
- Jangan berpura-pura jadi psikolog/terapis berlisensi, dan jangan mendiagnosis kondisi mental apapun.
- Jika ada tanda-tanda seseorang dalam bahaya (misalnya menyebutkan keinginan menyakiti diri sendiri atau orang lain),
  tetap tenang, tunjukkan kepedulian, dan dorong dengan lembut untuk menghubungi layanan darurat atau orang
  yang mereka percaya, tanpa menghakimi atau membuat mereka merasa lebih buruk.
- Balasan cukup singkat-menengah, natural seperti chat, bukan esai panjang.
- Sesekali gunakan emoji secukupnya biar terasa hangat, jangan berlebihan.
"""

# ----------------------------------------------------------------------------
# STATE
# ----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ----------------------------------------------------------------------------
# TAMPILKAN RIWAYAT CHAT
# ----------------------------------------------------------------------------
if not st.session_state["messages"]:
    st.markdown(
        """
        <div style="text-align:center; color:#888; padding: 2rem 1rem;">
            👋 Halo! Aku di sini buat dengerin ceritamu.<br>
            Mau curhat soal apa hari ini?
        </div>
        """,
        unsafe_allow_html=True,
    )

for msg in st.session_state["messages"]:
    avatar = "🧑" if msg["role"] == "user" else "🤗"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ----------------------------------------------------------------------------
# INPUT CHAT
# ----------------------------------------------------------------------------
user_input = st.chat_input("Tulis cerita atau perasaanmu di sini...")

if user_input:
    if not API_KEY:
        st.error("⚠️ Server belum dikonfigurasi dengan API key. Hubungi admin/pemilik aplikasi ya 🙏")
    else:
        # Tampilkan pesan user
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        # Panggil Gemini API dan tampilkan balasan dengan efek streaming
        with st.chat_message("assistant", avatar="🤗"):
            placeholder = st.empty()
            full_response = ""
            try:
                client = get_client(API_KEY)

                # Batasi riwayat yang dikirim ke model (misal 8 pesan terakhir = ~4 giliran).
                # Riwayat yang terlalu panjang membuat setiap request lebih lambat karena
                # model harus memproses ulang seluruh percakapan tiap kali.
                MAX_HISTORY_MESSAGES = 8
                recent_messages = st.session_state["messages"][:-1][-MAX_HISTORY_MESSAGES:]

                history = [
                    types.Content(
                        role=("model" if m["role"] == "assistant" else "user"),
                        parts=[types.Part(text=m["content"])],
                    )
                    for m in recent_messages
                ]

                chat = client.chats.create(
                    model="gemini-3.6-flash",
                    history=history,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        max_output_tokens=512,  # jawaban chat singkat -> lebih cepat selesai
                        thinking_config=types.ThinkingConfig(
                            thinking_level=types.ThinkingLevel.LOW,
                            # LOW = model tidak "mikir panjang" sebelum jawab.
                            # Default model ini sebenarnya MEDIUM, yang menambah
                            # waktu tunggu sebelum kata pertama muncul — cocok untuk
                            # coding/tugas kompleks, tapi berlebihan untuk chat santai.
                        ),
                    ),
                )

                # Update tampilan tiap beberapa chunk (bukan tiap chunk) supaya
                # rendering UI tidak jadi bottleneck saat token datang cepat.
                UPDATE_EVERY_N_CHUNKS = 3
                chunk_count = 0
                for chunk in chat.send_message_stream(user_input):
                    if chunk.text:
                        full_response += chunk.text
                        chunk_count += 1
                        if chunk_count % UPDATE_EVERY_N_CHUNKS == 0:
                            placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
            except Exception as e:
                full_response = (
                    "Aduh, aku lagi ada kendala teknis nih 😔 "
                    f"({e}). Coba cek lagi API key-nya (pastikan valid dari aistudio.google.com/apikey) "
                    "atau coba beberapa saat lagi ya — kalau kena limit harian, tunggu sampai besok."
                )
                placeholder.markdown(full_response)

        st.session_state["messages"].append(
            {"role": "assistant", "content": full_response}
        )