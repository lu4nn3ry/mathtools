import { useState, useEffect } from "react";

function Preview({ content }) {
  const [svg, setSvg] = useState(null);

  useEffect(() => {
    async function render() {
      try {
        const response = await fetch("http://localhost:8080/api/v1/export", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content, format: "svg" }),
        });
        const data = await response.json();
        if (data.ok) setSvg(data.file);
      } catch {
        setSvg(null);
      }
    }
    if (content) render();
  }, [content]);

  return (
    <div className="preview">
      {svg ? (
        <img src={`data:image/svg+xml;utf8,${encodeURIComponent(svg)}`} alt="preview" />
      ) : (
        <p className="placeholder">Preview will appear here</p>
      )}
    </div>
  );
}

export default Preview;
