= Įmonės "Apple Inc." akcijų kaina

#figure(
  grid(
    columns: (1.3fr, 1fr, 1fr),
    gutter: 12pt,
    image("../assets/diagrams/finance/signal.png"),
    image("../assets/diagrams/finance/a.png"),
    image("../assets/diagrams/finance/b.png")
  ),
  caption: [
    "Apple Inc." akcijų kainos svyravimai 2025 m. Duomenys gauti naudojant `yfinance` python paketą @yfinance2024. Rekurentinės diagramos gautos naudojant parametrus $p=0.1, d=1$, kur $p$ yra vartotojo pasirinktas juodų ir baltų taškų santykis diagramoje. Diagramoms gauti naudota Euklidinė norma. Centrinės diagramos parametras $D=1$, o esančios dešinėje $D=5$.
  ]
) <finance>

@finance[Pav.] pateiktos rekurentinės diagramose matome nehomogeniškai pasiskirsčiusius juodus taškus, signalas yra nestacionarus. Diagramose taip pat pastebime vertikalių ir horizontalių linijų, tai rodo, kad signale yra atkarpų per kurias jis kinta nežymiai palyginus su visa signalo imtimi. Diagrama su didesniu $D$ parametru pasireiškia glotnesniais raštais, kuris primena Gauso suliejimą (_angl. Gaussian blur_); šio parametro didinimas padeda atsikratyti triukšmo.


