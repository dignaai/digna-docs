---
title: digna CLI 참조 2024.12 – 명령어 및 예제 | digna 문서
description: digna CLI 릴리스 2024.12에 대한 완전한 참조입니다. add-user, check-repo-connection, upgrade-repo, inspect 등 사용자, 리포지토리 및 데이터를 관리하는 방법을 명령어 예제와 함께 설명합니다.
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

이 페이지는 ***digna*** CLI 릴리스 **2024.12**에서 제공되는 전체 명령어 집합을 사용 예제 및 옵션과 함께 문서화합니다.

---


**2024-12-09**


---

## CLI 기초

---

## `help` 옵션 사용

`--help` 옵션은 사용 가능한 명령어와 사용법에 대한 정보를 제공합니다. 이 옵션을 사용하는 주요 방법은 두 가지입니다:

1. **일반 도움말 표시:**
   
   키워드 ***dignacli*** 바로 뒤에 `--help`를 사용하세요.  
   ```bash
   dignacli --help
   ```

3.  **특정 명령어에 대한 도움말 얻기:**  
  
    특정 명령어에 대한 자세한 정보를 보려면 해당 명령어 뒤에 `--help`를 추가하세요.  
    예를 들어 `add-user` 명령어에 대한 도움을 얻으려면 다음을 실행합니다:
     ```bash
     dignacli add-user --help
     ```

     ### 출력:
      
     - **명령 설명:** 명령이 수행하는 작업에 대한 자세한 설명을 제공합니다.  
     - **구문:** 필수 및 선택 인수를 포함한 정확한 구문을 표시합니다.  
     - **옵션:** 명령어에 특정한 옵션과 그 설명을 나열합니다.  
     - **예제:** 명령어를 효과적으로 실행하는 방법에 대한 예제를 제공합니다.

  
## `check-repo-connection` 명령어 사용

`check-repo-connection` 명령어는 지정된 ***digna*** 리포지토리에 대한 연결 및 접근성을 테스트하기 위한 ***digna*** CLI 도구의 유틸리티입니다. 이 명령어는 CLI가 리포지토리와 상호 작용할 수 있는지 확인합니다.
      
### 명령 사용법
```bash
dignacli check-repo-connection
```

명령이 성공적으로 실행되면 리포지토리 버전, 호스트, 데이터베이스 및 스키마 등의 리포지토리 세부 정보와 함께 연결 확인을 출력합니다.  
  
리포지토리 연결이 성공하지 않으면 config.toml 파일의 설정이 올바른지 확인하세요.

## `version` 명령어 사용

설치된 *dignacli* 버전을 확인하려면 `--version` 옵션을 사용하세요.  
  
### 명령 사용법
```bash
dignacli --version
```
  
### 예제 출력
```bash
dignacli version 2024.12
```

## 로깅 옵션 사용
  
기본적으로 ***digna*** 명령어의 콘솔 출력은 최소한의 정보만 표시하도록 설계되어 있습니다. 대부분의 명령어는 다음 옵션을 사용하여 추가 정보를 제공할 수 있습니다:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose”와 “debug”는 상세 수준을 정의하며, “logfile” 스위치는 출력을 콘솔 대신 파일로 스트리밍하도록 리디렉션하는 데 사용됩니다.

# 사용자 관리

## `add-user` 명령어 사용
  
***digna*** CLI의 `add-user` 명령어는 ***digna*** 시스템에 새 사용자를 추가하는 데 사용됩니다.
  
### 명령 사용법
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### 인수

- **USER_NAME**: 새 사용자의 사용자 이름(필수).
- **USER_FULL_NAME**: 새 사용자의 전체 이름(필수).
- **USER_PASSWORD**: 새 사용자의 비밀번호(필수).

### 옵션

- `--is_superuser`, `-su`: 새 사용자를 관리자(슈퍼유저)로 지정하는 플래그입니다.
- `--valid_until`, `-vu`: 계정 만료일을 `YYYY-MM-DD HH:MI:SS` 형식으로 설정합니다. 설정하지 않으면 계정에 만료일이 없습니다.

