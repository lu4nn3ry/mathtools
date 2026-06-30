import subprocess
import json
from pathlib import Path


class LLMEngine:
    def __init__(self, model_path: str = ""):
        self.model_path = model_path or str(
            Path(__file__).parent.parent.parent / "models" / "qwen"
        )

    def explain(self, expression: str, level: str = "graduacao",
                style: str = "didatico") -> dict:
        """
        Explain a mathematical concept at three possible levels.

        Levels:
        - "medio":       High school (fundamental concepts, simple examples)
        - "graduacao":   Undergraduate (formal definitions, standard proofs)
        - "posgraduacao": Graduate (advanced theory, research connections)

        Styles:
        - "didatico":    Detailed, pedagogical, with examples
        - "conciso":     Direct and brief, just the essential facts
        - "formal":      Rigorous mathematical language
        """
        levels = {
            "medio": "Ensino Médio",
            "graduacao": "Graduação",
            "posgraduacao": "Pós-Graduação",
        }
        label = levels.get(level, "Graduação")

        # Try LLM first
        llm = self._try_llm(expression, label)
        if llm:
            return {
                "expression": expression,
                "level": level,
                "level_label": label,
                "style": style,
                "explanation": llm,
                "source": "llm",
            }

        # Fallback: rule-based explanations
        rule = self._rule_based(expression, level, style)
        return {
            "expression": expression,
            "level": level,
            "level_label": label,
            "style": style,
            "explanation": rule,
            "source": "rule-based",
        }

    def _try_llm(self, expression: str, level: str) -> str | None:
        """Try to generate an explanation using a local LLM."""
        prompt = (
            f"Você é um professor de matemática. Explique o conceito abaixo "
            f"em nível de {level}. Seja claro, use exemplos e mostre passos "
            f"intermediários quando possível.\n\n"
            f"Conceito: {expression}\n\n"
            f"Explicação:"
        )

        try:
            model_file = Path(self.model_path) / "qwen2.5-7b-instruct-q4_k_m.gguf"
            result = subprocess.run(
                ["llama-cli", "-m", str(model_file),
                 "-p", prompt, "-n", "512", "--temp", "0.7"],
                capture_output=True, text=True, timeout=60,
            )
            output = result.stdout.strip()
            if output and len(output) > 20:
                return output
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass
        return None

    def _rule_based(self, expression: str, level: str, style: str = "didatico") -> str:
        """Generate a structured, multi-level explanation from rules."""
        expr_lower = expression.lower()

        if style == "conciso":
            return self._explain_concise(expr_lower, level)

        # --- Nível Médio ---
        if level == "medio":
            return self._explain_high_school(expr_lower)

        # --- Nível Graduação ---
        if level == "graduacao":
            return self._explain_undergrad(expr_lower)

        # --- Nível Pós-Graduação ---
        return self._explain_grad(expr_lower)

    def _explain_high_school(self, expr: str) -> str:
        steps = [
            "📘 **Visão Geral**",
            f"Vamos entender o que significa '{expr}' de forma simples.",
            "",
        ]
        if "deriv" in expr or "derivative" in expr:
            steps += [
                "📐 **O que é uma derivada?**",
                "A derivada mede a taxa de variação de uma função. Imagine um carro "
                "em movimento: a derivada da posição é a velocidade.",
                "",
                "🔢 **Exemplo prático:**",
                "Se f(x) = x², a derivada f'(x) = 2x nos diz como f varia em cada ponto x.",
                "",
                "💡 **Interpretação geométrica:**",
                "A derivada em um ponto é a inclinação da reta tangente ao gráfico "
                "da função naquele ponto.",
            ]
        elif "integral" in expr:
            steps += [
                "📐 **O que é uma integral?**",
                "A integral calcula a área acumulada sob uma curva. Se a derivada "
                "é a taxa de variação, a integral é o valor acumulado.",
                "",
                "🔢 **Exemplo prático:**",
                "A integral de 2x de 0 a 3 é 9 — a área do triângulo sob a reta 2x.",
            ]
        elif "limite" in expr or "limit" in expr:
            steps += [
                "📐 **O que é um limite?**",
                "O limite descreve o comportamento de uma função quando a variável "
                "se aproxima de um valor, sem necessariamente atingi-lo.",
                "",
                "🔢 **Exemplo prático:**",
                "lim(x→0) sin(x)/x = 1 — a função se aproxima de 1 mesmo sem estar "
                "definida em x=0.",
            ]
        elif "=" in expr or "equação" in expr:
            steps += [
                "📐 **Resolvendo equações**",
                f"Para resolver '{expr}', isolamos a variável desconhecida "
                f"aplicando operações inversas em ambos os lados.",
                "",
                "💡 **Dica:**",
                "Lembre-se: o que fazemos de um lado, fazemos do outro!",
            ]
        else:
            steps += [
                f"📐 **Sobre '{expr}'**",
                "Este conceito matemático pode ser compreendido praticando com "
                "exemplos numéricos simples e gradualmente aumentando a complexidade.",
                "",
                "💡 **Como estudar:**",
                "1. Entenda a definição\n2. Faça exemplos numéricos\n"
                "3. Resolva exercícios do livro-texto",
            ]
        steps += [
            "",
            "✅ **Resumo:**",
            "A matemática se constrói passo a passo. Pratique bastante!",
        ]
        return "\n".join(steps)

    def _explain_undergrad(self, expr: str) -> str:
        steps = [
            "📘 **Análise Formal**",
            f"Exploração do conceito '{expr}' em nível universitário.",
            "",
        ]
        if "deriv" in expr or "derivative" in expr:
            steps += [
                "📐 **Definição Formal**",
                "Seja f: I → ℝ diferenciável em a ∈ I. A derivada é:",
                "  f'(a) = lim_{h→0} (f(a+h) - f(a)) / h",
                "",
                "📋 **Propriedades:**",
                "• Linearidade: (af + bg)' = af' + bg'",
                "• Regra do Produto: (fg)' = f'g + fg'",
                "• Regra da Cadeia: (f∘g)' = (f'∘g) · g'",
                "",
                "🔗 **Aplicações:**",
                "• Otimização (pontos críticos, teste da segunda derivada)",
                "• Séries de Taylor (aproximação polinomial local)",
                "• Equações diferenciais (modelagem de fenômenos)",
            ]
        elif "integral" in expr:
            steps += [
                "📐 **Definição Formal**",
                "A integral de Riemann de f em [a,b] é o limite das somas:",
                "  ∫_a^b f(x) dx = lim_{‖P‖→0} Σ f(ξ_k) Δx_k",
                "",
                "📋 **Teorema Fundamental do Cálculo:**",
                "  d/dx ∫_a^x f(t) dt = f(x)",
                "  ∫_a^b f'(x) dx = f(b) - f(a)",
                "",
                "🔗 **Técnicas de Integração:**",
                "• Substituição simples (regra da cadeia ao reverso)",
                "• Integração por partes (∫ u dv = uv - ∫ v du)",
                "• Frações parciais (para funções racionais)",
            ]
        elif "limite" in expr or "limit" in expr:
            steps += [
                "📐 **Definição Formal (ε-δ)**",
                "lim_{x→a} f(x) = L se ∀ε>0, ∃δ>0 tal que",
                "  0 < |x - a| < δ ⇒ |f(x) - L| < ε",
                "",
                "📋 **Propriedades:**",
                "• Limite da soma = soma dos limites",
                "• Limite do produto = produto dos limites",
                "• Teorema do Confronto (Sanduíche)",
            ]
        else:
            steps += [
                "📋 **Análise do Conceito**",
                f"O estudo de '{expr}' envolve compreender sua definição formal, "
                f"propriedades estruturais e conexões com outros tópicos.",
                "",
                "🔗 **Conexões:**",
                "• Fundamentos em teoria de conjuntos e estruturas algébricas",
                "• Aplicações em física, engenharia e ciência da computação",
                "• Generalizações em níveis mais avançados",
            ]
        steps += [
            "",
            "📚 **Leitura Recomendada:**",
            "• Guidorizzi, Um Curso de Cálculo (vol. 1-4)",
            "• Stewart, Cálculo (vol. 1-2)",
            "• Rudin, Principles of Mathematical Analysis",
        ]
        return "\n".join(steps)

    def _explain_grad(self, expr: str) -> str:
        steps = [
            "📘 **Tratamento Avançado**",
            f"Análise do conceito '{expr}' em nível de pesquisa.",
            "",
        ]
        if "deriv" in expr or "derivative" in expr:
            steps += [
                "📐 **Generalizações**",
                "• Derivada de Fréchet em espaços de Banach",
                "• Derivada de Gateaux para funcionais não-lineares",
                "• Derivada de Lie em geometria diferencial",
                "• Diferenciação no sentido das distribuições (Schwartz)",
                "",
                "🔬 **Conexões com Pesquisa Atual:**",
                "• Gradientes em Deep Learning (backpropagation)",
                "• Derivadas fracionárias (modelos anômalos de difusão)",
                "• Fluxos gradientes em espaços de Wasserstein",
                "• Diferenciação automática (AD) em computação simbólica",
            ]
        elif "integral" in expr:
            steps += [
                "📐 **Teoria da Medida e Integração**",
                "• Integral de Lebesgue (superando limitações de Riemann)",
                "• Integral de Itô (cálculo estocástico)",
                "• Integrais de contorno (análise complexa)",
                "• Integrais funcionais (mecânica quântica)",
                "",
                "🔬 **Aplicações Avançadas:**",
                "• Teoria de gauge em física de partículas",
                "• Integrais de caminho de Feynman",
                "• Wavelets e análise multirresolução",
                "• Métodos de elementos finitos",
            ]
        else:
            steps += [
                "📐 **Perspectiva de Pesquisa**",
                f"O conceito '{expr}' se insere em um contexto mais amplo de "
                f"matemática pura e aplicada, com conexões a problemas em aberto.",
                "",
                "🔬 **Direções de Pesquisa Relacionadas:**",
                "• Problemas de Hilbert e conjecturas atuais",
                "• Conexões com geometria algébrica e teoria de números",
                "• Aplicações em machine learning teórico",
            ]
        steps += [
            "",
            "📚 **Bibliografia Recomendada:**",
            "• Rudin, Real and Complex Analysis",
            "• Brezis, Functional Analysis",
            "• Arnold, Mathematical Methods of Classical Mechanics",
            "• Artigos recentes nos arquivos do arXiv (math.xx)",
        ]
        return "\n".join(steps)

    def _explain_concise(self, expr: str, level: str) -> str:
        """Short, direct explanation without emojis or padding."""
        lines = []
        if "deriv" in expr or "derivative" in expr:
            lines += [
                f"Derivative of '{expr}'",
                f"f'(a) = lim_{{h→0}} (f(a+h) - f(a)) / h",
                "Properties: linearity, product rule, chain rule.",
                "Measures rate of change / slope of tangent.",
            ]
        elif "integral" in expr:
            lines += [
                f"Integral of '{expr}'",
                "∫ f(x) dx = limit of Riemann sums",
                "TFC: d/dx ∫_a^x f(t) dt = f(x), ∫_a^b f'(x) dx = f(b)-f(a)",
                "Methods: substitution, parts, partial fractions.",
            ]
        elif "limit" in expr:
            lines += [
                f"Limit of '{expr}'",
                "lim_{x→a} f(x) = L ⇔ ∀ε>0 ∃δ>0: 0<|x-a|<δ ⇒ |f(x)-L|<ε",
                "Properties: sum, product, quotient, squeeze theorem.",
            ]
        elif "=" in expr:
            lines += [
                f"Solving '{expr}'",
                "Isolate variable using inverse operations on both sides.",
            ]
        else:
            lines += [
                f"'{expr}'",
                "Apply definitions and known theorems step by step.",
            ]

        if level == "posgraduacao":
            lines += ["Advanced connections: functional analysis, measure theory, research applications."]
        elif level == "graduacao":
            lines += ["Standard undergraduate treatment with formal proofs."]
        else:
            lines += ["Elementary approach with basic examples."]

        return "\n".join(lines)
