# Historicko-krejčovská příručka (15. století)

Tento dokument slouží jako krejčovská a anatomická reference pro evropské oděvy 15. století implementované v aplikaci JPPatternCreator.

---

## 1. Silueta a krejčovská mechanika 15. století

Pozdně středověké krejčovství (cca 1420–1500) dosahovalo anatomicky dokonale padnoucí, přiléhavé siluety bez existence moderních elastických materiálů. Toho bylo dosahováno třemi hlavními postupy:
1. **Zakřivené švy a stříhání po šikmém směru látky (Bias Cut)**: Využití přirozené mechanické pružnosti vlněného sukna při diagonálním namáhání vláken.
2. **Strukturální výztužné vrstvy**: Kabátce byly hustě prošívány (*pad-stitched*) několika vrstvami hrubého lněného plátna, čímž vznikl pevný korzetový základ trupu.
3. **Závěsná mechanika (Doublet Points)**: Nohavice byly přivázány přímo k pasovému lemu kabátce pomocí pevných tkanic s kovovými nákončími provlečených páry obšitých dírek.

---

## 2. Nohavice (Hosen / Chausses)

Během 15. století se nohavice definitivně vyvinuly ze dvou samostatných trubic do jednoho spojeného kusu oděvu.

```
                      Pasový lem / vázací pás
               ┌───────────────────────────┐
               │    o  o           o  o    │  <- Páry dírek pro uvázání ke kabátci
               │                           │
   Horní       │    ┌─────────────────┐    │
   sedová ────>│   /                   \   │
   křivka      │  │      Krytí          │  │  <- Klín / krytí rozkroku (codpiece)
               │   \    rozkroku       /   │
               │    └─────────────────┘    │
               │                           │
               │       Levá       Pravá    │
               │     nohavice    nohavice  │
               │                           │
               │        (Linie kolene)     │
               │                           │
               │        (Linie lýtka)      │
               │                           │
               │        (Linie kotníku)    │
               │                           │
               │    Nárt / chodidlo        │
               └───────────────────────────┘
```

### Klíčové anatomické zóny:
1. **Pasový lem**: Sedí buď těsně pod přirozeným pasem, nebo na pánevním hřebeni, kde je pevně přivázán ke kabátci.
2. **Sedová a rozkroková křivka**:
   - Zadní sedová křivka musí poskytovat dostatek prostoru pro předklon, sezení i jízdu na koni.
   - Dělené nohavice: rozkrok a hýždě jsou otevřené a je pod nimi vidět lněné prádlo (*braies*).
   - Spojené nohavice: zadní šev je plně uzavřen a v přední části je přišit krycí klín rozkroku (*codpiece*).
3. **Tvarování nohy**:
   - Extrémně těsný střih od stehna až ke kotníku.
   - Vyžaduje nulový nebo mírně záporný přídavek na volnost kolem kolene a lýtka, protože vlněné sukno střižené mírně šikmo se přirozeně natáhne.
4. **Varianty zakončení nohy**:
   - **Se šlapkou a chodidlem**: Plně uzavřená nohavice s našitou koženou nebo sukněnou podrážkou.
   - **Špičatá bota (*crakow / poulaine*)**: Prodloužený zobákovitý hrot špičky, módní v polovině 15. století.
   - **S třmínkem pod chodidlo**: Nohavice končí u kotníku a pod chodidlem vede pouze páska; nosí se přes lněné ponožky.

---

## 3. Kabátec (Doublet / Pourpoint)

Kabátec tvoří architektonický základ mužského oděvu 15. století.

### Požadované díly pro 1. fázi:
1. **Přední díly (2x)**:
   - Hluboký průramek umožňující zvednutí paží, aniž by se kabátec vytahoval z pasu.
   - Zapínání: přední okraj šněrovaný spirálovým šněrováním nebo zapínaný na hustou řadu drobných litých knoflíků.
   - Tvarování hrudi: střiženo s lehkým vyklenutím pro vycpání a zpevnění hrudi.
2. **Zadní díl (1x se středovým přehybem nebo 2x se zadním švem)**:
   - Výrazné projmutí kopírující prohnutí bederní páteře.
3. **Stojáčkový límec (2x vnější + vnitřní výztuha)**:
   - Vysoký tuhý límec objímající krk s mírným rozevřením pod bradou.
4. **Prohnuté rukávy (2 páry)**:
   - Rukávy se stříhají s anatomicky předehnutým loktem, aby kopírovaly přirozený klidový postoj rukou.
5. **Spodní šůsky / sukénka (*peplum*) (4 až 8 samostatných dílků)**:
   - Krátké lichoběžníkové šůsky našité do pasového švu. Chrání boky a překrývají šněrovací dírky na nohavice.

---

## 4. Systém vázacích dírek (Doublet Points)

Mechanické propojení kabátce a nohavic:
- **Umístění**: Podél vnitřního pasového švu kabátce a na horním lemu nohavic.
- **Rozmístění**:
  - Dírky jsou vždy v párech vzdálených od sebe cca $2,0\text{ až }2,5\text{ cm}$.
  - Obvyklý počet: 4 až 6 párů po obvodu pasu (2 vpředu na bocích podbřišku, 2 na bocích, 2 vzadu na bedrech).
- **Zobrazení v CADu**:
  - Dírky se značí jako kružnice ($\varnothing 4\text{ mm}$) se středovým křížkem.
  - Včetně zobrazení zpevňujícího obšití ($\varnothing 12\text{ mm}$).
