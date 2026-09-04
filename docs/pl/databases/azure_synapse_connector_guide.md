---
title: Azure Synapse Connector – Database Integration | digna Documentation
description: Skonfiguruj digna, aby łączyła się z Azure Synapse Analytics za pomocą natywnego sterownika Python lub sterownika ODBC. Obsługuje zarówno serverless, jak i dedicated SQL pools.
canonical_url: https://docs.digna.ai/databases/azure_synapse_connector_guide/
image: /assets/logo_square.png
---


# Source Connector for Azure Synapse Analytics

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się z Azure Synapse Analytics przy użyciu natywnego konektora Python lub sterownika ODBC.
Obsługuje zarówno serverless, jak i dedicated SQL pools.

Ta konfiguracja odnosi się do ekranu  **"INTEGRATIONS" →  "DB CONNECTIONS" → "+ ADD DB CONNECTION"**.

![Utwórz połączenie z bazą danych](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Biblioteka:** `pymssql`  
**Obsługiwane uwierzytelnianie:** tylko uwierzytelnianie oparte na haśle

> Dla innych metod uwierzytelniania użyj proszę sterownika ODBC.

### *digna* — konfiguracja (nattywny sterownik)

Podaj następujące informacje na ekranie **"Create Database Connection"**:

```
Name:               Nazwa połączenia. Będzie używana do odwołań do połączenia na innych ekranach.
Technology:         MS SQL Server
Host Address:       <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:          Numer portu, np. 1433
Database Name:      Nazwa bazy danych
User Name:          Nazwa użytkownika bazy danych
User Password:      Hasło dla użytkownika
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki obliczane są bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla oglądanego dnia są kopiowane do tabeli permanentnej, a metryki obliczane są na skopiowanych danych.
                    - Session: Dane kopiowane są do sesyjnej lub tymczasowej tabeli, a metryki obliczane są na tych tymczasowych danych.
                    Dla serverless SQL pool obsługiwany jest tylko tryb "Standard".
Work Schema Name:   Przy użyciu trybu "Permanent", tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Disabled (domyślnie)
```

---

## ODBC Driver

Sterownik ODBC może oferować szerszy zakres opcji uwierzytelniania i łączności. Sekcja ta skupia się na uwierzytelnianiu opartym na haśle przy użyciu sterownika **ODBC Driver 18 for SQL Server**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj sterownik **ODBC Driver 18 for SQL Server** (lub podobny) postępując zgodnie z oficjalnym przewodnikiem instalacyjnym dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem na podstawie hasła:

#### Krok 1
![Krok 1](images/azure_synapse/create_odbc_data_source_step1.png)

Wypełnij pole "Server".
Użyj nazwy workspace Synapse i rozszerz ją o ".sql.azuresynapse.net".  
**Uwaga**, jeśli chcesz połączyć się przez serverless SQL pool, upewnij się, że uwzględnisz "-ondemand", jak pokazano na zrzucie ekranu poniżej.

Kliknij przycisk **Next >**.

#### Krok 2
![Krok 2](images/azure_synapse/create_odbc_data_source_step2.png)

Wybierz metodę uwierzytelniania (np. nazwa użytkownika i hasło)
i podaj wymagane dane.

Kliknij przycisk **Next >**.

#### Krok 3
![Krok 3](images/azure_synapse/create_odbc_data_source_step3.png)

Wybierz ustawienia zgodne z ANSI, następnie kliknij przycisk **Next >**.

#### Krok 4
![Krok 4](images/azure_synapse/create_odbc_data_source_step4.png)

Możesz pozostawić ustawienia domyślne lub wybrać opcje według potrzeb 
i kliknąć przycisk **Finish**. 

#### Krok 5
![Krok 5](images/azure_synapse/create_odbc_data_source_step5.png)

Teraz kliknij przycisk **Test datasource**.

#### Krok 6
![Krok 6](images/azure_synapse/create_odbc_data_source_step6.png)

Gdy zobaczysz ekran potwierdzający powodzenie, ODBC został poprawnie skonfigurowany.

---

Teraz możesz skonfigurować *digna*, aby używała połączenia ODBC, albo z użyciem **DSN (Data Source Name)**, albo w konfiguracji **DSN-less**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Będzie używana do odwołań do połączenia na innych ekranach.
Technology:         MS SQL Server
Database Name:      Baza danych zawierająca schematy źródłowe
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki obliczane są bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla oglądanego dnia są kopiowane do tabeli permanentnej, a metryki obliczane są na skopiowanych danych.
                    - Session: Dane kopiowane są do sesyjnej lub tymczasowej tabeli, a metryki obliczane są na tych tymczasowych danych.
                    Dla serverless SQL pool obsługiwany jest tylko tryb "Standard".
Work Schema Name:   Przy użyciu trybu "Permanent", tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Enabled
```

#### Właściwości ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "twój użytkownik bazy danych"
name: "PWD",        value: "twoje hasło do bazy danych"
name: "DATABASE",   value: "nazwa bazy danych zawierającej schemat danych źródłowych"
```

> Wartość `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez użycia DSN (DSN-less)

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Będzie używana do odwołań do połączenia na innych ekranach.
Technology:         MS SQL Server
Database Name:      Nazwa bazy danych zawierającej schemat danych źródłowych
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki obliczane są bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla oglądanego dnia są kopiowane do tabeli permanentnej, a metryki obliczane są na skopiowanych danych.
                    - Session: Dane kopiowane są do sesyjnej lub tymczasowej tabeli, a metryki obliczane są na tych tymczasowych danych.
                    Dla serverless SQL pool obsługiwany jest tylko tryb "Standard".
Work Schema Name:   Przy użyciu trybu "Permanent", tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Enabled
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "twój użytkownik bazy danych"
name: "PWD",        value: "twoje hasło do bazy danych"
name: "DATABASE",   value: "nazwa bazy danych zawierającej schematy danych źródłowych"
```

**Uwaga** dotycząca właściwości SERVER:  
Użyj nazwy workspace Synapse i dodaj końcówkę ".sql.azuresynapse.net". Jeśli chcesz połączyć się przez serverless SQL pool, upewnij się, że uwzględnisz "-ondemand", jak pokazano na zrzucie ekranu poniżej.