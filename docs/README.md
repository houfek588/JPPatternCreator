# Technická dokumentace JPPatternCreator

Vítejte v technické dokumentaci projektu **JPPatternCreator**. Tato složka obsahuje ucelené architektonické specifikace, matematickou a geometrickou dokumentaci, rozhraní API, uživatelské požadavky a vývojové postupy.

## Rozcestník dokumentace

1. **[Požadavky na webovou aplikaci (PRD)](web_application_requirements.md)** ⭐
   - Vize projektu, cílová skupina reenactorů a oděvní doména 15. století.
   - Funkční požadavky: parametrické generování, tvarovací posuvníky, přepínání dílů, krejčovské CAD prvky.
   - Specifikace exportní sady: velkoformátové PDF pro plotry, dlaždicový tisk A4/A3, vektorové SVG a CAD DXF.
   - Nefunkční požadavky, ochrana soukromí (bezstavový server) a plán fází implementace.

2. **[Specifikace deklarativního formátu střihů](pattern_definition_spec.md)** ⭐
   - Deklarativní schéma v JSON/YAML pro přidávání nových střihů bez nutnosti programování v Pythonu.
   - Definice bodů, sekvenčních matematických vzorců, Bézierových křivek a Catmull-Rom splinů.
   - Tvorba švových přídavků, sesazovacích značek a vázacích dírek ke kabátci.

3. **[Historicko-krejčovská příručka 15. století](historical_tailoring_15th_c.md)** ⭐
   - Historická mechanika: využití šikmého střihu látky, anatomická silueta, vyztužení prošitým plátnem.
   - Anatomie nohavic: spojené vs. dělené nohavice, krytí rozkroku, varianty šlapky, špičky a třmínku.
   - Anatomie kabátce: přední díly, zádová křivka, stojáček, prohnuté rukávy a pasové šůsky.
   - Mechanika šněrování nohavic ke kabátci pomocí tkanic (*doublet points*).

4. **[Architektura systému](architecture.md)**
   - Návrh systému a interakce jednotlivých vrstev.
   - Bezstavový model ochrany soukromí (Strategie 1).
   - Souběh webové aplikace (Flask/React) a desktopové verze (PyQt6).

5. **[Geometrický engine a matematika](geometry_engine.md)**
   - Matematické základy: přímky, Bézierovy křivky, Catmull-Rom spliny.
   - Datové modely tělesných rozměrů a jejich validace.
   - Algoritmy rýsování nohavic (`hosen`) a horního dílu (`bodice`).
   - Souřadnicové systémy a převody jednotek (`cm` vs `pt`).

6. **[Referenční příručka webového API](web_api.md)**
   - Dokumentace REST API endpointů Flask serveru.
   - Formáty požadavků a odpovědí pro `/generate`, `/export/pdf`, `/export/png` a `/save`.
   - Specifikace parametrů (`patternType`, `part`, `sliders`, `inputs`).

7. **[Vývojové a nasazovací postupy](development_workflow.md)**
   - Příprava vývojového prostředí a závislosti.
   - Spouštění automatizovaných testů.
   - Sestavení produkčního balíčku React frontendu.
   - Kompilace samostatné desktopové aplikace pro Windows (.exe).
