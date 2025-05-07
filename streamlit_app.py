import streamlit as st
import openai
from openai import OpenAI

# Judul aplikasi
st.title("Deteksi Berita Hoaks")
st.write("Masukkan teks berita untuk menganalisis apakah berita tersebut berpotensi hoaks atau tidak.")

# Form input teks
with st.form("hoax_form"):
    news_text = st.text_area("Teks Berita", height=200, placeholder="Masukkan teks berita di sini...")
    submit_button = st.form_submit_button("Analisis")

# Fungsi untuk memanggil OpenAI API
def analyze_news(news_text):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # Ambil API key dari secrets
        prompt = (
            "Analisis teks berita berikut dan tentukan apakah berita ini berpotensi hoaks atau tidak. "
            "Berikan penjelasan singkat tentang alasan Anda. Jika teks tidak cukup jelas, nyatakan bahwa informasi tambahan diperlukan. "
            f"Teks berita: {news_text}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Gunakan model yang sesuai, misalnya gpt-4o-mini
            messages=[
                {"role": "system", "content": "Anda adalah asisten yang ahli dalam mendeteksi berita hoaks."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
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
