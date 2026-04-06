#import "config/style.typ": style_config
#import "config/titlepage.typ": title_page

#show: style_config("lt")

#title_page(
  "Signalų analizės antras projektinis darbas",
  [ 
    Cooley-Tukey greitosios Furje transformacijos algoritmu paremtas skaitmeninis ekvalaizeris
  ],
  "Arnas Vaicekauskas",
  "",
  "lt",
)

#outline(depth: 3, title: "Turinys")
#pagebreak()

#pagebreak(weak: true)
#include "chapters/conclusions.typ"
#pagebreak(weak: true)
#bibliography("references.bib")
#pagebreak(weak: true)
#include "backmatter/appendices.typ"