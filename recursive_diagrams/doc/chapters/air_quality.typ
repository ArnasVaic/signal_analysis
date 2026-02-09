= Oro kokybė

#figure(
  grid(
    columns: 240pt,
    gutter: 12pt,
    image("../assets/diagrams/air_quality/signal.png")
  ),
  caption: [ 
    Anglies monoksido koncentracijos ore duomenys iš sensoriaus, kuris buvo pastatytas Italijos miestelio laukuose. Duomenis gauti iš oro kokybės duomenų rinkinio @air_quality_360.
  ]
) <air_quality_sig>

Šio signalo imčių skaičius yra $N=9356$, todėl prieš rekurentinių diagramų generavimą duomenys buvo praretinti 20 kartų.

#figure(
  grid(
    columns: (120pt, 120pt, 120pt),
    gutter: 24pt,
    image("../assets/diagrams/air_quality/a.png"),
    image("../assets/diagrams/air_quality/b.png"),
    image("../assets/diagrams/air_quality/c.png")
  ),
  caption: [ 
    Rekurentinės diagramos sugeneruotos iš anglies monoksido konkcentracijos signalo. Parametrai $D=2, d=1$, naudojama Euklidinė metrika. Keičiamas parametras $p$, kuris žymi vartotojo pasirinktą juodų taškų procentą diagramoje (iš kairės į dešinę): $0.1, 0.25, 0.5$
  ]
) <air_quality_rd>
