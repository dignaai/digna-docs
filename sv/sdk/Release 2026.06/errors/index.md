# digna Python SDK-fel 2026.06

Den här sidan dokumenterar den undantagshierarki som ***digna*** Python SDK exponerar. Felen täcker API-fel, problem med autentisering och auktorisering samt fall där en resurs inte hittas.

Alla fel som SDK:t kastar ärver från `DignaError`.

::: digna_sdk.exceptions