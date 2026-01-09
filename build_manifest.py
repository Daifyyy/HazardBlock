import hashlib, json, base64, pathlib
from nacl.signing import SigningKey

# TODO: uprav USERNAME
GITHUB_USER = "TVUJ_USERNAME"
REPO = "HazardBlock"
BRANCH = "main"
BASE_RAW = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/{BRANCH}/"

FILES = ["gambling.txt", "ads.txt", "affiliate.txt", "doh.txt"]

# Vlož PRIVATE_KEY_BASE64 z gen_keys.py
PRIVATE_KEY_B64 = "SEM_VLOZ_PRIVATE_KEY_BASE64"

sk = SigningKey(base64.b64decode(PRIVATE_KEY_B64))

def sha256_hex(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

files = []
for fn in FILES:
    p = pathlib.Path("lists") / fn
    if not p.exists():
        raise SystemExit(f"Missing file: {p}")
    files.append({
        "id": fn.replace(".txt",""),
        "url": f"{BASE_RAW}lists/{fn}",
        "sha256": sha256_hex(p),
        "minAppVersion": 1
    })

manifest = {
    "version": 1,
    "publishedAt": "2026-01-08T00:00:00Z",
    "ttlHours": 6,
    "files": files
}

# deterministický JSON (důležité kvůli podpisu)
manifest_bytes = json.dumps(manifest, separators=(",", ":"), sort_keys=True).encode("utf-8")
sig = sk.sign(manifest_bytes).signature

pathlib.Path("manifest.json").write_bytes(manifest_bytes)
pathlib.Path("manifest.sig").write_text(base64.b64encode(sig).decode("ascii"))

print("OK: wrote manifest.json and manifest.sig")
