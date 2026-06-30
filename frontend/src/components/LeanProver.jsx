import { useState, useEffect } from "react";
import { fetchLeanTheorem, verifyTheorem, extractGoal } from "../lib/api.js";

function LeanProver() {
  const [data, setData] = useState(null);
  const [code, setCode] = useState("");
  const [goal, setGoal] = useState(null);
  const [messages, setMessages] = useState([]);
  const [verifying, setVerifying] = useState(false);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchLeanTheorem()
      .then((res) => {
        setData(res);
        setCode(res.code);
        if (res.context) {
          setGoal({ context: res.context, target: res.goal || "" });
        }
        setStatus("ready");
      })
      .catch((err) => {
        setError("Failed to load theorem: " + err.message);
        setStatus("error");
      });
  }, []);

  async function handleVerify() {
    setVerifying(true);
    setMessages([...messages, { level: "info", message: "Verifying..." }]);
    try {
      const result = await verifyTheorem(code);
      const diag = result.diagnostics || [];
      setMessages(diag);
      if (result.verified) {
        setMessages([
          ...diag,
          {
            level: "info",
            message:
              "All goals proved. Use `#check helix_curvature` to inspect the theorem signature.",
          },
        ]);
      }
      // Try to extract goal
      try {
        const g = await extractGoal(code);
        if (g.context || g.target) {
          setGoal(g);
        }
      } catch (e) {
        // keep existing goal
      }
    } catch (err) {
      setMessages([...messages, { level: "error", message: err.message }]);
    }
    setVerifying(false);
  }

  async function handleTactic(tactic) {
    const lines = code.split("\n");
    const proofStart = lines.findIndex((l) => l.trim().startsWith("by"));
    if (proofStart >= 0) {
      // append the tactic after the `by` line
      const indent = lines[proofStart].match(/^\s*/)[0] + "  ";
      lines.splice(proofStart + 1, 0, `${indent}${tactic}`);
      const newCode = lines.join("\n");
      setCode(newCode);
      // Auto-verify after tactic
      setTimeout(() => handleVerify(), 100);
    }
  }

  async function handleRefreshGoal() {
    try {
      const g = await extractGoal(code);
      if (g.context || g.target) setGoal(g);
    } catch (_) {}
  }

  if (status === "loading") {
    return (
      <div className="lean-workspace">
        <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
          Loading theorem...
        </div>
      </div>
    );
  }

  const lines = code.split("\n");

  return (
    <div className="lean-workspace">
      <aside className="lean-file-tree">
        <button className="lean-file-btn active" title="Theorem Explorer">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>
            account_tree
          </span>
        </button>
        <button className="lean-file-btn" title="Search Tactics">
          <span className="material-symbols-outlined">search</span>
        </button>
        <button className="lean-file-btn" title="Imports">
          <span className="material-symbols-outlined">input</span>
        </button>
        <button className="lean-file-btn" title="Git Status">
          <span className="material-symbols-outlined">commit</span>
        </button>
      </aside>

      <section className="lean-editor-pane">
        <div className="lean-file-tab">
          <span className="material-symbols-outlined" style={{ fontSize: "14px" }}>
            description
          </span>
          {data?.filename || "HelixCurvature.lean"}
          <span className="lean-unsaved-badge">unsaved</span>
        </div>
        <div className="lean-code-area">
          <div className="lean-line-numbers">
            {Array.from({ length: lines.length }, (_, i) => (
              <span key={i} style={i === 13 ? { color: "var(--on-primary-fixed-variant)", fontWeight: 700 } : {}}>
                {i + 1}
              </span>
            ))}
          </div>
          <div className="lean-code-content">
            <textarea
              style={{
                width: "100%",
                height: "100%",
                minHeight: `${lines.length * 24 + 32}px`,
                background: "transparent",
                border: "none",
                fontFamily: "inherit",
                fontSize: "inherit",
                lineHeight: "24px",
                color: "#003366",
                resize: "none",
                whiteSpace: "pre",
                overflow: "hidden",
              }}
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck={false}
            />
          </div>
        </div>
        <div className="lean-tactic-drawer">
          <div className="lean-tactic-left">
            <span className="lean-tactic-label">TACTICS</span>
            <div className="lean-tactic-list">
              {["simp", "ring", "unfold", "nlinarith"].map((t) => (
                <span
                  key={t}
                  className="lean-tactic-chip"
                  style={{ cursor: "pointer" }}
                  onClick={() => handleTactic(t)}
                >
                  {t}
                </span>
              ))}
            </div>
          </div>
          <span className="lean-tactic-hint">Click to apply tactic</span>
        </div>
      </section>

      <aside className="lean-goal-pane">
        <div className="lean-goal-header">
          <span className="lean-goal-header-label">Goal View</span>
          <div className="lean-goal-header-actions">
            <span
              className="material-symbols-outlined"
              style={{ cursor: "pointer" }}
              onClick={handleRefreshGoal}
            >
              refresh
            </span>
            <span
              className="material-symbols-outlined"
              style={{ cursor: "pointer" }}
              onClick={handleVerify}
            >
              visibility
            </span>
          </div>
        </div>
        <div className="lean-goal-body">
          {error && (
            <div className="lean-message" style={{ marginBottom: "16px", borderLeftColor: "var(--error)" }}>
              <span className="material-symbols-outlined" style={{ color: "var(--error)" }}>
                error
              </span>
              <p>{error}</p>
            </div>
          )}

          {goal && (
            <>
              <div>
                <div className="lean-context-title">
                  CONTEXT
                  <div className="divider" />
                </div>
                <div>
                  {goal.context?.map((v, i) => (
                    <div className="lean-context-var" key={i}>
                      <span className="name">{v.name}</span>
                      <span className="colon">:</span>
                      <span className="type">{v.type}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="lean-goal-card" style={{ marginTop: "24px" }}>
                <div className="lean-goal-card-title">
                  TARGET GOAL
                  <div className="divider" />
                </div>
                <div className="lean-goal-statement">{goal.target}</div>
              </div>
            </>
          )}

          <div>
            <div className="lean-context-title">
              MESSAGES
              <div className="divider" />
            </div>
            {messages.length === 0 && (
              <div style={{ fontSize: "12px", color: "var(--on-surface-variant)", fontStyle: "italic" }}>
                Verify the theorem to see messages.
              </div>
            )}
            {messages.map((m, i) => (
              <div
                className="lean-message"
                key={i}
                style={{
                  marginBottom: "8px",
                  borderLeftColor:
                    m.level === "error"
                      ? "var(--error)"
                      : m.level === "warning"
                      ? "#ffb300"
                      : "var(--tertiary-fixed-dim)",
                }}
              >
                <span
                  className="material-symbols-outlined"
                  style={{
                    color:
                      m.level === "error"
                        ? "var(--error)"
                        : m.level === "warning"
                        ? "#ffb300"
                        : "var(--tertiary)",
                  }}
                >
                  {m.level === "error" ? "error" : m.level === "warning" ? "warning" : "check_circle"}
                </span>
                <p style={{ whiteSpace: "pre-wrap" }}>{m.message}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="lean-status-bar">
          <div className="lean-status-left">
            <div
              className="lean-status-dot"
              style={{
                background: verifying
                  ? "#ffb300"
                  : status === "ready"
                  ? "#00bcd4"
                  : "#ef5350",
              }}
            />
            <span className="lean-status-text">
              {verifying ? "VERIFYING..." : status === "ready" ? "LEAN WORKER: IDLE" : "ERROR"}
            </span>
          </div>
          <button
            className="lean-status-info"
            style={{
              background: "var(--primary)",
              color: "var(--on-primary)",
              border: "none",
              padding: "4px 12px",
              borderRadius: "var(--radius)",
              fontSize: "11px",
              fontWeight: 700,
              cursor: "pointer",
            }}
            onClick={handleVerify}
            disabled={verifying}
          >
            {verifying ? "..." : "VERIFY"}
          </button>
        </div>
      </aside>
    </div>
  );
}

export default LeanProver;
