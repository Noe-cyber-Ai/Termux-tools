# Termux-tools

Kumpulan tools sederhana untuk Termux (Python 100%).

## Tools
- `ceklink.py` - Cek URL pakai VirusTotal API

## Cara Pakai

1. Daftar di virustotal.com buat dapetin API key gratis
2. Set API key sebagai environment variable:
```bash
export VT_API_KEY="isi-key-kamu-disini"
python ceklink.py https://contoh-link.com
Keamanan
Jangan pernah upload API key ke GitHub. Selalu pakai os.getenv("VT_API_KEY").

---
Dibuat dengan ❤️ di Termux
