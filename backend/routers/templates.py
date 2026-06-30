from fastapi import APIRouter, HTTPException
from backend.core.sympy_engine import SympyEngine

router = APIRouter(prefix="/api/v1/templates", tags=["templates"])

engine = SympyEngine()

LATEX_TEMPLATE = r"""\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage{fullpage}

\title{The Frenet--Serret Formulas}
\author{MathTools Session}
\date{\today}

\begin{document}

\maketitle

\section{Curves in $\mathbb{R}^3$}

Let $\gamma: I \to \mathbb{R}^3$ be a smooth curve
parametrized by arc length $s$. The unit tangent vector is
\begin{equation}
    \mathbf{T}(s) = \gamma'(s).
\end{equation}

The curvature measures deviation from a straight line:
\begin{equation}
    \kappa(s) = \|\gamma''(s)\| = \|\mathbf{T}'(s)\|.
\end{equation}

The principal normal vector is
\begin{equation}
    \mathbf{N}(s) = \frac{\mathbf{T}'(s)}{\kappa(s)}.
\end{equation}

Together $\{\mathbf{T}, \mathbf{N}, \mathbf{B}\}$ form the
orthonormal Frenet frame, where the binormal is
\begin{equation}
    \mathbf{B}(s) = \mathbf{T}(s) \times \mathbf{N}(s).
\end{equation}

\section{Frenet--Serret Equations}

The frame satisfies
\begin{align}
    \mathbf{T}' &= \kappa\,\mathbf{N} \\
    \mathbf{N}' &= -\kappa\,\mathbf{T} + \tau\,\mathbf{B} \\
    \mathbf{B}' &= -\tau\,\mathbf{N}.
\end{align}

For a general parametrization $\gamma(t)$ the curvature is
\begin{equation}
    \kappa(t) = \frac{\|\gamma'(t) \times \gamma''(t)\|}{\|\gamma'(t)\|^3}.
\end{equation}

\section{Example: Helix}

The circular helix
\begin{equation}
    \gamma(t) = (a\cos t,\, a\sin t,\, bt), \quad a,b > 0
\end{equation}
has constant curvature and torsion:
\begin{align}
    \kappa &= \frac{a}{a^2 + b^2}, \\
    \tau &= \frac{b}{a^2 + b^2}.
\end{align}

\end{document}"""

SYMPY_SESSION = {
    "id": "helix-curvature",
    "title": "Curvature of a Helix",
    "description": "Symbolic computation of the Frenet\u2013Serret apparatus for a circular helix.",
    "python_version": "Python 3.13",
    "sympy_version": "SymPy 1.13 (Offline Core)",
    "cells": [
        {
            "id": 1,
            "code": "import sympy as sp\na, b, t = sp.symbols('a b t', positive=True, real=True)\ngamma = sp.Matrix([a * sp.cos(t), a * sp.sin(t), b * t])",
            "prompt": "In [1]",
            "type": "code",
        },
        {
            "id": 2,
            "code": "gamma_dot = sp.diff(gamma, t)\ngamma_ddot = sp.diff(gamma_dot, t)\nsp.simplify(gamma_dot), sp.simplify(gamma_ddot)",
            "prompt": "In [2]",
            "type": "code",
        },
        {
            "id": 3,
            "code": "cross = gamma_dot.cross(gamma_ddot)\nsp.simplify(cross)",
            "prompt": "In [3]",
            "type": "code",
        },
        {
            "id": 4,
            "code": "speed = sp.sqrt(gamma_dot.dot(gamma_dot))\nnum = sp.sqrt(cross.dot(cross))\nkappa = sp.simplify(num / speed**3)\nkappa",
            "prompt": "In [4]",
            "type": "code",
        },
        {
            "id": 5,
            "code": "torsion = sp.simplify(gamma_dot.dot(cross) / num**2)\ntorsion",
            "prompt": "In [5]",
            "type": "code",
        },
    ],
    "common_operations": ["INTEGRATE", "DERIVATIVE", "SUMMATION", "LIMIT", "CURL", "CROSS"],
}

LEAN_TEMPLATE = {
    "id": "helix-curvature",
    "filename": "DifferentialGeometry/HelixCurvature.lean",
    "code": (
        "import Mathlib.Analysis.Calculus.Deriv.Basic\n"
        "import Mathlib.Analysis.SpecialFunctions.Trigonometric\n\n"
        "noncomputable section\n\n"
        "def helix (a b : \u211d) : \u211d \u2192 \u211d\u00b3 :=\n"
        "  \u03bb t => (a * Real.cos t, a * Real.sin t, b * t)\n\n"
        "def curvature (\u03b3 : \u211d \u2192 \u211d\u00b3) (t : \u211d) : \u211d :=\n"
        "  \u2016deriv \u03b3 t \u00d7 deriv (deriv \u03b3) t\u2016 / \u2016deriv \u03b3 t\u2016 ^ 3\n\n"
        "theorem helix_curvature (a b : \u211d) (hpos : a > 0 \u2227 b > 0) (t : \u211d) :\n"
        "  curvature (helix a b) t = a / (a ^ 2 + b ^ 2) :=\n"
        "by\n"
        "  unfold curvature helix\n"
        "  simp [deriv, Real.deriv_cos, Real.deriv_sin]\n"
        "  ring\n"
        "  simp [hpos.1, hpos.2]"
    ),
    "context": [
        {"name": "a", "type": "\u211d"},
        {"name": "b", "type": "\u211d"},
        {"name": "hpos", "type": "a > 0 \u2227 b > 0"},
        {"name": "t", "type": "\u211d"},
    ],
    "goal": "curvature (helix a b) t = a / (a \u00b2 + b \u00b2)",
    "tactics": ["simp", "ring", "unfold", "nlinarith"],
}

