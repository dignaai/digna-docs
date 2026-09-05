# Źródłowy konektor dla Oracle

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się z Oracle DB używając natywnego konektora Python lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Utwórz połączenie z bazą danych](images/data_source_config_input_mask.png)

---

## Natywny sterownik Python

**Biblioteka:** `python-oracledb`  
**Obsługiwane uwierzytelnianie:** Tylko uwierzytelnianie za pomocą hasła

> Dla innych metod uwierzytelniania prosimy użyć sterownika ODBC.

### Konfiguracja *digna* (natywny sterownik)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Name:               Nazwa połączenia. Używana do odwołań do tego połączenia na innych ekranach.
Technology:         Oracle
Host Address:       Nazwa serwera lub adres IP
Host Port:          Numer portu, np. 1521
Database Name:      Nazwa instancji lub service name
Schema Name:        Schemat zawierający źródłowe dane
User Name:          Nazwa użytkownika bazy danych
User Password:      Hasło użytkownika
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki obliczane są bezpośrednio na źródłowych tabelach bez kopiowania danych.
                    - Permanent: Dane dla inspekcjonowanego dnia są kopiowane do stałej tabeli, a metryki obliczane są na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki obliczane są na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent" tabele robocze będą umieszczone w tym schemacie.
Use ODBC:           Wyłączone (domyślnie)
```

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu za pomocą hasła z użyciem sterownika **Oracle in OraDB21Home1**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **Oracle in OraDB21Home1** (lub podobny), postępując zgodnie z oficjalnym przewodnikiem instalacyjnym dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem za pomocą hasła:

#### Krok 1
![Krok 1](images/oracle/create_odbc_data_source_step1.png)

Uwaga:
Nazwa usługi TNS (TNS Service Name) musi być skonfigurowana w pliku tnsnames.ora instalacji klienta Oracle. To tam podajesz deskryptor połączenia (host, port, service name).

#### Krok 2 – Test połączenia

Kliknij przycisk **Test Connection**.

![Krok 2](images/oracle/create_odbc_data_source_step2.png)

Podaj hasło i kliknij przycisk **OK**.

![Krok 2](images/oracle/create_odbc_data_source_step3.png)

---

Teraz możesz skonfigurować *digna*, aby używała połączenia ODBC, albo z użyciem **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Używana do odwołań do tego połączenia na innych ekranach.
Technology:         Oracle
Database Name:      Baza danych zawierająca schemat źródłowy
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki obliczane są bezpośrednio na źródłowych tabelach bez kopiowania danych.
                    - Permanent: Dane dla inspekcjonowanego dnia są kopiowane do stałej tabeli, a metryki obliczane są na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki obliczane są na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent" tabele robocze będą umieszczone w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "twoj_uzytkownik_oracle"
name: "PWD",            value: "{twoje haslo w nawiasach klamrowych}"
```

> `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji Twojego sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Używana do odwołań do tego połączenia na innych ekranach.
Technology:         Oracle
Database Name:      Schemat zawierający źródłowe dane (to samo co Schema Name)
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki obliczane są bezpośrednio na źródłowych tabelach bez kopiowania danych.
                    - Permanent: Dane dla inspekcjonowanego dnia są kopiowane do stałej tabeli, a metryki obliczane są na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki obliczane są na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent" tabele robocze będą umieszczone w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```