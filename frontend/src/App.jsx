import { useState } from "react";
import Editor from "./components/Editor";
import Toolbar from "./components/Toolbar";
import Preview from "./components/Preview";
import Sidebar from "./components/Sidebar";

function App() {
  const [content, setContent] = useState("");
  const [activePanel, setActivePanel] = useState("editor");

  return (
    <div className="app">
      <Sidebar active={activePanel} onNavigate={setActivePanel} />
      <main className="main">
        <Toolbar />
        <div className="workspace">
          {activePanel === "editor" && (
            <Editor value={content} onChange={setContent} />
          )}
          {activePanel === "preview" && <Preview content={content} />}
        </div>
      </main>
    </div>
  );
}

export default App;
