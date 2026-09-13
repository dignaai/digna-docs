---
title: Przegląd połączeń z bazami danych – Konfiguracja ODBC bez DSN | digna Dokumentacja
description: Jak działają połączenia z bazami danych w digna. Każda technologia źródłowa jest osiągana przez ODBC za pomocą ciągu połączenia bez DSN, zbudowanego z właściwości ODBC. Obejmuje instalację sterownika na hoście digna, ekran Add DB Connection, szyfrowanie właściwości, testowanie połączeń, rozwiązywanie problemów oraz odnośniki do przewodników dla poszczególnych technologii.
image: /assets/logo_square.png
keywords:
  - digna database connection
  - dsn-less odbc
  - odbc connection string
  - odbc driver setup
  - unixodbc
  - odbc properties
  - data source configuration
lang: pl
robots: index, follow
og_title: Połączenia z bazami danych digna – Konfiguracja ODBC bez DSN
og_description: Skonfiguruj połączenie źródłowe digna przez ODBC bez DSN. Instalacja sterownika, właściwości ODBC, szyfrowanie, testy i rozwiązywanie problemów.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Przegląd połączeń z bazami danych

---

## Spis treści

1. [Jak działają połączenia](#how-connections-work)
2. [Przewodniki dla technologii](#technology-guides)
3. [Wymaganie wstępne: instalacja sterownika ODBC na hoście digna](#install-the-driver)
4. [Tworzenie połączenia z bazą danych](#create-a-database-connection)
5. [Właściwości ODBC](#odbc-properties)
6. [Szyfrowanie wartości właściwości](#encrypting-property-values)
7. [Testowanie połączenia](#testing-a-connection)
8. [Którą bazę danych widzi połączenie](#which-database-the-connection-sees)
9. [Tryb profilowania i Work Schema](#profiling-mode-and-work-schema)
10. [Użycie DSN zamiast tego](#using-a-dsn-instead)
11. [Rozwiązywanie problemów](#troubleshooting)

---

## Jak działają połączenia {: #how-connections-work }

*digna* sięga do każdej technologii źródłowej przez **ODBC**. Połączenie to lista właściwości
ODBC, które wprowadzasz jako pary klucz/wartość. Gdy *digna* otwiera połączenie, łączy te pary w
ciąg połączenia — `Key=Value`, rozdzielone `;`, w podanej przez Ciebie kolejności — i przekazuje
go menedżerowi sterowników ODBC na hoście *digna*.

To właśnie samodzielne wprowadzanie właściwości sprawia, że konfiguracja jest **bez DSN**:
połączenie niesie ze sobą wszystko, czego potrzebuje sterownik, więc na hoście nie trzeba
rejestrować żadnego źródła danych ODBC (DSN). To zalecany sposób konfigurowania *digna*,
ponieważ definicja połączenia znajduje się w całości w *digna* i przenosi się razem z nią.

### Dlaczego ODBC {: #why-odbc }

Wcześniejsze wydania oferowały wybór między sterownikiem dla danej technologii a ODBC,
wskazywany przełącznikiem **Use ODBC**. Od wydania 2026.06 *digna* opiera się wyłącznie na ODBC.
Jeden standardowy interfejs daje więcej niż zestaw sterowników pisanych na miarę:

- **Uwierzytelnianie** — uwierzytelnianie jest częścią ODBC, więc połączenie może korzystać ze
  wszystkiego, co obsługuje jego sterownik: haseł, tokenów i PAT-ów, Kerberosa i Active
  Directory, MFA i logowania jednokrotnego przez przeglądarkę, tożsamości chmurowych,
  certyfikatów klienta i TLS. Nowe metody pojawiają się wraz z aktualizacją sterownika, a nie po
  oczekiwaniu na wydanie *digna*.
- **Sterowniki utrzymywane przez dostawców baz danych** — sterownik producenta nadąża za nowymi
  wersjami serwera i poprawkami bezpieczeństwa, a Ty możesz aktualizować go we własnym tempie,
  niezależnie od *digna*.
- **Jeden sposób konfigurowania wszystkiego** — każda technologia to lista właściwości
  klucz/wartość, z tym samym interfejsem, tym samym szyfrowaniem wartości wrażliwych i tą samą
  diagnostyką, zamiast innego zestawu pól dla każdego źródła.
- **Strojenie i zasięg** — opcje sterownika, takie jak limity czasu, ustawienia TLS, serwery
  proxy i rozmiary pobierania, są dostępne dla każdego źródła, a podłączyć można każdą
  technologię ze zgodnym sterownikiem ODBC, również taką, dla której *digna* nie publikuje
  osobnego przewodnika.

!!! note "Co zmieniło się w interfejsie"

    Przełącznik **Use ODBC** oraz osobne pola hosta, portu, bazy danych, użytkownika i hasła już
    nie istnieją. Połączenie, które nie korzysta jeszcze z ODBC, wymaga wprowadzenia swoich
    właściwości ODBC, zanim znów zadziała — zobacz
    [Tworzenie połączenia z bazą danych](#create-a-database-connection).

---

## Przewodniki dla technologii {: #technology-guides }

Nazwy właściwości różnią się w zależności od sterownika, a każda technologia ma jeden lub dwa
szczegóły, których nie mają pozostałe. Poniższe przewodniki obejmują tę część; ta strona
obejmuje stronę *digna*, która jest taka sama dla wszystkich.

!!! important "Zestawy właściwości w przewodnikach są przykładami"

    Każdy przewodnik pokazuje jedną kombinację, o której wiadomo, że działa — tę, względem
    której *digna* jest testowana. To punkt wyjścia, a nie specyfikacja: właściwości należą do
    sterownika ODBC, a to, które istnieją, jak się nazywają i jakie wartości przyjmują, różni się
    między wersjami i producentami sterowników, między systemami Windows, Linux i macOS oraz w
    zależności od konfiguracji serwera źródłowego — metody uwierzytelniania, TLS, bramy, portu.
    Licz się z dostosowaniem jednej czy dwóch wartości i traktuj dokumentację zainstalowanej
    wersji sterownika jako rozstrzygającą.

| Technologia | Przewodnik | Warto wiedzieć |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Pule bezserwerowe wymagają `-ondemand` w nazwie hosta i obsługują wyłącznie profilowanie *Standard* |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Uwierzytelnianie tokenem: `UID=token`, PAT w `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Katalogi pochodzą ze sterownika, a nie z zapytania |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Nazwa sterownika jest w nawiasach klamrowych: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` przyjmuje pełny deskryptor połączenia albo alias z `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` musi odpowiadać temu, czego wymaga serwer |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` decyduje, które schematy *digna* może zobaczyć |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programowy token dostępu to przetestowana ścieżka uwierzytelniania |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Host trafia do `DBCNAME`; bazy danych pełnią rolę schematów |

---

## Wymaganie wstępne: instalacja sterownika ODBC na hoście digna {: #install-the-driver }

*digna* otwiera połączenia źródłowe z **serwera, na którym działa backend digna**, a nie z
przeglądarki. Sterownik ODBC musi więc być zainstalowany na tej maszynie, a jego nazwa
zarejestrowana w lokalnym menedżerze sterowników.

=== "Windows"

    Zainstaluj 64-bitowy sterownik producenta, następnie otwórz **Administratora źródeł danych
    ODBC (64-bitowego)** i przejdź na zakładkę **Drivers**. Wymienione tam nazwy to dokładnie te
    wartości, których możesz użyć dla właściwości `Driver`.

=== "Linux"

    Zainstaluj **unixODBC** i sterownik producenta, a następnie wyświetl zarejestrowane nazwy
    sterowników:

    ```bash
    odbcinst -q -d
    ```

    Nazwy wypisane w nawiasach kwadratowych to wartości, których możesz użyć dla właściwości
    `Driver`. Pochodzą z pliku `/etc/odbcinst.ini` (lub z pliku, który wskazuje `odbcinst -j`).

=== "macOS"

    Zainstaluj **unixODBC** (na przykład poleceniem `brew install unixodbc`) i sterownik
    producenta, a następnie wyświetl zarejestrowane nazwy sterowników:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Nazwa sterownika musi zgadzać się co do znaku"

    `Driver` jest przekazywany menedżerowi sterowników bez zmian. `Simba Spark ODBC Driver` i
    `Simba Spark ODBC Driver 64` to dla menedżera sterowników różne sterowniki, a nazwa, która
    nie jest zarejestrowana, powoduje błąd *data source name not found*, mimo że żaden DSN nie
    jest tu używany.

Zamiast zarejestrowanej nazwy wszystkie popularne menedżery sterowników akceptują też pełną
ścieżkę do biblioteki sterownika, na przykład
`Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Przydaje się to, gdy sterownik jest
zainstalowany, ale niezarejestrowany.

---

## Tworzenie połączenia z bazą danych {: #create-a-database-connection }

Otwórz **Admin Panel**, przejdź na zakładkę **Database Connections** i kliknij
**Add DB Connection**. Ekran pyta o pięć rzeczy:

| Pole | Opis |
|---|---|
| **Name** | Nazwa połączenia. Służy do odwoływania się do połączenia na innych ekranach. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake lub Hive. Wybiera dialekt SQL, który generuje *digna*, musi więc odpowiadać źródłu — a nie sterownikowi. Azure Synapse Analytics to połączenie **SQL Server**. |
| **ODBC Properties** | Pary klucz/wartość opisane w [Właściwościach ODBC](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* lub *Session* — zobacz [Tryb profilowania i Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schemat zawierający tabele robocze dla profilowania *Permanent*. |

Połączeniem zarządza się centralnie, a następnie przypisuje się je do jednego lub kilku
projektów, więc to samo połączenie może obsługiwać wiele projektów.

---

## Właściwości ODBC {: #odbc-properties }

Kliknij **Add Property** dla każdej właściwości i wypełnij **Key**, **Value**, a dla sekretów —
pole wyboru **Encrypted**. Każdy przewodnik technologiczny wymienia przykładowy zestaw dla danej
technologii, który dostosowujesz do swojej wersji sterownika i serwera — zobacz
[uwagę powyżej](#technology-guides).

Niezależnie od sterownika zestaw właściwości obejmuje te same cztery rzeczy:

- **`Driver`** — zarejestrowaną nazwę sterownika, jak opisano [powyżej](#install-the-driver).
- **Adres serwera** — klucz różni się w zależności od sterownika: `SERVER`, `HOST`, `DBCNAME`,
  `Server` albo, w przypadku Oracle, deskryptor połączenia `DBQ`.
- **Poświadczenia** — zwykle `UID` i `PWD`; Snowflake używa `UID` oraz `token`, a Databricks
  dosłownego użytkownika `token` wraz z osobistym tokenem dostępu w `PWD`.
- **Bazę danych lub katalog, w którym się pracuje**, jeśli technologia je ma — zobacz
  [Którą bazę danych widzi połączenie](#which-database-the-connection-sees).

Wszystko inne, co dokumentuje sterownik, można dodać w ten sam sposób — pulę połączeń, limity
czasu gniazd, ustawienia Kerberosa, ustawienia serwera proxy. *digna* nie interpretuje
właściwości; jedynie je przekazuje.

!!! warning "Wartości nie są escapowane — ujmij w klamry wszystko ze średnikiem"

    Ponieważ właściwości są łączone znakiem `;`, wartość zawierająca sama w sobie `;`
    podzieliłaby ciąg połączenia w niewłaściwym miejscu. Ujmij takie wartości w nawiasy
    klamrowe: `PWD={p@ss;word}`. To samo dotyczy wartości ze znakiem `=` lub ze spacjami na
    początku. To również powód, dla którego niektóre sterowniki zapisuje się zwyczajowo w
    klamrach, jak `{NetezzaSQL}` czy `{SnowflakeDSIIDriver}`.

---

## Szyfrowanie wartości właściwości {: #encrypting-property-values }

Zaznacz **Encrypted** dla każdej właściwości, która zawiera sekret — `PWD`, `token`, klucz tajny
klienta. Wartość jest wtedy szyfrowana przed zapisaniem w repozytorium *digna*, maskowana na
ekranie i odszyfrowywana dopiero przy składaniu ciągu połączenia.

!!! tip "Wskazówka"

    Zaszyfrowanej wartości nie da się odczytać — ani w interfejsie, ani przez API — można ją
    jedynie zastąpić. Przechowuj sekrety także we własnym menedżerze haseł.

Właściwości, które nie są sekretami — nazwa sterownika, host, port, baza danych — najlepiej
zostawić niezaszyfrowane, aby pozostały czytelne dla osoby, która będzie później utrzymywać
połączenie.

---

## Testowanie połączenia {: #testing-a-connection }

Kliknij **Test** w oknie *Add DB Connection* **przed** zapisaniem. Test korzysta z wartości
aktualnie znajdujących się w formularzu i nawiązuje rzeczywiste połączenie, więc zgłasza
dokładnie to, na co natrafiłaby inspekcja — błędną nazwę sterownika, odrzucone hasło,
nieosiągalny host. Nic nie jest zapisywane: połączenie testowe jest wycofywane niezależnie od
tego, czy się powiedzie, czy nie.

W przypadku istniejącego już połączenia najedź na jego wiersz w zakładce
**Database Connections** i kliknij ikonę **wtyczki**, aby przetestować je ponownie. To najszybszy
sposób sprawdzenia, czy źródło jest osiągalne po rotacji hasła lub zmianie w zaporze.

---

## Którą bazę danych widzi połączenie {: #which-database-the-connection-sees }

Gdy dodajesz źródło danych, *digna* udostępnia katalogi, schematy i tabele, do których
połączenie może sięgnąć. Jak daleko sięga, zależy od technologii:

| Technologia | Udostępniane katalogi |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Wyłącznie **bieżąca** baza połączenia |
| **Teradata**, **Netezza**, **Databricks** | Wszystkie bazy lub katalogi, które użytkownik może zobaczyć |
| **Hive**, **Impala** | Zgłaszane przez sterownik |

!!! important "Jedno połączenie, jedna baza danych"

    W przypadku PostgreSQL, SQL Server, Oracle i Snowflake właściwości muszą wskazywać bazę
    zawierającą schematy źródłowe — `DATABASE=…`, `Database=…` albo nazwę usługi wewnątrz `DBQ`
    w Oracle. Tabele w innej bazie nie są osiągalne przez to połączenie; dodaj dla nich drugie
    połączenie.

---

## Tryb profilowania i Work Schema {: #profiling-mode-and-work-schema }

Tryb profilowania określa, jak *digna* przetwarza dane i oblicza metryki:

- **Standard:** metryki są obliczane bezpośrednio na tabelach źródłowych, bez kopiowania danych.
- **Permanent:** dane z inspekcjonowanego dnia są kopiowane do tabeli trwałej, a metryki
  obliczane są na skopiowanych danych.
- **Session:** dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki obliczane są na
  tych danych tymczasowych.

Tryb decyduje o tym, co musi być dozwolone użytkownikowi połączenia:

| Tryb | Zapisuje | Uprawnienia potrzebne użytkownikowi połączenia |
|---|---|---|
| **Standard** | nic | Odczyt tabel źródłowych |
| **Permanent** | jedną tabelę na źródło danych w **Work Schema** | Tworzenie i usuwanie tabel w **Work Schema** |
| **Session** | tabelę tymczasową, którą baza usuwa wraz z sesją | Tworzenie tabel tymczasowych — **Work Schema** nie jest używany |

*Standard* wyłącznie odczytuje, co czyni go trybem do wyboru, gdy *digna* otrzymuje dostęp tylko
do odczytu. **Work Schema** jest odczytywany jedynie przy *Permanent*, ale i tak warto go
wypełnić, aby połączenie działało dalej, jeśli tryb zostanie później zmieniony.

---

## Użycie DSN zamiast tego {: #using-a-dsn-instead }

DSN nadal działa — `DSN` to po prostu kolejna właściwość:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN musi być zarejestrowany na hoście *digna*, dla tego samego konta użytkownika, na którym
działa backend *digna*, oraz jako **System DSN**, gdy *digna* działa jako usługa. Wszystko, co
jest skonfigurowane w DSN, można nadpisać, dodając to również jako właściwość.

Tryb bez DSN jest udokumentowanym ustawieniem domyślnym, ponieważ pozwala uniknąć takiego stanu
po stronie hosta: połączenie jest w pełni opisane w *digna*, a nowy host *digna* potrzebuje
zainstalowanego sterownika, ale niczego skonfigurowanego.

---

## Rozwiązywanie problemów {: #troubleshooting }

### Nie znaleziono nazwy źródła danych / nie określono domyślnego sterownika

**Objawy:**
- Przycisk **Test** zgłasza błąd wspominający *data source name not found*, mimo że konfiguracja
  jest bez DSN

**Przyczyny i rozwiązania:**
1. Wartość `Driver` nie odpowiada żadnej zarejestrowanej nazwie sterownika — porównaj ją z
   zakładką **Drivers** *Administratora źródeł danych ODBC (64-bitowego)* albo z
   `odbcinst -q -d`
2. Sterownik jest zainstalowany na Twojej stacji roboczej, ale nie na hoście *digna*
3. Sterownik jest 32-bitowy, podczas gdy *digna* jest 64-bitowa — zainstaluj sterownik
   64-bitowy
4. Właściwości `Driver` w ogóle brakuje, a `DSN` również nie podano
5. W systemach Linux i macOS sterownik jest zainstalowany, ale niezarejestrowany — podaj zamiast
   tego pełną ścieżkę do biblioteki sterownika albo zarejestruj go w `odbcinst.ini`

---

### Test połączenia przekracza limit czasu

**Objawy:**
- **Test** zawiesza się, a następnie kończy się niepowodzeniem po mniej więcej pół minuty

**Przyczyny i rozwiązania:**
1. Host lub port nieosiągalne z hosta *digna* — sprawdź zaporę, a w przypadku źródeł chmurowych
   listę dozwolonych adresów IP
2. Nazwa hosta jest poprawna, ale port należy do innej usługi
3. Źródło potrzebuje więcej niż domyślne 30 sekund, aby przyjąć połączenie — zwiększ
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` w sekcji `[base]` pliku `config.toml` (`0` oznacza
   oczekiwanie bez ograniczeń) i uruchom ponownie backend
4. Bezserwerowy punkt końcowy wybudza się ze stanu bezczynności — ponów próbę, a jeśli zdarza
   się to regularnie, zwiększ limit czasu logowania jak wyżej

---

### Uwierzytelnianie zawodzi, choć poświadczenia są poprawne

**Objawy:**
- Sterownik zgłasza nieprawidłowe poświadczenia, ale ten sam użytkownik działa w innym kliencie
  SQL

**Przyczyny i rozwiązania:**
1. Hasło zawiera `;` — ujmij wartość w nawiasy klamrowe: `{p@ss;word}`
2. Do wartości skopiowano końcową spację
3. Sterownik oczekuje określonego mechanizmu uwierzytelniania — na przykład `AuthMech` w
   sterownikach Hive i Databricks albo `authenticator` w Snowflake
4. Wartość została zapisana jako zaszyfrowana, a następnie edytowana — zaszyfrowanych wartości
   nie można odczytać, więc wprowadź sekret ponownie w całości
5. Token wygasł — osobiste tokeny dostępu i programowe tokeny dostępu są wydawane z datą
   wygaśnięcia

---

### Ekran źródła danych nie udostępnia oczekiwanej bazy lub schematu

**Objawy:**
- Przy dodawaniu źródła danych brakuje katalogów, schematów lub tabel

**Przyczyny i rozwiązania:**
1. Połączenie wskazuje inną bazę danych — zobacz
   [Którą bazę danych widzi połączenie](#which-database-the-connection-sees)
2. Użytkownikowi połączenia brakuje uprawnień odczytu do schematu albo do słownika danych
3. **Technology** nie odpowiada źródłu, więc *digna* odpytuje niewłaściwy słownik danych
4. W przypadku Snowflake użytkownik nie ma przypisanego domyślnego magazynu i nie podano
   właściwości `Warehouse`, więc zapytania o metadane nie mogą się wykonać

---

### Profilowanie zawodzi, choć test połączenia się powiódł

**Objawy:**
- **Test** przechodzi, ale inspekcja kończy się niepowodzeniem przy tworzeniu tabel roboczych

**Przyczyny i rozwiązania:**
1. Wybrano profilowanie *Permanent*, a użytkownik połączenia nie może tworzyć tabel w
   **Work Schema** — nadaj uprawnienia albo przełącz się na *Session* lub *Standard*
2. **Work Schema** jest puste albo wskazuje nieistniejący schemat, podczas gdy wybrano
   profilowanie *Permanent*
3. Wybrano profilowanie *Session*, a użytkownik połączenia nie może tworzyć tabel tymczasowych
4. Długo działające zapytanie profilujące osiąga limit czasu zapytania — zwiększ
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` w sekcji `[base]` pliku `config.toml` (domyślnie 3600
   sekund, `0` wyłącza limit)

---

## Dobre praktyki

**RÓB TAK:**

- Zainstaluj i zarejestruj sterownik na hoście *digna*, zanim skonfigurujesz połączenie
- Zaznaczaj **Encrypted** dla każdego hasła i każdego tokenu
- Klikaj **Test** przed zapisaniem i testuj ponownie po rotacji hasła
- Nazywaj połączenia według źródła i środowiska, na przykład `sales_dwh_prod`
- Daj *digna* dedykowanego użytkownika bazy danych, tylko do odczytu tam, gdzie wystarcza
  profilowanie *Standard*
- Utrzymuj jedno połączenie na każdą źródłową bazę danych i dodawaj drugie zamiast przestawiać
  pierwsze

**NIE RÓB TAK:**

- Nie przechowuj sekretów bez szyfrowania i nie współdziel jednego użytkownika bazy danych
  między *digna* a innymi narzędziami
- Nie używaj sterownika 32-bitowego z 64-bitową instalacją *digna*
- Nie polegaj na DSN użytkownika, gdy *digna* działa jako usługa — nie będzie widoczny
- Nie umieszczaj we właściwości wartości zawierającej `;` bez nawiasów klamrowych
- Nie kieruj **Work Schema** na schemat zawierający dane źródłowe

---

## Wsparcie

Potrzebujesz pomocy przy połączeniu z bazą danych?

- **E-mail:** support@digna.ai
- **Dokumentacja:** https://docs.digna.ai
- **Strona internetowa:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
