---
title: Netezza 커넥터 – 데이터베이스 통합 | digna 문서
description: NetezzaSQL ODBC 드라이버를 사용하여 digna가 Netezza에 연결하도록 구성하는 방법입니다. DSN 기반 또는 DSN-less 설정을 통한 비밀번호 기반 인증을 지원하여 유연한 연결을 제공합니다.
image: /assets/logo_square.png
---


# Netezza용 소스 커넥터

이 가이드는 ODBC 드라이버를 사용해 *digna*를 Netezza에 연결하도록 구성하는 방법을 설명합니다.

이 문서는 **"Create a Database Connection"** 화면을 참조합니다.

![데이터베이스 연결 생성](images/data_source_config_input_mask.png)

---

## ODBC 드라이버

ODBC 드라이버는 다양한 인증 및 연결 옵션을 지원할 수 있습니다. 이 섹션에서는 드라이버 **NetezzaSQL**을 사용한 비밀번호 기반 인증에 중점을 둡니다.

### 1. ODBC 드라이버 설치

공급업체의 공식 설치 가이드를 따라 **NetezzaSQL**(또는 이와 유사한) 드라이버를 설치합니다.

### 2. ODBC 데이터 소스 구성

비밀번호 기반 인증을 사용하여 새 ODBC 데이터 소스를 구성하려면 다음 단계를 따르세요:

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

사용 중인 Netezza 드라이버와 설정 및 보안 요구사항에 따라 **Advanced DSN Options**, **SSL DSN Options** 또는 **Driver Options** 탭에도 정보를 입력해야 할 수 있습니다. 가장 간단한 설정의 경우 **DSN Options**에만 정보를 입력하는 것으로 충분합니다.

**Test Connection** 버튼을 클릭하세요.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

성공 화면이 표시되면 ODBC가 제대로 구성된 것입니다.

---

이제 **DSN (Data Source Name)** 기반 또는 **DSN-less** 설정 중 하나를 사용하여 *digna*에서 ODBC 연결을 구성할 수 있습니다.

---

### A. DSN 기반 구성

#### *digna* 구성

**"Create a Database Connection"** 화면에서 다음 항목을 입력하세요:

```
Technology:      Netezza
Database Name:   소스 스키마를 포함한 데이터베이스
Schema Name:     소스 데이터를 포함한 스키마
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "데이터베이스 사용자"
name: "PWD",        value: "데이터베이스 비밀번호"
```

> `DSN`은 ODBC 드라이버 구성에서 정의한 이름과 일치해야 합니다.

---

### B. DSN-less 구성

#### *digna* 구성

**"Create a Database Connection"** 화면에서 다음 항목을 입력하세요:

```
Technology:      Netezza
Database Name:   소스 데이터를 포함한 스키마 (Schema Name과 동일)
Schema Name:     소스 데이터를 포함한 스키마
Use ODBC:        Enabled
```

#### ODBC 속성

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "서버 이름 또는 IP 주소"
name: "PORT",       value: "포트 번호 (예: 5480)"
name: "DATABASE",   value: "소스 데이터 스키마를 포함한 데이터베이스 이름"
name: "UID",        value: "데이터베이스 사용자"
name: "PWD",        value: "데이터베이스 비밀번호"
```