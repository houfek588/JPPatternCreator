# Pravidlo: Bezstavové zpracování a ochrana soukromí (Strategie 1)

## Kontext a cíle
V krejčovství představují tělesné rozměry (např. obvod hrudníku, boků, pasu, výška) citlivé osobní údaje (PII) chráněné nařízením GDPR. Webová aplikace JPPatternCreator funguje na principu přísně **bezstavového serveru** (Strategie 1).

## Závazná pravidla pro agenty:

1. **ZÁKAZ perzistentního úložiště na serveru**:
   - Nikdy nepřidávejte na backend trvalou databázi (SQLite, PostgreSQL, MongoDB apod.) pro ukládání rozměrů zákazníků či vygenerovaných střihů.
   - Neukládejte profily do stálých složek serveru (jako `web/server_data/` či `data/`).

2. **Izolace a mazání dočasných souborů**:
   - Při generování vektorových dat (SVG) nebo tiskových dokumentů (PDF/PNG) vždy vygenerujte unikátní identifikátor pomocí `uuid.uuid4()`.
   - Dočasné soubory měr a exportů ukládejte výhradně do systémové dočasné složky (`tempfile.gettempdir()`).
   - Po odeslání dat uživateli dočasné soubory JSON a PDF neprodleně smažte v bloku `finally` nebo v čistícím kroku.

3. **Ukládání profilů na straně klienta**:
   - Zákaznické profily (jména, tělesné míry, nastavení) musí zůstat striktně v prohlížeči uživatele s využitím `localStorage` nebo `IndexedDB`.
   - Veškeré funkce pro ukládání, načítání a mazání profilů se implementují na frontendu (`web/frontend/src/App.jsx`).

4. **Upozornění o ochraně soukromí**:
   - Rozhraní musí uživatele transparentně informovat o tom, že data se zpracovávají pouze v operační paměti a nikam na server se neukládají.
