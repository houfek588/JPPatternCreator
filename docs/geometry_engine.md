# Geometrický a konstrukční engine

Balíček `geometry/` představuje matematické jádro aplikace JPPatternCreator. Je zodpovědný za transformaci tělesných rozměrů do spojitých vektorových křivek a obrysů střihových dílů.

---

## 1. Matematická primitiva (`geometry/base.py`)

### `Line` (Úsečka a přímka)
Reprezentuje orientovanou 2D úsečku nebo nekonečný vektor.
- **Obecná rovnice přímky**: Podporuje obecné přímky ($ax + by + c = 0$), svislé ($x = k$) i vodorovné přímky ($y = k$).
- **Výpočty**:
  - `.line_length()`: Euklidovská délka mezi počátečním a koncovým bodem.
  - `.normal_line(x)`: Vygenerování kolmice v dané $x$-ové souřadnici.
  - `.parallel_line(distance)`: Vygenerování rovnoběžky v zadané vzdálenosti.
  - `.intersection(other_line)`: Přesný průsečík dvou přímek $(x, y)$.
  - `.get_point_distance(dist)`: Bod v definované vzdálenosti podél směrového vektoru.

### `Bezier` (Bézierova křivka)
Počítá polynomiální Bézierovy křivky $n$-tého stupně z libovolného počtu řídicích bodů:
$$B(t) = \sum_{i=0}^n \binom{n}{i} (1 - t)^{n - i} t^i P_i, \quad t \in [0, 1]$$
- Používá se pro plynulé křivky v pase, klenbu rozkroku, výstřih límce a průramky.
- `.sample(resolution)`: Vzorkuje křivku na sekvenci 2D bodů pro vykreslení.

### `CatmullRomSpline` (Catmull-Rom spline)
Implementuje kubický Catmull-Rom spline, který prochází přímo všemi zadanými řídicími body bez nutnosti manuálního nastavování tečen:
- Využívá se pro křivky, které musí přesně procházet anatomickými body těla (koleno, lýtko, kotník, pata).
- `.sample(resolution)`: Kubická Hermitovská interpolace mezi sousedními body.

---

## 2. Datové modely rozměrů (`geometry/measurements.py`)

### Jednotky a souřadnicový systém
- **Uživatelské vstupy**: Centimetry (`cm`).
- **Rozlišení na obrazovce (SVG)**: Škálované centimetry (`cm * SVG_SCALE`).
- **Tiskové jednotky (PDF)**: Typografické body ReportLabu (`pt`, kde $1\text{ in} = 72\text{ pt}$, $1\text{ cm} \approx 28,3465\text{ pt}$).
- Převody zajišťuje `reportlab.lib.units.cm` a pomocné funkce v `data/manage.py` (`cm_to_pt`, `pt_to_cm`).

### `Measurements` (Horní část těla / Kabátec)
| Klíč | Český název | Anglický název | Typická hodnota (cm) |
| :--- | :--- | :--- | :--- |
| `OH` | Obvod hrudníku | Chest Circumference | 100 |
| `OP` | Obvod pasu | Waist Circumference | 80 |
| `DZ` | Délka zad | Back Length | 40 |
| `Szad` | Šířka zad | Back Width | 42 |

### `LowerMeasurements` (Dolní část těla / Nohavice)
| Klíč | Český název | Anglický název | Typická hodnota (cm) |
| :--- | :--- | :--- | :--- |
| `title` | Název střihu | Pattern Title | "Vzorové kalhoty" |
| `VP` | Výška postavy | Total Body Height | 175 |
| `OP` | Obvod pasu | Waist Circumference | 98 |
| `OS` | Obvod sedu | Hips Circumference | 116 |
| `BDK` | Boční délka kalhot | Side Leg Length | 122 |
| `KD` | Kroková délka | Crotch Length | 90 |
| `O_st` | Obvod stehna | Thigh Circumference | 61 |
| `O_nk` | Obvod nad kolenem | Above Knee Circumference | 46 |
| `O_l` | Obvod lýtka | Calf Circumference | 40 |
| `O_kot`| Obvod kotníku | Ankle Circumference | 26 |

### Validační pravidla
Metoda `.validate()` vyvolává výjimku `ValidationError`:
- Všechny povinné rozměry musí být zadány.
- Hodnoty musí být číselné a kladné ($hodnota > 0$).

---

## 3. Algoritmy konstrukce střihů

### Střih nohavic (`geometry/hosen.py`)
Nohavice se rýsují jako **spojený střih** (přední i zadní díl sdílí základní konstrukční síť):
1. **`HosenBaseSkeleton`**: Základní vodorovné linie těla (sed, koleno, lýtko, kotník, pata).
2. **`HosenFrontContour`**: Přední linie pasu, boční linie a náběh předního rozkroku.
3. **`HosenCrotchSkeleton`**: Sklon rozkroku, zadní sedová křivka a rozšíření stehna.
4. **`HosenPattern`**: Sestavení celého vnějšího obvodu pomocí Bézierových křivek a Catmull-Rom splinů.

### Střih kabátce a límce (`geometry/skeleton.py`)
1. **`BackSkeleton`**: Základní síť odvozená z délky zad a obvodu hrudníku.
2. **`BackContour`**: Hloubka výstřihu, sklon ramene, šířka průramku a boční šev.
3. **`BackPattern`**: Křivka průramku a obrysové body. Volba mezi oblým výstřihem nebo V-výstřihem pro límec.
4. **`CollarPattern`**: Parametrický stojáčkový límec s nastavitelnou hloubkou, výškou a sklonem.

---

## 4. Přepínání zobrazovaných částí střihu

Generovací funkce podporují filtr zobrazení přes parametr `part`:

| Oděv | Hodnota `part` | Zobrazený výstup |
| :--- | :--- | :--- |
| `hosen` | `'all'` | Kompletní obrys nohavice + veškeré konstrukční linie |
| `hosen` | `'front'` | Obrys nohavice + základní a přední konstrukční linie |
| `hosen` | `'back'` | Obrys nohavice + základní a zadní/sedové linie |
| `bodice` | `'all'` | Obrys zadního dílu + obrys límce + konstrukční síť |
| `bodice` | `'back'` | Pouze zadní díl (zaoblený výstřih) + konstrukční síť |
| `bodice` | `'collar'` | Samostatný obrys límce |
