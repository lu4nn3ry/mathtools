import { describe, it, expect } from "vitest";

describe("API module exports", () => {
  it("should export all expected functions", async () => {
    const api = await import("../api.js");
    const expected = [
      "solveEquation",
      "evaluateExpression",
      "simplifyExpression",
      "differentiateExpression",
      "explainExpression",
      "exportDocument",
      "fetchEditorTemplate",
      "fetchSympySession",
      "fetchLeanTheorem",
      "fetchExplainerContent",
      "fetchLeanTemplates",
      "checkQuizAnswer",
      "verifyTheorem",
      "sympyToLean",
      "extractGoal",
      "execSympyCode",
      "resetSympySession",
      "fetchSympySymbols",
    ];
    for (const name of expected) {
      expect(api[name]).toBeDefined();
    }
  });
});
