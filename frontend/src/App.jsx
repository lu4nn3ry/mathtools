import { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import Editor from "./components/Editor";
import SympyConsole from "./components/SympyConsole";
import LeanProver from "./components/LeanProver";
import Explainer from "./components/Explainer";
import Settings from "./components/Settings";

const topLinks = ["Editor", "Console", "Prover", "Explainer"];

function App() {
  const [activePanel, setActivePanel] = useState("editor");
  const [theme, setTheme] = useState(() => localStorage.getItem("mathtools-theme") || "light");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("mathtools-theme", theme);
  }, [theme]);

  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === "1" && e.ctrlKey) { e.preventDefault(); setActivePanel("editor"); }
      if (e.key === "2" && e.ctrlKey) { e.preventDefault(); setActivePanel("console"); }
      if (e.key === "3" && e.ctrlKey) { e.preventDefault(); setActivePanel("prover"); }
      if (e.key === "4" && e.ctrlKey) { e.preventDefault(); setActivePanel("explainer"); }
      if (e.key === "5" && e.ctrlKey) { e.preventDefault(); setActivePanel("settings"); }
      if (e.key === "t" && e.ctrlKey && e.shiftKey) {
        e.preventDefault();
        setTheme((t) => (t === "light" ? "dark" : "light"));
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const panelId = (label) => label.toLowerCase();

  return (
    <div className="app-shell">
      <Sidebar active={activePanel} onNavigate={setActivePanel} />
      <div className="main-area">
        <header className="top-navbar">
          <div className="top-navbar-left">
            <span className="top-navbar-title">MathTools Offline</span>
            <nav className="top-navbar-links">
              {topLinks.map((label) => (
                <button
                  key={label}
                  className={`top-navbar-link${panelId(label) === activePanel ? " active" : ""}`}
                  onClick={() => setActivePanel(panelId(label))}
                >
                  {label}
                </button>
              ))}
            </nav>
          </div>
          <div className="top-navbar-right">
            <div className="top-navbar-badge">
              <div className="badge-dot" />
              <span>Offline Mode</span>
            </div>
            <button
              className="top-navbar-icon material-symbols-outlined"
              onClick={() => setTheme((t) => (t === "light" ? "dark" : "light"))}
              title="Toggle theme (Ctrl+Shift+T)"
            >
              {theme === "light" ? "dark_mode" : "light_mode"}
            </button>
            <button className="top-navbar-icon material-symbols-outlined" onClick={() => setActivePanel("settings")} title="Settings">
              settings
            </button>
            <div className="top-navbar-avatar">
              <div style={{ width: "100%", height: "100%", background: "var(--primary-fixed-dim)" }} />
            </div>
          </div>
        </header>
        <div className="workspace-content">
          {activePanel === "editor" && <Editor />}
          {activePanel === "console" && <SympyConsole />}
          {activePanel === "prover" && <LeanProver />}
          {activePanel === "explainer" && <Explainer />}
          {activePanel === "settings" && <Settings />}
        </div>
      </div>
    </div>
  );
}

export default App;
