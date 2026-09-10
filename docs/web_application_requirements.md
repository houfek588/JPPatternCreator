# Požadavky na webovou aplikaci (PRD)

## 1. Shrnutí a vize projektu

**JPPatternCreator Web** je parametrický CAD nástroj určený pro rýsování a tvorbu oděvních střihů specializovaný na **historické oděvy 15. století** (Living History, HEMA a muzejní krejčovství).

Ačkoliv projekt začal jako desktopový prototyp v Python/PyQt6, těžiště vývoje se přesouvá na **webovou platformu jako primární cíl**. Webová aplikace umožňuje krejčím, reenactorům a kostymérům generovat střihy na míru podle tělesných rozměrů zákazníka, upravovat tvarovací parametry pomocí posuvníků, kontrolovat jednotlivé díly a exportovat data pro velkoformátové plotry, běžné tiskárny i digitální řezací stoly.

---

## 2. Cílová skupina a doména oděvů 15. století

### Cílová skupina uživatelů
- **Historická krejčovství a kostyméři**: Profesionální tvůrci šijící historicky věrné oděvy na míru klientům.
- **Reenactoři a living history nadšenci**: Jednotlivci, kteří si šijí vlastní dobový šatník na historické akce.
- **Divadelní a muzejní dílny**: Týmy vyžadující přesné repliky oděvů v měřítku 1:1.

### Zaměření na oděvy pozdního středověku (15. století)
1. **Kalhoty (Nohavice – Hosen / Chausses)**:
   - Spojené nohavice s krytím rozkroku / klínem (*codpiece*).
   - Dělené nohavice vázané ke kabátci nebo spodkům (*braies*).
   - Anatomické varianty zakončení nohy: se šlapkou a chodidlem, tvarovaná klenba nártu, protažená špička (*crakow / poulaine*) nebo třmínek pod chodidlo.
2. **Kabátec (Doublet / Pourpoint)**:
   - Anatomický základ mužského oděvu nesoucí váhu nohavic.
   - **Požadované díly pro 1. fázi**:
     - Přední díly s předním zapínáním na knoflíky nebo šněrováním.
     - Zadní díl s vykrojenými lopatkami a přiléhavou zádovou křivkou.
     - Stojáčkový límec s nastavitelnou výškou a obvodem krku.
     - Prohnuté rukávy (anatomicky zahnutý loket pro volnost pohybu paže).
     - Spodní šůsky / sukénka (*peplum*).
     - **Vázací dírky (Doublet Points)**: Přesně rozmístěné páry zpevněných dírek podél pasové linie pro uvázání a držení nohavic.
3. **Další rozšiřitelné oděvy (2. fáze a dále)**:
   - Svrchníky (cotehardie, houppelande), košile, spodky (braies), kukly (chaperon) a pláště.

---

## 3. Základní architektonické požadavky

### 3.1. Bezstavový server a ochrana soukromí (Strategie 1)
- **Nulové ukládání na serveru**: Server nesmí uchovávat databázi tělesných rozměrů ani osobních údajů zákazníků.
- **Izolované dočasné zpracování**: Veškeré výpočty a exporty probíhají v operační paměti nebo v dočasných souborech v systémovém adresáři (`tempfile.gettempdir()`) s unikátním ID (`uuid.uuid4()`), které jsou po odeslání ihned smazány.
- **Vlastnictví dat u klienta**: Měřené profily a nastavení jsou uloženy výhradně v prohlížeči uživatele.

### 3.2. Deklarativní systém střihů (bez zásahu do kódu)
- **Přidávání střihů bez programování**: Nové oděvy a jejich varianty musí být možné definovat bez nutnosti přepisovat Python kód jádra aplikace.
- **Šablonová architektura**: Oděvy, konstrukční body, výpočetní vzorce, křivky, díly a švové přídavky jsou definovány v deklarativních souborech JSON/YAML.
- Python server tyto šablony dynamicky interpretuje a generuje výstupní geometrii.

### 3.3. Pokročilá správa klientských profilů
- **Lokální perzistence**: Využití `localStorage` a `IndexedDB` v prohlížeči.
- **Přenositelnost dat**:
  - **Jednotlivý export/import**: Export profilu klienta do souboru `.json`.
  - **Hromadná záloha**: Export celé databáze profilů ateliéru do jednoho souboru.
  - **Drag & Drop**: Možnost přetáhnout `.json` soubor s mírami přímo myší do okna prohlížeče pro okamžité načtení.

---

## 4. Funkční požadavky

### 4.1. Generování střihu a parametrické úpravy
- **FR-1.1**: Výpočet geometrie střihu v reálném čase na základě tělesných rozměrů (v centimetrech).
- **FR-1.2**: Tvarovací posuvníky pro úpravu detailů (snížení pasu, šířka nártu, tvar šlapky, křivka rozkroku, hloubka výstřihu límce, zahnutí rukávu).
- **FR-1.3**: Automatická kontrola chyb ve vstupech (`ValidationError`), zamezení nezadaným či záporným rozměrům s lokalizovaným hlášením v češtině a angličtině.

