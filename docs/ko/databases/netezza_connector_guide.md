---
title: Netezza 커넥터 – 데이터베이스 통합 | digna 문서
description: DSN 없는 연결 문자열을 사용해 ODBC로 Netezza에 연결하도록 digna를 구성합니다. NetezzaSQL 드라이버, 필수 ODBC 속성 및 digna 측 연결 설정을 다룹니다.
image: /assets/logo_square.png
---


# Netezza용 소스 커넥터

이 가이드는 **DSN 없는(DSN-less)** 연결 문자열을 사용하여 **ODBC**로 Netezza에 연결하도록
*digna*를 구성하는 방법을 설명합니다.

설정 중 *digna* 측 부분은 모든 기술에서 동일합니다. 연결을 만드는 위치, 속성 값을 암호화하는 방법,
연결을 테스트하는 방법, 프로파일링 모드의 의미가 여기에 해당하며
[데이터베이스 연결 개요](overview.md)에 설명되어 있습니다. 이 페이지에서는 Netezza에만 해당하는
내용을 다룹니다.

---

## 1. ODBC 드라이버 설치 {: #1-install-the-odbc-driver }

공급업체의 공식 설치 가이드에 따라 *digna* 백엔드가 실행되는 머신에 **NetezzaSQL** ODBC
드라이버(IBM Netezza 클라이언트 도구에 포함)를 설치합니다.

[digna 호스트에 ODBC 드라이버 설치](overview.md#install-the-driver)에 설명된 대로 호스트에서
등록된 정확한 드라이버 이름을 확인합니다.

---

## 2. ODBC 속성 {: #2-odbc-properties }

!!! important "사양이 아닌 예시"

    아래 속성 세트는 정상 동작이 확인된 조합 중 하나입니다. 이 속성들은 NetezzaSQL 드라이버에
    속하므로 이름, 기본값, 허용되는 값이 클라이언트 버전과 플랫폼마다 다르며, TLS로 보호되는
    어플라이언스에는 여기에 나온 것보다 많은 속성이 필요합니다. 이를 출발점으로 삼고, 설치한
    클라이언트 버전의 문서를 확인하세요.

**Add DB Connection** 화면에서 다음 속성을 추가합니다:

| 키 | 예시 값 | 참고 |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | *digna* 호스트에 등록된 드라이버 이름과 일치해야 합니다. 이 이름은 보통 중괄호로 감싸서 씁니다 |
| `SERVER` | `netezza.example.com` | 서버 이름 또는 IP 주소 |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | 세션이 시작되는 데이터베이스 |
| `UID` | `ADMIN` | 데이터베이스 사용자 |
| `PWD` | `<password>` | **Encrypted**를 선택합니다 |

결과 연결 문자열은 다음과 같습니다:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

드라이버 버전, 설정 및 보안 요구 사항에 따라 추가 속성이 필요할 수 있습니다. 예를 들어 TLS로
보호되는 어플라이언스에는 `SecurityLevel`과 `CaCertFile`이 필요합니다. 드라이버의 *Advanced*,
*SSL*, *Driver* 대화 상자에서 제공하는 모든 옵션은 속성으로 추가할 수 있습니다.

---

## 3. *digna* 구성 {: #3-digna-configuration }

**Add DB Connection** 화면에서 다음을 입력합니다:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Netezza 관련 참고 사항 {: #4-notes-on-netezza }

- **카탈로그와 스키마가 모두 적용됩니다.** *digna*는 사용자가 볼 수 있는 데이터베이스(`_V_DATABASE`
  기준)를 카탈로그로, 그 스키마(`_V_SCHEMA` 기준)를 하위 항목으로 나열하므로, 하나의 연결로 여러
  데이터베이스의 소스를 처리할 수 있습니다. `DATABASE`는 세션이 시작되는 위치만 결정합니다.
- **식별자는 대문자입니다.** 따옴표로 묶어 생성하지 않은 한 식별자는 대문자이며, 그래서 위의 예시에서
  `TEST`와 `ADMIN`을 사용합니다.
- **프로파일링 모드.** *Permanent*는 **Work Schema**에 작업 테이블을 만들므로 사용자에게 그곳에
  대한 `CREATE TABLE` 권한이 필요합니다. *Session*은 `CREATE TEMPORARY TABLE`을 사용하며
  **Work Schema**를 건드리지 않습니다. *Standard*는 읽기 권한만 필요합니다.

---

## 5. 드라이버 확인(선택 사항) {: #5-verifying-the-driver-optional }

DSN 없는 연결에는 ODBC 데이터 소스를 구성할 필요가 없지만, 드라이버 자체의 대화 상자를 사용하면
*digna*에 값을 입력하기 전에 드라이버와 자격 증명이 동작하는지 간편하게 확인할 수 있습니다.

#### 1단계
![Step 1](images/netezza/create_odbc_data_source_step1.png)

**DSN Options**의 필드는 [섹션 2](#2-odbc-properties)의 속성과 일대일로 대응합니다.
Netezza 드라이버, 설정 및 보안 요구 사항에 따라 **Advanced DSN Options**, **SSL DSN Options**
또는 **Driver Options** 탭에도 값을 입력해야 할 수 있습니다. 가장 간단한 설정에서는
**DSN Options**만으로 충분합니다.

**Test Connection** 버튼을 클릭합니다.

#### 2단계
![Step 2](images/netezza/create_odbc_data_source_step2.png)

성공 화면이 표시되면 드라이버가 동작하고 값이 올바른 것입니다.
