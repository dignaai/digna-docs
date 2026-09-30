# Bronconnector voor Hive

Deze gids beschrijft hoe je *digna* configureert om via **ODBC** verbinding te maken met Apache
Hive, met een **DSN-loze** connection string.

De *digna*-kant van de configuratie is voor elke technologie hetzelfde — waar verbindingen worden
aangemaakt, hoe property-waarden worden versleuteld, hoe een verbinding wordt getest en wat de
profiling modes betekenen. Dat wordt beschreven in het
[Overzicht databaseverbindingen](overview.md). Deze pagina behandelt wat specifiek is voor Hive.

---

## 1. Installeer de ODBC-driver {: #1-install-the-odbc-driver }

Installeer de **Cloudera ODBC Driver for Apache Hive** op de machine waarop de *digna*-backend
draait, volgens de officiële installatiegids van de leverancier.

Lees de exacte geregistreerde drivernaam op je host af zoals beschreven in
[Installeer de ODBC-driver op de digna-host](overview.md#install-the-driver).

---

## 2. ODBC-properties {: #2-odbc-properties }

!!! important "Een voorbeeld, geen specificatie"

    De onderstaande set is één combinatie waarvan bekend is dat ze werkt. De properties horen bij
    de Cloudera Hive-driver, dus hun namen, standaardwaarden en toegestane waarden verschillen per
    driverversie en platform, en wat HiveServer2 accepteert, hangt volledig af van hoe het cluster
    is beveiligd — authenticatiemechanisme, transportmodus, TLS, gateway. Gebruik dit als
    startpunt en raadpleeg de documentatie van de geïnstalleerde driverversie.

Voeg de volgende properties toe in het scherm **Add DB Connection**:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Moet overeenkomen met de drivernaam die op de *digna*-host is geregistreerd |
| `HOST` | `hive.example.com` | Hostnaam of IP-adres van HiveServer2 |
| `PORT` | `10000` | Poort van HiveServer2; `10001` voor HTTP-transport |

De resulterende connection string ziet er zo uit:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Authenticatie

Een onbeveiligde HiveServer2 accepteert de drie bovenstaande properties zoals ze zijn. Als
authenticatie is ingeschakeld, voeg je toe:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `AuthMech` | `3` | `0` geen authenticatie, `2` alleen gebruikersnaam, `3` gebruikersnaam en wachtwoord, `1` Kerberos |
| `UID` | `digna_source_user` | Vereist voor `AuthMech` `2` en `3` |
| `PWD` | `<password>` | Vereist voor `AuthMech` `3`. Vink **Encrypted** aan |

Voor Kerberos (`AuthMech=1`) heeft de *digna*-host daarnaast een geldig ticket of een keytab
nodig, plus de properties `KrbHostFQDN`, `KrbServiceName` en `KrbRealm` die de driver
documenteert.

### Transport en TLS

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `ThriftTransport` | `2` | `0` binair (de standaard, poort 10000), `1` SASL, `2` HTTP (poort 10001, en wat een Knox-gateway verwacht) |
| `HTTPPath` | `cliservice` | Bij `ThriftTransport=2` |
| `SSL` | `1` | Als HiveServer2 met TLS is beveiligd |
| `Schema` | `dignadata` | Hive-database waarin de sessie start. Optioneel — *digna* kwalificeert zijn queries |

---

## 3. *digna*-configuratie {: #3-digna-configuration }

Geef in het scherm **Add DB Connection** het volgende op:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Opmerkingen over Hive {: #4-notes-on-hive }

- **Catalogs komen van de driver.** Hive heeft zelf geen catalog, dus *digna* neemt wat de driver
  meldt — normaal één item met de naam `HIVE` — en toont de Hive-databases daaronder als schema's.
- **Work Schema is een Hive-database.** Voor *Permanent* profiling heeft de gebruiker het recht
  nodig om er tabellen in aan te maken en te verwijderen, en moet de onderliggende opslaglocatie
  beschrijfbaar zijn.
- **Profiling modes.** *Permanent* maakt de werktabellen aan in **Work Schema**. *Session*
  gebruikt `CREATE TEMPORARY TABLE`, waarvoor een HiveServer2 nodig is die tijdelijke tabellen
  ondersteunt, en raakt **Work Schema** niet aan. *Standard* heeft alleen leesrechten nodig en is
  de aangewezen mode op een cluster waar *digna* helemaal geen schrijfrechten heeft.
- **Profiling is een reeks queries, geen scan.** Elke statistiek wordt door HiveServer2 berekend,
  dus de queue waarin de gebruiker van *digna* queries indient, moet genoeg capaciteit hebben voor
  het inspectievenster.

---

## 5. De driver controleren (optioneel) {: #5-verifying-the-driver-optional }

Voor een DSN-loze verbinding hoef je geen ODBC-databron te configureren, maar het eigen
dialoogvenster van de driver is een handige manier om te bevestigen dat de driver, de
transportmodus en je inloggegevens werken, voordat je ze in *digna* invoert.

#### Stap 1
![Stap 1](images/hive/create_odbc_data_source_step1.png)

De velden **Host**, **Port**, **Database**, **Mechanism** en **Thrift Transport** hier zijn de
properties `HOST`, `PORT`, `Schema`, `AuthMech` en `ThriftTransport` in
[sectie 2](#2-odbc-properties).

#### Stap 2 – Test de verbinding

Geef het wachtwoord op en klik op de knop **Test**.

![Stap 2](images/hive/create_odbc_data_source_step2.png)

Klik na een geslaagde test op de knop **OK**.