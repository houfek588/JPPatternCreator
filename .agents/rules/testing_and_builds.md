# Pravidlo: Testování, kontrola linterem a ověření sestavení

## Kontrolní brány kvality pro agenty

Každý úkol upravující kód aplikace musí před dokončením splnit tyto verifikační kroky:

### 1. Kontrola backendu (jednotkové testy)
- **Pravidlo**: Po každé úpravě ve složkách `geometry/`, `exporters/` nebo v souboru `web/server.py` spusťte jednotkové testy v Pythonu.
- **Příkaz**:
  ```powershell
  python -m unittest discover tests
  ```
- **Požadavek**: Všechny testy musí projít (návratový kód 0). Při přidání nových tříd střihů či parametrů doplňte odpovídající testy do složky `tests/`.

### 2. Kontrola frontendu (linter a sestavení)
- **Pravidlo**: Po každé úpravě souborů ve složce `web/frontend/src/`:
  1. Spusťte kontrolu linterem, aby nevznikly syntaktické chyby či nedefinované proměnné:
     ```powershell
     npm --prefix web/frontend run lint
     ```
     *(Musí skončit s 0 chybami)*
  2. Sestavte produkční distribuční balíček:
     ```powershell
     npm --prefix web/frontend run build
     ```
     *(Musí proběhnout bez chyb a zapsat aktuální soubory do `web/frontend/dist/`)*

> [!CAUTION]
> Flask server servíruje klientské soubory přímo ze složky `web/frontend/dist/`. Pokud upravíte `web/frontend/src/App.jsx` a nespustíte `npm run build`, prohlížeč bude nadále načítat starou neaktuální verzi aplikace!