### 예제

사용자 이름이 `jdoe`, 전체 이름이 `John Doe`, 비밀번호가 `password123`인 새 사용자를 추가하려면:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
계정 만료일을 설정하여 새 사용자를 추가하려면:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` 명령어 사용
  
***digna*** CLI의 `delete-user` 명령어는 기존 사용자를 ***digna*** 시스템에서 제거하는 데 사용됩니다.
  
### 명령 사용법
```bash
dignacli delete-user USER_NAME
```
  
### 인수
- **USER_NAME**: 삭제할 사용자의 사용자 이름(필수). 이 명령어가 요구하는 유일한 인수입니다.

### 예제
```bash
dignacli delete-user jdoe
```
  
이 명령을 실행하면 `jdoe` 사용자가 ***digna*** 시스템에서 제거되어 접근 권한이 취소되고 리포지토리에서 관련 데이터와 권한이 삭제됩니다.

## `modify-user` 명령어 사용

***digna*** CLI의 `modify-user` 명령어는 기존 사용자의 세부 정보를 업데이트하는 데 사용됩니다.

### 명령 사용법
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### 인수
  
- **USER_NAME**: 수정할 사용자의 사용자 이름(필수).
- **USER_FULL_NAME**: 사용자의 새 전체 이름(필수).
  
### 옵션  
  
- `--is_superuser`, `-su`: 사용자를 슈퍼유저로 설정하여 권한을 상승시킵니다. 이 플래그는 값이 필요하지 않습니다.  
- `--valid_until`, `-vu`: 계정 만료일을 `YYYY-MM-DD HH:MI:SS` 형식으로 설정합니다. 제공하지 않으면 계정은 무기한 유효합니다.  
  
### 예제
  
사용자 `jdoe`의 전체 이름을 “Johnathan Doe”로 수정하고 해당 사용자를 슈퍼유저로 설정하려면:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` 명령어 사용
  
***digna*** CLI의 `modify-user-pwd` 명령어는 기존 사용자의 비밀번호를 변경하는 데 사용됩니다.
  
### 명령 사용법
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### 인수
  
- **USER_NAME**: 비밀번호를 변경할 사용자의 사용자 이름(필수).
- **USER_PWD**: 사용자의 새 비밀번호(필수).
  
### 예제
  
