const BASE = "http://localhost:8080/api/v1";

async function request(path, options = {}) {
  const url = `${BASE}${path}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
  return data;
}

// Editor
export function fetchEditorTemplate() {
  return request("/templates/editor");
}

// SymPy
export function fetchSympySession() {
  return request("/templates/sympy/session");
}

export function execSympyCode(code) {
  return request("/solve/exec", { method: "POST", body: JSON.stringify({ code }) });
}

export function resetSympySession() {
  return request("/solve/reset", { method: "POST" });
}

export function fetchSympySymbols() {
  return request("/solve/symbols");
}

export function evaluateExpression(expression) {
  return request("/solve/evaluate", { method: "POST", body: JSON.stringify({ expression }) });
}

export function simplifyExpression(expression) {
  return request("/solve/simplify", { method: "POST", body: JSON.stringify({ expression }) });
}

export function differentiateExpression(expression, variable = "x", order = 1) {
  return request("/solve/differentiate", {
    method: "POST",
    body: JSON.stringify({ expression, variable, order }),
  });
}

export function solveEquation(expression, variable = "x") {
  return request("/solve", { method: "POST", body: JSON.stringify({ expression, variable }) });
}

// Lean
export function fetchLeanTheorem() {
  return request("/templates/lean/theorem");
}

export function verifyTheorem(theorem, proof = "") {
  return request("/verify", { method: "POST", body: JSON.stringify({ theorem, proof }) });
}

export function fetchLeanTemplates() {
  return request("/verify/templates");
}

export function sympyToLean(expression) {
  return request("/verify/sympy-to-lean", {
    method: "POST",
    body: JSON.stringify({ expression, theorem_name: "auto" }),
  });
}

export function extractGoal(theorem) {
  return request("/verify/extract-goal", {
    method: "POST",
    body: JSON.stringify({ theorem }),
  });
}

// Explainer
export function fetchExplainerContent() {
  return request("/templates/explainer/content");
}

export function explainExpression(expression, level = "graduacao", style = "didatico") {
  return request("/explain", { method: "POST", body: JSON.stringify({ expression, level, style }) });
}

export function checkQuizAnswer(question, answer) {
  return request("/templates/quiz/check", {
    method: "POST",
    body: JSON.stringify({ question, answer }),
  });
}

// Series
export function seriesExpression(expression, variable = "x", point = "0", order = 6) {
  return request("/solve/series", {
    method: "POST",
    body: JSON.stringify({ expression, variable, point, order }),
  });
}

// Linear Systems
export function solveLinearSystem(equations, variables) {
  return request("/solve/linsolve", {
    method: "POST",
    body: JSON.stringify({ equations, variables }),
  });
}

// Export
export function exportDocument(content, format = "pdf") {
  return request("/export", { method: "POST", body: JSON.stringify({ content, format }) });
}
