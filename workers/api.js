// Cloudflare Workers — 轻量 API 模板
// 限制：100,000 请求/天，每请求 CPU 10ms，内存 128MB
// 用法：把 OPENROUTER_API_KEY 设为 Worker secret，不要写进代码
// wrangler secret put OPENROUTER_API_KEY
// 部署：npx wrangler deploy

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/health") {
      return Response.json({ ok: true, ts: new Date().toISOString() });
    }

    if (url.pathname === "/chat" && request.method === "POST") {
      const body = await request.json().catch(() => ({}));
      const prompt = String(body.prompt || "").slice(0, 2000);
      if (!prompt) return Response.json({ error: "prompt required" }, { status: 400 });

      // OpenRouter 免费档：20/min，50/day。模型不要硬编码，
      // 部署前查 https://openrouter.ai/collections/free-models/ 实时名单
      const model = body.model || "openrouter/free";
      const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${env.OPENROUTER_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model,
          messages: [{ role: "user", content: prompt }],
        }),
      });
      const data = await res.json().catch(() => ({}));
      return Response.json(data, { status: res.status });
    }

    return Response.json({ error: "not found" }, { status: 404 });
  },
};
