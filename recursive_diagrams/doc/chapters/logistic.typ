= Logistinis atvaizdis

#figure(
  grid(
    columns: (1.1fr, 1fr, 1fr),
    gutter: 12pt,
    image("../assets/diagrams/logistic/c.png"),
    image("../assets/diagrams/logistic/a.png"),
    image("../assets/diagrams/logistic/b.png"),
  ),
  caption: [ 
    Logistinio atvaizdžio $x_(n+1)=4x_n (1-x_n), x_0=0.51$ chaotinis signalas (kairėje) ir jo rekurentinės diagramos su parametrais $r=0.1$ (centre), $r=0.5$ (dešinėje). Signalo imčių skaičius $N=400$.
  ]
) <logistic>

@logistic[Pav.] pateiktas logistinio atvaizdžio signalas yra skirtas parodymui, kad rekurentinių diagramų algoritmas yra įgyvendintas korektiškai. Šiuos rezultatus reikėtų lygintis su kurso medžiagoje @sig2021 pateiktomis logistinio atvaizdžio rekurentinėmis diagramomis su tokiais pačiais parametrais. Kaip pažymėta kurso medžiagoje, trumpos atkarpos paralelios centrinei linijai sufleruoja, kad signalo struktūroje yra panašumų, tačiau jie yra trumpi ir greit nyksta, dėl to diagrama gana panaši į visiškai atsitiktinio signalo.

