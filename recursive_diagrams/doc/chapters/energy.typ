= Elektros energijos kiekis suvartojamas Lietuvoje

#figure(
  image("../assets/diagrams/energy/signal.png"),
  caption: [ 2025m. Elektros energijos kiekio suvartojimo Lietuvoje  priklausomybė nuo paros valandos. Intervalas tarp diskrečių signalo taškų -- 15 min. Kairėje duomenys pavaizduotas visiem metams, o dešinėje tik birželio mėnesiui. ]
) <energy_sig>

Toliau naudosime apibrėšime ir analizei naudosime neįprasta techniką, kuri yra pagrįsta rekurentinėmis diagramomis. Turint ilgą signalą, mes sudalinsime intervalą į $N$ dalių ir kiekvienai individualiai sudarysime rekurentinę diagramą, tuomet panariui sudėsime šias diagramas, kadangi jos yra matricos su reikšmėmis 0 arba 1. Rezultate turėtume gauti jungtinį paveikslą, kuris išryškina sutampančias rekurentinės diagramos detales. Šiam paveikslui galime taikyti panašias struktūrų atpažinimo taisykles kaip ir įprastoms rekurentinėms diagramoms.

#figure(
  grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 12pt,
    rect(stroke: 2pt, inset: 0pt, )[
      #image("../assets/diagrams/energy/megadiagram.png")
    ],
    image("../assets/diagrams/energy/rd_main_diag.png", scaling: "pixelated"),
    image("../assets/diagrams/energy/rd_off_diag.png", scaling: "pixelated")
  ),
  caption: [Jungtinė rekurentinė diagrama gauta naudojant anksčiau apibūdintą techniką. 2025m. duomenys buvo sukarpyti į dvylika dalių (po diagramą kiekvienam iš mėnesių, tačiau norint užtikrinti tokį patį diagramų dydi buvo paimtos tik pirmos 28 kiekvieno mėnesio dienos). Kiekvienai signalo atkarpai buvo sudaryta rekurentinė diagrama su parametrais $D=2, p=0.3, d=1$ bei maksimumo norma. Bendras rezultatas matomas kairėje, tačiau dėl didelės diagramos raiškos įdėtos individualių dienų iškarpos. Centre matome 8 mėnesio dienos iškarpą esančia ant pagrindinės diagonalės, o dešinėje iškarpą ne ant pagrindinės diagonalės -- 8 d., 15 d. Visoms diagramoms naudojama "Viridis" spalvų paletė.]
) <energy_img>

@energy_img pagrindinėje diagramoje matome homogenišką raštą, kuris dengia visą diagramos sritį, čia galima pastebėti, kad šis raštas pasikartoja 28 kartus -- tiek, kiek kiekvienam mėnesiui buvo paimta dienų norint sudaryti diagramą, iš šios detalės galime spręsti, kad individualių dienų signalai tarpusavyje yra pakankamai panašūs, tai matosi pažvelgus ir į @energy_sig pateiktą mėnesio suvartojamos energijos diagramą -- suvartojamas kiekis diena pakyla, o naktį krenta.

@energy_img centrinėje iškarpoje, kuri yra ties jungtinės diagramos pagrindine diagonale, matome, kad paveiklas yra gana šviesus vietose toliau nuo diagonalės, tai žymi, kad individualios dienos signale yra trendas, o signalas nėra stacionarus.

@energy_img kairėje esančioje diagramoje matome, kad iki 6 val. ir nuo 18 val. susidaro panašios struktūros kaip ir centrinėje diagramos iškarpoje, tai reiškia, kad nepriklausomai nuo mėnesio dienos, nakti suvartojamas energijos kiekis išlieka panašus, o dienos metu šis sąryšis pranyksta.