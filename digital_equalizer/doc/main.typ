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

= Naudojami signalai

#set enum(numbering: "1.")

+ Gitaros garsas
+ Muzikiniai įrašai
+ Sintetiniai signalai

= Algoritmo korektiškumas

Kad būtume užtikrinti mūsų greitosios Furje transformacijos (_angl. fast fourier transform, FFT_) algoritmo teisingumu, palyginsime rezultatus su SciPy mokslinių skaičiavimų paketo FFT algoritmo implementacija. Pirmiausia palyginkime skirtumą tarp realių ir menamų reikšmių kurias gauname apdoroję tokį signalą:

$
f(t)=sin(2pi (2t) / N)+1/2 sin(2pi (4t)/N), quad "kur" t = 1, 2, ...,N, quad "o" N = 16
$

Mažą skaičių taškų $N$ renkamės tam, kad palyginimo rezultatus būtų paprasčiau interpretuoti.

#figure(
    image("assets/diagrams/values_cmp.png"),
    caption: [Transformuoto signalo $cal(F){f(t)}$ realių ir menamų reikšmių palyginimas, kai naudojamos skirtingos FFT algoritmo implementacijos (SciPy ir šiam tyrimui skirtas Cooley-Tukey algoritmas @cooley1965algorithm). ]
) <values_cmp>

Kaip matome @values_cmp menamos reikšmės sutampa idealiai, tuo tarpu realios reikšmes turi nedidelių skirtumų, tai gali lemti float tipo tikslumas python aplinkoje $epsilon approx 2.22 times 10^(-16)$.

#pagebreak()

= Algoritmų greitaveikos palyginimas

Standartinis diskrečios furje transformacijos algoritmas (_angl. discrete fourier transform, DFT_) yra neefektyvus praktiniams taikymams, nes jo veikimo sudėtingumas yra $O(n^2)$, o garso signaluose esančių diskrečių taškų kiekis dažniausiai siekia kelias dešimtis tūkstančių per sekundę. Dėl šios priežasties praktikoje dažniausiai naudojame greitąją Furje transformaciją (_angl. fast fourier transform, FFT_). Šiame turime naudosime Cooley-Tukey algoritmo implementaciją kurios sudėtingumas yra $O(n log n)$. Palyginsime šių algoritmų greitaveiką su įvairių ilgių signalais.

#figure(
  image("assets/diagrams/speed.png", width: 320pt),
  caption: [Klasikinio DFT ir Cooley-Tukey FFT algoritmų veikimo trukmės priklausomybė nuo signalo ilgio. Naudojama logaritminė skalė.]
) <speed>

@speed matome, kad Cooley-Tukey FFT algoritmas yra daug efektyvesnis negu klasikinis DFT algoritmas, tokio rezultato ir galėjome tikėtis. Logaritminė skalė naudojame todėl, kad be jos FFT algoritmas yra tiek kartų greitesnis, kad atrodo, kaip horizontali linija lyginant su kitu algoritmu.

= Skaitmeninis ekvalaizeris

== Audio įrašo garsinimas pasirinktame dažnių spektre

#figure(
  grid(
    columns: 2,
      image("assets/diagrams/ceg-sound.png"),
      image("assets/diagrams/ceg-spectral.png"),
  ),
  caption: [Kairėje -- FFT algoritmas pritaikytas audio signalui kuriame iš eilės gitara sugrojamos natos C, E, G. Dešinėje -- šio signalo dažnių spektras.]
) <ceg-sig-and-spec>

Norint pademonstruoti skaitmeninio ekvalaizerio veikimą naudosime @ceg-sig-and-spec pavaizduotą audio signalą. Kadangi trijų natų dažniai yra skirtingi ir nėra vienas kito kartotiniai, taikantis į specifinį dažnių intervalą aplink vieną iš natų turėtume gauti garso signalą, kuriame būtų pagarsinta tik pasirinkta nata. Galima pastebėti, kad dažnių spektre yra ir kitų dažnių, kurie sutampa su grojamų natų oktavomis, taip yra todėl, kad instrumentų skleidžiamos bangos nėra idealios ir turi harmoningų dažnių.

