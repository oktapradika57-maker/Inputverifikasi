import streamlit as st
import gspread
import pandas as pd

st.title("Sistem Verifikasi Transfer SWFM")

# 1. Mengambil kredensial dari nama yang benar (gcp_service_account)
try:
    creds_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(creds_dict)
except Exception as e:
    st.error(f"Gagal memuat kredensial: {e}")
    st.stop()

# 2. Hubungkan ke Google Sheets
try:
    sh = gc.open_by_key('1HvgVicTWwO4RMQI6ZR3Mu3IgGicwjcLZl9mDN1auvJU')
    worksheet = sh.worksheet("Form Request dana") # Pastikan nama sheet ini benar
except Exception as e:
    st.error(f"Gagal terhubung ke Google Sheets: {e}")
    st.stop()

# 3. Tarik data
def get_data():
    return pd.DataFrame(worksheet.get_all_records())

df = get_data()

# 4. Form Input Pencarian
nama_kolom_tiket = "Nomor Tiket SWFM ( tulis cth BPS-2026-000000034391)"
ticket_id = st.text_input(f"Masukkan {nama_kolom_tiket}")

if ticket_id:
    # Validasi jika Nomor Tiket cocok
    if ticket_id in df[nama_kolom_tiket].values:
        # Hitung posisi baris (+2 karena header di sheet ada di baris 1, dan pandas index mulai dari 0)
        row_idx = df.index[df[nama_kolom_tiket] == ticket_id].tolist()[0] + 2
        
        st.success(f"Tiket {ticket_id} ditemukan!")
        
        # 5. Form Input Verifikasi
        status_verifikasi = st.selectbox("Pilih Status Verifikasi Transfer", ["Sudah Transfer", "Pending", "Ditolak"])
        
        if st.button("Simpan Verifikasi"):
            try:
                # Update kolom AD (Verifikasi Transfer)
                worksheet.update_acell(f'AD{row_idx}', status_verifikasi)
                st.success(f"Berhasil! Data tiket {ticket_id} di kolom AD telah diupdate menjadi '{status_verifikasi}'.")
            except Exception as e:
                st.error(f"Gagal mengupdate data: {e}")
    else:
        st.error("Nomor Tiket tidak ditemukan di dalam database.")
