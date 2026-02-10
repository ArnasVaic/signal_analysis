#import "config/style.typ": vu_template_style_config
#import "config/titlepage.typ": vu_template_title_page

#show: vu_template_style_config

#vu_template_title_page(
  "Signalų analizės pirmas projektinis darbas",
  [ 
    Rekurentinės diagramos, algortimo parametrų analizė
  ],
  "Arnas Vaicekauskas",
  "",
  in-lithuanian: true,
)

#outline(depth: 3, title: "Turinys")
#pagebreak()

#include "chapters/signals.typ"
#include "chapters/logistic.typ"
#include "chapters/finance.typ"
#include "chapters/lung_sound.typ"
#include "chapters/heart_sound.typ"
#include "chapters/air_quality.typ"
#pagebreak(weak: true)
#include "chapters/conclusions.typ"
#pagebreak(weak: true)
#bibliography("references.bib")
#pagebreak(weak: true)
#include "backmatter/appendices.typ"