EXPLAINER_CONTENT = {
    "title": "Curvature of a Circular Helix",
    "description": "A step-by-step derivation of the curvature formula for a helix using vector calculus and the Frenet\u2013Serret apparatus.",
    "breadcrumbs": [
        {"label": "Library", "href": "#"},
        {"label": "Differential Geometry", "href": "#"},
        {"label": "Curvature of a Helix", "current": True},
    ],
    "goal": "Compute \u03ba(t) for \u03b3(t) = (a cos t, a sin t, b t)",
    "steps": [
        {
            "number": 1,
            "title": "Compute the Velocity Vector",
            "description": "Differentiate \u03b3 componentwise to obtain the tangent vector.",
            "formula": "\u03b3'(t) = (\u2212a sin t, a cos t, b)",
            "transition": {"from": "d/dt (a cos t)", "to": "\u2212a sin t"},
        },
        {
            "number": 2,
            "title": "Compute the Acceleration Vector",
            "description": "Differentiate the velocity to get the acceleration.",
            "formula": "\u03b3''(t) = (\u2212a cos t, \u2212a sin t, 0)",
            "transition": {"from": "d/dt (\u2212a sin t)", "to": "\u2212a cos t"},
        },
        {
            "number": 3,
            "title": "Cross Product \u03b3' \u00d7 \u03b3''",
            "description": "The cross product of velocity and acceleration eliminates the parameter t from the horizontal components.",
            "formula": "\u03b3' \u00d7 \u03b3'' = (a b sin t, \u2212a b cos t, a\u00b2)",
            "transition": {"from": "det([e\u2081 e\u2082 e\u2083; \u03b3'; \u03b3'']", "to": "(a b sin t, \u2212a b cos t, a\u00b2)"},
        },
        {
            "number": 4,
            "title": "Apply the Curvature Formula",
            "description": "For a general parametrization, \u03ba = \u2016\u03b3' \u00d7 \u03b3''\u2016 / \u2016\u03b3'\u2016\u00b3. The cross product norm simplifies to \u2016\u03b3' \u00d7 \u03b3''\u2016 = a\u221a(a\u00b2 + b\u00b2) and speed is \u2016\u03b3'\u2016 = \u221a(a\u00b2 + b\u00b2).",
            "formula": "\u03ba = a / (a\u00b2 + b\u00b2)",
            "transition": None,
        },
    ],
    "related": [
        {"icon": "link", "title": "Frenet\u2013Serret Frame", "sub": "Orthonormal moving frame"},
        {"icon": "layers", "title": "Torsion", "sub": "Twisting of a space curve"},
    ],
    "quiz": {
        "question": "For the helix \u03b3(t) = (4 cos t, 4 sin t, 3 t), what is the curvature \u03ba?",
        "options": [
            {"id": "A", "label": "\u03ba = 4 / 25", "value": "4/25", "correct": True},
            {"id": "B", "label": "\u03ba = 3 / 25", "value": "3/25", "correct": False},
            {"id": "C", "label": "\u03ba = 4 / 7", "value": "4/7", "correct": False},
            {"id": "D", "label": "\u03ba = 3 / 7", "value": "3/7", "correct": False},
        ],
    },
}


@router.get("/editor")
async def get_editor_template():
    lines = LATEX_TEMPLATE.strip().split("\n")
    return {
        "ok": True,
        "id": "frenet-serret",
        "filename": "frenet_serret.tex",
        "title": "The Frenet--Serret Formulas",
        "author": "MathTools Session",
        "language": "latex",
        "content": LATEX_TEMPLATE.strip(),
        "line_count": len(lines),
    }


@router.get("/sympy/session")
async def get_sympy_session():
    return {"ok": True, **SYMPY_SESSION}


@router.get("/lean/theorem")
async def get_lean_theorem():
    return {"ok": True, **LEAN_TEMPLATE}


@router.get("/explainer/content")
async def get_explainer_content():
    return {"ok": True, **EXPLAINER_CONTENT}


@router.post("/quiz/check")
async def check_quiz_answer(data: dict):
    answer = data.get("answer", "")
    question = data.get("question", "")
    for q_data in [EXPLAINER_CONTENT.get("quiz", {})]:
        if q_data.get("question") == question:
            for opt in q_data.get("options", []):
                if opt["id"] == answer or opt["value"] == answer:
                    return {"ok": True, "correct": opt["correct"], "correct_answer": opt["value"]}
    return {"ok": True, "correct": False, "correct_answer": ""}


@router.get("/health")
async def templates_health():
    return {"ok": True, "templates": ["editor", "sympy/session", "lean/theorem", "explainer/content", "quiz"]}
