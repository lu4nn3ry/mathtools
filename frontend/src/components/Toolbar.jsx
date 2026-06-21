function Toolbar() {
  return (
    <header className="toolbar">
      <h1>MathTools Offline</h1>
      <div className="toolbar-actions">
        <button onClick={() => window.__tauri?.invoke("solve")}>Solve</button>
        <button onClick={() => window.__tauri?.invoke("export")}>Export PDF</button>
      </div>
    </header>
  );
}

export default Toolbar;
