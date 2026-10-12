"""Generate a Seedance 2.5 video on Replicate and log it.

Usage: python3 scripts/gen_video_replicate.py <out.mp4> <480p|720p> <ratio> <seconds> "<prompt>" <first.jpg> [last.jpg]
Reads REPLICATE_API_TOKEN from .env.local. Every run is appended to assets/PROMPTS.md.
"""
import base64, datetime, json, os, sys, time, urllib.request

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
MODEL = "bytedance/seedance-2.5"


def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:600]}")


def data_uri(path):
    return "data:image/jpeg;base64," + base64.b64encode(open(path, "rb").read()).decode()


out, res, ratio, seconds, prompt, first, *last = sys.argv[1:]
inp = {"prompt": prompt, "image": data_uri(first), "resolution": res, "aspect_ratio": ratio,
       "duration": int(seconds), "generate_audio": False, "watermark": False}
if last:
    inp["last_frame_image"] = data_uri(last[0])
p = call(f"https://api.replicate.com/v1/models/{MODEL}/predictions", {"input": inp})
while p["status"] not in ("succeeded", "failed", "canceled"):
    time.sleep(10)
    p = call(p["urls"]["get"])
if p["status"] != "succeeded":
    sys.exit(f"{out}: {p['status']} {p.get('error')}")
src = p["output"] if isinstance(p["output"], str) else p["output"][0]
urllib.request.urlretrieve(src, out)
with open(os.path.join(ROOT, "assets", "PROMPTS.md"), "a") as log:
    log.write(f"\n### {os.path.relpath(out, ROOT)}\n- {datetime.date.today()} · {MODEL} · {res} · {ratio} · {seconds}s · "
              f"first: {first}{' · last: ' + last[0] if last else ''} · prediction {p['id']}\n\n> {prompt}\n")
print(out, "ok · prediction", p["id"], "· predict_time", p.get("metrics", {}).get("predict_time"))
