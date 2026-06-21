const BASE_URL = "http://localhost:8080/api/v1";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export function useApi() {
  return {
    solve: (expression, variable = "x") =>
      request("/solve", { method: "POST", body: JSON.stringify({ expression, variable }) }),

    explain: (expression, level = "graduacao") =>
      request("/explain", { method: "POST", body: JSON.stringify({ expression, level }) }),

    verify: (theorem, proof = "") =>
      request("/verify", { method: "POST", body: JSON.stringify({ theorem, proof }) }),

    export: (content, format = "pdf") =>
      request("/export", { method: "POST", body: JSON.stringify({ content, format }) }),
  };
}
