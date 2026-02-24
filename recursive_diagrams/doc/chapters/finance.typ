= Įmonės "Apple Inc." akcijų kaina

#figure(
  grid(
    columns: (1.3fr, 1fr, 1fr),
    gutter: 12pt,
    image("../assets/diagrams/finance/signal.png"),
    rect(stroke: 2pt, inset: 0pt, )[
      #image("../assets/diagrams/finance/a.png")
    ],
    rect(stroke: 2pt, inset: 0pt, )[
      #image("../assets/diagrams/finance/c.png")
    ]
  ),
  caption: [
    "Apple Inc." akcijų kainos svyravimai 2025 m. Duomenys gauti naudojant `yfinance` python paketą @yfinance2024. Rekurentinės diagramos gautos su parametrais $p=0.1, d=1$, kur $p$ yra vartotojo pasirinktas juodų taškų procentas diagramoje. Diagramoms gauti naudota Euklidinė norma. Centrinės diagramos parametras $D=1$, o esančios dešinėje $D=5$. Signalo imčių skaičius $N=494$ su 4 val. tarpais (neskaitant laiko, kada akcijų birža nedirba). Duomenys papildomai apdoroti nebuvo.
  ]
) <finance>

@finance pateiktose rekurentinėse diagramose matome nehomogeniškai pasiskirsčiusius juodus taškus, todėl signalas yra nestacionarus. Remiantis @marwan2007recurrence pateiktomis raštų prasmės interpretacijomis, vertikalios bei horizontalios linijos žymi lėtai kintančias arba laminarines būsenas. Išbalę diagramos kampai žymi, kad signale yra vienas arba daugiau trendų. Diagrama su didesniu $D$ parametru pasireiškia glotnesniais raštais, kurie primena Gauso suliejimą (_angl. Gaussian blur_); šio parametro didinimas padeda atsikratyti triukšmo, tačiau gali paslėpti svarbias detales, pavyzdžiui, glotnioje diagramoje nebematome plonų vertikalių bei horizontalių linijų, kurias matėme viduriniame pavyzdyje. Verta paminėti, kad to galėtume išvengti naudojant duomenys, kur intervalas tarp diskrečių taškų būtų didesnis nei 4 val., todėl prieš ruošiant rekurentines diagramas yra svarbu suprasti įvesties duomenis ir rinktis parametrus atsižvelgus į juos.