#figure(
  grid(
    columns: 2,
    image("assets/diagrams/eq-gain.png"),
    image("assets/diagrams/eq-applied.png")
  ),
  caption: [Kairėje -- garso stiprinimo (_angl. gain_) funkcija, taikomasi į dažnių intervalą išsidėsčiusį aplink 130.81 Hz, arba kitaip, C natą per oktavą žemiau nei vidurinė C nata. Dešinėje -- audio signalas iš @ceg-sig-and-spec ir naujas signalas, kuriam su skaitmeniniu ekvalaizeriu buvo pritaikyta kairėje matoma garso stiprinimo funkcija. ]
) <eq-applied>

Kaip matome @eq-applied signalui pritaikius garso stiprinimo funkcija su skaitmeniniu ekvalaizeriu naujame garso signale matome stiprų audio signalo formos padidėjimą (ir pastebimą pagarsėjimą audio įraše). Galima pastebėti, kad audio įrašę, nežymiai pagarsėjusi yra ir E nata, tačiau taip yra todėl, kad garso stiprinimo funkcijos varpo forma nežymiai apima yra E natos dažnį -- 164.81 Hz. Norint išvengti tokio efekto reikėtų susiaurinti garso stiprinimo funkciją, kuri šiuo metu apsirašo taip:

$
  "gain"(f) = 1 + A exp(-(f - f_"C3")^2 / (2w^2))
$

kur $f_"C3"$ yra C3 natos dažnis (130.81 Hz), $w=15$ yra funkcijos plotį reguliuojantis parametras, o $A=10$ yra gaunamo garso stiprumą reguliuojantis parametras. Jei padidintume parametro $w$ reikšmę, stiprinimo funkcija apimtų ir kitų natų dažnius, todėl jie taip pat būtų pagarsinti kaip matoma @eq-applied-wider

#figure(
  grid(
    columns: 2,
    image("assets/diagrams/eq-gain-wide.png"),
    image("assets/diagrams/eq-applied-wide.png")
  ),
  caption: [Kairėje -- garso stiprinimo (_angl. gain_) funkcija, taikomasi į dažnių intervalą išsidėsčiusį aplink 130.81 Hz, arba kitaip, C natą per oktavą žemiau nei vidurinė C nata. Dešinėje -- audio signalas iš @ceg-sig-and-spec ir naujas signalas, kuriam su skaitmeniniu ekvalaizeriu buvo pritaikyta kairėje matoma garso stiprinimo funkcija. ]
) <eq-applied-wider>

== Pašalinių garsų šalinimas

Skaitmeninį ekvalaizerį galime panaudoti daugybe įvairių būdų -- vienas iš jų pašalinių garsų panašalinimui. Jei triūkšmo garso dažniai artimai nesutampa su orginalaus audio signalo dažniais, naudodami skaitmenini ekvalaizerį, galime nesunkiai jį pašalinti. Šiame pavyzdžiui nagrinėsime gitaros melodijos garso signalą:

#figure(
  grid(
    columns: 2,
    image("assets/diagrams/melody-original-time.png"),
    image("assets/diagrams/melody-original-spectrum.png")
  )
  ,
  caption: [Orginalus melodijos garso įrašas be pridėto triukšmo bei jo dažnių spektras dešinėje.]
) <orig-melody>

Garso įrašą užteršime sintetiniu garso signalu, kuris egzistuoja trijuose specifiniuose dažniuose, kurie randasi už @orig-melody matomų melodiją sudarančių dažnių.

#figure(
  grid(
    columns: 2,
    image("assets/diagrams/noise-time.png"),
    image("assets/diagrams/noise-spectrum.png")
  )
  ,
  caption: [Sintentinis triukšmas, kurį sudaro trys dažniai: 1000Hz, 2500Hz ir 5000Hz ir jo dažnių spektras dešinėje.]
) <noise>

Sintetinį audio signalą @noise sudėsime su melodijos audio signalu ir gausime užterštą signalą:

