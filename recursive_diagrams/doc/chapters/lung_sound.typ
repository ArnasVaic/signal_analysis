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
    rect(stroke: 2pt, inset: 0pt, )[
      #image("../assets/diagrams/lung_sound/a.png") 
    ],
    rect(stroke: 2pt, inset: 0pt, )[
      #image("../assets/diagrams/lung_sound/b.png")
    ],
    rect(stroke: 2pt, inset: 0pt, )[
      #image("../assets/diagrams/lung_sound/c.png")
    ]
  ),
  caption: [ Plaučių garso įrašo rekurentinės diagramos su parametrais $D=2,r=0.1, d=1$ ir skirtingomis normomis (iš kairės į dešinę): Manheteno, Euklidinė ir maksimumo. ]
) <lung_sound_rd>

@lung_sound_rd pavaizduotos diagramos pasireiškia nehomogeniniu juodų taškų pasiskirstimu, tai reiškia, kad signalas yra nestacionarus, tačiau verta paminėti, kad nestacionarumas yra kitoks negu matėme @finance, šiu atveju signalas turi dvi būsenas -- aplinkos triukšmo ir plaučių kvėpavimo. Taip pat matome daugelį juodų taškų telkinių, kurie signalizuoja (pun intended), kad tarpais signalo būsena nekinta ir taip iš ties galime pamatyti net pačiame signale -- iš viso turime šešis intervalus, kuriuose signalo reikšmė atrodo pastovi ir tai sutampa su rekurentinėje diagramoje matomu skaičiu telkinių (horizontaliai).

Šiame pavyzdyje bandome keisti normą, o kitus parametrus laikyti pastoviais. Kaip ir nurodytą mokymo priemonėje @sig2021 kokybinio skirtumo nėra, nes diagramoje neatsiranda papildomų darinių bei struktūrų. Iš pirmo žvilgsnio šis parametras gali pasirodyti kiek nereikšmingas -- diagramos atrodo taip pat, tik turi skirtingą juodų taškų skaičių, tačiau pažvelgus iš greitaveikos vertinimo pusės skirtumas yra didžiulis. Manheteno metrika reikalauja suskaičiuoti kiekvieno nario modulį ir tuomet bendrą jų sumą, kas reikalauja daug CPU ciklų, taip pat gali atsirasti perteklius (_angl. overflow_). Tokia pati problema atsiranda pasirinkus Euklidinę metriką, čia aritmetiniai veiksmai net sudėtingesni -- modulis, sumavimas, daugyba ir kvadratinė šaknis. Nors kvadratinės šaknies galima išvengti iš anksto suskaičiavus $r^2$ ir lyginimą atliekant su ja, nedingsta pertekliaus rizika bei daugybos ir sumavimo operacijų sudėtingumas. Greitaveikos prasme patraukliausia norma yra maksimumo dėl to, kad ji nereikalauja aritmetinių veiksmų, o tik surasti narį su didžiausių moduliu. Generuojant diagramas šiam projektui, naudojant maksimumo normą diagrama sugeneruojama 6% greičiau negu naudojant Euklidinę normą, o naudojant Manheteno normą -- 2% greičiau nei naudojant Euklidinę normą.