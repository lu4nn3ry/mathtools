import { useState, useRef, useEffect } from "react";

function Viz2D({ expr = "sin(x)", xMin = -6.28, xMax = 6.28, height = 300 }) {
  const canvasRef = useRef(null);
  const [input, setInput] = useState(expr);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;

    ctx.clearRect(0, 0, w, h);

    const pad = 40;
    const plotW = w - 2 * pad;
    const plotH = h - 2 * pad;

    ctx.strokeStyle = "var(--outline-variant)";
    ctx.lineWidth = 1;

    const yMin = -5;
    const yMax = 5;

    function xToPixel(x) { return pad + ((x - xMin) / (xMax - xMin)) * plotW; }
    function yToPixel(y) { return pad + ((yMax - y) / (yMax - yMin)) * plotH; }

    ctx.beginPath();
    ctx.moveTo(pad, pad);
    ctx.lineTo(pad, pad + plotH);
    ctx.lineTo(pad + plotW, pad + plotH);
    ctx.stroke();

    for (let i = -5; i <= 5; i += 1) {
      const xPx = xToPixel(i);
      const yPx = yToPixel(0);
      ctx.beginPath();
      ctx.moveTo(xPx, pad);
      ctx.lineTo(xPx, pad + plotH);
      ctx.strokeStyle = "var(--outline-variant)";
      ctx.stroke();

      ctx.fillStyle = "var(--on-surface-variant)";
      ctx.font = "10px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(i, xPx, yPx + 14);
    }

    for (let i = -4; i <= 4; i += 1) {
      if (i === 0) continue;
      const yPx = yToPixel(i);
      ctx.beginPath();
      ctx.moveTo(pad, yPx);
      ctx.lineTo(pad + plotW, yPx);
      ctx.strokeStyle = "var(--outline-variant)";
      ctx.stroke();

      ctx.fillStyle = "var(--on-surface-variant)";
      ctx.font = "10px sans-serif";
      ctx.textAlign = "right";
      ctx.fillText(i, pad - 4, yPx + 3);
    }

    try {
      const compiled = new Function("x", `"use strict"; return (${input});`);
      ctx.beginPath();
      ctx.strokeStyle = "var(--primary)";
      ctx.lineWidth = 2;
      let first = true;

      for (let px = 0; px <= plotW; px++) {
        const x = xMin + (px / plotW) * (xMax - xMin);
        try {
          const y = compiled(x);
          if (typeof y !== "number" || !isFinite(y)) { first = true; continue; }
          const xPx = pad + px;
          const yPx = yToPixel(y);
          if (first) { ctx.moveTo(xPx, yPx); first = false; }
          else ctx.lineTo(xPx, yPx);
        } catch {
          first = true;
        }
      }
      ctx.stroke();
    } catch {
      ctx.fillStyle = "var(--error)";
      ctx.font = "12px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("Invalid expression", w / 2, h / 2);
    }
  }, [input, xMin, xMax]);

  return (
    <div style={{ marginTop: "24px" }}>
      <div style={{ display: "flex", gap: "8px", marginBottom: "8px", alignItems: "center" }}>
        <span className="material-symbols-outlined" style={{ fontSize: "18px", color: "var(--primary)" }}>
          timeline
        </span>
        <span style={{ fontWeight: 700, fontSize: "12px", letterSpacing: "0.05em", color: "var(--on-surface-variant)" }}>
          2D PLOT
        </span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{
            flex: 1, padding: "4px 8px", borderRadius: "var(--radius)",
            border: "1px solid var(--outline-variant)", fontFamily: "var(--font-code)",
            fontSize: "12px", background: "var(--surface-container-lowest)",
            color: "var(--on-surface)",
          }}
        />
      </div>
      <canvas
        ref={canvasRef}
        width={500}
        height={height}
        style={{
          width: "100%", height: `${height}px`,
          borderRadius: "var(--radius-lg)", border: "1px solid var(--outline-variant)",
          background: "var(--surface-container-lowest)",
        }}
      />
    </div>
  );
}

export default Viz2D;
