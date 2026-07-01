import streamlit as st
import gspread
import pandas as pd
import json

st.title("Sistem Verifikasi Transfer SWFM")

# 1. Mengambil kredensial dari Streamlit Secrets (Tanpa file fisik JSON!)
creds_dict = json.loads(st.secrets["google_credentials"])
gc = gspread.service_account_from_dict(creds_dict)

# 2. Hubungkan ke Google Sheets Anda
sh = gc.open_by_key('1HvgVicTWwO4RMQI6ZR3Mu3IgGicwjcLZl9mDN1auvJU')
worksheet = sh.sheet1 # Membuka sheet pertama

# 3. Tarik data untuk mencari Nomor Tiket
def get_data():
    return pd.DataFrame(worksheet.get_all_records())

df = get_data()

# 4. Form Input Pencarian
ticket_id = st.text_input("Masukkan Nomor Tiket SWFM (Contoh: BPS-2026-000000034391)")

if ticket_id:
    # Validasi jika Nomor Tiket cocok
    if ticket_id in df['Nomor Tiket SWFM'].values:
        # Hitung posisi baris. Ditambah 2 karena DataFrame mulai dari 0, sedangkan baris di Google Sheets mulai dari 1 dan baris 1 adalah Header.
        row_idx = df.index[df['Nomor Tiket SWFM'] == ticket_id].tolist()[0] + 2
        
        st.success(f"Tiket ditemukan! Siap untuk verifikasi.")
        
        # 5. Form Input ke Kolom AD (Verifikasi)
        status_verifikasi = st.selectbox("Pilih Status Verifikasi Transfer", ["Sudah Transfer", "Pending", "Ditolak"])
        
        if st.button("Simpan Verifikasi"):
            # Update sel tepat di kolom AD pada baris yang sesuai
            worksheet.update_acell(f'AD{row_idx}', status_verifikasi)
            st.success(f"Berhasil! Data tiket {ticket_id} di kolom AD telah diupdate menjadi '{status_verifikasi}'.")
    else:
        st.error("Nomor Tiket tidak ditemukan di dalam database.")