#figure(
  grid(
    columns: 2,
    image("assets/diagrams/melody-noisy-time.png"),
    image("assets/diagrams/melody-noisy-spectrum.png")
  )
  ,
  caption: [Triukšmu užterštas melodijos signalas ir jo dažnių spektras]
) <noisy_melody>

@noisy_melody pavaizduotas užterštas audio signalas. Galime įsivaizduoti, kad taikydami šį metodą, mūsų įvesties signalas atrodytų būtent taip, o užduotis būtų surasti orginalų signalą iš @orig-melody Kaip matome iš užteršto signalo spektro, melodijos ir triukšmo dažniai nepersidengia, todėl galime sukonstruoti garso stiprinimo funkciją, kuri taikosi į šiuo dažnius ir juos pašalina. Tokia funkcija galėtų atrodytų štai taip:

$
  "gain"(f) = cases(
    0\, "jei" f in (900, 1100) union (2400, 2600) union (4900, 5100),
    1 "kitu atvjeu"
  )
$

Vizualiai tokia stiprinimo funkcija atrodo taip:

#figure(
  image("assets/diagrams/eq-function.png", width: 300pt),
  caption: [Garso stiprinimo funkcija specifiniams dažniams panaikinti.]
) <noise-cancel_gain>

Pritaike @noise-cancel_gain pavaizduotą garso stiprinimo funkciją užterštam garso signalui @noisy_melody gauname naują audio signalą:

#figure(
  grid(
    columns: 2,
    image("assets/diagrams/melody-recovered-time.png"),
    image("assets/diagrams/recovered-spectrum.png")
  )
  ,
  caption: [Atkurtas garso signalas ir jo dažnių spektras]
) <recovered_melody>

Kaip matome @recovered_melody, atkurto garso signalo spektre nebėra triukšmo dažnių, o garso signalas taip pat vizualiai panašus į prieš tai buvusį, tačiau geresniam matomumui parodysime skirtumą tiesiogiai:

#figure(
  image("assets/diagrams/all-signals-comparison.png", width: 300pt),
  caption: [Audio signalų palyginimas -- orginali melodija, triukšmas ir atkurtas signalas.]
) <compare_signals>

Kaip matome @compare_signals, atkura melodijos signalas yra panašus į orginalios melodijos, nors ir yra matomas skirtumas tarp šių signalų (oranžinės juostos), klausant šių įrašų skirtumas yra beveik nepastebimas.

== Seno telefono efektas

Naudojant skaitmeninį ekvalaizerį galime suteikti audio įrašui įvairių efektų, vienas iš klasikinių pavyzdžių yra seno telefono efektas -- senieji telefonai ne taip gerai pernešdavo labai žemus bei labai aukštus dažnius, dėl šios priežasties ir atsiranda gerai žinomas seno telefono garso efektas. Kaip naudojantis skaitmenino ekvalaizerio pagalba pašalinti tam tikrus dažnius jau matėme praeitame pavizdyje, šiuo atvjeu darome tą patį, tik su kitokiu tikslu. Pritaikisime šį efektą muzikinio įrašo Rex Orange County -- Sunflower iškarpai.

#figure(
  grid(
    columns: 2,
    image("assets/diagrams/telephone-gain.png"),
    image("assets/diagrams/telephone-time-comparison.png")
  )
  ,
  caption: [Kairėje -- garso stiprinimo funkcija, kuri šalina labai žemus (< 300Hz) ir aukštus (> 3kHz) dažnius, o dešinėje -- skirtumas tarp audio įrašų, kai jam buvo pritaikytas telefono efektas.]
) <telephone>

Kaip matome @telephone, pritaikius efektą, signalo kreivė šiek tiek susitraukia, nes naikindami dažnius panaikiname dalį informacijos ir sumažiname signalo energiją. Nors ir vizualiai nesimato, gautas įrašo kokybė yra stipriai sumažėjusi ir atrodo lyg audio signalas buvo gautas įrašant orginalų įrašą pro seną telefoną.

== _Bass boost_ efektas

