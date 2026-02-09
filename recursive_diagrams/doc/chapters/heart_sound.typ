= Širdies garsas

#figure(
  grid(
    columns: 240pt,
    gutter: 12pt,
    image("../assets/diagrams/heart_sound/signal.png")
  ),
  caption: [ Širdies garso įrašo signalas ]
) <heart_sound_sig>

@heart_sound_sig[Pav.] matome pavyzdinį sveiko vyro dešiniosios viršutinės krūtinkaulio kraštinės (širdies) garso įrašą paimtą iš širdies ir plaučių duomenų rinkinio įrašyto su klinikiniu manekenu naudojant skaitmeninį stetoskopą @hls-cmds. Garso įrašo diskretizavimo dažnis (_angl. sampling rate_) yra $4000$Hz. Prieš rekurentinių diagramų generavimą duomenys buvo praretinti 100 kartų. Rezultate diagramos buvo generuojamos iš signalo, kurio imčių skaičius yra $N=599$.

#figure(
  grid(
    columns: (120pt, 120pt, 120pt),
    gutter: 24pt,
    image("../assets/diagrams/heart_sound/a.png"),
    image("../assets/diagrams/heart_sound/b.png"),
    image("../assets/diagrams/heart_sound/c.png")
  ),
  caption: [ Širdies garso įrašo rekurentinės diagramos su parametrais $D=2,p=0.1$ (vartotojo pasirinktas juodų taškų procentas diagramoje) ir Euklidine norma. Keičiamas parametras $d$ (iš kairės į dešinę): $2, 5, 7$ ]
) <heart_sound_rd>

@heart_sound_rd[Pav.] matome, kad širdies garso signalas pasižymi beveik homogenišku juodų taškų išsidėstymu, kas žymi signalo stacionarumą. Išsidėstymas turi nežymią tvarką, kuri nyksta didinant parametrą $d$ ir kartu su homogenišku juodų taškų pasiskirstymu žymi vyraujantį atsitiktinį triukšmą.