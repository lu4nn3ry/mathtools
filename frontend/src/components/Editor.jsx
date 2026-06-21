import { useRef, useEffect } from "react";
import * as monaco from "monaco-editor";

function Editor({ value, onChange }) {
  const containerRef = useRef(null);
  const editorRef = useRef(null);

  useEffect(() => {
    if (containerRef.current && !editorRef.current) {
      editorRef.current = monaco.editor.create(containerRef.current, {
        value: value || "",
        language: "latex",
        theme: "vs-dark",
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 14,
      });

      editorRef.current.onDidChangeModelContent(() => {
        onChange(editorRef.current.getValue());
      });
    }

    return () => {
      editorRef.current?.dispose();
    };
  }, []);

  return <div ref={containerRef} className="editor-container" />;
}

export default Editor;
