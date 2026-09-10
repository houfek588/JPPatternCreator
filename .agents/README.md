# Konfigurace agentů pro workspace (.agents)

Tato složka obsahuje pravidla a konfigurační soubory pro systém Antigravity a další AI asistenty v tomto projektu.

## Struktura složky

```
.agents/
├── README.md                      # Přehled konfigurace agentů
├── rules/                         # Modulární pravidla pro agenty
│   ├── web_requirements.md       # Požadavky PRD a pravidla webové aplikace
│   ├── declarative_patterns.md   # Schéma a pravidla pro deklarativní střihy
│   ├── historical_reenactment.md # Pravidla pro věrnost oděvů 15. století
│   ├── stateless_privacy.md       # Pravidla pro ochranu soukromí a bezstavový server
│   ├── code_style.md              # Standardy pro Python, React a geometrii
│   └── testing_and_builds.md      # Kontrola kvality, testy a sestavení frontendu
└── skills/                        # Specializované dovednosti (workflows) agentů
    ├── garment-pattern-creator/   # Dovednost pro rýsování a validaci střihů 15. století
    │   └── SKILL.md
    └── tiled-pdf-exporter/        # Dovednost pro dlaždicový tisk A4/A3 a velkoformátové PDF
        └── SKILL.md
```

## Načítání a platnost pravidel
- Soubory v této složce se vztahují specificky na workspace `JPPatternCreator`.
- Hlavní instrukce v kořeni repozitáře [`AGENTS.md`](../AGENTS.md) poskytují obecný architektonický rámec, zatímco jednotlivé soubory v `rules/` a `skills/` obsahují konkrétní omezení a procedurální návody.
