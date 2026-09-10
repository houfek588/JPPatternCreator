# Instrukce pro agenty (JPPatternCreator)

Vítejte v repozitáři **JPPatternCreator**. Tento dokument obsahuje architektonická pravidla, zásady, konvence a pracovní postupy pro AI agenty působící v tomto projektu.

---

## 1. Mise a přehled projektu

**JPPatternCreator** je parametrický CAD generátor oděvních střihů zaměřený na **historické oděvy 15. století** (Living History, HEMA a historické krejčovství). Původní prototyp vznikl jako desktopová aplikace v Python/PyQt6, přičemž vývoj nyní přechází na **webovou platformu jako primární cíl**.

### Primární typy oděvů (15. století):
1. **Kalhoty (`hosen` – Nohavice)**:
   - Spojené nohavice a dělené nohavice.
   - Anatomické tvarování nohavic, sedová křivka, klenba nártu, špičatá šlapka (*crakow*) a varianta s třmínkem pod chodidlo.
   - Zpevněné vázací dírky podél pasového lemu pro uvázání ke kabátci.
2. **Kabátec (`bodice` / `doublet` – Doublet / Pourpoint)**:
   - Kompletní sada dílů kabátce 15. století: přední díly, zadní díl, stojáčkový límec, anatomicky prohnuté rukávy a spodní šůsky/sukénka (*peplum*).
   - Párové zpevněné dírky podél pasu pro šněrování a držení nohavic (*doublet points*).

### Klíčové možnosti platformy:
- **Webová aplikace (primární platforma)**: Moderní responzivní SPA (`web/frontend/`) napojená na lehký bezstavový Flask server (`web/server.py`).
- **Desktopová aplikace (prototyp / lokální stanice)**: PyQt6 rozhraní (`desktop/layout.py`).
- **Deklarativní systém střihů**: Rozšiřitelný engine načítající JSON/YAML šablony bez nutnosti zasahovat do kódu v Pythonu.
- **Kompletní exportní sada**:
  1. *1:1 Plotrové PDF*: Kontinuální tisk na role papíru s kalibračním čtvercem $10 \times 10\text{ cm}$.
  2. *Dlaždicové PDF (Tiled)*: Rozřezáno na listy A4 / US Letter s přesahy, pasovacími značkami a číslováním stránek.
  3. *Vektorové SVG*: Čisté vrstvené vektorové křivky pro Inkscape a Illustrator.
  4. *CAD DXF*: Standard AAMA/ASTM pro automatické stříhací stoly a laserové řezačky.
- **Krejčovské CAD nástroje**: Nastavitelné švové přídavky, směr osnovy (grainline), sesazovací značky (notches) a vázací dírky.
- **Ochrana soukromí klienta**: Bezpečné lokální úložiště (`localStorage` / `IndexedDB`) s exportem/importem do JSON a podporou Drag & Drop.
- **Dvojjazyčné rozhraní**: Plná podpora češtiny (CZ) i angličtiny (EN).
- **Vzhled**: Přepínání tmavého (Dark) a světlého (Light) režimu.

---

## 2. Základní architektonické principy

Všichni agenti **musí bezpodmínečně dodržovat** tyto principy:

### 1. Důraz na soukromí a bezstavový server (Strategie 1)
- **Žádné trvalé úložiště na serveru**: Server **nesmí** ukládat databázi tělesných rozměrů či profilů zákazníků.
- **Dočasné zpracování**: Při generování SVG či PDF se míry načtou do paměti a zapíší do izolovaného dočasného souboru (pomocí `tempfile.gettempdir()` a `uuid.uuid4()`). Dočasné soubory **musí** být ihned po odeslání smazány.
- **Vlastnictví dat na straně klienta**: Klientské profily s mírami a nastaveními jsou uloženy výhradně v prohlížeči uživatele (`localStorage`), případně přenášeny v `.json` souborech.

### 2. Deklarativní rozšiřitelnost (žádné hardcodované střihy)
- Řiďte se **[Specifikací deklarativního formátu střihů](docs/pattern_definition_spec.md)**.
- Nové střihy a jejich varianty musí být přidávány přes deklarativní šablony, nikoliv psaním nových Python funkcí do jádra aplikace.

### 3. Centralizovaná konfigurace
- Nikdy neuvádějte rozměry plátna, měřítka, cesty k souborům ani okraje napevno do kódu geometrie či rozhraní.
- Vždy importujte konstanty z [`config.py`](./config.py), jako jsou `PAPER_WIDTH_CM`, `PAPER_HEIGHT_CM`, `SVG_SCALE`, `PATTERN_ORIGIN_Y_CM` atd.

