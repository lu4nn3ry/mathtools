const panels = [
  { id: "editor", label: "LaTeX Editor", icon: "edit_note" },
  { id: "console", label: "SymPy Console", icon: "terminal" },
  { id: "prover", label: "Lean 4 Prover", icon: "verified" },
  { id: "explainer", label: "Math Explainer", icon: "menu_book" },
];

const footerLinks = [
  { id: "settings", label: "Settings", icon: "settings" },
  { id: "docs", label: "Documentation", icon: "help_outline" },
];

function Sidebar({ active, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-brand-inner">
          <div className="sidebar-logo">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>functions</span>
          </div>
          <div>
            <div className="sidebar-title">MathTools</div>
            <div className="sidebar-subtitle">Offline First</div>
          </div>
        </div>
        <button className="sidebar-new-btn">
          <span className="material-symbols-outlined">add_circle</span>
          New Proof
        </button>
      </div>
      <nav className="sidebar-nav">
        {panels.map((p) => (
          <button
            key={p.id}
            className={`sidebar-link${active === p.id ? " active" : ""}`}
            onClick={() => onNavigate(p.id)}
          >
            <span className="material-symbols-outlined" style={active === p.id ? { fontVariationSettings: "'FILL' 1" } : {}}>{p.icon}</span>
            <span>{p.label}</span>
          </button>
        ))}
      </nav>
      <div className="sidebar-footer">
        {footerLinks.map((l) => (
          <button key={l.id} className="sidebar-footer-link" onClick={() => onNavigate(l.id)}>
            <span className="material-symbols-outlined">{l.icon}</span>
            <span>{l.label}</span>
          </button>
        ))}
      </div>
    </aside>
  );
}

export default Sidebar;
