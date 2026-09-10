# Specifikace deklarativního formátu střihů

## 1. Přehled a cíl

Aby bylo možné přidávat nové historické oděvy a jejich varianty bez nutnosti zasahovat do zdrojového kódu v Pythonu, využívá JPPatternCreator **deklarativní schéma střihů** (ve formátu JSON nebo YAML).

Soubor se šablonou střihu deklarativně popisuje:
1. **Metadata**: Název, historické období, kategorie, autor, popis.
2. **Požadované tělesné míry**: Seznam tělesných rozměrů vyžadovaných z profilu zákazníka.
3. **Tvarovací posuvníky a parametry**: Uživatelské ovladače s minimem, maximem, výchozí hodnotou a jednotkou.
4. **Vypočítané proměnné a vzorce**: Matematické výrazy vyhodnocované v přesném pořadí závislostí.
5. **Konstrukční body**: 2D souřadnice odvozené z měr a vzorců.
6. **Křivky a obrysy**: Úsečky, Catmull-Rom spliny a Bézierovy křivky.
7. **Střihové dílce (Pieces)**: Samostatné díly určené ke stříhání sdružující obrysové křivky, pomocné linie, směr osnovy, sesazovací značky a švové přídavky.

---

## 2. Struktura šablony (příklad v YAML)

```yaml
schema_version: "1.0"
pattern_id: "hosen_15th_c_joined"
name:
  cz: "Spojené nohavice 15. století"
  en: "15th Century Joined Hosen"
category: "lower_body"
historical_period: "1450-1500"

# 1. Požadované tělesné míry
measurements:
  - id: "VP"
    label: { cz: "Celková výška", en: "Total Height" }
    unit: "cm"
    default: 175
  - id: "OP"
    label: { cz: "Obvod pasu", en: "Waist Circumference" }
    unit: "cm"
    default: 98
  - id: "OS"
    label: { cz: "Obvod sedu", en: "Hips Circumference" }
    unit: "cm"
    default: 116
  - id: "BDK"
    label: { cz: "Boční délka kalhot", en: "Side Leg Length" }
    unit: "cm"
    default: 122
  - id: "KD"
    label: { cz: "Kroková délka", en: "Crotch Length" }
    unit: "cm"
    default: 90
  - id: "O_st"
    label: { cz: "Obvod stehna", en: "Thigh Circumference" }
    unit: "cm"
    default: 61
  - id: "O_nk"
    label: { cz: "Obvod nad kolenem", en: "Above Knee Circumference" }
    unit: "cm"
    default: 46
  - id: "O_l"
    label: { cz: "Obvod lýtka", en: "Calf Circumference" }
    unit: "cm"
    default: 40
  - id: "O_kot"
    label: { cz: "Obvod kotníku", en: "Ankle Circumference" }
    unit: "cm"
    default: 26

# 2. Tvarovací posuvníky a parametry
parameters:
  - id: "waist_lowering"
    label: { cz: "Snížení pasu", en: "Waist Lowering" }
    min: 0
    max: 25
    default: 5
    unit: "cm"
  - id: "instep_width"
    label: { cz: "Šířka nártu", en: "Instep Width" }
    min: 0
    max: 24
    default: 12
    unit: "cm"
  - id: "foot_finger_curve"
    label: { cz: "Tvar paty a šlapky", en: "Foot Arch Shape" }
    min: 0
    max: 10
    default: 5
    unit: "cm"
  - id: "corner_shape"
    label: { cz: "Tvar rozkroku", en: "Crotch Corner Shape" }
    min: 0
    max: 24
    default: 12
    unit: "cm"

# 3. Vzorce a proměnné (vyhodnocují se postupně)
variables:
  hip_width: "OS / 4.0 + 6"
  knee_width: "O_nk"
  calf_width: "O_l"
  ankle_width: "O_kot + 5"
  ground_width: "O_kot + 7"
  hip_y: "origin_y + BDK - KD"
  knee_y: "origin_y + BDK - (KD / 2.0 + 6)"
  ankle_y: "origin_y + BDK - 11"
  ground_y: "origin_y + BDK"

# 4. Konstrukční body (souřadnice X, Y)
points:
  P_waist_center: [ "origin_x", "origin_y" ]
  P_ground_center: [ "origin_x", "ground_y" ]
  P_knee_left: [ "origin_x - knee_width / 2", "knee_y" ]
  P_knee_right: [ "origin_x + knee_width / 2", "knee_y" ]
  P_ankle_left: [ "origin_x - ankle_width / 2", "ankle_y" ]
  P_ankle_right: [ "origin_x + ankle_width / 2", "ankle_y" ]

# 5. Křivky a obrysy
curves:
  - id: "left_leg_seam"
    type: "catmull_rom"
    points: [ "P_thigh_left", "P_knee_left", "P_calf_left", "P_ankle_left", "P_ground_left" ]
  - id: "waist_curve"
    type: "bezier"
    points: [ "P_waist_front_top", "P_waist_control", "P_waist_back_top" ]

# 6. Střihové dílce a krejčovské prvky
pieces:
  - id: "joined_leg"
    name: { cz: "Spojená nohavice", en: "Joined Trouser Leg" }
    quantity: 2
    cut_on_fold: false
    default_seam_allowance_cm: 1.5
    grainline:
      start: "P_waist_center"
      end: "P_ground_center"
    notches:
      - point: "P_knee_left"
        type: "single"
      - point: "P_knee_right"
        type: "double"
    lacing_holes: # Dobové dírky pro uvázání ke kabátci
      - point: "P_waist_front_top"
        reinforced: true
        pair_offset_cm: 2.0
      - point: "P_waist_back_top"
        reinforced: true
        pair_offset_cm: 2.0
    outline:
      - ref: "waist_curve"
      - ref: "left_leg_seam"
      - ref: "foot_contour"
      - ref: "right_leg_seam"
      - ref: "crotch_curve"
```

---

## 3. Matematický vyhodnocovací engine

Aplikace obsahuje bezpečný matematický parser výrazů, který podporuje:
- Aritmetiku: `+`, `-`, `*`, `/`, `^`, `%`
- Funkce: `min(a, b)`, `max(a, b)`, `sqrt(x)`, `sin(rad)`, `cos(rad)`, `hypot(dx, dy)`
- Geometrické reference:
  - `normal_offset(PointA, PointB, distance)`
  - `intersection(Line1, Line2)`
  - `distance(PointA, PointB)`
  - `midpoint(PointA, PointB)`

---

## 4. Propojení s exportéry
Při zpracování deklarativní šablony:
1. Zadané míry a polohy posuvníků se sloučí s výchozími hodnotami.
2. Proměnné a body se vyhodnotí v topologickém pořadí.
3. Křivky (Bézier, Catmull-Rom, úsečky) se vzorkují na spojité lomené čáry.
4. Jsou-li aktivovány švové přídavky, vypočte se rovnoběžný vnější obrys řezu.
5. Výsledek je odeslán do `SVGCreator` pro zobrazení na webu, nebo do `MakePdf` a `DXFWriter` pro export.
