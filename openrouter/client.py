"""OpenRouter 免费模型客户端模板
免费档：:free 模型 $0，20 请求/分钟，50 请求/天（UTC 午夜重置）
名单轮换很快：部署前先查 https://openrouter.ai/collections/free-models/
不要硬编码某个免费模型；充 $10 积分后日限升到 1,000/天。
用法：OPENROUTER_API_KEY=<key> python3 client.py "你好"
"""
import os, sys, json, urllib.request

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
BASE = "https://openrouter.ai/api/v1"

def list_free_models():
    req = urllib.request.Request(
        f"{BASE}/models",
        headers={"Authorization": f"Bearer {API_KEY}"} if API_KEY else {},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    free = [m["id"] for m in data.get("data", []) if m["id"].endswith(":free")]
    return free

def chat(prompt, model="openrouter/free"):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        f"{BASE}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

if __name__ == "__main__":
    if not API_KEY:
        print("先设 OPENROUTER_API_KEY")
        raise SystemExit(1)
    print("免费模型（实时）：", list_free_models())
    print(json.dumps(chat(sys.argv[1] if len(sys.argv) > 1 else "你好"), ensure_ascii=False, indent=2))
