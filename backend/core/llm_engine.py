import subprocess
import json
from pathlib import Path

class LLMEngine:
    def __init__(self, model_path: str = ""):
        self.model_path = model_path or str(Path(__file__).parent.parent.parent / "models" / "qwen")

    def explain(self, expression: str, level: str = "graduacao") -> str:
        levels = {
            "medio": "Ensino Medio",
            "graduacao": "Graduacao",
            "posgraduacao": "Pos-Graduacao",
        }
        label = levels.get(level, "Graduacao")

        prompt = (
            f"Explique o conceito matematico a seguir em nivel de {label}.\n"
            f"Seja claro, didatico and use exemplos quando possivel.\n\n"
            f"Conceito: {expression}\n\n"
            f"Explicacao:"
        )

        try:
            result = subprocess.run(
                ["llama-cli", "-m", str(Path(self.model_path) / "qwen2.5-7b-instruct-q4_k_m.gguf"),
                 "-p", prompt, "-n", "512", "--temp", "0.7"],
                capture_output=True, text=True, timeout=60,
            )
            return result.stdout.strip() or self._fallback_explain(expression, label)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return self._fallback_explain(expression, label)

    def _fallback_explain(self, expression: str, level: str) -> str:
        return (
            f"[Explicador offline - nivel {level}]\n\n"
            f"O conceito '{expression}' pode ser compreendido "
            f"por meio do estudo de seus fundamentos e aplicacoes.\n"
            f"(Modo fallback ativo - instale o modelo Qwen 2.5 em models/qwen/)"
        )
