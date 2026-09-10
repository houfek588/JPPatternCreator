# Referenční příručka webového API

Webový server JPPatternCreator je lehká bezstavová aplikace ve Flasku umístěná v souboru [`web/server.py`](../app/web/server.py).

---

## 1. Přehled endpointů

| Metoda | Trasa | Popis | Content-Type odpovědi |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Servíruje klientskou aplikaci v Reactu (`index.html`) | `text/html` |
| `POST` | `/generate` | Generuje SVG řetězec střihu | `application/json` |
| `POST` | `/export/pdf` | Generuje tiskové PDF v měřítku 1:1 | `application/pdf` |
| `POST` | `/export/png` | Generuje rastrový náhled v PNG | `image/png` |
| `POST` | `/save` | Ukládá šablonu měr na server | `application/json` |

---

## 2. Podrobný popis endpointů

### `POST /generate`
Vypočte geometrii a vrátí SVG řetězec odpovídající zadaným parametrům.

#### Tělo požadavku (JSON)
```json
{
  "patternType": "hosen",
  "part": "all",
  "inputs": {
    "title": "Vzorové kalhoty",
    "VP": 175,
    "OP": 98,
    "OS": 116,
    "BDK": 122,
    "KD": 90,
    "O_st": 61,
    "O_nk": 46,
    "O_l": 40,
    "O_kot": 26
  },
  "sliders": {
    "slider1": 5,
    "slider2": 12,
    "slider3": 5,
    "slider4": 12,
    "slider5": 0,
    "slider6": 0,
    "slider7": 0
  }
}
```

#### Popis polí:
- `patternType` *(string, výchozí: `"hosen"`)*: `"hosen"` nebo `"bodice"`.
- `part` *(string, výchozí: `"all"`)*:
  - Pro `hosen`: `"all"`, `"front"` nebo `"back"`.
  - Pro `bodice`: `"all"`, `"back"` nebo `"collar"`.
- `inputs` *(object)*: Slovník tělesných rozměrů (v centimetrech).
- `sliders` *(object)*: Hodnoty tvarovacích posuvníků:
  - `slider1` (snížení pasu / hloubka límce)
  - `slider2` (šířka nártu)
  - `slider3` (tvar paty / šlapky)
  - `slider4` (tvar rozkroku)
  - `slider5` (posun dělicí linie)
  - `slider6` (levý posun stehna)
  - `slider7` (pravý posun sedu)

#### Úspěšná odpověď (200 OK)
```json
{
  "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"4800\" height=\"6400\" ...>...</svg>"
}
```

#### Chybová odpověď (400 Bad Request / 500 Internal Error)
```json
{
  "status": "error",
  "message": "Chybí povinný rozměr: OP"
}
```

---

### `POST /export/pdf`
Vygeneruje a odešle tiskový PDF soubor v měřítku 1:1.

- **Tělo požadavku**: Shodná JSON struktura jako u `/generate`.
- **Odpověď**: Binární proud PDF souboru.
- **Hlavičky**:
  ```http
  Content-Type: application/pdf
  Content-Disposition: attachment; filename=pattern.pdf
  ```

---

### `POST /export/png`
Vygeneruje a odešle rastrový PNG obrázek střihu ve vysokém rozlišení.

- **Tělo požadavku**: Shodná JSON struktura jako u `/generate`.
- **Odpověď**: Binární proud PNG obrázku.
- **Hlavičky**:
  ```http
  Content-Type: image/png
  Content-Disposition: attachment; filename=pattern.png
  ```

---

### `POST /save`
Uloží zadané parametry do souboru definovaného v `config.SERVER_SAVE_PATH`.

- **Tělo požadavku**: Libovolný JSON objekt.
- **Úspěšná odpověď (200 OK)**:
  ```json
  {
    "status": "ok",
    "message": "Data saved successfully."
  }
  ```