### 4. Oddělení vrstev aplikace
```
┌─────────────────────────────────────────────────────────┐
│                 Uživatelská rozhraní                    │
│   Webový frontend (React 19) │  Desktopové GUI (PyQt6)  │
└──────────────┬───────────────┴──────────┬───────────────┘
               │ HTTP / JSON              │ Přímé volání
               ▼                          ▼
┌──────────────────────────┐    ┌─────────────────────────┐
│   Bezstavové API (Flask) │    │  Logika desktopového GUI│
└──────────────┬───────────┘    └─────────┬───────────────┘
               │                          │
               └───────────┬──────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│               Exportéry a generátory souborů            │
│    Plotrové PDF, dlaždicové A4 PDF, vektorové SVG, DXF  │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│        Deklarativní geometrický engine a matematika     │
│    Line, Bezier, CatmullRomSpline, evaluátor šablon     │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Specializované dovednosti a pravidla agentů

Pravidla a dovednosti pro agenty jsou uloženy ve složce `.agents/`:

| Cesta | Typ | Účel |
| :--- | :--- | :--- |
| [`.agents/rules/web_requirements.md`](.agents/rules/web_requirements.md) | Pravidlo | Požadavky PRD, bezstavový provoz a exportní formáty |
| [`.agents/rules/declarative_patterns.md`](.agents/rules/declarative_patterns.md) | Pravidlo | Zásady tvorby deklarativních šablon střihů |
| [`.agents/rules/historical_reenactment.md`](.agents/rules/historical_reenactment.md) | Pravidlo | Pravidla střihů 15. století, osnovy, přídavky na volnost a šněrování |
| [`.agents/rules/stateless_privacy.md`](.agents/rules/stateless_privacy.md) | Pravidlo | Soulad s GDPR a bezpečné mazání dočasných souborů |
| [`.agents/rules/code_style.md`](.agents/rules/code_style.md) | Pravidlo | Standardy Python PEP 8, React/Tailwind a geometrické jednotky |
| [`.agents/rules/testing_and_builds.md`](.agents/rules/testing_and_builds.md) | Pravidlo | Kontrola kvality, jednotkové testy a příkazy pro sestavení |
| [`.agents/skills/garment-pattern-creator/`](.agents/skills/garment-pattern-creator/SKILL.md) | Dovednost | Postup pro rýsování a validaci střihů 15. století |
| [`.agents/skills/tiled-pdf-exporter/`](.agents/skills/tiled-pdf-exporter/SKILL.md) | Dovednost | Algoritmy pro dlaždicový tisk A4/A3 a velkoformátové PDF |

---

## 4. Odkazy na dokumentaci

Podrobné příručky naleznete ve složce `docs/`:
- **[Požadavky na webovou aplikaci (PRD)](docs/web_application_requirements.md)**
- **[Specifikace deklarativního formátu střihů](docs/pattern_definition_spec.md)**
- **[Historicko-krejčovská příručka 15. století](docs/historical_tailoring_15th_c.md)**
- **[Architektura systému](docs/architecture.md)**
- **[Geometrický engine a matematika](docs/geometry_engine.md)**
- **[Referenční příručka webového API](docs/web_api.md)**
- **[Vývojové a nasazovací postupy](docs/development_workflow.md)**

---

## 5. Pracovní postupy a základní příkazy

### Spouštění jednotkových testů
Jednotkové testy spouštějte před i po každé úpravě kódu:
```powershell
python -m unittest discover tests
```

### Spuštění webové aplikace (primární platforma)
```powershell
python main.py
# nebo
python app/web/server.py
```
- Aplikace běží na `http://127.0.0.1:5000`.
- Automaticky servíruje sestavené soubory z `app/web/frontend/dist/`.

### Vývoj a sestavení frontendu
Při úpravách souborů ve složce `app/web/frontend/`:
```powershell
npm --prefix app/web/frontend run lint    # Kontrola syntaxe a nedefinovaných proměnných
npm --prefix app/web/frontend run build   # Sestavení produkčního balíčku do app/web/frontend/dist/
```
> [!IMPORTANT]
> Po každé úpravě `app/web/frontend/` souborů **musíte** spustit `npm run build`, aby Flask servíroval aktuální klientský kód.

### Sestavení desktopového spustitelného souboru (.exe)
```powershell
python app/desktop/make_exe.py
```
