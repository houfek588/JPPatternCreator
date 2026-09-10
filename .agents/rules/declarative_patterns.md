# Pravidlo: Deklarativní systém střihů

## 1. Cíl
Pro zachování snadné rozšiřitelnosti musí být nové varianty oděvů a střihů vytvářeny deklarativně podle dokumentu [`docs/pattern_definition_spec.md`](../../docs/pattern_definition_spec.md).

## 2. Závazná pravidla pro autory střihů a agenty

1. **Zákaz hardcodování nových oděvů v Pythonu**:
   - Nové oděvy a varianty střihů se přidávají tvorbou deklarativních šablon v JSON/YAML, nikoliv psaním jednoúčelových Python skriptů.
   - Python jádro slouží jako dynamický evaluátor těchto šablon.

2. **Sekvenční vyhodnocování vzorců**:
   - Vzorce v sekci `variables:` musí být seřazeny tak, aby proměnné závislé na předchozích výpočtech byly vyhodnocovány až po nich.
   - Chraňte výpočty před dělením nulou (např. při výpočtu proporcí z rozkroku či pasu).

3. **Oddělení bodů a křivek**:
   - **Body (points)** definují souřadnice v centimetrech vzhledem k počátku plátna.
   - **Křivky (curves)** propojují body pomocí `bezier`, `catmull_rom` nebo přímých úseček.
   - Obrysy dílů musí tvořit uzavřené smyčky pro korektní výpočet švových přídavků.

4. **Členění na dílce (pieces)**:
   - Každý střih musí definovat jednotlivé střihové díly (např. přední díl, zadní díl, rukáv, límec, šůsky).
   - Každý díl musí mít definován počet kusů, směr osnovy, sesazovací značky a případné vázací dírky.

5. **Validace šablon**:
   - Před vykreslením vždy zkontrolujte, zda šablona splňuje specifikaci.
   - Ověřte, že všechny proměnné měr použité ve vzorcích jsou uvedeny v sekci `measurements`.
