import os
import json
import shutil
from tqdm import tqdm
import hashlib

def calculate_fingerprint_hash(canvas, webgl, width, height):
    """
    Menghitung hash fingerprint berdasarkan kombinasi canvas, webgl, width, dan height.
    
    :param canvas: Nilai dari canvas.
    :param webgl: Nilai dari webgl.
    :param width: Lebar perangkat.
    :param height: Tinggi perangkat.
    :return: Hash dari kombinasi canvas, webgl, width, dan height.
    """
    # Gabungkan semua informasi menjadi satu string dan hitung hash-nya
    fingerprint_string = f"{canvas}|{webgl}|{width}|{height}"
    return hashlib.sha256(fingerprint_string.encode('utf-8')).hexdigest()

def scan_folder(source_folder, target_folder):
    """
    Memindai folder sumber yang berisi file JSON, dan memindahkan file dengan fingerprint unik ke folder tujuan.
    
    :param source_folder: Folder yang berisi file JSON yang ingin dipindai.
    :param target_folder: Folder tujuan untuk file dengan fingerprint unik.
    """
    # Membuat folder target jika belum ada
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # Menyimpan set hash fingerprint unik untuk membandingkan file
    seen_fingerprints = set()

    # Mendapatkan daftar semua file JSON dalam folder sumber
    files = [f for f in os.listdir(source_folder) if f.endswith('.json')]
    
    # Progress bar untuk memantau pemrosesan
    with tqdm(total=len(files), desc="Scanning files", unit="file") as pbar:
        for file_name in files:
            file_path = os.path.join(source_folder, file_name)
            
            # Membaca konten file JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    # Skip file jika ada error dalam parsing JSON
                    pbar.update(1)
                    continue
            
            # Mengambil nilai canvas, webgl, width, dan height
            canvas = data.get('perfectcanvas', {}).get('2452430454', '')
            webgl = data.get('perfectcanvas', {}).get('2950473529', '')
            width = data.get('width', None)
            height = data.get('height', None)
            
            # Menghitung hash fingerprint dari nilai canvas, webgl, width, dan height
            fingerprint_hash = calculate_fingerprint_hash(canvas, webgl, width, height)

            # Mengecek apakah hash fingerprint sudah ada, jika belum, pindahkan file
            if fingerprint_hash not in seen_fingerprints:
                seen_fingerprints.add(fingerprint_hash)
                shutil.copy(file_path, os.path.join(target_folder, file_name))
            
            # Memperbarui progress bar
            pbar.update(1)

if __name__ == "__main__":
    # Ganti dengan folder sumber Anda
    source_folder = r'D:\FP'  # Misalnya: 'C:/data/json_files'
    
    # Ganti dengan folder tujuan Anda
    target_folder = r'D:\FPhasil'  # Misalnya: 'C:/data/unique_fingerprints'
    
    # Panggil fungsi untuk mulai pemindaian dan pemindahan file unik
    scan_folder(source_folder, target_folder)
