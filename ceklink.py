import os, requests
from urllib.parse import urlparse
from datetime import datetime

import os
KEY = os.getenv("VT_API_KEY")

def get_final_url(url):
    try:
        u = url if url.startswith("http") else "http://" + url
        r = requests.get(u, timeout=10, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        chain = [h.url for h in r.history] + [r.url]
        return r.url, chain
    except Exception as e:
        return url, [f"Gagal follow: {e}"]

def cek_http(url):
    try:
        u = url if url.startswith("http") else "http://" + url
        r = requests.head(u, timeout=5, allow_redirects=True)
        return str(r.status_code)
    except:
        return "FAIL"

def cek_whois(domain):
    curiga = ["bansos","gratis","giveaway","login","verifikasi","whatsapp","bonus"]
    if any(k in domain for k in curiga) or len(domain)>28 or domain.count("-")>2:
        return "TIDAK TERDAFTAR"
    return "TERDAFTAR"

def cek_vt_real(url):
    if not VT_API_KEY:
        return "VT: API Key belum di-set"
    try:
        headers = {"x-apikey": VT_API_KEY}
        import base64
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        r = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            stats = data['data']['attributes']['last_analysis_stats']
            mal = stats.get('malicious',0)
            return f"VT: {mal} deteksi BAHAYA / {stats.get('harmless',0)} aman"
        else:
            return f"VT: Belum pernah di-scan (atau baru), kode {r.status_code}"
    except Exception as e:
        return f"VT: Gagal cek - {e}"

def laporan(url):
    url=url.strip()
    if not url: return

    # Follow redirect dulu
    final_url, chain = get_final_url(url)
    url_cek = final_url

    dom = urlparse(url_cek if url_cek.startswith("http") else "http://"+url_cek).netloc or url_cek.split("/")[0]
    http = cek_http(url_cek)
    whois = cek_whois(dom)
    vt = cek_vt_real(url_cek)

    bahaya = whois=="TIDAK TERDAFTAR" or http=="FAIL" or ("deteksi BAHAYA" in vt and "0 deteksi" not in vt)

    if bahaya:
        hasil=">>> BAHAYA / PHISING <<<"; emoji="🚨"; saran="JANGAN DIKLIK!"
    else:
        hasil=">>> AMAN <<<"; emoji="✅"; saran="Terlihat aman."

    redirect_info = "\n".join([f" -> {u}" for u in chain])

    pesan=f"""{emoji} [CEK LINK v9 - {datetime.now().strftime('%d/%m %H:%M')}]
Link awal: {url}
URL Final: {final_url}
Redirect chain:
{redirect_info}
Domain: {dom}
WHOIS: {whois} | HTTP: {http}
{vt}
Hasil: {hasil}
{saran}
"""
    print(pesan)
    with open("hasil_phising.txt","a",encoding="utf-8") as f:
        f.write(pesan+"\n"+"="*50+"\n")
    print("[✓] Tersimpan -> hasil_phising.txt\n")

print("=== CEK LINK v9 FINAL (VT Real + Follow Redirect) ===")
print(f"VT Key: {'AKTIF ✓' if VT_API_KEY else 'MATI - export dulu'}")
p=input("1. Satu link\n2. Massal list.txt\nPilih: ")
if p=="1":
    laporan(input("Link: "))
else:
    if not os.path.exists("list.txt"): print("Buat list.txt dulu")
    else:
        for l in open("list.txt"): laporan(l)
