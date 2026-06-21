#let exercise(number: none, body: content) = {
  set text(size: 10pt)
  block(
    inset: 8pt,
    fill: luma(240),
    stroke: 0.5pt + black,
    radius: 4pt,
  )[
    #if number != none [
      *Exercise #number.*
    ]
    #body
  ]
}

#let solution(body: content) = {
  block(
    inset: 8pt,
    fill: luma(255),
    stroke: 0.5pt + gray,
    radius: 4pt,
  )[
    *Solution.*
    #body
  ]
}

= Exercises

#exercise(number: 1)[
  Simplify the following expression:

  $ (x + 3)(x - 3) $
]

#exercise(number: 2)[
  Compute the derivative:

  $ d/dx (sin(x) + cos(x)) $
]
