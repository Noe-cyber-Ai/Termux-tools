target = input("Target domain (contoh: example.com): ").strip().replace("https://","").replace("http://","").split("/")[0]

dorks = [
    f'site:{target} filetype:pdf',
    f'site:{target} filetype:xls OR filetype:xlsx',
    f'site:{target} inurl:admin',
    f'site:{target} inurl:login',
    f'site:{target} "index of"',
    f'site:{target} intext:"password"',
    f'site:{target} ext:log',
    f'site:{target} ext:sql',
]

print(f"\n[+] Dork untuk {target}:\n")
for d in dorks:
    print(d)
    # bikin link google langsung
    import urllib.parse
    q = urllib.parse.quote_plus(d)
    print(f" -> https://www.google.com/search?q={q}\n")

print("[✓] Copy dork di atas ke Google")