Dar vienas dažnas skaitmeninio ekvalaizerio taikymas yra žemų dažnių stiprinimas (_angl. bass boost_). Toks efektas plačiai naudojamas muzikos grotuvuose, atumobilių garso sistemose bei įvairiose garso apdorojimo programose. Stiprinant žemus dažnius garsas tampa „gilesnis“, labiau juntamas žemų tonų ritmas bei smūgiai.

Šiame pavyzdyje nagrinėsime elektroninės muzikos (_angl. drum and bass_) garso įrašo fragmentą, kuriame žemų dažnių komponentai yra itin svarbūs. Kadangi būtent žemųjų dažnių srityje randasi mušamųjų bei bosinių instrumentų garsas, sustiprinę šį dažnių intervalą galime aiškiai išgirsti skirtumą tarp orginalaus ir apdoroto signalo.

Naudosime tokią garso stiprinimo funkciją:

$
  "gain"(f) = 1 + A exp(-(f - f_c)^2 / (2w^2))
$

kur $f_c = 120"Hz"$ -- stiprinimo centro dažnis, $w = 120$ -- stiprinimo funkcijos plotis, o $A = 3$ -- stiprinimo intensyvumas. Ši funkcija stiprina dažnius esančius aplink 120 Hz ir palaipsniui silpnėja tolstant nuo šio dažnio.

#figure(
  grid(
    columns: 2,
    image("assets/diagrams/bass-boost-gain.png"),
    image("assets/diagrams/bass-boost-comparison.png")
  ),
  caption: [
    Kairėje -- žemų dažnių stiprinimo funkcija, kurios maksimumas yra ties 120 Hz. 
    Dešinėje -- audio signalas prieš ir po bass boost efekto pritaikymo.
  ]
) <bass_boost>

Kaip matome @bass_boost, pritaikius žemų dažnių stiprinimą, signalo amplitudė padidėja, nes žemųjų dažnių komponentai įgauna didesnę energiją. Klausant apdoroto įrašo per garso sistemą, kuri gali perteikti žemus dažnius, galima aiškiai girdėti sustiprintą mušamųjų bei boso garsą.

== _Dial-up_ modemų protokolo spektrograma

Spektrograma yra vienas iš Furje transformacijos taikymų, leidžiantis analizuoti signalo dažnius laiko atžvilgiu. Ji gaunama taikant trumpalaikę Furje transformaciją (_angl. short-time Fourier transform, STFT_), kai signalas padalinamas į persidengiančius laiko langus ir kiekvienam langui apskaičiuojamas atskiras dažnių spektras. Tokiu būdu gaunamas dvimatis vaizdas, kuriame horizontalioje ašyje vaizduojamas laikas, vertikalioje -- dažnis, o spalvos intensyvumas atitinka signalo amplitudę. Norint pademonstruoti spektrogramos pritaikymą realaus pasaulio signalams, analizuosime _dial-up_ (telefono linijomis veikiančių modemų) signalo pavyzdį. Analizei naudojamas lango dydis 4096 ir žingsnis tarp langų 1024.

#figure(
  grid(
    columns: 2,
    image("assets/diagrams/spectrogram-time.png"),
    image("assets/diagrams/spectrogram-log.png")
  ),
  caption: [
    Kairėje -- _dial-up_ audio signalas signal. 
    Dešinėje -- to paties signalo spektrogramos iškarpa logaritminėje skalėje, kurioje matomos protokolo fazės.
  ]
) <dialup-spec>

Kaip matyti @dialup-spec, spektrogramoje aiškiai išskiriamos kelios skirtingos signalo fazės. Paralelios linijos spektrogramos pradžioje skambučio signalą pradžią, tai yra pirmas portokolo žingsnis, tuomet matome išdėstytus taškus (2-4s), kurios savyje laiko užkoduotą informaciją apie telefono numerį, kuriam yra skambinama. Protokolas turi ir tolimesnių fazių, tačiau šioje ataskaitoje į tai nesigilinsime, o apie jas detaliau sužinoti galima @windytan_dialup. Šis pavyzdys yra demonstracija, kad spektrogramą galima naudoti kaip garso įrašo nuotrauką, kuri suteikia naudingos informacijos apie tai, kas vyksta signale, šis metodas turi begale taikymų įvairiose mokslo srityse. Verta paminėti, kadl ogaritminė amplitudės skalė yra ypač svarbi (y ašis yra matuojama decibelais, o ne abstrakčiais normalizuotos aplitudės vienetais), nes leidžia vizualizuoti tiek stiprius, tiek silpnesnius dažninius komponentus viename paveiksle. Be jos silpnesni signalai būtų sunkiai pastebimi dėl didelio rodomų dažnių intervalo.

