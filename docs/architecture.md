# Architektura systému

## 1. Celkový přehled architektury

JPPatternCreator je navržen jako vrstvený, modulární systém, který striktně odděluje matematické výpočty střihů od prezentační vrstvy a výstupních exportů.

```mermaid
flowchart TD
    subgraph UI ["Prezentační vrstva"]
        WebUI["Webový frontend (React 19 + Tailwind)\nweb/frontend/"]
        Desktop["Desktopové GUI (PyQt6)\ndesktop/layout.py"]
    end

    subgraph Service ["Vrstva služeb a adaptérů"]
        WebServer["Bezstavový Flask API server\nweb/server.py"]
        DesktopApp["Desktopový kontrolér\n(přímá Python volání)"]
    end

    subgraph Exporters ["Exportní sada pro výrobu"]
        SVGEx["SVGCreator (vektorový náhled)\nexporters/create_svg.py"]
        PDFPlotter["MakePdf (1:1 plotrový tisk)\nexporters/create_pdf.py"]
        PDFTiled["TiledPdfGenerator (dlaždicový tisk A4/A3)\nexporters/tiled_pdf.py"]
        DXFWriter["DXFExporter (AAMA / ASTM CAD)\nexporters/dxf_exporter.py"]
        Orchestrator["Orchestrátor exportů\nexporters/gen_hosen_files.py"]
    end

    subgraph Engine ["Geometrické a deklarativní jádro"]
        Evaluator["Evaluátor deklarativních šablon\ngeometry/evaluator.py"]
        Manifests["Šablony střihů (JSON / YAML)\npatterns/hosen.yaml, doublet.yaml"]
        Math["Geometrická primitiva\ngeometry/base.py"]
        Meas["Míry a validace\ngeometry/measurements.py"]
        LegacyHosen["Výpočet nohavic\ngeometry/hosen.py"]
        LegacyBodice["Výpočet kabátce\ngeometry/skeleton.py"]
    end

    WebUI -- "JSON přes HTTP" --> WebServer
    Desktop --> DesktopApp
    WebServer --> Orchestrator
    DesktopApp --> Orchestrator

    Orchestrator --> SVGEx
    Orchestrator --> PDFPlotter
    Orchestrator --> PDFTiled
    Orchestrator --> DXFWriter

    Orchestrator --> Evaluator
    Evaluator --> Manifests
    Evaluator --> Math
    Evaluator --> Meas
    Orchestrator --> LegacyHosen
    Orchestrator --> LegacyBodice
```

---

## 2. Architektonická rozhodnutí a principy

### Bezstavový server (Strategie 1)
- **Důvod**: Tělesné rozměry zákazníků představují citlivé osobní údaje (PII). Ukládání měr do centrální databáze na serveru přináší bezpečnostní rizika a zátěž spojenou s GDPR.
- **Implementace**:
  - Flask backend není připojen k žádné databázi.
  - Každý požadavek na výpočet obsahuje kompletní stav (míry, polohy posuvníků, typ oděvu, vybraný díl).
  - Server zpracuje výpočet v paměti nebo v izolovaném dočasném souboru v `tempfile.gettempdir()` s unikátním UUID a po odeslání výstupu jej ihned smaže.
  - Klientské profily jsou uloženy výhradně v prohlížeči uživatele (`localStorage` a `IndexedDB`).

### Deklarativní rozšiřitelnost (přidávání střihů bez zásahu do kódu)
- **Důvod**: Historické oděvy mají desítky variant a střihových modifikací. Zapisovat každou variantu napevno do Python kódu je neudržitelné.
- **Implementace**:
  - Všechny vzorce, konstrukční body, křivky, švové přídavky i vázací dírky jsou zapsány v deklarativních šablonách v YAML/JSON ([Specifikace](pattern_definition_spec.md)).
  - Python jádro šablonu načte, topologicky vyhodnotí vzorce a sestaví vektorovou geometrii.

### Čtyřúrovňová exportní pipeline
- **1:1 Plotrové PDF**: Spojitý tisk pro velkoformátové plotry na role papíru v ateliéru.
- **Dlaždicové PDF (A4/A3)**: Rozřezání do mřížky stránek s přesahy na slepení pro běžné kancelářské tiskárny.
- **Vektorové SVG**: Čisté křivky ve vrstvách pro grafické editory (Inkscape, Illustrator).
- **CAD DXF**: Průmyslový standard AAMA/ASTM pro automatické CNC stříhací stoly.

### Centralizovaná konfigurace (`config.py`)
- Rozměry plátna (`PAPER_WIDTH_CM = 120`, `PAPER_HEIGHT_CM = 160`), rozlišení (`SVG_SCALE = 4`), odsazení a systémové cesty jsou centralizovány v `config.py`.
