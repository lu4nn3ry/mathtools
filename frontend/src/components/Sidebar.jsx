const panels = [
  { id: "editor", label: "Editor", icon: "✏️" },
  { id: "preview", label: "Preview", icon: "👁️" },
  { id: "library", label: "Library", icon: "📚" },
  { id: "settings", label: "Settings", icon: "⚙️" },
];

function Sidebar({ active, onNavigate }) {
  return (
    <nav className="sidebar">
      {panels.map((p) => (
        <button
          key={p.id}
          className={active === p.id ? "active" : ""}
          onClick={() => onNavigate(p.id)}
          title={p.label}
        >
          <span>{p.icon}</span>
        </button>
      ))}
    </nav>
  );
}

export default Sidebar;
