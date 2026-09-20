import requests
from datetime import datetime

def bugscan(url):
    if not url.startswith("http"):
        url = "https://" + url

    print(f"[+] Scanning {url}...\n")
    hasil = [f"\n=== SCAN {url} | {datetime.now()} ==="]

    try:
        r = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})

        # [1] Security Headers (versi kamu yang 5)
        print("[1] Cek Security Headers:")
        headers_to_check = ["X-Frame-Options", "Content-Security-Policy", "X-XSS-Protection", "Strict-Transport-Security", "X-Content-Type-Options"]
        for h in headers_to_check:
            if h not in r.headers:
                msg = f" [-] MISSING: {h} -> potensi bug!"
                print(msg)
                hasil.append(msg)
            else:
                print(f" [+] Ada: {h}")

        # [2] robots.txt
        print("\n[2] Cek robots.txt:")
        robots_url = url.rstrip("/") + "/robots.txt"
        rr = requests.get(robots_url, timeout=5)
        if rr.status_code == 200:
            msg = f" [+] Ketemu robots.txt: {robots_url}"
            print(msg)
            hasil.append(msg)
        else:
            print(" [-] Tidak ada robots.txt")

        # [3] Deteksi Teknologi
        print("\n[3] Deteksi Teknologi:")
        for tech in ["Server", "X-Powered-By"]:
            if tech in r.headers:
                msg = f" [+] {tech}: {r.headers[tech]}"
                print(msg)
                hasil.append(msg)

        # [4] Cek HTTP Methods
        print("\n[4] Cek HTTP Methods:")
        try:
            mo = requests.options(url, timeout=5)
            allow = mo.headers.get("Allow", "tidak terdeteksi")
            print(f" [+] Allow: {allow}")
            if any(m in allow for m in ["PUT", "DELETE", "TRACE"]):
                msg = " [-] Method berbahaya aktif! -> potensi bug!"
                print(msg)
                hasil.append(msg)
        except:
            print(" [-] Gagal cek methods")

        # [5] BARU - OPEN REDIRECT SCANNER (Skill ceklink kamu kepake disini)
        print("\n[5] Cek Open Redirect:")
        payloads = ["/redirect?url=https://google.com", "/out?url=https://google.com", "/?next=https://google.com", "/?redirect=https://evil.com"]
        found_redirect = False
        for p in payloads:
            test_url = url.rstrip("/") + p
            try:
                # allow_redirects=False biar kita liat dia mau nge-redirect kemana
                res = requests.get(test_url, timeout=5, allow_redirects=False)
                if res.status_code in [301, 302, 303, 307, 308]:
                    loc = res.headers.get("Location", "")
                    if "google.com" in loc or "evil.com" in loc:
                        msg = f" [!] POTENSI OPEN REDIRECT: {test_url} -> {loc}"
                        print(msg)
                        hasil.append(msg)
                        found_redirect = True
            except:
                pass
        if not found_redirect:
            print(" [-] Tidak ada Open Redirect dari payload umum")

        # Simpan
        with open("hasil_scan.txt", "a") as f:
            for line in hasil:
                f.write(line + "\n")
        print("\n[✓] Laporan disimpan di hasil_scan.txt")

    except Exception as e:
        print(f"[ERROR] {e}")

target = input("Masukin target (contoh: google.com): ")
bugscan(target)