#pagebreak()

= Išvados

Šio darbo metu buvo įgyvendintas ir išanalizuotas greitosios Furje transformacijos (FFT) algoritmas, paremtas Cooley-Tukey metodu. Palyginus su SciPy realizacija nustatyta, kad rezultatai sutampa su labai maža paklaida, kurią galima paaiškinti slankiojo kablelio skaičiavimų tikslumo ribotumais.

Greitaveikos analizė parodė, kad FFT algoritmas yra ženkliai efektyvesnis už klasikinę diskrečią Furje transformaciją (DFT), ypač didėjant signalo ilgiui. Tai patvirtina teorinį sudėtingumų skirtumą $O(n^2)$ ir $O(n log n)$.

Praktinėje dalyje sukurta skaitmeninio ekvalaizerio sistema parodė, kad galima selektyviai stiprinti arba slopinti pasirinktus dažnius audio signale. Pritaikius stiprinimo funkciją C natos dažniui, buvo pastebėtas šio komponento išryškinimas signale, kas patvirtina filtravimo metodo veikimą. Taip pat parodyta, kad keičiant stiprinimo funkcijos parametrus galima reguliuoti paveikiamų dažnių plotį ir tokiu būdu valdyti, kiek aplinkinių dažnių bus sustiprinta.

Triukšmo šalinimo eksperimento metu parodyta, kad FFT pagrindu veikiantis ekvalaizeris gali būti naudojamas siaurajuosčio triukšmo pašalinimui. Kadangi sintetinio triukšmo dažniai nesutapo su pagrindiniais melodijos komponentais, pritaikius atitinkamą slopinimo funkciją pavyko beveik pilnai pašalinti pašalinius dažnius ir atkurti signalą, kuris vizualiai bei akustiškai buvo labai panašus į originalų įrašą.

Telefono efekto pavyzdys parodė, kad ekvalaizeris gali būti naudojamas ne tik signalo atkūrimui, bet ir garso efektų kūrimui. Pašalinus labai žemus bei aukštus dažnius buvo gautas garsas, primenantis senų telefono linijų perduodamą signalą.

Bass boost eksperimento metu parodyta, kad stiprinant žemųjų dažnių sritį galima išryškinti mušamųjų bei bosinių instrumentų komponentus. Pritaikius žemų dažnių stiprinimą padidėjo signalo amplitudė bei subjektyviai sustiprėjo garso „gilumas“, kas atitinka praktikoje naudojamų garso sistemų veikimo principus.

Darbo pabaigoje FFT algoritmas buvo pritaikytas spektrogramos sudarymui naudojant trumpalaikę Furje transformaciją (STFT). Analizuojant dial-up modemų signalą parodyta, kad spektrograma leidžia stebėti, kaip signalo dažninė sudėtis kinta laike. Gautoje spektrogramoje buvo galima atskirti skirtingas protokolo fazes bei charakteringus siaurajuosčius dažninius komponentus. Taip parodyta, kad Furje transformacijos metodai gali būti naudojami ne tik garso filtravimui, bet ir sudėtingų realaus pasaulio signalų analizei bei vizualizacijai.

Apibendrinant galima teigti, kad Furje transformacija yra vienas svarbiausių skaitmeninio signalų apdorojimo metodų, leidžiantis efektyviai analizuoti, modifikuoti ir interpretuoti įvairius audio signalus tiek teoriniuose, tiek praktiniuose taikymuose.
 
#pagebreak(weak: true)
#include "chapters/conclusions.typ"
#pagebreak(weak: true)
#bibliography("references.bib")
#pagebreak(weak: true)
#include "backmatter/appendices.typ"