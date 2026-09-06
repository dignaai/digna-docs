# digna CLI 참조 2026.06
**2026-09-05**

이 페이지는 ***digna*** CLI 릴리스 **2026.06**에서 사용할 수 있는 전체 명령을 사용 예시와 옵션과 함께 설명합니다.

실행 파일의 이름은 `digna`입니다.

---

## CLI 기본 사항

---

### 개요 및 구문

릴리스 **2026.06**의 CLI는 범주 기반의 구조화된 명령 계층을 사용합니다.

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version`과 `serve`는 하위 명령이 없는 단일 명령입니다.

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### 전역 옵션

다음 전역 옵션은 모든 명령에 적용됩니다.

- `--help`, `-h`: CLI 전체 또는 특정 명령 범주나 하위 명령에 대한 도움말 정보를 표시합니다.
- `--stacktrace`: 실패 시 최상위 메시지만이 아니라 전체 오류 체인을 표시합니다.

`--stacktrace`는 엄밀한 의미의 전역 옵션입니다. 명령 범주 **앞에** 지정해야 하며, 뒤에 둘 수 없습니다.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

`--version` 플래그는 없습니다. 대신 [`version`](#version) 명령을 사용하십시오.

### 전제 조건

대부분의 명령은 읽을 수 있고 유효한 `config.toml`이 필요하며, 일부는 추가로 유효한 라이선스를 요구합니다.
다음 표는 각 명령 범주가 어떤 작업을 하기 전에 무엇을 로드하는지 기록한 것입니다.

| 명령 범주 | `config.toml` 필요 | 유효한 라이선스 필요 |
|---|---|---|
| `version` | 아니요 | 아니요 |
| `config check` | 아니요(명령이 보고하는 대상 자체입니다) | 아니요 |
| `license check` | 아니요 | 그것 *자체가* 검사입니다 |
| `crypt` | 예 | 아니요 |
| `serve` | 예 | 아니요 |
| `project` | 예 | 아니요 |
| `user` | 예 | 예 |
| `inspection` | 예 | 예 |
| `repo` | 예 | 예 |

라이선스가 필요한 경우 서명과 만료일이 모두 검사되며, 둘 중 하나라도 실패하면 명령은 저장소에 접근하기 전에 중단됩니다.

### 종료 코드

- `0`: 명령이 성공했습니다.
- `1`: 명령이 실패했습니다. 오류 메시지는 `Error: ` 접두사와 함께 stderr에 기록됩니다.

### help

`--help` 옵션은 사용 가능한 명령 범주, 하위 명령, 옵션에 대한 정보를 제공합니다.

1. **일반 도움말 표시:**
   ```bash
   digna --help
   ```

2. **특정 범주 및 명령에 대한 도움말 확인:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **출력에 포함되는 내용:**
   - **명령 설명:** 명령의 목적 요약.
   - **구문:** 필수 및 선택 인수.
   - **옵션:** 해당 명령 고유의 플래그와 매개변수.

### version

`version` 명령은 설치된 ***digna*** 릴리스를 출력합니다. 어떤 구성도 읽지 않고 라이선스도 검증하지 않으므로, `config.toml`이나 라이선스가 없거나 유효하지 않은 설치에서도 동작합니다.

릴리스 버전은 [`repo check`](#repo-check)가 보고하는 저장소 스키마 버전과 별개입니다.

#### 명령 사용법
```bash
digna version
```

#### 출력 예시
```text
2026.06
```

---

## 구성 관리

---

### config check

`config check` 명령은 구성 파일(`config.toml`)을 검증하여 모든 필수 섹션과 설정이 존재하고 올바른 형식인지 확인합니다. 각 섹션은 개별적으로 검증되므로 손상된 `[app]` 섹션이 `[repo]`의 상태를 가리지 않습니다.

보고되는 섹션은 다음과 같습니다.

- `App config`(`[app]`)
- `Repository config`(`[repo]`)
- `Base config`(`[base]`)
- `Logging config`(`[logging]`)
- `Encryption config`(`[encryption]`)
- `OIDC config(s)`(`oidc_clients`) — 선택 사항이며, 키가 없으면 통과하고 존재하지만 형식이 잘못된 목록은 실패합니다

이 명령은 다른 명령과 달리 애플리케이션 구성을 의도적으로 로드하지 않습니다. 그렇기 때문에 ***digna***가 아예 시작되지 못하게 만드는 `config.toml`도 진단할 수 있습니다.

#### 명령 사용법
```bash
digna config check [OPTIONS]
```

#### 옵션
- `--configpath`, `-c`: 구성 파일 경로 또는 `config.toml`이 들어 있는 디렉터리 경로(기본값 `./config.toml`).
- `--json`: 검증 보고서를 JSON으로 출력합니다. `--quiet`보다 우선합니다.
- `--quiet`, `-q`: 보고서를 표시하지 않고 종료 코드에만 의존합니다.

#### 예시
```bash
digna config check
```

특정 구성 파일을 검증하고 출력을 JSON 형식으로 지정:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### 출력 예시
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

파일이 없거나 TOML 구문 오류가 있으면 섹션별로 검증할 대상이 남지 않으므로, `--quiet`나 `--json` 지정과 무관하게 보고서가 아닌 단일 오류로 보고됩니다.

---

## 저장소 관리

---

### repo check

`repo check` 명령은 데이터베이스 연결을 테스트하고 저장소의 설치 상태와 버전을 확인합니다. 구성된 스키마가 존재하지 않거나, 존재하더라도 ***digna*** 저장소가 들어 있지 않으면 실패합니다.

보고되는 버전은 저장소 스키마의 버전이며, 이는 [`version`](#version)이 출력하는 ***digna*** 릴리스와 별도로 관리됩니다.

#### 명령 사용법
```bash
digna repo check
```

#### 출력 예시
```text
Repo version 3.0.0 installed
```

### repo install

`repo install` 명령은 `config.toml`에 구성된 스키마에 새로운 ***digna*** 저장소를 설치하며, 필요한 모든 시퀀스, 테이블, 인덱스, 제약 조건, 초기 레코드를 생성합니다.

스키마 자체는 이 명령으로 생성되지 **않습니다** — 미리 존재해야 합니다. 또한 해당 스키마에 이미 저장소가 설치되어 있으면 명령은 실행을 거부하며, 설치된 버전이 더 낮은 경우 [`repo upgrade`](#repo-upgrade)를 안내합니다.

#### 명령 사용법
```bash
digna repo install
```

#### 출력 예시
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

`repo upgrade` 명령은 데이터베이스 스키마 마이그레이션을 적용하여 기존 저장소를 설치된 릴리스가 요구하는 버전으로 끌어올립니다. 업그레이드는 정해진 업그레이드 경로를 따라 한 번에 한 버전씩 적용되며, 완료된 각 단계는 저장소에 기록됩니다.

저장소가 이미 요구 버전이라면, 명령은 업그레이드가 필요 없다고 보고하고 아무것도 변경하지 않습니다.

#### 명령 사용법
```bash
digna repo upgrade
```

#### 출력 예시
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## 암호화 관리

---

### crypt gen-key

`crypt gen-key` 명령은 `config.toml`의 암호화 키로 사용할 새 AES-GCM 암호화 키를 생성합니다. 생성되는 키가 `config.toml`에 의존하지는 않지만, 로드 가능한 `config.toml`이 이미 존재해야 합니다.

#### 명령 사용법
```bash
digna crypt gen-key
```

#### 출력 예시
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

`crypt encrypt` 명령은 `config.toml`에 구성된 AES-GCM 키로 문자열(예: 데이터베이스 비밀번호)을 암호화하고 암호문을 출력합니다.

#### 명령 사용법
```bash
digna crypt encrypt <VALUE>
```

#### 인수
- **VALUE**: 암호화할 평문 문자열(필수).

#### 예시
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

`crypt decrypt` 명령은 `config.toml`에 구성된 키로 AES-GCM으로 암호화된 문자열을 복호화하고 평문을 출력합니다.

#### 명령 사용법
```bash
digna crypt decrypt <VALUE>
```

#### 인수
- **VALUE**: 복호화할 암호문 문자열(필수).

#### 예시
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## 사용자 관리

---

### user add

`user add` 명령은 ***digna*** 저장소에 새 사용자 계정을 만듭니다. 지정한 이메일 주소를 가진 사용자가 이미 있으면 명령은 실패합니다.

#### 명령 사용법
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### 인수
- **EMAIL**: 사용자의 이메일 주소(필수).
- **PASSWORD**: 사용자의 초기 비밀번호(필수).
- **DISPLAY_NAME**: 사용자의 전체 표시 이름(필수).

#### 옵션
- `--admin`, `-a`: 관리자(슈퍼유저) 권한으로 사용자를 만듭니다.

#### 예시
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

관리자 계정을 만들려면:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### 출력 예시
```text
User created with ID: 42
```

### user list

`user list` 명령은 등록된 모든 사용자를 ID, 이메일, 표시 이름, 관리자 플래그와 함께 표 형식으로 나열합니다.

#### 명령 사용법
```bash
digna user list
```

#### 출력 예시
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

`user modify` 명령은 이메일 주소로 식별되는 기존 사용자 계정의 표시 이름과 관리자 권한을 갱신합니다.

표시 이름과 관리자 플래그는 항상 함께 기록됩니다. `--admin`은 값이 아니라 스위치입니다. **생략하면 관리자 권한이 회수되므로**, 사용자가 권한을 유지하거나 새로 받아야 할 때는 반드시 지정하십시오.

#### 명령 사용법
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### 인수
- **EMAIL**: 수정할 사용자의 이메일(필수).
- **DISPLAY_NAME**: 갱신된 표시 이름(필수).

#### 옵션
- `--admin`, `-a`: 관리자 권한을 부여합니다. 회수하려면 생략하십시오.
- `--valid-until`, `-v`: 호환성을 위해 허용되지만 **현재 적용되지 않습니다**. 지정하면 경고가 출력되고 아무것도 변경되지 않습니다.

#### 예시
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### 출력 예시
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

`user modify-pwd` 명령은 기존 사용자 계정의 비밀번호를 갱신합니다.

#### 명령 사용법
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### 인수
- **EMAIL**: 비밀번호를 갱신할 사용자의 이메일(필수).
- **PASSWORD**: 새 비밀번호(필수).

#### 예시
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

`user delete` 명령은 시스템에서 사용자 계정을 제거합니다.

#### 명령 사용법
```bash
digna user delete <EMAIL>
```

#### 인수
- **EMAIL**: 삭제할 사용자의 이메일(필수).

#### 예시
```bash
digna user delete jdoe@example.com
```

---

## 프로젝트 및 데이터 소스 관리

---

### project list

`project list` 명령은 저장소에서 사용할 수 있는 모든 프로젝트를 ID, 이름, 설명과 함께 나열합니다.

#### 명령 사용법
```bash
digna project list
```

#### 출력 예시
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

`project list-ds` 명령은 지정한 프로젝트에 연결된 모든 데이터 소스를 ID, 이름, 종류, 스키마, 테이블 이름과 함께 나열합니다.

#### 명령 사용법
```bash
digna project list-ds <PROJECT_NAME>
```

#### 인수
- **PROJECT_NAME**: 데이터 소스를 나열할 프로젝트의 이름(필수). 이름은 정확히 일치해야 합니다.

#### 예시
```bash
digna project list-ds ProjectA
```

#### 출력 예시
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

`project export-ds` 명령은 프로젝트의 데이터 소스를 JSON 문서로 내보냅니다.

`--table-name`과 `--table-id`를 모두 지정하지 않으면 프로젝트의 모든 데이터 소스를 내보냅니다.

#### 명령 사용법
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### 인수
- **PROJECT_NAME**: 데이터 소스를 내보낼 프로젝트의 이름(필수).

#### 옵션
- `--table-name`, `-n`: 내보낼 데이터 소스의 이름. 공백으로 구분하여 여러 이름을 지정할 수 있습니다.
- `--table-id`, `-i`: 내보낼 데이터 소스의 ID. 공백으로 구분하여 여러 ID를 지정할 수 있습니다.
- `--exportfile`, `-f`: 내보낸 데이터 소스를 저장할 경로(기본값: `data_sources_export.json`).

#### 예시
`ProjectA`의 모든 데이터 소스를 내보내려면:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

특정 테이블을 내보내려면:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### 출력 예시
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

`project import-ds` 명령은 내보내기 파일에서 대상 프로젝트로 데이터 소스를 가져오고, 객체별로 생성·갱신·건너뜀 여부를 보고합니다.

#### 명령 사용법
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### 인수
- **PROJECT_NAME**: 가져올 대상 프로젝트 이름(필수).
- **EXPORT_FILE**: JSON 내보내기 파일 경로(필수).

#### 옵션
- `--output-file`, `-o`: 가져오기 보고서를 기록할 파일. 지정하지 않으면 보고서는 stdout으로 출력됩니다.
- `--output-format`, `-f`: 가져오기 보고서의 형식 — `table`, `json`, `csv`(기본값: `table`).

#### 예시
```bash
digna project import-ds ProjectB my_export.json
```

기계가 읽을 수 있는 보고서를 얻으려면:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

보고서는 네 가지 객체 수준 — 데이터 소스, 데이터 세트 정의, 속성, 검증 규칙 — 을 다루며, 각각에 대해 가져오기 작업, 결과, 생성된 객체 ID, 추가 정보를 포함합니다.

### project plan-import-ds

`project plan-import-ds` 명령은 대상 프로젝트로의 데이터 소스 가져오기를 미리 보여 주며, 어떤 객체가 생성·갱신·건너뜀 처리될지를 아무것도 변경하지 않고 표시합니다. [`project import-ds`](#project-import-ds)와 동일한 내보내기 파일 및 동일한 보고 옵션을 받아들이며, 계획된 각 객체에 단계 번호를 추가합니다.

#### 명령 사용법
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### 인수
- **PROJECT_NAME**: 대상 프로젝트 이름(필수).
- **EXPORT_FILE**: 내보내기 파일 경로(필수).

#### 옵션
- `--output-file`, `-o`: 가져오기 계획을 기록할 파일. 지정하지 않으면 계획은 stdout으로 출력됩니다.
- `--output-format`, `-f`: 가져오기 계획의 형식 — `table`, `json`, `csv`(기본값: `table`).

#### 예시
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## 검사 관리

---

### inspection run

`inspection run` 명령은 프로젝트와 날짜 범위에 대한 검사 요청을 생성한 다음, 지정된 옵션에 따라 완료를 기다리거나, 즉시 반환하거나, 자체 프로세스에서 실행합니다.

세 가지 실행 모드는 다음과 같습니다.

- **기본값(플래그 없음)**: 요청이 백엔드용 큐에 등록되고, CLI가 2초마다 상태를 조회하면서 작업 진행 상황을 출력하다가 검사가 최종 상태에 도달하면 종료됩니다. 실행 중인 `digna serve`가 필요하며, 그렇지 않으면 요청을 가져가는 주체가 없습니다.
- **`--async-mode`**: 요청이 큐에 등록되고 해당 ID가 즉시 출력됩니다. 추적하려면 [`inspection status`](#inspection-status)를 사용하십시오.
- **`--bypass-backend`**: 검사가 CLI 프로세스 자체에서 실행되며 큐에 등록되지 않으므로 실행 중인 서버가 필요하지 않습니다.

`--async-mode`와 `--bypass-backend`는 함께 사용할 수 없습니다.

모든 모드에서 검사가 성공적으로 완료되지 않으면 명령은 0이 아닌 종료 코드로 끝납니다.

#### 명령 사용법
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### 인수
- **PROJECT_NAME**: 대상 프로젝트 이름(필수). 이름은 정확히 일치해야 합니다.
- **START_DATE**: 날짜 범위의 시작일. 형식은 `YYYY-MM-DD`(필수).
- **END_DATE**: 날짜 범위의 종료일. 형식은 `YYYY-MM-DD`(필수).

#### 옵션
- `--table-name`: 검사를 프로젝트의 단일 데이터 소스로 제한하며, 데이터 소스 이름으로 지정합니다. 지정하지 않으면 프로젝트의 모든 데이터 소스를 검사합니다.
- `--async-mode`: 검사를 큐에 등록하고 완료를 기다리는 대신 요청 ID를 출력합니다. `--bypass-backend`와 함께 사용할 수 없습니다.
- `--bypass-backend`: 백엔드용 큐에 등록하는 대신 CLI 프로세스에서 직접 검사를 실행합니다. `--async-mode`와 함께 사용할 수 없습니다.

#### 예시
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

비동기 검사를 제출하려면:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

단일 데이터 소스를 검사하려면:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### 출력 예시
기본 모드:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

비동기 모드:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

`inspection status` 명령은 요청 ID로 검사 요청의 상태와 작업 진행 상황을 조회합니다.

#### 명령 사용법
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### 인수
- **INSPECTION_REQUEST_ID**: 검사 요청의 숫자 ID(필수).

#### 예시
```bash
digna inspection status 1024
```

#### 출력 예시
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

`inspection abort` 명령은 실행 중이거나 대기 중인 검사 요청의 취소를 요청합니다. 영향을 받는 각 요청에 대해 중지 이벤트를 기록하며, 이에 따라 백엔드가 동작하므로 중단은 즉시 종료가 아니라 중지 요청입니다.

#### 명령 사용법
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### 인수
- **INSPECTION_REQUEST_ID**: 중단할 검사 요청의 ID. `--killall`을 지정하지 않는 한 필수입니다.

#### 옵션
- `--killall`: 현재 실행 중이거나 대기 중인 모든 검사 요청을 중단합니다. 함께 지정된 요청 ID보다 우선합니다.

#### 예시
특정 요청을 중단하려면:
```bash
digna inspection abort 1024
```

활성 및 대기 중인 모든 검사를 중단하려면:
```bash
digna inspection abort --killall
```

#### 출력 예시
`--killall`은 수행한 작업을 보고합니다. 단일 요청의 중단은 출력을 생성하지 않으며 종료 코드로 성공 여부를 알립니다.
```text
All running and pending inspections have been aborted.
```

---

## 라이선스 관리

---

### license check

`license check` 명령은 `license.toml`을 검증하여, 설치와 함께 제공된 공개 키로 서명을 확인하고 만료되지 않았는지 검사합니다. 애플리케이션 구성을 읽지 않으므로 `config.toml`을 설정하기 전에도 동작합니다.

#### 명령 사용법
```bash
digna license check
```

#### 출력 예시
```text
License is valid
```

유효하지 않은 서명과 만료된 라이선스는 서로 다른 오류로 보고되며, 둘 다 종료 코드 1을 사용합니다.

---

## 서버 및 백그라운드 서비스

---

### serve

`serve` 명령은 ***digna*** REST API 서버를 백그라운드 검사 스케줄러 및 검사 관리자와 함께 시작합니다. 시작 시점에는 저장소가 여전히 실행 중으로 기록하고 있는 검사를 모두 실패 처리합니다. 이전 프로세스에서 살아남은 것이 있을 수 없기 때문입니다.

명령은 중지될 때까지 포그라운드에서 실행됩니다.

#### 명령 사용법
```bash
digna serve [OPTIONS]
```

#### 옵션
- `--address`: API 서버를 바인딩할 네트워크 주소(기본값: `127.0.0.1`).
- `--port`: 수신 대기할 포트 번호(기본값: `8000`).

#### 예시
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### 출력 예시
```text
Server running on http://0.0.0.0:8000
```