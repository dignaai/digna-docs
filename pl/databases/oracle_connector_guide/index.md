# Konektor źródłowy dla Oracle

Ten przewodnik opisuje, jak skonfigurować *digna* do połączenia z Oracle Database przez
**ODBC**, używając ciągu połączenia **bez DSN**.

Część konfiguracji po stronie digna jest taka sama dla każdej technologii — gdzie tworzy się
połączenia, jak szyfrowane są wartości właściwości, jak testuje się połączenie i co oznaczają
tryby profilowania. Opisano to w
[Przeglądzie połączeń z bazami danych](overview.md). Ta strona omawia to, co jest specyficzne
dla Oracle.

---

## 1. Zainstaluj sterownik ODBC {: #1-install-the-odbc-driver }

Sterownik ODBC Oracle jest częścią **klienta Oracle** (wystarczy pakiet „ODBC” z Instant
Client). Zainstaluj go na maszynie, na której działa backend *digna*, postępując zgodnie z
oficjalną instrukcją instalacji producenta.

Sterownik rejestruje się jako **Oracle in `<OracleHomeName>`** — na przykład
`Oracle in OraDB21Home1` lub `Oracle in instantclient_21_13`. Nazwa katalogu domowego różni się
w zależności od instalacji, więc odczytaj dokładną nazwę na swoim hoście, jak opisano w
[Instalacji sterownika ODBC na hoście digna](overview.md#install-the-driver).

---

## 2. Właściwości ODBC {: #2-odbc-properties }

!!! important "Przykład, nie specyfikacja"

    Poniższy zestaw to jedna z kombinacji, o których wiadomo, że działają. Właściwości należą do
    sterownika ODBC Oracle, więc ich nazwy, wartości domyślne i akceptowane wartości różnią się
    między wersjami klienta, a zwłaszcza nazwa sterownika zależy od katalogu domowego Oracle na
    Twoim hoście. Potraktuj to jako punkt wyjścia i sprawdź dokumentację zainstalowanej wersji
    klienta.

Dodaj następujące właściwości w ekranie **Add DB Connection**:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Musi odpowiadać nazwie sterownika zarejestrowanej na hoście *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Baza danych, z którą następuje połączenie — patrz niżej |
| `UID` | `DIGNA_SOURCE_USER` | Użytkownik bazy danych |
| `PWD` | `<password>` | Zaznacz **Encrypted** |

Powstały ciąg połączenia wygląda tak:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Wartość `DBQ`

`DBQ` przyjmuje trzy formy. Dla *digna* są równoważne; różnią się tym, co musi być
skonfigurowane na hoście *digna*:

| Forma | Przykład | Wymaga |
|---|---|---|
| **Pełny deskryptor połączenia** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Niczego — wszystko jest we właściwości. Zalecane |
| **Alias TNS** | `DIGNA_SOURCE` | Alias musi istnieć w pliku `tnsnames.ora` klienta Oracle na hoście *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Klienta Oracle obsługującego Easy Connect (12c i nowsze) |

!!! tip "Preferuj pełny deskryptor"

    Alias TNS przenosi połowę definicji połączenia do pliku na hoście *digna*, gdzie łatwo o nim
    zapomnieć, gdy host jest odtwarzany albo *digna* jest przenoszona. Pełny deskryptor
    utrzymuje połączenie samowystarczalne — a o to właśnie chodzi w konfiguracji bez DSN.

Zwróć uwagę, że nawiasy w deskryptorze nie sprawiają problemu wewnątrz ciągu połączenia, ale
jeśli Twoje hasło zawiera `;`, ujmij je w nawiasy klamrowe: `PWD={p@ss;word}`.

---

## 3. Konfiguracja *digna* {: #3-digna-configuration }

W ekranie **Add DB Connection** podaj następujące dane:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Uwagi dotyczące Oracle {: #4-notes-on-oracle }

- **Schematy to użytkownicy.** *digna* wyświetla użytkowników Oracle jako schematy, więc schemat
  źródłowy jest właścicielem tabel — w powyższym przykładzie `DIGNA_SOURCE_USER`. Użytkownik
  połączenia potrzebuje uprawnienia `SELECT` do tych tabel, bezpośrednio albo poprzez rolę.
- **Jedno połączenie widzi jedną bazę danych.** Katalog udostępniany przez *digna* to baza, do
  której przypięte jest połączenie, więc `DBQ` decyduje, która usługa, a zatem która baza, jest
  profilowana.
- **Identyfikatory rozróżniają wielkość liter po ujęciu w cudzysłowy.** *digna* ujmuje w
  cudzysłowy nazwy odczytane ze słownika danych, czyli to, co przechowuje Oracle — wielkie
  litery dla obiektów bez cudzysłowów.
- **Tryby profilowania.** *Permanent* tworzy tabele robocze w **Work Schema**, więc użytkownik
  potrzebuje tam uprawnienia `CREATE TABLE` oraz przydziału na przestrzeni tabel. *Session*
  używa prywatnej tabeli tymczasowej (`ORA$PTT_…`, Oracle 18c i nowsze) i nie dotyka
  **Work Schema**. *Standard* wymaga wyłącznie dostępu do odczytu.

---

## 5. Weryfikacja sterownika (opcjonalnie) {: #5-verifying-the-driver-optional }

Konfigurowanie źródła danych ODBC nie jest wymagane dla połączenia bez DSN, ale okno dialogowe
samego sterownika to wygodny sposób, aby przed wprowadzeniem danych w *digna* potwierdzić, że
klient Oracle, nazwa usługi i Twoje poświadczenia działają.

#### Krok 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Oferowana tutaj **TNS Service Name** pochodzi z pliku `tnsnames.ora` Twojej instalacji klienta
Oracle — to tam zdefiniowany jest alias, a wraz z nim host, port i nazwa usługi. W *digna*
możesz użyć aliasu jako `DBQ` albo zamiast tego pełnego deskryptora.

#### Krok 2 – Przetestuj połączenie

Kliknij przycisk **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Podaj hasło i kliknij przycisk **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Komunikat powodzenia potwierdza, że sterownik i poświadczenia działają.