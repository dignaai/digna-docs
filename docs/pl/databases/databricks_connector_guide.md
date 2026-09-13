---
title: Konektor Databricks – Integracja baz danych | digna Dokumentacja
description: Skonfiguruj digna do połączenia z Databricks z Unity Catalog przez ODBC za pomocą ciągu połączenia bez DSN. Obejmuje sterownik ODBC Databricks, osobiste tokeny dostępu, ścieżkę HTTP oraz ustawienia połączenia po stronie digna.
image: /assets/logo_square.png
---

# Konektor źródłowy dla Databricks

Ten przewodnik opisuje, jak skonfigurować *digna* do połączenia z Databricks przez **ODBC**,
używając ciągu połączenia **bez DSN**.

Część konfiguracji po stronie digna jest taka sama dla każdej technologii — gdzie tworzy się
połączenia, jak szyfrowane są wartości właściwości, jak testuje się połączenie i co oznaczają
tryby profilowania. Opisano to w
[Przeglądzie połączeń z bazami danych](overview.md). Ta strona omawia to, co jest specyficzne
dla Databricks.

!!! note "Unity Catalog jest wymagany"

    *digna* odczytuje dostępne katalogi z `system.information_schema.catalogs`, więc obszar
    roboczy musi mieć włączony Unity Catalog. Wcześniejsze wydania *digna* oferowały osobną
    technologię „Databricks Legacy” dla obszarów roboczych bez Unity Catalog; nie jest ona już
    dostępna.

---

## 1. Zainstaluj sterownik ODBC {: #1-install-the-odbc-driver }

Zainstaluj **Databricks ODBC Driver** na maszynie, na której działa backend *digna*, postępując
zgodnie z
[instrukcją instalacji Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

W zależności od wersji sterownik rejestruje się jako **Simba Spark ODBC Driver** albo jako
**Databricks ODBC Driver**. Odczytaj dokładną zarejestrowaną nazwę na swoim hoście, jak opisano
w [Instalacji sterownika ODBC na hoście digna](overview.md#install-the-driver).

---

## 2. Zbierz dane połączenia {: #2-gather-the-connection-details }

Wszystkie wartości pochodzą z magazynu SQL (lub klastra), z którego ma korzystać *digna*.
Otwórz go w obszarze roboczym Databricks i przejdź do **Connection details**:

| Pole Databricks | Używane jako |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, zwykle `443` |
| **HTTP path** | `HTTPPath` |

Na potrzeby uwierzytelniania utwórz **osobisty token dostępu** — zobacz
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Tokeny należą do użytkownika lub jednostki usługi, a ta jednostka potrzebuje uprawnień
`USE CATALOG`, `USE SCHEMA` i `SELECT` do danych źródłowych.

---

## 3. Właściwości ODBC {: #3-odbc-properties }

!!! important "Przykład, nie specyfikacja"

    Poniższy zestaw to jedna z kombinacji, o których wiadomo, że działają. Właściwości należą do
    sterownika Databricks/Simba, więc ich nazwy, wartości domyślne i akceptowane wartości różnią
    się między wersjami sterownika — sterownik był przemianowany, a jego opcje uwierzytelniania
    rozszerzane więcej niż raz — oraz między platformami. Potraktuj to jako punkt wyjścia i
    sprawdź dokumentację zainstalowanej wersji sterownika.

Dodaj następujące właściwości w ekranie **Add DB Connection**:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Musi odpowiadać nazwie sterownika zarejestrowanej na hoście *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Nazwa hosta serwera magazynu, np. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | Ścieżka HTTP magazynu lub klastra |
| `SSL` | `1` | Punkty końcowe Databricks działają wyłącznie po TLS |
| `ThriftTransport` | `2` | Transport HTTP, którym posługują się punkty końcowe SQL |
| `AuthMech` | `3` | Uwierzytelnianie tokenem |
| `UID` | `token` | Dosłowne słowo `token`, a nie nazwa użytkownika |
| `PWD` | `dapi…` | Osobisty token dostępu. Zaznacz **Encrypted** |
| `UseNativeQuery` | `1` | Przekazuje SQL z *digna* bez zmian — patrz niżej |

Powstały ciąg połączenia wygląda tak:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Zostaw `UseNativeQuery=1`"

    Przy `UseNativeQuery=0` — domyślnym ustawieniu sterownika — sterownik przepisuje przychodzący
    SQL na to, co uznaje za przenośną składnię ODBC. *digna* generuje już SQL dla Databricks,
    więc przepisanie może zmienić cytowanie apostrofami wstecznymi i literały dat, a profilowanie
    kończy się wtedy niepowodzeniem na instrukcjach, które w zapisanej postaci są poprawne.

### OAuth zamiast tokenu

Dla jednostki usługi z uwierzytelnianiem OAuth typu maszyna-maszyna zastąp `AuthMech`, `UID` i
`PWD` przez:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Poświadczenia klienta |
| `Auth_Client_ID` | `<application id>` | Jednostka usługi |
| `Auth_Client_Secret` | `<client secret>` | Zaznacz **Encrypted** |

---

## 4. Konfiguracja *digna* {: #4-digna-configuration }

W ekranie **Add DB Connection** podaj następujące dane:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Uwagi dotyczące Databricks {: #5-notes-on-databricks }

- **Magazyn musi działać** lub móc się uruchomić w momencie, gdy *digna* się łączy. Magazyn
  wznawiany ze stanu zatrzymania może potrzebować więcej czasu niż limit połączenia — jeśli test
  zawiedzie przy pierwszej próbie po okresie bezczynności, ponów go.
- **Katalogi pochodzą z obszaru roboczego.** W odróżnieniu od większości technologii jedno
  połączenie Databricks sięga do każdego katalogu, który jednostka może zobaczyć, więc
  pojedyncze połączenie może obsługiwać źródła w wielu katalogach.
- **Tryby profilowania.** *Permanent* tworzy tabele robocze w **Work Schema** wewnątrz katalogu
  źródła, więc jednostka potrzebuje tam uprawnienia `CREATE TABLE`. *Session* używa
  `CREATE TEMPORARY TABLE` i nie dotyka **Work Schema**. *Standard* wymaga wyłącznie dostępu do
  odczytu.
- **Magazyny bezserwerowe działają** tak samo; różni się tylko `HTTPPath`.

---

## 6. Weryfikacja sterownika (opcjonalnie) {: #6-verifying-the-driver-optional }

Konfigurowanie źródła danych ODBC nie jest wymagane dla połączenia bez DSN, ale okno dialogowe
samego sterownika to wygodny sposób, aby przed wprowadzeniem danych w *digna* potwierdzić, że
sterownik, magazyn i token działają.

#### Krok 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Krok 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Krok 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Krok 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Krok 5 – Przetestuj połączenie

Kliknij przycisk **TEST**. Udane połączenie powinno wyglądać tak:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

Host, ścieżka HTTP i token wprowadzone tutaj to dokładnie te same wartości, które przyjmują
właściwości z [sekcji 3](#3-odbc-properties).
