# ADR 0001 — Avaliador matemático restrito em vez de exec/eval

- **Status:** Aceito
- **Data:** 2026-02-14
- **Contexto:** Revisão de segurança semanal (issue #2)

## Contexto

O endpoint `POST /api/v1/solve/exec` e o método `SympyEngine.evaluate()`
executavam código enviado pelo cliente com `exec()`/`eval()` (com
`__builtins__` completo no `execute`) e usavam `sp.sympify()` em ~15 pontos,
que internamente também faz `eval`. Qualquer pessoa com acesso à API podia
executar Python arbitrário no servidor (RCE — por exemplo
`__import__('os').system(...)`), classificado como **CRÍTICO (10/10)**.

O console SymPy do frontend depende do endpoint `/solve/exec` para células
com `import sympy as sp`, atribuições (inclusive desempacotamento de tuplas
e kwargs como `positive=True`), matrizes e métodos (`.det()`, `.T`,
`.cross()`), então remover o endpoint quebraria o produto.

## Decisão

Substituir `exec`/`eval`/`sympify` por um **avaliador de AST restrito**
(`backend/core/safe_math.py`, `SafeMathEvaluator`):

1. A entrada é parseada com `ast.parse` e **convertida diretamente para
   objetos SymPy** — nunca executada como código Python.
2. Whitelists explícitas: funções SymPy matemáticas (`sin`, `solve`,
   `Matrix`, ...), constantes (`pi`, `E`, `I`, `oo`), métodos de objetos
   (`det`, `subs`, `T`, ...) e apenas `import sympy`.
3. Nomes e atributos começando com `_` são rejeitados (bloqueia
   `__import__`, `__class__`, `__dict__`); `getattr`/`setattr`,
   `sympify`, `parse_expr`, `lambdify`, `open`, `exec`, `eval`, `lambda`,
   comprehensions, `def`/`class`/`for`/`while` são rejeitados.
4. Strings nunca chegam cruas a funções SymPy que poderiam encaminhá-las
   ao `eval` interno: são pré-parseadas recursivamente, exceto nas funções
   que tratam strings como *nomes de símbolos* (`symbols`, `Symbol`,
   `Function`, `Wild`, `Dummy`) e no `print`.
5. O contrato da API não muda: `/solve/exec` continua existindo com o mesmo
   formato de resposta; erros de célula continuam retornando
   `type: "error"` no corpo.

## Consequências

- **Positivas:** RCE eliminado sem quebrar o console SymPy; todas as 137
  suítes de teste passam, incluindo 40+ novos testes de regressão de
  segurança (`backend/tests/test_security.py`) que tentam RCE, traversal
  de atributos e imports perigosos.
- **Negativas:** células do console ficam limitadas à DSL matemática
  (sem loops, funções Python arbitrárias ou imports além de `sympy`) —
  aceitável para o caso de uso do produto.
- **Riscos futuros:** novas funções SymPy precisam ser adicionadas
  explicitamente às whitelists; revisar a lista a cada upgrade maior do
  SymPy.
