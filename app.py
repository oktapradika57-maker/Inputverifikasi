import streamlit as st
import gspread
import pandas as pd

st.title("Sistem Verifikasi Transfer SWFM")

# 1. Mengambil kredensial dari Streamlit Secrets
try:
    creds_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(creds_dict)
except Exception as e:
    st.error(f"Gagal memuat kredensial dari Secrets: {e}")
    st.stop()

# 2. Hubungkan ke Google Sheets
try:
    sh = gc.open_by_key('1HvgVicTWwO4RMQI6ZR3Mu3IgGicwjcLZl9mDN1auvJU')
    worksheet = sh.worksheet("Form Request dana") 
except Exception as e:
    st.error(f"Gagal terhubung ke Google Sheets: {e}")
    st.stop()

# 3. Fungsi untuk menarik data dari Google Sheets
def get_data():
    return pd.DataFrame(worksheet.get_all_records())

df = get_data()

# 4. Form Input Pencarian Berdasarkan Nomor Tiket
nama_kolom_tiket = "Nomor Tiket SWFM ( tulis cth BPS-2026-000000034391)"
ticket_id = st.text_input(f"Masukkan {nama_kolom_tiket}")

if ticket_id:
    # Validasi jika Nomor Tiket cocok dengan database
    if ticket_id in df[nama_kolom_tiket].values:
        # Hitung posisi baris (+2 karena indeks pandas mulai dari 0 dan baris 1 di Sheet adalah Header)
        row_idx = df.index[df[nama_kolom_tiket] == ticket_id].tolist()[0] + 2
        
        st.success(f"Tiket ditemukan di database! (Berada pada baris ke-{row_idx})")
        
        # 5. Pilihan Input untuk Kolom AD (Verifikasi Transfer)
        status_verifikasi = st.selectbox("Pilih Status Verifikasi Transfer", ["Sudah Transfer", "Pending", "Ditolak"])
        
        if st.button("Simpan Verifikasi"):
            try:
                # Kolom AD adalah kolom ke-30 dalam format angka koordinat gspread
                kolom_ad = 30
                
                # Melakukan update data ke Google Sheets menggunakan metode yang aman untuk versi baru
                worksheet.update_cell(row_idx, kolom_ad, status_verifikasi)
                st.success(f"Berhasil! Data tiket '{ticket_id}' di kolom AD (Verifikasi Transfer) telah diperbarui menjadi '{status_verifikasi}'.")
            except Exception as e:
                st.error(f"Gagal mengupdate data ke Google Sheets: {e}")
    else:
        st.error("Nomor Tiket tidak ditemukan di dalam database. Mohon periksa kembali inputan Anda.")
