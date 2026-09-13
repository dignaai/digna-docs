# Konektor źródłowy dla Hive

Ten przewodnik opisuje, jak skonfigurować *digna* do połączenia z Apache Hive przez **ODBC**,
używając ciągu połączenia **bez DSN**.

Część konfiguracji po stronie digna jest taka sama dla każdej technologii — gdzie tworzy się
połączenia, jak szyfrowane są wartości właściwości, jak testuje się połączenie i co oznaczają
tryby profilowania. Opisano to w
[Przeglądzie połączeń z bazami danych](overview.md). Ta strona omawia to, co jest specyficzne
dla Hive.

---

## 1. Zainstaluj sterownik ODBC {: #1-install-the-odbc-driver }

Zainstaluj **Cloudera ODBC Driver for Apache Hive** na maszynie, na której działa backend
*digna*, postępując zgodnie z oficjalną instrukcją instalacji producenta.

Odczytaj dokładną nazwę zarejestrowanego sterownika na swoim hoście, jak opisano w
[Instalacji sterownika ODBC na hoście digna](overview.md#install-the-driver).

---

## 2. Właściwości ODBC {: #2-odbc-properties }

!!! important "Przykład, nie specyfikacja"

    Poniższy zestaw to jedna z kombinacji, o których wiadomo, że działają. Właściwości należą do
    sterownika Cloudera dla Hive, więc ich nazwy, wartości domyślne i akceptowane wartości
    różnią się między wersjami sterownika i platformami, a to, co akceptuje HiveServer2, zależy
    całkowicie od sposobu zabezpieczenia klastra — mechanizmu uwierzytelniania, trybu
    transportu, TLS, bramy. Potraktuj to jako punkt wyjścia i sprawdź dokumentację
    zainstalowanej wersji sterownika.

Dodaj następujące właściwości w ekranie **Add DB Connection**:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Musi odpowiadać nazwie sterownika zarejestrowanej na hoście *digna* |
| `HOST` | `hive.example.com` | Nazwa hosta lub adres IP HiveServer2 |
| `PORT` | `10000` | Port HiveServer2; `10001` dla transportu HTTP |

Powstały ciąg połączenia wygląda tak:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Uwierzytelnianie

Niezabezpieczony HiveServer2 akceptuje trzy powyższe właściwości bez zmian. Tam, gdzie
uwierzytelnianie jest włączone, dodaj:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `AuthMech` | `3` | `0` brak uwierzytelniania, `2` tylko nazwa użytkownika, `3` nazwa użytkownika i hasło, `1` Kerberos |
| `UID` | `digna_source_user` | Wymagane dla `AuthMech` `2` i `3` |
| `PWD` | `<password>` | Wymagane dla `AuthMech` `3`. Zaznacz **Encrypted** |

W przypadku Kerberos (`AuthMech=1`) host *digna* potrzebuje dodatkowo ważnego biletu lub pliku
keytab oraz właściwości `KrbHostFQDN`, `KrbServiceName` i `KrbRealm`, które dokumentuje
sterownik.

### Transport i TLS

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `ThriftTransport` | `2` | `0` binarny (domyślny, port 10000), `1` SASL, `2` HTTP (port 10001, i tego oczekuje brama Knox) |
| `HTTPPath` | `cliservice` | Przy `ThriftTransport=2` |
| `SSL` | `1` | Tam, gdzie HiveServer2 jest zabezpieczony TLS |
| `Schema` | `dignadata` | Baza Hive, w której rozpoczyna się sesja. Opcjonalne — *digna* kwalifikuje swoje zapytania |

---

## 3. Konfiguracja *digna* {: #3-digna-configuration }

W ekranie **Add DB Connection** podaj następujące dane:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Uwagi dotyczące Hive {: #4-notes-on-hive }

- **Katalogi pochodzą ze sterownika.** Hive nie ma własnego katalogu, więc *digna* przyjmuje to,
  co zgłasza sterownik — zwykle pojedynczy wpis o nazwie `HIVE` — i wyświetla poniżej bazy Hive
  jako schematy.
- **Work Schema to baza Hive.** Dla profilowania *Permanent* użytkownik potrzebuje w niej prawa
  do tworzenia i usuwania tabel, a podstawowa lokalizacja magazynu musi być zapisywalna.
- **Tryby profilowania.** *Permanent* tworzy tabele robocze w **Work Schema**. *Session* używa
  `CREATE TEMPORARY TABLE`, co wymaga HiveServer2 obsługującego tabele tymczasowe, i nie dotyka
  **Work Schema**. *Standard* wymaga wyłącznie dostępu do odczytu i jest trybem, który należy
  wybrać w klastrze, w którym *digna* w ogóle nie ma dostępu do zapisu.
- **Profilowanie to zestaw zapytań, a nie skanowanie.** Każdą statystykę oblicza HiveServer2,
  więc kolejka, do której wysyła użytkownik *digna*, powinna mieć wystarczającą przepustowość na
  okno inspekcji.

---

## 5. Weryfikacja sterownika (opcjonalnie) {: #5-verifying-the-driver-optional }

Konfigurowanie źródła danych ODBC nie jest wymagane dla połączenia bez DSN, ale okno dialogowe
samego sterownika to wygodny sposób, aby przed wprowadzeniem danych w *digna* potwierdzić, że
sterownik, tryb transportu i Twoje poświadczenia działają.

#### Krok 1
![Step 1](images/hive/create_odbc_data_source_step1.png)

Pola **Host**, **Port**, **Database**, **Mechanism** i **Thrift Transport** odpowiadają tutaj
właściwościom `HOST`, `PORT`, `Schema`, `AuthMech` i `ThriftTransport` z
[sekcji 2](#2-odbc-properties).

#### Krok 2 – Przetestuj połączenie

Podaj hasło i kliknij przycisk **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Po pomyślnym teście kliknij przycisk **OK**.