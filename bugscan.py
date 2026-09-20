'PYEOF'
import requests

def bugscan(url):
    if not url.startswith("http"):
        url = "https://" + url

    print(f"[+] Scanning {url}...\n")
    hasil = [f"\n=== SCAN {url} ==="]

    try:
        r = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})

        # [1] Cek Security Headers - upgrade jadi 5
        print("[1] Cek Security Headers:")
        headers_to_check = ["X-Frame-Options", "Content-Security-Policy", "X-XSS-Protection", "Strict-Transport-Security", "X-Content-Type-Options"]
        for h in headers_to_check:
            if h not in r.headers:
                msg = f" [-] MISSING: {h} -> potensi bug!"
                print(msg)
                hasil.append(msg)
            else:
                print(f" [+] Ada: {h}")
                hasil.append(f" [+] Ada: {h}")

        # [2] Cek robots.txt (punya kamu, dipertahankan)
        print("\n[2] Cek robots.txt:")
        robots_url = url.rstrip("/") + "/robots.txt"
        rr = requests.get(robots_url, timeout=5)
        if rr.status_code == 200:
            msg = f" [+] Ketemu robots.txt: {robots_url}"
            print(msg)
            print(f" Isinya: {rr.text[:200]}...")
            hasil.append(msg)
            hasil.append(f" Isi preview: {rr.text[:200]}")
        else:
            print(" [-] Tidak ada robots.txt")

        # [3] BARU: Deteksi Teknologi
        print("\n[3] Deteksi Teknologi:")
        for tech in ["Server", "X-Powered-By"]:
            if tech in r.headers:
                msg = f" [+] {tech}: {r.headers[tech]}"
                print(msg)
                hasil.append(msg)

        # [4] BARU: Cek HTTP Methods berbahaya
        print("\n[4] Cek HTTP Methods:")
        try:
            mo = requests.options(url, timeout=5)
            allow = mo.headers.get("Allow", "tidak terdeteksi")
            print(f" [+] Allow: {allow}")
            hasil.append(f" Allow: {allow}")
            if any(m in allow for m in ["PUT", "DELETE", "TRACE"]):
                msg = " [-] Method berbahaya aktif! -> potensi bug!"
                print(msg)
                hasil.append(msg)
        except:
            print(" [-] Gagal cek methods")

        # Simpan laporan
        with open("hasil_scan.txt", "a") as f:
            for line in hasil:
                f.write(line + "\n")
        print("\n[✓] Laporan disimpan di hasil_scan.txt")

    except Exception as e:
        print(f"[ERROR] {e}")

target = input("Masukin target (contoh: google.com): ")
bugscan(target)

