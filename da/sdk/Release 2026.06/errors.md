# digna Python SDK-fejl 2026.06

Denne side dokumenterer det undtagelseshierarki, som ***digna*** Python SDK stiller til rådighed. Fejlene dækker API-fejl, problemer med godkendelse og autorisation samt tilfælde, hvor en ressource ikke findes.

Alle fejl, som SDK'et kaster, nedarver fra `DignaError`.

::: digna_sdk.exceptions