### 4.2. Přepínání dílů a zobrazení na plátně
- **FR-2.1**: Interaktivní vektorové plátno s vysokým rozlišením SVG, podporou přiblížení (zoom), posunu a resetu pohledu.
- **FR-2.2**: **Přepínač částí střihu**: Možnost zobrazit celý střih naráz nebo izolovat jednotlivé dílce:
  - *Nohavice*: Celý spojený střih, konstrukční linie předního dílu, sedová křivka zadního dílu.
  - *Kabátec*: Celá sestava, přední díl, zadní díl, rukáv, límec, pasové šůsky.
- **FR-2.3**: Rozložení dílů na šíři látky (náhled polohování pro stříhání na roli látky).

### 4.3. Krejčovské CAD nástroje
- **FR-3.1 Nastavitelné švové přídavky**:
  - Možnost zapnout/vypnout švové přídavky.
  - Volitelná šířka přídavku (výchozí 1,0 cm, 1,5 cm nebo vlastní hodnota).
  - Vykreslení odsazené linie řezu kolem obrysu dílu.
- **FR-3.2 Značka směru osnovy (Grainline)**:
  - Podélná šipka směru osnovy na každém střihovém dílu pro správné položení na látku.
- **FR-3.3 Sesazovací značky (Notches)**:
  - Značky (nástřihy) podél navazujících švů (průramek–rukávová hlavice, boční švy, úroveň kolene).
- **FR-3.4 Vázací dírky (Doublet Points)**:
  - Automatické vygenerování párů vázacích dírek podél pasu kabátce i nohavic pro šněrování tkanicemi.
- **FR-3.5 Vizuální průvodce měřením těla**:
  - Ilustrovaný diagram těla s přesným popisem, kde a jak jednotlivé míry měřit (VP, OP, OS, BDK, KD, OH, DZ atd.).

---

## 5. Exportní formáty a tiskové výstupy

Aplikace musí podporovat 4 produkční výstupní formáty:

| Formát | Účel použití | Cílové médium | Specifikace |
| :--- | :--- | :--- | :--- |
| **1:1 Plotrové PDF** | Profesionální velkoformátový tisk | Role papíru (A0/A1, šíře 90–120 cm) | Spojitý tisk v měřítku 1:1, kontrolní kalibrační čtverec $10 \times 10\text{ cm}$, název střihu, směr osnovy, soupiska dílů. |
| **Dlaždicové PDF (Tiled)** | Tisk na běžné tiskárně | Kancelářské papíry A4 / US Letter | Automatické rozřezání střihu do mřížky stránek s okrajem na slepení (10 mm), pasovacími křížky a označením pozice (např. „Řada 2, Sloupec 3“). |
| **Vektorové SVG** | Další úpravy v grafických editorech | Inkscape, Adobe Illustrator, CorelDRAW | Čisté vektorové křivky rozdělené do logických vrstev (`linie_rezu`, `linie_svu`, `smer_osnovy`, `znacky`, `popisky`). |
| **CAD DXF** | Průmyslové řezací plotry a CNC | Gerber, Lectra, Optitex, laserové stoly | Formát podle standardu AAMA / ASTM s vrstvami CUT, INTERNAL, GRAINLINE a NOTCH. |

---

## 6. Nefunkční požadavky

### 6.1. Výkon a odezva
- **NFR-1**: Přepočet a překreslení střihu v prohlížeči po pohybu posuvníkem musí proběhnout do **400 ms** (s debouncingem).
- **NFR-2**: Vektorové plátno musí podporovat plynulý posun a zoomování při 60 FPS.

### 6.2. Použitelnost a vzhled
- **NFR-3**: Čisté krejčovské rozhraní s podporou světlého i tmavého režimu.
- **NFR-4**: Responzivní rozvržení fungující na stolním počítači, notebooku i tabletu v dílně.
- **NFR-5**: 100% dvojjazyčné rozhraní s okamžitým přepnutím mezi **češtinou (CZ)** a **angličtinou (EN)** bez znovunačtení stránky.

### 6.3. Spolehlivost a testování
- **NFR-6**: Automatizované testy v Pythonu (`tests/`) pokrývající validaci měr, geometrické výpočty a generování souborů.
- **NFR-7**: Čistý klientský kód bez chyb linteru (`npm run lint`) a spolehlivé sestavení produkčního balíčku (`npm run build`).

---

## 7. Plán fází implementace

### Fáze 1 (aktuální priorita)
- Dokončení kabátce 15. století (přední díl, zadní díl, stojáček, rukávy, šůsky).
- Vázací dírky v pase kabátce a nohavic.
- Švové přídavky a šipky směru osnovy na plátně.
- Generátor dlaždicového PDF na formát A4 s pasovacími značkami.
- Export a import profilů v JSON s podporou Drag & Drop.

### Fáze 2 (deklarativní jádro a průmyslový CAD)
- Přechod na deklarativní šablony střihů v JSON/YAML.
- Export do formátu DXF (standard AAMA/ASTM).
- Interaktivní ilustrovaný průvodce měřením těla.
- Optimalizace polohování dílů na látku (marker making).
