import { useState, useEffect } from "react";

function Settings() {
  const [activeTab, setActiveTab] = useState("projects");
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    const stored = localStorage.getItem("mathtools-projects");
    if (stored) {
      try { setProjects(JSON.parse(stored)); } catch {}
    }
  }, []);

  function saveProjects(list) {
    setProjects(list);
    localStorage.setItem("mathtools-projects", JSON.stringify(list));
  }

  function createProject() {
    const name = prompt("Project name:");
    if (!name) return;
    saveProjects([...projects, { id: Date.now(), name, created: new Date().toISOString(), documents: [] }]);
  }

  function deleteProject(id) {
    saveProjects(projects.filter((p) => p.id !== id));
  }

  return (
    <div style={{ flex: 1, overflow: "auto", padding: "32px", maxWidth: "800px", margin: "0 auto" }}>
      <h2 style={{ fontSize: "24px", fontWeight: 700, color: "var(--primary)", marginBottom: "24px" }}>
        Settings & Diagnostics
      </h2>

      <div style={{ display: "flex", gap: "4px", marginBottom: "24px", borderBottom: "1px solid var(--outline-variant)" }}>
        {["projects", "performance", "diagnostics", "profiles"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: "8px 16px", border: "none", background: "none",
              color: activeTab === tab ? "var(--primary)" : "var(--on-surface-variant)",
              fontWeight: 700, fontSize: "12px", letterSpacing: "0.05em",
              borderBottom: activeTab === tab ? "2px solid var(--primary)" : "2px solid transparent",
              cursor: "pointer", textTransform: "uppercase",
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {activeTab === "projects" && (
        <div>
          <button
            onClick={createProject}
            style={{
              padding: "8px 16px", background: "var(--primary)", color: "var(--on-primary)",
              border: "none", borderRadius: "var(--radius)", fontWeight: 700, cursor: "pointer",
              marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px",
            }}
          >
            <span className="material-symbols-outlined" style={{ fontSize: "16px" }}>add</span>
            New Project
          </button>
          {projects.length === 0 && (
            <p style={{ color: "var(--on-surface-variant)", fontStyle: "italic" }}>No projects yet. Create one to get started.</p>
          )}
          {projects.map((p) => (
            <div
              key={p.id}
              style={{
                display: "flex", alignItems: "center", justifyContent: "space-between",
                padding: "12px 16px", border: "1px solid var(--outline-variant)",
                borderRadius: "var(--radius-lg)", marginBottom: "8px",
                background: "var(--surface-container-lowest)",
              }}
            >
              <div>
                <div style={{ fontWeight: 700, color: "var(--on-surface)" }}>{p.name}</div>
                <div style={{ fontSize: "11px", color: "var(--on-surface-variant)" }}>
                  Created: {new Date(p.created).toLocaleDateString()}
                </div>
              </div>
              <button
                onClick={() => deleteProject(p.id)}
                style={{ background: "none", border: "none", color: "var(--error)", cursor: "pointer" }}
              >
                <span className="material-symbols-outlined">delete</span>
              </button>
            </div>
          ))}
          <p style={{ fontSize: "11px", color: "var(--on-surface-variant)", marginTop: "8px" }}>
            Projects are stored locally in your browser. In the Tauri desktop build, they sync to SQLite.
          </p>
        </div>
      )}

      {activeTab === "performance" && (
        <div>
          <p style={{ color: "var(--on-surface-variant)", marginBottom: "16px" }}>
            Choose the performance mode that best fits your hardware and battery preferences.
          </p>
          {[
            { id: "economy", label: "Econômico", desc: "Minimiza uso de CPU/RAM. Ideal para bateria ou máquinas modestas.", icon: "battery_saver" },
            { id: "balanced", label: "Balanceado", desc: "Equilíbrio entre desempenho e consumo. Padrão recomendado.", icon: "balance" },
            { id: "maximum", label: "Máximo", desc: "Usa todos os recursos disponíveis. Melhor para tarefas pesadas.", icon: "bolt" },
          ].map((m) => (
            <label
              key={m.id}
              style={{
                display: "flex", gap: "12px", padding: "16px",
                border: "1px solid var(--outline-variant)", borderRadius: "var(--radius-lg)",
                marginBottom: "8px", cursor: "pointer", background: "var(--surface-container-lowest)",
                alignItems: "flex-start",
              }}
            >
              <input type="radio" name="perf" value={m.id} defaultChecked={m.id === "balanced"} />
              <div>
                <div style={{ fontWeight: 700, display: "flex", alignItems: "center", gap: "8px" }}>
                  <span className="material-symbols-outlined" style={{ fontSize: "16px", color: "var(--primary)" }}>{m.icon}</span>
                  {m.label}
                </div>
                <div style={{ fontSize: "12px", color: "var(--on-surface-variant)" }}>{m.desc}</div>
              </div>
            </label>
          ))}
        </div>
      )}

      {activeTab === "diagnostics" && (
        <div>
          <p style={{ color: "var(--on-surface-variant)", marginBottom: "16px" }}>
            Run diagnostics to verify that all MathTools components are working correctly.
          </p>
          <DiagnosticRun />
        </div>
      )}

      {activeTab === "profiles" && (
        <div>
          <p style={{ color: "var(--on-surface-variant)", marginBottom: "16px" }}>
            Choose your profile to customize the interface, explanation level, and features.
          </p>
          {[
            { id: "researcher", label: "Pesquisador", icon: "science", desc: "Foco em verificação formal, manipulação simbólica avançada e exportação." },
            { id: "professor", label: "Professor", icon: "school", desc: "Foco em explicações didáticas, visualizações e criação de material didático." },
            { id: "student", label: "Estudante", icon: "psychology", desc: "Foco em aprendizado passo a passo, tutoriais e exercícios." },
            { id: "self-taught", label: "Autodidata", icon: "person", desc: "Acesso completo a todas as ferramentas com explicações adaptativas." },
            { id: "developer", label: "Desenvolvedor/Físico", icon: "code", desc: "Foco em console SymPy, Lean 4 e integração com ferramentas externas." },
          ].map((p) => (
            <div
              key={p.id}
              style={{
                display: "flex", gap: "12px", padding: "16px",
                border: "1px solid var(--outline-variant)", borderRadius: "var(--radius-lg)",
                marginBottom: "8px", cursor: "pointer", background: "var(--surface-container-lowest)",
                alignItems: "flex-start",
              }}
            >
              <span className="material-symbols-outlined" style={{ color: "var(--primary)" }}>{p.icon}</span>
              <div>
                <div style={{ fontWeight: 700 }}>{p.label}</div>
                <div style={{ fontSize: "12px", color: "var(--on-surface-variant)" }}>{p.desc}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function DiagnosticRun() {
  const [results, setResults] = useState(null);
  const [running, setRunning] = useState(false);

  async function runTests() {
    setRunning(true);
    const res = [];

    res.push({ name: "Backend Health", status: "testing" });
    try {
      const health = await fetch("http://localhost:8080/api/v1/health");
      const data = await health.json();
      res[0] = { name: "Backend Health", status: data.status === "ok" ? "pass" : "fail", detail: JSON.stringify(data) };
    } catch (e) {
      res[0] = { name: "Backend Health", status: "fail", detail: e.message };
    }

    res.push({ name: "SymPy Engine", status: "testing" });
    try {
      const r = await fetch("http://localhost:8080/api/v1/solve/evaluate", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression: "2+2" }),
      });
      const d = await r.json();
      res[1] = { name: "SymPy Engine", status: d.ok && d.result === "4" ? "pass" : "fail", detail: d.result || "unexpected" };
    } catch (e) {
      res[1] = { name: "SymPy Engine", status: "fail", detail: e.message };
    }

    res.push({ name: "Lean Bridge", status: "testing" });
    try {
      const r = await fetch("http://localhost:8080/api/v1/verify/templates");
      const d = await r.json();
      res[2] = { name: "Lean Bridge", status: Array.isArray(d) && d.length >= 4 ? "pass" : "fail", detail: `${d.length || 0} templates` };
    } catch (e) {
      res[2] = { name: "Lean Bridge", status: "fail", detail: e.message };
    }

    res.push({ name: "Explainer Engine", status: "testing" });
    try {
      const r = await fetch("http://localhost:8080/api/v1/explain", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression: "derivative", level: "medio", style: "conciso" }),
      });
      const d = await r.json();
      res[3] = { name: "Explainer Engine", status: d.ok ? "pass" : "fail", detail: d.source || "rule-based" };
    } catch (e) {
      res[3] = { name: "Explainer Engine", status: "fail", detail: e.message };
    }

    res.push({ name: "Typst Export", status: "testing" });
    try {
      const r = await fetch("http://localhost:8080/api/v1/export", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: "$x^2$", format: "pdf" }),
      });
      const d = await r.json();
      res[4] = { name: "Typst Export", status: d.ok ? "pass" : "warn", detail: d.ok ? "ready" : d.error?.substring(0, 60) };
    } catch (e) {
      res[4] = { name: "Typst Export", status: "fail", detail: e.message };
    }

    setResults(res);
    setRunning(false);
  }

  return (
    <div>
      <button
        onClick={runTests}
        disabled={running}
        style={{
          padding: "8px 16px", background: "var(--primary)", color: "var(--on-primary)",
          border: "none", borderRadius: "var(--radius)", fontWeight: 700, cursor: "pointer",
          marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px",
        }}
      >
        <span className="material-symbols-outlined" style={{ fontSize: "16px" }}>diagnosis</span>
        {running ? "Running..." : "Run Diagnostics"}
      </button>

      {results && (
        <div>
          {results.map((r, i) => (
            <div
              key={i}
              style={{
                display: "flex", alignItems: "center", gap: "12px",
                padding: "10px 12px", marginBottom: "6px",
                borderRadius: "var(--radius)", fontSize: "13px",
                background: r.status === "pass" ? "rgba(46,125,50,0.08)" : r.status === "warn" ? "rgba(255,179,0,0.08)" : "rgba(211,47,47,0.08)",
                border: `1px solid ${r.status === "pass" ? "#2e7d32" : r.status === "warn" ? "#ffb300" : "#d32f2f"}`,
              }}
            >
              <span className="material-symbols-outlined" style={{ fontSize: "18px", color: r.status === "pass" ? "#2e7d32" : r.status === "warn" ? "#ffb300" : "#d32f2f" }}>
                {r.status === "pass" ? "check_circle" : r.status === "warn" ? "warning" : "error"}
              </span>
              <div>
                <div style={{ fontWeight: 700 }}>{r.name}</div>
                <div style={{ fontSize: "11px", color: "var(--on-surface-variant)" }}>{r.detail}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Settings;
