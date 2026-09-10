# Vývojové a nasazovací postupy

Tato příručka popisuje přípravu vývojového prostředí, běžné pracovní postupy, testování a postupy pro sestavení aplikace JPPatternCreator.

---

## 1. Požadavky na systém

- **Python**: Doporučen Python 3.10 nebo 3.11.
- **Node.js**: Verze 18+ a správce balíčků `npm` (pro frontend).
- **Poppler / Cairo**: Vyžadováno pouze při exportu PNG z PDF přes `pdf2image`.

---

## 2. Příprava prostředí

### 1. Virtuální prostředí Pythonu
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt # případně: pip install reportlab PyQt6 Flask matplotlib pyinstaller
```

### 2. Závislosti klientského frontendu
```powershell
cd web/frontend
npm install
cd ../..
```

---

## 3. Běžné vývojové postupy

### Spouštění automatizovaných testů
Spuštění sady jednotkových testů:
```powershell
python -m unittest discover tests
```

### Spuštění webového serveru
Spuštění Flask backendu:
```powershell
python web/server.py
```
- Aplikace je dostupná na adrese: `http://127.0.0.1:5000`
- Server automaticky servíruje sestavený React frontend ze složky `web/frontend/dist`.

### Úpravy klientského rozhraní (Frontend)
Při provádění změn ve složce `web/frontend/src/`:

1. **Samostatný Vite dev server** (volitelně pro hot-reload při vývoji UI):
   ```powershell
   cd web/frontend
   npm run dev
   ```
2. **Kontrola linterem (ESLint)**:
   ```powershell
   cd web/frontend
   npm run lint
   ```
3. **Produkční sestavení**:
   ```powershell
   cd web/frontend
   npm run build
   ```
   *Poznámka: Po úpravě kódu frontendu je vždy nutné provést nové sestavení, aby Flask servíroval aktuální kód.*

### Spuštění desktopové aplikace
Spuštění desktopového GUI v PyQt6:
```powershell
python desktop/layout.py
# nebo
python main.py
```

---

## 4. Sestavení desktopové aplikace (.exe)

Kompilace samostatného spustitelného souboru pro Windows:
```powershell
python desktop/make_exe.py
```
Tento skript spouští PyInstaller:
```powershell
python -m PyInstaller --onefile --noconsole desktop/layout.py
```
Výsledný soubor `.exe` bude vytvořen ve složce `dist/`.

---

## 5. Řešení častých problémů

### Prázdná tmavá obrazovka ve webovém rozhraní
- **Příčina**: Běhová výjimka v JavaScriptu při vykreslování komponenty Reactu.
- **Diagnostika**: Otevřete vývojářské nástroje v prohlížeči (klávesa F12) a zkontrolujte záložku *Konzole (Console)*.
- **Náprava**: Zkontrolujte soubor `web/frontend/src/App.jsx`, zda neobsahuje nedefinované proměnné (spusťte `npm run lint`).
- **Mezipaměť prohlížeče**: Po novém sestavení stiskněte v prohlížeči **Ctrl + F5** pro vymazání staré mezipaměti skriptů.

### Chyby měřítek a písma v ReportLabu
- Ujistěte se, že všechny rozměry předávané do ReportLabu jsou převedeny na body (`pt`) z centimetrů pomocí `from reportlab.lib.units import cm`.
- Ověřte, že tělesné míry jsou kladná čísla, aby nedocházelo k dělení nulou.
