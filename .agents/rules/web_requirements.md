# Pravidlo: Požadavky na vývoj webové aplikace

## 1. Doména a zaměření
- **Specializace**: Webová aplikace je specializována na **historické oděvy 15. století** (nohavice, kabátec a další dobové oděvy).
- **Aktuální priorita (1. fáze)**: Zdokonalit stávající nohavice a dokončit kabátec 15. století (přední díly, zadní díl, stojáček, prohnuté rukávy, spodní šůsky a vázací dírky).

## 2. Bezstavová architektura a ochrana soukromí (Strategie 1)
- **Zákaz perzistentní databáze na serveru**: Na serveru nesmí být zavedena databáze (SQL/NoSQL) pro ukládání měr či zákaznických profilů.
- **Klientské úložiště**: Profily zákazníků se ukládají v prohlížeči (`localStorage` / `IndexedDB`).
- **Přenositelnost souborů**: Podpora exportu a importu profilů v souborech `.json` včetně hromadné zálohy a Drag & Drop nahrávání.
- **Dočasné zpracování**: Výpočetní endpointy serveru pracují výhradně v paměti nebo v dočasných souborech v systémovém adresáři s unikátním UUID, které se po odeslání ihned mažou.

## 3. Požadavky na exportní sadu
Webová platforma musí podporovat 4 výstupní formáty:
1. **1:1 Plotrové PDF**: Spojitý tisk na role papíru s popiskem, kontrolním čtvercem $10 \times 10\text{ cm}$ a anotacemi.
2. **Dlaždicové PDF (A4/A3)**: Automatické rozřezání do mřížky stránek s okrajem na slepení (10 mm), pasovacími křížky a označením stránek (např. „Stránka 2-3“).
3. **Čisté vektorové SVG**: S vrstvami (`linie_rezu`, `linie_svu`, `smer_osnovy`, `znacky`, `popisky`) pro Inkscape a Illustrator.
4. **CAD DXF**: Podle standardu AAMA / ASTM pro automatické stříhací stoly.

## 4. Krejčovské CAD prvky
Při generování geometrie střihů musí být konfigurovatelné tyto prvky:
- **Švové přídavky**: Nastavitelná šířka (výchozí 1,5 cm nebo 1,0 cm) vykreslená jako rovnoběžný vnější obrys.
- **Směr osnovy**: Výrazná šipka podél hlavní osy tkaniny na každém střihovém dílu.
- **Sesazovací značky**: Značky podél navazujících švů (průramky, rukávové hlavice, boční švy, kolena).
- **Vázací dírky**: Páry dírek podél pasu kabátce a nohavic vzdálené 2,0 až 2,5 cm pro dobové vázání tkanicemi.
- **Vizuální průvodce měřením**: Anatomické nákresy a vysvětlení správného postupu měření těla.

## 5. Zásada rozšiřitelnosti
- Nezapisujte matematiku nových střihů přímo do Python funkcí.
- Řiďte se Specifikací deklarativního formátu střihů (`docs/pattern_definition_spec.md`), aby nové varianty mohly vznikat v JSON/YAML konfiguraci.
