---
name: garment-pattern-creator
description: >-
  Specializovaná dovednost pro tvorbu, rozšiřování a validaci historických oděvních střihů
  15. století (nohavice, kabátec apod.) a tvorbu deklarativních šablon v aplikaci JPPatternCreator.
---

# Dovednost: Tvůrce oděvních střihů (Garment Pattern Creator)

Tato dovednost vybavuje agenta metodikou pro návrh, rýsování a ověřování historických oděvních střihů pro evropské oděvy 15. století v CAD architektuře JPPatternCreator.

## Klíčové schopnosti
- Transformace tělesných rozměrů do historické geometrie střihu.
- Konstrukce nohavic 15. století (spojené i dělené, se šlapkou, špičatou botou i třmínkem).
- Konstrukce dílů kabátce 15. století (přední díly hrudi, zadní díl, stojáčkový límec, prohnuté dvoudílné rukávy, pasové šůsky).
- Výpočet a umisťování vázacích dírek (*doublet points*) a zpevňujících značek.
- Tvorba deklarativních šablon podle specifikace [`docs/pattern_definition_spec.md`](../../../docs/pattern_definition_spec.md).

---

## Postup rýsování střihu krok za krokem

### 1. Zpracování měr a validace
1. Určete všechny anatomické tělesné míry potřebné pro daný oděv.
2. Zkontrolujte, že všechny rozměry jsou zadané a jsou to kladná čísla pomocí `geometry.measurements.ValidationError`.
3. Zohledněte přídavky na volnost a pohyb:
   - Nohavice: Minimální nebo nulový přídavek (využívá se přirozená šikmá pružnost vlněného sukna).
   - Kabátec – hruď: Přídavek $2\text{ až }4\text{ cm}$ přes spodní prádlo.
   - Kabátec – pas: Přídavek $0\text{ až }2\text{ cm}$ (musí těsně sedět, aby spolehlivě nesl váhu nohavic).

### 2. Konstrukční síť (základní a osní přímky)
1. Zvolte počáteční bod $(x_0, y_0)$ z konfigurace `config.PATTERN_ORIGIN_Y_CM`.
2. Sestrojte svislé osy (střed zad, střed předního dílu, boční linie).
3. Vyneste vodorovné výškové úrovně těla:
   - Pas, hloubka podpaží/hrudi, sed, koleno, lýtko, kotník, pata.
4. Přímky vždy vytvářejte pomocí třídy `geometry.base.Line`.

### 3. Tvarování obrysů a křivek
1. Vypočítejte odsazení bočních švů a sedové křivky rozkroku.
2. **Bézierovy křivky** (`geometry.base.Bezier`) použijte pro:
   - Klenbu pasové linie.
   - Průramky rukávů.
   - Horní sedovou křivku rozkroku.
   - Oblouk výstřihu krku.
3. **Catmull-Rom spliny** (`geometry.base.CatmullRomSpline`) použijte pro:
   - Vnější švy nohavic procházející stehnem, kolenem, lýtkem a kotníkem.
   - Klenbu nártu, paty a špičky chodidla.

### 4. Krejčovské značky a sestavení dílů
1. **Směr osnovy**: Svislý či šikmý vektor s šipkami směru tkaní.
2. **Švové přídavky**: Odsazený obrys šíře $1,5\text{ cm}$ kolem uzavřeného dílu.
3. **Sesazovací značky**: Nástřihy v klíčových místech spojení (koleno, loket, podpaží).
4. **Vázací body ke kabátci**: Páry vázacích kroužků vzdálené $2,0\text{ až }2,5\text{ cm}$ podél pasu.

---

## Ověření a testování
Před dokončením jakékoliv úpravy střihu:
1. Spusťte automatizované testy geometrie:
   ```powershell
   python -m unittest discover tests
   ```
2. Zkontrolujte vygenerované SVG:
   - Křivky tvoří uzavřené obrysy bez nežádoucího křížení.
   - Všechny díly se vejdou do rozměrů plátna `PAPER_WIDTH_CM` a `PAPER_HEIGHT_CM`.
3. Sestavte frontend a vizuálně ověřte náhled:
   ```powershell
   npm --prefix web/frontend run build
   ```
