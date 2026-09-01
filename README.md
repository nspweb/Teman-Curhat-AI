# 💬 Teman Curhat AI

Aplikasi chat 2 arah dengan AI yang berperan sebagai teman curhat, dibuat dengan Streamlit
dan **Google Gemini API (gratis)**.

## Cara Menjalankan

1. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

3. Buka browser ke alamat yang muncul (biasanya `http://localhost:8501`).

4. Dapatkan **API key GRATIS** di https://aistudio.google.com/apikey
   - Login pakai akun Google
   - Klik "Create API key"
   - Tidak perlu kartu kredit
   - Atur API di file secrets.toml atau secret web streamlit

## Kenapa Gemini?

Google Gemini API punya free tier yang paling "genuinely free" dibanding provider lain:
- Tidak perlu kartu kredit
- Model `gemini-3.5-flash-lite` yang dipakai di sini kualitasnya bagus (setara model premium) dan gratis
- Limit harian cukup besar untuk pemakaian personal (ratusan request/hari)
- Kalau kena limit, tinggal tunggu reset di hari berikutnya

Alternatif gratis lain kalau suatu saat Gemini limitnya kurang: **Groq** (super cepat, model Llama)
atau **OpenRouter** (banyak pilihan model gratis) — tinggal ganti bagian pemanggilan API di `app.py`.

## Fitur

- 💬 Chat dua arah dengan bot AI yang merespons secara natural (streaming, seperti mengetik)
- 🎭 4 pilihan gaya kepribadian bot: Hangat & Suportif, Santai (bahasa gaul), Kalem & Reflektif, Ceria & Semangat
- 🎨 Tampilan gradient warna hangat, bubble chat rapi, sidebar rapi
- 🗑️ Tombol untuk mulai obrolan baru kapan saja
- ⚠️ Catatan sumber daya krisis kesehatan jiwa selalu terlihat di sidebar

## Kustomisasi

- Ganti model di `app.py` pada baris `model="gemini-2.5-flash"` — misalnya ke `gemini-2.5-flash-lite`
  untuk respons lebih ringan/cepat, atau model Flash terbaru kalau tersedia di akunmu.
- Edit dictionary `PERSONA_STYLES` untuk menambah gaya kepribadian baru.
- Ubah warna gradient di bagian `<style>` untuk tema visual yang berbeda.

## Catatan Privasi & Keamanan

- API key **tidak disimpan** secara permanen — hanya ada di session Streamlit kamu selama aplikasi berjalan.
- Riwayat chat juga hanya tersimpan di memori session (hilang saat aplikasi di-refresh/restart), jadi cocok untuk curhat yang sifatnya privat.
- Perlu diketahui: pada free tier, Google dapat menggunakan data prompt untuk meningkatkan produk mereka
  (beda dengan tier berbayar). Kalau privasi adalah prioritas utama, pertimbangkan provider lain seperti Mistral.
