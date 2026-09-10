---
name: tiled-pdf-exporter
description: >-
  Specializovaná dovednost pro implementaci a správu vícestránkového dlaždicového tisku PDF
  (A4/A3 s přesahy, pasovacími značkami a číslováním), velkoformátového PDF a exportu do DXF
  pomocí knihovny ReportLab v aplikaci JPPatternCreator.
---

# Dovednost: Dlaždicový tisk a produkční exporty (Tiled PDF Exporter)

Tato dovednost vede agenta při implementaci vícestránkového dlaždicového tisku PDF, spojitého 1:1 plotrového PDF a průmyslových CAD výstupů z vektorových střihů.

## Technické cíle
- **Spojité 1:1 plotrové PDF**: Výstup v plném měřítku pro role papíru a plotry (A0/A1).
- **Dlaždicové vícestránkové PDF**: Automatické rozřezání velkého plátna (např. $120\text{ cm} \times 160\text{ cm}$) do mřížky běžných kancelářských listů A4 / US Letter.
- **Slepovací pomůcky**: Okraje na přesah, ořezové linie, pasovací křížky a indexování stránek (řada/sloupec).
- **Kontrolní kalibrační čtverec**: Vložený testovací čtverec $10\text{ cm} \times 10\text{ cm}$.

---

## Algoritmus a matematika dlaždicového rozřezání

### Rozměry stránek a tisknutelná oblast (příklad pro A4)
- Celkový rozměr A4: $210\text{ mm} \times 297\text{ mm}$ ($595,28\text{ pt} \times 841,89\text{ pt}$).
- Netisknutelný okraj tiskárny: $10\text{ mm}$ na každé straně.
- Tisknutelný rozměr dlaždice:
  $$W_{\text{dlaždice}} = 210\text{ mm} - 20\text{ mm} = 190\text{ mm}$$
  $$H_{\text{dlaždice}} = 297\text{ mm} - 20\text{ mm} = 277\text{ mm}$$
- Přesah pro slepení: $10\text{ mm}$ pro přeložení a slepení sousedních listů.

### Výpočet mřížky stránek
Pro rozměry plátna střihu $W_{\text{plátno}}$ a $H_{\text{plátno}}$:
$$\text{Sloupce} = \lceil W_{\text{plátno}} / W_{\text{dlaždice}} \rceil$$
$$\text{Řady} = \lceil H_{\text{plátno}} / H_{\text{dlaždice}} \rceil$$
$$\text{Celkem stránek} = \text{Sloupce} \times \text{Řady}$$

### Posun souřadnic v ReportLabu
Pro každou dlaždici $(s, r)$, kde $s \in [0, \text{Sloupce}-1]$ a $r \in [0, \text{Řady}-1]$:
1. `canvas.saveState()`
2. Nastavte ořezový obdélník (*clipping box*) na hranice aktuální dlaždice.
3. Aplikujte posun souřadnic:
   ```python
   x_posun = -s * sirka_dlazdice_pt
   y_posun = -r * vyska_dlazdice_pt
   canvas.translate(x_posun, y_posun)
   ```
4. Vykreslete křivky střihu, linie a textové popisky.
5. `canvas.restoreState()`
6. Vykreslete pasovací křížky na okrajích, ořezové značky a označení stránky:
   `"List (Sloupec {s+1}, Řada {r+1}) z {Sloupce}x{Řady} – sesaďte křížky"`
7. Zavolejte `canvas.showPage()` pro přechod na další list.

---

## Kontrolní kalibrační čtverec
Každý tiskový export musí obsahovat kalibrační čtverec na prvním listu nebo na začátku role:
- Vnější rozměr: Přesně $100\text{ mm} \times 100\text{ mm}$ ($10\text{ cm} \times 10\text{ cm}$).
- Vnitřní rozměr: Přesně $50\text{ mm} \times 50\text{ mm}$.
- Textový popisek: `"KONTROLNÍ ČTVEREC: Před stříháním ověřte pravítkem, že rozměr měří přesně 100 mm."`

---

## Kontrolní seznam před odevzdáním exportéru
- [ ] Kalibrační čtverec měří při tisku na 100 % (bez přizpůsobení stránce) přesně $10,0\text{ cm} \pm 0,5\text{ mm}$.
- [ ] Sousední stránky dlaždicového PDF na sebe po odstřižení okrajů přesně navazují.
- [ ] Proud souboru se korektně uzavře a nezanechá na serveru opuštěné dočasné soubory.