사용자 `jdoe`의 비밀번호를 `newpassword123`으로 변경하려면:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` 명령어 사용

***digna*** CLI의 `list-users` 명령어는 ***digna*** 시스템에 등록된 모든 사용자의 목록을 표시합니다.

### 명령 사용법

```bash
dignacli list-users
```

이 명령을 실행하면 ***digna*** 리포지토리에 연결하여 모든 사용자의 ID, 사용자 이름, 전체 이름, 슈퍼유저 상태 및 만료 타임스탬프를 표시합니다.

# 리포지토리 관리

### `upgrade-repo` 명령어 사용
  
***digna*** CLI의 `upgrade-repo` 명령어는 ***digna*** 리포지토리를 업그레이드하거나 초기화하는 데 사용됩니다. 이 명령어는 업데이트를 적용하거나 처음으로 리포지토리 인프라를 설정하는 데 필수적입니다.
  
### 명령 사용법

```bash
dignacli upgrade-repo [options]
```
  
### 옵션
  
- `--simulation-mode`, `-s`: 활성화하면 시뮬레이션 모드로 명령을 실행하여 실제로는 실행하지 않고 실행될 SQL 문을 출력합니다. 변경 사항을 미리 확인할 때 유용합니다.  

  
### 예제
  
옵션 없이 ***digna*** 리포지토리를 업그레이드하려면:
  
```bash
dignacli upgrade-repo
```  
시뮬레이션 모드로 업그레이드를 실행하여 SQL 문을 확인하려면:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
이 명령은 데이터베이스 스키마 및 기타 리포지토리 구성 요소가 소프트웨어의 최신 버전과 일치하도록 하여 ***digna*** 시스템을 유지관리하는 데 중요합니다.

## `encrypt` 명령어 사용
  
***digna*** CLI의 `encrypt` 명령어는 비밀번호를 암호화하는 데 사용됩니다.
  
### 명령 사용법
  
```bash
dignacli encrypt <PASSWORD>
```
    
### 인수
- **PASSWORD**: 암호화해야 할 비밀번호(필수).
  
### 예제
  
비밀번호를 암호화하려면 비밀번호를 인수로 제공해야 합니다.  
예를 들어 비밀번호 `mypassword123`을 암호화하려면 다음과 같이 사용합니다:
```bash
dignacli encrypt mypassword123
```
이 명령은 제공된 비밀번호의 암호화된 버전을 출력하며, 이를 안전한 컨텍스트에서 사용할 수 있습니다. 비밀번호 인수를 제공하지 않으면 CLI는 누락된 인수에 대한 오류를 표시합니다.

## `generate-key` 명령어 사용
  
`generate-key` 명령어는 ***digna*** 리포지토리에 저장된 비밀번호를 보호하는 데 필수적인 Fernet 키를 생성하는 데 사용됩니다.
  
### 명령 사용법
```bash
dignacli generate-key
```
  
# 데이터 관리

## `clean-up` 명령어 사용

***digna*** CLI의 `clean-up` 명령어는 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로파일, 예측 및 트래픽 라이트 시스템 데이터를 제거하는 데 사용됩니다. 이 명령어는 데이터 수명 주기 관리를 위해 필수적이며, 오래되었거나 불필요한 데이터를 정리하여 조직적이고 효율적인 데이터 환경을 유지하는 데 도움이 됩니다.

### 명령 사용법

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### 인수
  
- **PROJECT_NAME**: 데이터가 제거될 프로젝트 이름(필수). 이 인수에 `all-projects` 키워드를 사용하면 ***digna***가 모든 기존 프로젝트를 반복하면서 이 명령을 적용합니다.
- **FROM_DATE**: 데이터 제거의 시작 날짜 및 시간. 허용되는 형식에는 %Y-%m-%d, %Y-%m-%dT%H:%M:%S 또는 %Y-%m-%d %H:%M:%S가 포함됩니다(필수).
- **TO_DATE**: 데이터 제거의 종료 날짜 및 시간(FROM_DATE와 동일한 형식, 필수).
  
### 옵션
  
- `--table-name`, `-tn`: 정리 작업을 프로젝트 내 특정 테이블로 제한합니다.
- `--table-filter`, `-tf`: 이름에 지정한 하위 문자열이 포함된 테이블로 정리 범위를 제한합니다.
- `--timing`, `-tm`: 완료 후 정리 작업의 소요 시간을 표시합니다.
- `--help`: clean-up 명령어에 대한 도움말을 표시하고 종료합니다.
  
### 예제
  
프로젝트 ProjectA에서 2023년 1월 1일부터 2023년 6월 30일까지의 데이터를 제거하려면:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
특정 테이블 `Table1`의 데이터만 제거하려면:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
이 명령은 데이터 저장소 관리를 돕고 리포지토리에 관련 정보만 남도록 보장합니다.

## `inspect` 명령어 사용

***digna*** CLI의 `inspect` 명령어는 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로파일, 예측 및 트래픽 라이트 시스템 데이터를 생성하는 데 사용됩니다. 이 명령어는 정의된 기간 동안 데이터를 분석하고 모니터링하는 데 도움이 됩니다.

### 명령 사용법

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### 인수
  
- **PROJECT_NAME**: 검사를 수행할 프로젝트 이름(필수). 이 인수에 `all-projects` 키워드를 사용하면 ***digna***가 모든 기존 프로젝트를 반복하면서 이 명령을 적용합니다.
- **FROM_DATE**: 검사 시작 날짜 및 시간. 허용되는 형식에는 %Y-%m-%d, %Y-%m-%dT%H:%M:%S 또는 %Y-%m-%d %H:%M:%S가 포함됩니다(필수).
- **TO_DATE**: 검사 종료 날짜 및 시간(FROM_DATE와 동일한 형식, 필수).
  
### 옵션

- `--table-name`, `-tn`: 검사를 프로젝트 내 특정 테이블로 제한합니다.
- `--table-filter`, `-tf`: 이름에 지정한 하위 문자열이 포함된 테이블만 검사를 수행합니다.
- `--do-profile`: 프로파일 재수집을 트리거합니다. 기본값은 do-profile입니다.
- `--no-do-profile`: 프로파일 재수집을 방지합니다.
- `--do-prediction`: 예측 재계산을 트리거합니다. 기본값은 do-prediction입니다.
- `--no-do-prediction`: 예측 재계산을 방지합니다.
- `--do-alert-status`: 경고 상태 재계산을 트리거합니다. 기본값은 do-alert-status입니다.
- `--no-do-alert-status`: 경고 상태 재계산을 방지합니다.
- `--iterative`: 일별 반복을 사용하여 기간을 검사합니다. 기본값은 iterative입니다.
- `--no-iterative`: 전체 기간을 한 번에 검사합니다.
- `--timing`, `-tm`: 검사 완료 후 소요 시간을 표시합니다.
  
### 예제
  
프로젝트 `ProjectA`에 대해 2024년 1월 1일부터 2024년 1월 31일까지 데이터를 검사하려면:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
특정 테이블만 검사하고 예측 재계산을 강제하려면:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
이 명령은 업데이트된 프로파일과 예측을 생성하고, 데이터 무결성을 모니터링하며, 지정된 프로젝트 기간 내 경고 시스템을 관리하는 데 유용합니다.

## `tls-status` 명령어 사용

***digna*** CLI의 `tls-status` 명령어는 특정 날짜에 프로젝트 내 특정 테이블의 트래픽 라이트 시스템(TLS) 상태를 조회하는 데 사용됩니다. 트래픽 라이트 시스템은 데이터의 건전성과 품질에 대한 통찰을 제공하며, 주의나 조치가 필요한 문제나 경고를 나타냅니다.
  
### 명령 사용법
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### 인수
  
- **PROJECT_NAME**: TLS 상태를 조회할 프로젝트 이름(필수).
- **TABLE_NAME**: TLS 상태가 필요한 프로젝트 내 특정 테이블(필수).
- **DATE**: TLS 상태를 조회할 날짜(일반적으로 %Y-%m-%d 형식, 필수).
  
### 예제
  
프로젝트 ProjectA의 `UserData`라는 테이블에 대해 2024년 7월 1일의 TLS 상태를 확인하려면:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

이 명령은 사전 정의된 기준에 따라 명확하고 실행 가능한 상태 보고서를 제공하여 사용자가 데이터 품질을 모니터링하고 유지관리할 수 있도록 돕습니다.

## `list-projects` 명령어 사용
  
***digna*** CLI의 `list-projects` 명령어는 ***digna*** 시스템 내 사용 가능한 모든 프로젝트의 목록을 표시합니다.
  
### 명령 사용법
  
```bash
dignacli list-projects
```

이 명령은 여러 프로젝트를 관리하는 관리자와 사용자에게 유용하며, ***digna*** 리포지토리에서 사용 가능한 프로젝트를 빠르게 개요하도록 제공합니다.

## `list-ds` 명령어 사용

***digna*** CLI의 `list-ds` 명령어는 지정된 프로젝트 내 사용 가능한 모든 데이터 소스의 목록을 표시합니다. 이 명령은 분석 및 관리를 위해 사용 가능한 데이터 자산을 이해하는 데 유용합니다.

### 명령 사용법
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### 인수
- **PROJECT_NAME**: 데이터 소스를 나열할 프로젝트 이름(필수).
  
### 예제
  
프로젝트 `ProjectA`에 있는 모든 데이터 소스를 나열하려면:
  
```bash
dignacli list-ds ProjectA
```
  
이 명령은 프로젝트에서 사용 가능한 데이터 소스의 개요를 제공하여 데이터 환경을 보다 효율적으로 탐색하고 관리할 수 있도록 돕습니다.