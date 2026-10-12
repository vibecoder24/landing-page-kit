"""Generate one still with OpenAI GPT Image 2 on Replicate and log the prompt.

Usage: python3 scripts/gen_image_openai.py <out.png> <aspect> <low|medium|high> <opaque|transparent> "<prompt>" [ref1 ref2 ...]
Low quality is for trying compositions cheaply; re-run the keepers at high.
Reads REPLICATE_API_TOKEN from .env.local. Every run is appended to assets/PROMPTS.md.
"""
import base64, datetime, json, mimetypes, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.path.join(ROOT, ".env.local")
if os.path.exists(ENV):
    for line in open(ENV):
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ.setdefault(k, v)
TOKEN = os.environ.get("REPLICATE_API_TOKEN")
if not TOKEN:
    sys.exit("REPLICATE_API_TOKEN is not set. Copy site/.env.example to site/.env.local and add your token "
             "(https://replicate.com/account/api-tokens). .env.local is git-ignored; never commit it.")
MODEL = "openai/gpt-image-2"


def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json", "Prefer": "wait=60"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=180))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:600]}")


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


out, aspect, quality, background, prompt, *refs = sys.argv[1:]
inp = {"prompt": prompt, "aspect_ratio": aspect, "quality": quality, "background": background, "output_format": "png"}
if refs:
    inp["input_images"] = [data_uri(r) for r in refs]
p = call(f"https://api.replicate.com/v1/models/{MODEL}/predictions", {"input": inp})
while p["status"] not in ("succeeded", "failed", "canceled"):
    time.sleep(3)
    p = call(p["urls"]["get"])
if p["status"] != "succeeded":
    sys.exit(f"{out}: {p['status']} {p.get('error')}")
src = p["output"] if isinstance(p["output"], str) else p["output"][0]
urllib.request.urlretrieve(src, out)
with open(os.path.join(ROOT, "assets", "PROMPTS.md"), "a") as log:
    log.write(f"\n### {os.path.relpath(out, ROOT)}\n- {datetime.date.today()} · {MODEL} · {aspect} · {quality} · {background}"
              f"{' · refs: ' + ', '.join(refs) if refs else ''} · prediction {p['id']}\n\n> {prompt}\n")
print(out, "ok · prediction", p["id"])
