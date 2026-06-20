#!/usr/bin/env python3
"""GEO Engine — deploy config-driven a Netlify (file-digest) + IndexNow.
Uso: python3 deploy.py <config.json> [--no-indexnow]

Lee config["site_dir"] y config["_deploy"]["netlify_site_id"]. Deploya TODO el
site_dir (file-digest atomico) excluyendo dirs/ext/nombres internos, luego pingea
IndexNow (Bing + IndexNow.org) con las URLs de la seccion GEO.

Token Netlify: ~/.config/vraven/netlify.token  (regex tolera comentario + espacio).
"""
import os, re, json, sys, hashlib, time, urllib.request, urllib.error, pathlib
from urllib.parse import quote

CFG = json.load(open(sys.argv[1]))
NO_INDEXNOW = "--no-indexnow" in sys.argv
SITE_DIR = CFG["site_dir"]
SITE_ID = CFG["_deploy"]["netlify_site_id"]
DOMAIN = CFG["domain"]
HOST = DOMAIN.split("//")[1].rstrip("/")

TOKEN = re.search(r'NETLIFY_DEPLOY_TOKEN=\s*([A-Za-z0-9_\-]+)',
                  open(os.path.expanduser("~/.config/vraven/netlify.token")).read()).group(1)

# excludes: dirs/ext/nombres que NUNCA se sirven (internos)
EXCLUDE_DIRS = set(CFG["_deploy"].get("exclude_dirs", ['.claude','sales','anim','.git','__pycache__']))
EXCLUDE_EXT  = set(CFG["_deploy"].get("exclude_ext",  ['.py','.pyc','.md']))
EXCLUDE_NAMES= set(CFG["_deploy"].get("exclude_names",['.DS_Store','LEEME.txt']))
# whitelist de .md a servir igual (ej. ninguno por defecto)
KEEP = set(CFG["_deploy"].get("keep", []))

def api(method, url, data=None, ctype="application/json"):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}"); req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]

def included(path, name):
    if name in EXCLUDE_NAMES: return name in KEEP
    ext = os.path.splitext(name)[1].lower()
    if ext in EXCLUDE_EXT: return ("/"+name) in KEEP or name in KEEP
    return True

# ---- build digest ----
os.chdir(SITE_DIR)
files = {}
INCLUDE = CFG["_deploy"].get("include")  # allowlist explicito (paths relativos). Si existe, modo seguro.
SECTION_GLOB = CFG["_deploy"].get("section_glob", CFG["section_dir"])  # dir de la seccion GEO a incluir entero
if INCLUDE:
    # modo allowlist: SOLO estos archivos + todo el dir de la seccion GEO. Seguro para dirs "sucios".
    explicit = list(INCLUDE)
    secdir = pathlib.Path(SITE_DIR) / CFG["section_dir"]
    if secdir.exists():
        explicit += [str(p.relative_to(SITE_DIR)) for p in secdir.rglob("*") if p.is_file()]
    secidx = f'{CFG["section_dir"]}.html'
    if (pathlib.Path(SITE_DIR)/secidx).exists(): explicit.append(secidx)
    missing = [r for r in explicit if not os.path.exists(r)]
    if missing: print("WARN faltan en include:", missing[:10])
    for rel in explicit:
        if os.path.exists(rel):
            files["/"+rel] = (rel, hashlib.sha1(open(rel,'rb').read()).hexdigest())
else:
    for root, dirs, fs in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in fs:
            if not included(root, f): continue
            p = os.path.join(root, f); rel = p[1:]
            files[rel] = (p, hashlib.sha1(open(p,'rb').read()).hexdigest())

st, site = api("GET", f"https://api.netlify.com/api/v1/sites/{SITE_ID}")
print(f"site: {site.get('name')} | domain: {site.get('custom_domain')} | files: {len(files)}")

st, dep = api("POST", f"https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys",
              json.dumps({"files": {r:s for r,(_,s) in files.items()}, "draft": False}).encode())
if st not in (200,201): print("ERROR create:", st, dep); sys.exit(1)
did = dep["id"]; required = set(dep.get("required", [])); up = 0; fail = []
for rel,(p,sha) in files.items():
    if sha in required:
        st,_ = api("PUT", f"https://api.netlify.com/api/v1/deploys/{did}/files"+quote(rel),
                   open(p,'rb').read(), "application/octet-stream")
        if st in (200,201): up += 1
        else: fail.append((rel,st))
for _ in range(45):
    st,d = api("GET", f"https://api.netlify.com/api/v1/deploys/{did}")
    if d.get("state") in ("ready","error"): break
    time.sleep(2)
print(f"deploy {did}: subidos {up} | state {d.get('state')} | fallos {fail[:3]}")

# ---- IndexNow ----
if not NO_INDEXNOW:
    runner = pathlib.Path(__file__).parent
    res_file = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].endswith(".json") else None
    # urls de la seccion: leer slugs del result.json si se pasa, si no del sitemap_fragment
    slugs = []
    rj = CFG["_deploy"].get("result_json")
    if rj and os.path.exists(rj):
        slugs = [a["slug"] for a in json.load(open(rj))["articles"]]
    base = DOMAIN + CFG["section_path"]
    urls = [base] + [f"{base}/{s}" for s in slugs] + [f"{DOMAIN}/llms.txt"]
    KEY = CFG["_deploy"].get("indexnow_key")
    if KEY and slugs:
        payload = json.dumps({"host":HOST,"key":KEY,"keyLocation":f"{DOMAIN}/{KEY}.txt","urlList":urls}).encode()
        for ep in ["https://api.indexnow.org/indexnow","https://www.bing.com/indexnow"]:
            req=urllib.request.Request(ep,data=payload,method="POST");req.add_header("Content-Type","application/json")
            try:
                with urllib.request.urlopen(req,timeout=30) as r: print(f"IndexNow {ep.split('//')[1].split('/')[0]}: HTTP {r.status} ({len(urls)} urls)")
            except urllib.error.HTTPError as e: print(f"IndexNow {ep}: HTTP {e.code}")
    else:
        print("IndexNow: skip (falta indexnow_key y/o result_json en _deploy). Crear key file en raiz primero.")

print("DONE")
