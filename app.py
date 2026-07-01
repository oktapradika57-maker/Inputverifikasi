import streamlit as st
import gspread
import pandas as pd

# Konfigurasi koneksi ke Google Sheets
# Anda perlu file credentials.json dari Google Cloud Console
gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1HvgVicTWwO4RMQI6ZR3Mu3IgGicwjcLZl9mDN1auvJU')
worksheet = sh.sheet1 # Sesuaikan dengan nama sheet Anda

def get_data():
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

st.title("Sistem Verifikasi Transfer SWFM")

df = get_data()

# Input Nomor Tiket
ticket_id = st.text_input("Masukkan Nomor Tiket SWFM (Contoh: BPS-2026-000000034391)")

if ticket_id:
    # Cari baris yang sesuai
    row_idx = df.index[df['Nomor Tiket SWFM'] == ticket_id].tolist()
    
    if row_idx:
        st.success(f"Tiket ditemukan! Baris: {row_idx[0] + 2}")
        
        # Input Verifikasi
        status_verifikasi = st.selectbox("Status Verifikasi", ["Verified", "Pending", "Rejected"])
        
        if st.button("Simpan Verifikasi"):
            # Update kolom AD (kolom ke-30)
            worksheet.update_cell(row_idx[0] + 2, 30, status_verifikasi)
            st.success("Data berhasil diupdate!")
    else:
        st.error("Nomor Tiket tidak ditemukan dalam database.")
