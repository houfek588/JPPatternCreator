"""
JPPatternCreator - Hlavní vstupní bod aplikace.

Spouští bezstavový webový server (Flask + React SPA), který představuje
primární platformu pro generování a export historických oděvních střihů.
Volitelně umožňuje spustit i desktopové rozhraní pomocí přepínače --desktop.
"""
import argparse
from app.web.server import start_server


def main():
    parser = argparse.ArgumentParser(description="JPPatternCreator - Parametrický CAD generátor historických střihů")
    parser.add_argument(
        "--desktop",
        action="store_true",
        help="Spustit lokální desktopové rozhraní (PyQt6) namísto webového serveru"
    )
    parser.add_argument("--host", default="127.0.0.1", help="Hostitel pro webový server (výchozí: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port pro webový server (výchozí: 5000)")
    parser.add_argument("--no-debug", action="store_true", help="Vypnout debug režim serveru")

    args = parser.parse_args()

    if args.desktop:
        from app.desktop.layout import start_window
        print("Spouštím desktopové rozhraní (PyQt6)...")
        start_window()
    else:
        print(f"Spouštím webový server na http://{args.host}:{args.port}")
        print("Pro ukončení stiskněte CTRL+C")
        start_server(host=args.host, port=args.port, debug=not args.no_debug)


if __name__ == "__main__":
    main()
