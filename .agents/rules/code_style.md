# Pravidlo: Standardy kódu a konvence vývoje

## 1. Centralizovaná konfigurace
- **Pravidlo**: Do funkčních modulů nikdy neuvádějte rozměry papíru, plátna, měřítka, okraje ani cesty k souborům napevno.
- **Postup**: Vždy importujte [`config.py`](../../config.py) a odkazujte na konstanty:
  - `PAPER_WIDTH_CM`, `PAPER_HEIGHT_CM` pro rozměry plátna.
  - `SVG_SCALE` pro rozlišení zobrazení na obrazovce.
  - `PATTERN_ORIGIN_Y_CM` pro horní okraj umístění střihu.
  - `SERVER_SAVE_PATH`, `DESKTOP_MEAS_FILE`, `LOGO_PATH` pro systémové cesty.

## 2. Standardy pro Python
- Dodržujte pravidla stylu **PEP 8**.
- **Geometrické jednotky**: Pozor na správný převod jednotek:
  - Vstupní tělesné míry od uživatele jsou v centimetrech (`cm`).
  - ReportLab interně počítá v bodech (`pt`, kde $1\text{ pt} = 1/72\text{ palce}$).
  - Využívejte `from reportlab.lib.units import cm, mm` nebo funkce z `data.manage` (`cm_to_pt`, `pt_to_cm`).
- **Validace měr**: Všechny třídy měr (`Measurements`, `LowerMeasurements`) musí obsahovat metodu `.validate()`:
  - Kontrola přítomnosti všech povinných klíčů.
  - Ověření, že míry jsou kladná čísla (`float(val) > 0`).
  - Při neplatných datech vyvolávejte výjimku `geometry.measurements.ValidationError`.

## 3. Standardy pro frontend (`web/frontend/`)
- **React 19 a moderní JavaScript**:
  - Využívejte funkcionální komponenty s háčky (`useState`, `useEffect`, `useRef`, `useCallback`).
  - Všechny proměnné a konstanty (jako `INPUT_LABELS`) musí být řádně deklarovány a importovány.
  - V blocích `catch` nedeklarujte nepoužité proměnné výjimek (používejte moderní `catch { ... }`).
- **Tailwind CSS**:
  - Používejte standardní třídy Tailwindu.
  - Podporujte tmavý režim pomocí prefixu `dark:`.
  - Využívejte projektovou paletu `brand` z `tailwind.config.js` (`brand-light`, `brand`, `brand-dark`, `brand-hover`).
- **Dvojjazyčnost (i18n)**:
  - Každý uživatelský text musí existovat v `TRANSLATIONS.EN` i `TRANSLATIONS.CZ`.
  - Do JSX šablon nikdy nevkládejte nepřeložené textové řetězce napevno.
