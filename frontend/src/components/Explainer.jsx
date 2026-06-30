import { useState, useEffect } from "react";
import { fetchExplainerContent, explainExpression, checkQuizAnswer } from "../lib/api.js";
import Viz2D from "./Viz2D";

const LEVELS = [
  { id: "medio", label: "Ensino Médio" },
  { id: "graduacao", label: "Graduação" },
  { id: "posgraduacao", label: "Pós-Graduação" },
];

const STYLES = [
  { id: "didatico", label: "Didático", icon: "school" },
  { id: "conciso", label: "Conciso", icon: "short_text" },
  { id: "formal", label: "Formal", icon: "article" },
];

function Explainer() {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quizAnswer, setQuizAnswer] = useState(null);
  const [quizResult, setQuizResult] = useState(null);
  const [error, setError] = useState("");
  const [level, setLevel] = useState("graduacao");
  const [style, setStyle] = useState("didatico");
  const [explanation, setExplanation] = useState("");
  const [explainLoading, setExplainLoading] = useState(false);
  const [expression, setExpression] = useState("");

  useEffect(() => {
    fetchExplainerContent()
      .then((res) => setContent(res))
      .catch((err) => setError("Failed to load content: " + err.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleExplain() {
    if (!expression.trim()) return;
    setExplainLoading(true);
    try {
      const res = await explainExpression(expression, level, style);
      setExplanation(res.explanation || "No explanation returned.");
    } catch (err) {
      setExplanation("Error: " + err.message);
    }
    setExplainLoading(false);
  }

  async function handleQuizSelect(optionId) {
    setQuizAnswer(optionId);
    try {
      const res = await checkQuizAnswer(
        content?.quiz?.question || "",
        optionId
      );
      setQuizResult(res);
    } catch (err) {
      setQuizResult({ correct: false, correct_answer: "" });
    }
  }

  if (loading) {
    return (
      <div className="explainer-content">
        <div style={{ padding: "48px", textAlign: "center", color: "var(--on-surface-variant)" }}>
          Loading explanation...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="explainer-content">
        <div style={{ padding: "48px", textAlign: "center", color: "var(--error)" }}>{error}</div>
      </div>
    );
  }

  return (
    <div className="explainer-content">
      <nav className="explainer-breadcrumbs">
        {(content?.breadcrumbs || []).map((crumb, i) => (
          <span key={i} style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            {crumb.current ? (
              <span className="current">{crumb.label}</span>
            ) : (
              <a href={crumb.href}>{crumb.label}</a>
            )}
            {i < content.breadcrumbs.length - 1 && (
              <span className="sep material-symbols-outlined">chevron_right</span>
            )}
          </span>
        ))}
      </nav>

      <div className="explainer-header">
        <h2>{content?.title || "Curvature of a Circular Helix"}</h2>
        <p>{content?.description || "Step-by-step derivation of the curvature formula."}</p>
      </div>

      <div className="explainer-controls" style={{ display: "flex", gap: "16px", marginBottom: "24px", flexWrap: "wrap", alignItems: "flex-end" }}>
        <div style={{ flex: 1, minWidth: "200px" }}>
          <label style={{ fontSize: "11px", fontWeight: 700, letterSpacing: "0.05em", color: "var(--on-surface-variant)", display: "block", marginBottom: "6px" }}>
            EXPRESSION
          </label>
          <div style={{ display: "flex", gap: "8px" }}>
            <input
              type="text"
              value={expression}
              onChange={(e) => setExpression(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleExplain()}
              placeholder="e.g., derivative of x^2"
              style={{
                flex: 1, padding: "8px 12px", borderRadius: "var(--radius)",
                border: "1px solid var(--outline-variant)", background: "var(--surface-container-lowest)",
                fontFamily: "var(--font-code)", fontSize: "13px", color: "var(--on-surface)",
              }}
            />
            <button
              onClick={handleExplain}
              disabled={explainLoading}
              style={{
                padding: "8px 16px", background: "var(--primary)", color: "var(--on-primary)",
                border: "none", borderRadius: "var(--radius)", fontWeight: 700, cursor: "pointer",
              }}
            >
              {explainLoading ? "..." : "Explain"}
            </button>
          </div>
        </div>
        <div>
          <label style={{ fontSize: "11px", fontWeight: 700, letterSpacing: "0.05em", color: "var(--on-surface-variant)", display: "block", marginBottom: "6px" }}>
            LEVEL
          </label>
          <select
            value={level}
            onChange={(e) => setLevel(e.target.value)}
            style={{
              padding: "8px 12px", borderRadius: "var(--radius)",
              border: "1px solid var(--outline-variant)", background: "var(--surface-container-lowest)",
              fontSize: "13px", color: "var(--on-surface)", cursor: "pointer",
            }}
          >
            {LEVELS.map((l) => <option key={l.id} value={l.id}>{l.label}</option>)}
          </select>
        </div>
        <div>
          <label style={{ fontSize: "11px", fontWeight: 700, letterSpacing: "0.05em", color: "var(--on-surface-variant)", display: "block", marginBottom: "6px" }}>
            STYLE
          </label>
          <div style={{ display: "flex", gap: "4px" }}>
            {STYLES.map((s) => (
              <button
                key={s.id}
                onClick={() => setStyle(s.id)}
                style={{
                  padding: "6px 12px", borderRadius: "var(--radius)",
                  border: style === s.id ? "2px solid var(--primary)" : "1px solid var(--outline-variant)",
                  background: style === s.id ? "rgba(0,6,102,0.08)" : "transparent",
                  color: style === s.id ? "var(--primary)" : "var(--on-surface-variant)",
                  fontWeight: 700, fontSize: "11px", cursor: "pointer", letterSpacing: "0.05em",
                  display: "flex", alignItems: "center", gap: "4px",
                }}
              >
                <span className="material-symbols-outlined" style={{ fontSize: "14px" }}>{s.icon}</span>
                {s.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {explanation && (
        <div className="explainer-main-card" style={{ marginBottom: "24px" }}>
          <div style={{ fontFamily: "var(--font-code)", fontSize: "13px", whiteSpace: "pre-wrap", lineHeight: 1.6, color: "var(--on-surface)" }}>
            {explanation}
          </div>
        </div>
      )}

      <div className="explainer-grid">
        <div>
          <div className="explainer-main-card">
            <div className="explainer-card-header">
              <span className="explainer-card-badge">Guided Derivation</span>
              <span className="explainer-card-time">
                <span className="material-symbols-outlined" style={{ fontSize: "16px" }}>
                  timer
                </span>
                {content?.steps?.length || 4} steps
              </span>
            </div>

            <div className="explainer-problem-box">
              <div className="explainer-problem-label">Goal</div>
              <div className="explainer-problem-math">
                {content?.goal || "Compute curvature of a helix"}
              </div>
            </div>

            <div className="explainer-steps">
              {(content?.steps || []).map((step) => (
                <div className="explainer-step" key={step.number}>
                  <div className="explainer-step-number">{step.number}</div>
                  <h3>{step.title}</h3>
                  <p>{step.description}</p>
                  <div className="explainer-step-box">
                    <i>{step.formula}</i>
                  </div>
                  {step.transition && (
                    <div className="explainer-step-transition">
                      <span style={{ color: "var(--on-surface-variant)" }}>
                        {step.transition.from}
                      </span>
                      <span className="arrow material-symbols-outlined">arrow_forward</span>
                      <span className="result">{step.transition.to}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {content?.quiz && (
            <section className="explainer-quiz">
              <div className="explainer-quiz-header">
                <span className="material-symbols-outlined">quiz</span>
                <h3>Check Your Understanding</h3>
              </div>
              <p>{content.quiz.question}</p>
              <div className="explainer-quiz-options">
                {(content.quiz.options || []).map((opt) => (
                  <button
                    key={opt.id}
                    className="explainer-quiz-option"
                    style={{
                      borderColor:
                        quizAnswer === opt.id
                          ? quizResult?.correct
                            ? "#2e7d32"
                            : "#d32f2f"
                          : undefined,
                      background:
                        quizAnswer === opt.id
                          ? quizResult?.correct
                            ? "rgba(46,125,50,0.08)"
                            : "rgba(211,47,47,0.08)"
                          : undefined,
                    }}
                    onClick={() => handleQuizSelect(opt.id)}
                    disabled={quizResult !== null}
                  >
                    {opt.label}
                    {quizAnswer === opt.id && quizResult && (
                      <span style={{ marginLeft: "8px" }}>
                        {quizResult.correct ? "\u2713" : "\u2717"}
                      </span>
                    )}
                  </button>
                ))}
              </div>
              {quizResult && !quizResult.correct && quizResult.correct_answer && (
                <p style={{ marginTop: "16px", color: "#2e7d32", fontWeight: 700 }}>
                  Correct answer: {"\u03ba"} = {quizResult.correct_answer}
                </p>
              )}
            </section>
          )}
        </div>

        <div className="explainer-sidebar">
          <div className="explainer-related-card">
            <h4>Related Concepts</h4>
            <div>
              {(content?.related || []).map((item, i) => (
                <div className="explainer-related-item" key={i}>
                  <div className={`explainer-related-icon ${i === 0 ? "chain" : "parts"}`}>
                    <span className="material-symbols-outlined">{item.icon}</span>
                  </div>
                  <div className="explainer-related-text">
                    <div className="title">{item.title}</div>
                    <div className="sub">{item.sub}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="explainer-offline-card">
            <div className="explainer-offline-dot" />
            <div>
              <h4>Offline Mode Active</h4>
              <p>
                Content loaded from local database. Computations cached for repeated
                access.
              </p>
            </div>
          </div>

          <Viz2D expr={content?.goal?.match(/[a-zA-Z]+\([^)]+\)|[a-zA-Z]+\^[0-9]/)?.[0] || "sin(x)"} />
        </div>
      </div>
    </div>
  );
}

export default Explainer;
