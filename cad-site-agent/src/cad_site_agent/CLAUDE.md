# CAD Cleanup (nested scope — kraunasi kai Claude Code dirba su šiuo katalogu)

- 47 stabilūs sluoksniai iš schema config. Nieko už schemos ribų.
- Layer egzistavimo check PRIVALOMAS prieš delete/merge (ezdxf wrapper).
- Mutacijos -> system logger. Parse errors -> try-except + JSON metadata log.
- Realų gardą vykdo PreToolUse hook (.claude/settings.json), ne šitas failas.
