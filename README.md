# Termux-tools

Kumpulan tools sederhana untuk Termux (Python 100%).

## Tools
- `ceklink.py` - Cek URL pakai VirusTotal API
  ```bash
  export VT_API_KEY="isi-key-kamu"
  python ceklink.py https://contoh.com
bugscan.py - Scan ringan buat bug hunter (cek security headers, robots.txt, deteksi server, cek HTTP methods)
  pip install requests
  python bugscan.py
Keamanan
Jangan pernah upload API key ke GitHub. Selalu pakai os.getenv("VT_API_KEY").
