import streamlit as st
import openai
from openai import OpenAI

# Judul aplikasi
st.title("📰 Evaluasi Berita")
st.subheader("Tugas Transformasi Digital")
st.write("Aplikasi evaluasi berita fakta dan hoaks dengan kecerdasan buatan")

# Form input teks
with st.form("hoax_form"):
    news_text = st.text_area("Masukkan teks berita untuk menganalisis apakah berita tersebut berpotensi hoaks atau tidak", height=200, placeholder="Masukkan teks berita di sini...")
    submit_button = st.form_submit_button("Evaluasi")

# Fungsi untuk memanggil OpenAI API
def analyze_news(news_text):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"], base_url="https://api.deepseek.com")  # Ambil API key dari secrets
        prompt = (
            "Analisis dan evaluasi teks berita berikut dan tentukan apakah berita ini berpotensi hoaks atau tidak. "
            "Berikan penjelasan singkat tentang alasan Anda. Jika teks tidak cukup jelas, nyatakan bahwa informasi tambahan diperlukan. "
            f"Teks berita: {news_text}"
        )

        response = client.chat.completions.create(
            model="deepseek-chat",  # Gunakan model yang sesuai, misalnya gpt-4o-mini
            messages=[
                {"role": "system", "content": "Anda adalah asisten yang ahli dalam mendeteksi berita hoaks."},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

# Logika saat tombol Analisis ditekan
if submit_button:
    if news_text.strip() == "":
        st.error("Harap masukkan teks berita!")
    else:
        with st.spinner("Menganalisis..."):
            result = analyze_news(news_text)
            st.subheader("Hasil Analisis")
            st.write(result)

footer_html = """
<div style='text-align: center;'>
<p>Dikembangan oleh Kelompok 2 ❤️</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
