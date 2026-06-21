#let project(title: "", authors: (), body: content) = {
  set page(paper: "a4", margin: 2.5cm)
  set text(font: "Linux Libertine", size: 11pt)

  align(center)[
    #text(size: 24pt, weight: "bold", title)
    #v(0.5cm)
    #for author in authors [
      #author \
    ]
  ]

  #v(1cm)
  #body
}

#show: project.with(
  title: "MathTools Offline Document",
  authors: ("Generated with MathTools Offline",),
)

= Introduction

This document was generated using MathTools Offline.

= Content

$ integral_0^infty e^(-x^2) dif x = sqrt(pi) / 2 $
