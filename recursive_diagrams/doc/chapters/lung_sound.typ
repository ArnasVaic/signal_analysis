= Plaučių garsas

#figure(
  grid(
    columns: 300pt,
    gutter: 12pt,
    image("../assets/diagrams/lung_sound/signal.png")
  ),
  caption: [ Plaučių garso įrašo signalas ]
) <lung_sound_sig>

@lung_sound_sig matome pavyzdinį sveikos moters dešiniojo viršutinio priekinio plaučio garso įrašą paimtą iš širdies ir plaučių duomenų rinkinio įrašyto su klinikiniu manekenu naudojant skaitmeninį stetoskopą @hls-cmds. Garso įrašo diskretizavimo dažnis (_angl. sampling rate_) yra $4000$Hz. Prieš rekurentinių diagramų generavimą duomenys buvo praretinti 100 kartų. Rezultate diagramos buvo generuojamos iš signalo, kurio imčių skaičius yra $N=599$.

#figure(
  grid(
    columns: (120pt, 120pt, 120pt),
    gutter: 24pt,
    image("../assets/diagrams/lung_sound/a.png"),
    image("../assets/diagrams/lung_sound/b.png"),
    image("../assets/diagrams/lung_sound/c.png")
  ),
  caption: [ Plaučių garso įrašo rekurentinės diagramos su parametrais $D=2,r=0.1, d=1$ ir skirtingomis normomis (iš kairės į dešinę): Manheteno, Euklidinė ir maksimumo. ]
) <lung_sound_rd>

@lung_sound_rd pavaizduotos diagramos pasireiškia nehogeniškų juodų taškų pasiskirstimu, tai reiškia, kad signalas yra nestacionarus. Taip pat matome daugelį juodų taškų telkinių, kurie signalizuoja (pun intended), kad tarpais signalo būsena nekinta ir taip iš ties galime patyti net pačiame signale -- iš viso turime šešis intervalus, kuriuose signalo reikšmė atrodo pastovi ir tai sutampa su rekurentinėje diagramoje matomu skaičiu telkinių (horizontaliai).

Šiame pavyzdyje bandome keisti normą, o kitus parametrus laikyti pastoviais. Kaip ir nurodytą mokymo priemonėje @sig2021 kokybinio skirtumo nėra, tačiau kiekvieną diagrama turi vis daugiau juodų taškų, tai nėra optinė apgaulė, juodų taškų koncentraciją pavyzdyje yra (iš kairės į dešinę): \~13%, \~18% ir \~21%.