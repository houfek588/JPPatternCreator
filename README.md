# JPPatternCreator

Parametrický CAD generátor oděvních střihů zaměřený na historické oděvy 15. století (living history, HEMA a zakázkové krejčovství).

---

## Možnosti spuštění aplikace

### 1. Spuštění webové aplikace (výchozí a doporučené)

Primární způsob spuštění aplikace přes hlavní vstupní bod:
```powershell
python main.py
```
nebo přímým spuštěním webového serveru:
```powershell
python app/web/server.py
```
Aplikace se spustí na adrese: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

#### Volitelné parametry příkazové řádky (`main.py`):
- `python main.py` – Spustí webový server na `127.0.0.1:5000` (výchozí).
- `python main.py --desktop` – Spustí lokální desktopové okno (PyQt6).
- `python main.py --host 0.0.0.0 --port 8080` – Umožňuje nastavit vlastní síťové rozhraní a port.
- `python main.py --no-debug` – Vypne vývojářský debug režim serveru.
- `python main.py --help` – Zobrazí nápovědu ke všem parametrům.

---

### 2. Spuštění desktopové aplikace (PyQt6)

Původní desktopový prototyp s interaktivním oknem PyQt6 můžete spustit přepínačem:
```powershell
python main.py --desktop
```
nebo přímo modulem desktopového rozhraní:
```powershell
python app/desktop/layout.py
```

---

## Další příkazy pro vývoj a sestavení

### Spuštění automatizovaných testů
Před odevzdáním změn vždy spusťte sadu jednotkových testů:
```powershell
python -m unittest discover tests
```

### Sestavení frontendu (React)
Při úpravách klientského kódu ve složce `app/web/frontend/`:
```powershell
npm --prefix app/web/frontend run build
```

### Sestavení desktopového .exe souboru
Pro vytvoření samostatného spustitelného balíčku pro Windows:
```powershell
python app/desktop/make_exe.py
```

---

## Dokumentace projektu
- **[Požadavky na webovou aplikaci (PRD)](docs/web_application_requirements.md)**
- **[Specifikace deklarativního formátu střihů](docs/pattern_definition_spec.md)**
- **[Referenční příručka webového API](docs/web_api.md)**
- **[Architektura systému](docs/architecture.md)**
- **[Geometrický engine a matematika](docs/geometry_engine.md)**
- Kompletní přehled naleznete ve složce [docs/](docs/README.md).
- Pravidla a instrukce pro AI agenty jsou k dispozici v [AGENTS.md](AGENTS.md) a ve složce [.agents/](.agents/README.md).