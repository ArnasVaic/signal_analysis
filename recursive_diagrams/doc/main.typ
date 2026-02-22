#import "config/style.typ": style_config
#import "config/titlepage.typ": title_page

#show: style_config("lt")

#title_page(
  "Signalų analizės pirmas projektinis darbas",
  [ 
    Rekurentinės diagramos, algortimo parametrų analizė
  ],
  "Arnas Vaicekauskas",
  "",
  "lt",
)

#outline(depth: 3, title: "Turinys")
#pagebreak()

#include "chapters/signals.typ"
#include "chapters/logistic.typ"
#include "chapters/finance.typ"
#include "chapters/lung_sound.typ"
// #include "chapters/heart_sound.typ"
#include "chapters/energy.typ"
#include "chapters/air_quality.typ"
#pagebreak(weak: true)
#include "chapters/conclusions.typ"
#pagebreak(weak: true)
#bibliography("references.bib")
#pagebreak(weak: true)
#include "backmatter/appendices.typ"