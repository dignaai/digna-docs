---
title: digna CLI Reference 2025.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2025.109 Learn how to manage users, repositories, and data with commands such as add-user, check-config, check-repo-connection, inspect, inspect-async, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

이 페이지는 ***digna*** CLI 릴리스 **2025.09** 에서 사용 가능한 모든 명령어 집합을 문서화하며, 사용 예시와 옵션을 포함합니다.

---

## CLI 기초

---

### help
`--help` 옵션은 사용 가능한 명령어와 사용법에 대한 정보를 제공합니다. 이 옵션을 사용하는 주요 방법은 두 가지입니다:

1. **일반 도움말 표시:**
   
    키워드 ***digna***cl 바로 다음에 –help를 사용하십시오  
   ```bash
   dignacli --help
   ```

2. **특정 명령어에 대한 도움말 얻기:**  
  
    특정 명령어에 대한 자세한 정보를 보려면 해당 명령어 뒤에 `--help` 를 추가하십시오.  
    예를 들어 `add-user` 명령어에 대한 도움말을 얻으려면 다음을 실행합니다:
     ```bash
     dignacli add-user --help
     ```

     ### 출력:
      
     - **명령어 설명:** 명령어가 수행하는 작업에 대한 상세 설명을 제공합니다.  
     - **구문:** 필수 및 선택 인수를 포함한 정확한 구문을 보여줍니다.  
     - **옵션:** 해당 명령어에 특화된 옵션들을 설명과 함께 나열합니다.  
     - **예제:** 명령어를 효과적으로 실행하는 방법에 대한 예제를 제공합니다.

### check-config

`check-config` 명령어는 ***digna*** CLI 도구 내에서 ***digna*** 설정을 테스트하기 위해 사용되는 유틸리티입니다. 이 명령어는 ***digna*** 구성 요소들이 config.toml에서 필요한 구성 요소를 찾을 수 있는지 확인합니다.

#### 옵션

- `--configpath`, `-cp`: 구성 파일이나 디렉토리 경로입니다. 생략하면 ../config.toml 이 사용됩니다.
      
#### 명령 사용법
```bash
dignacli check-config
```

성공적으로 실행되면 구성의 완전성에 대한 확인 메시지를 출력합니다.  
  
구성이 불완전해 보일 경우 누락된 구성 요소들이 나열됩니다.

  
### check-repo-connection

`check-repo-connection` 명령어는 지정된 ***digna*** 리포지토리와의 연결성 및 접근성을 테스트하기 위해 ***digna*** CLI 도구 내에서 사용되는 유틸리티입니다. 이 명령어는 CLI가 리포지토리와 상호작용할 수 있는지 확인합니다.
      
#### 명령 사용법
```bash
dignacli check-repo-connection
```

성공적으로 실행되면 연결 확인과 함께 리포지토리 정보(리포지토리 버전, 호스트, 데이터베이스 및 스키마)에 대한 세부 정보를 출력합니다.  
  
리포지토리 연결이 성공적이지 않은 경우 config.toml 파일의 설정이 올바른지 확인하십시오.


### version

설치된 *dignacli* 버전을 확인하려면 --version 옵션을 사용하십시오.  
  
#### 명령 사용법
```bash
dignacli --version
```
  
#### 예제 출력
```bash
dignacli version 2025.09
```

### 로깅 옵션
  
기본적으로 ***digna*** 명령어의 콘솔 출력은 최소화되어 있습니다. 대부분의 명령어는 다음 옵션들을 사용하여 추가 정보를 제공할 수 있습니다:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose”와 “debug”는 상세 수준을 정의하며, “logfile” 스위치는 출력을 콘솔 창 대신 파일로 스트리밍하도록 리다이렉션하는 데 사용됩니다.

## 사용자 관리

### add-user
  
`add-user` 명령어는 ***digna*** CLI에서 새로운 사용자를 ***digna*** 시스템에 추가하는 데 사용됩니다.
  
#### 명령 사용법
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### 인수

- **USER_NAME**: 새 사용자의 사용자 이름 (필수).
- **USER_FULL_NAME**: 새 사용자의 전체 이름 (필수).
- **USER_PASSWORD**: 새 사용자의 비밀번호 (필수).

#### 옵션

- `--is_superuser`, `-su`: 새 사용자를 관리자(슈퍼유저)로 지정하는 플래그.
- `--valid_until`, `-vu`: `YYYY-MM-DD HH:MI:SS` 형식으로 사용자 계정의 만료 날짜를 설정합니다. 설정하지 않으면 계정은 만료되지 않습니다.

#### 예제

사용자 이름 `jdoe`, 전체 이름 `John Doe`, 비밀번호 `password123` 으로 새 사용자를 추가하려면:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
계정 만료 날짜를 설정하여 새 사용자를 추가하려면:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user` 명령어는 ***digna*** CLI에서 기존 사용자를 ***digna*** 시스템에서 제거하는 데 사용됩니다.
  
#### 명령 사용법
```bash
dignacli delete-user USER_NAME
```
  
#### 인수
- **USER_NAME**: 삭제할 사용자의 사용자 이름 (필수). 이 인수만이 명령어에 필요합니다.

#### 예제
```bash
dignacli delete-user jdoe
```
  
이 명령어를 실행하면 `jdoe` 사용자가 ***digna*** 시스템에서 제거되며, 해당 사용자의 접근 권한이 취소되고 리포지토리에서 관련 데이터 및 권한이 삭제됩니다.

### modify-user

`modify-user` 명령어는 ***digna*** CLI에서 기존 사용자의 세부 정보를 업데이트하는 데 사용됩니다.

#### 명령 사용법
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### 인수
  
- **USER_NAME**: 수정할 사용자의 사용자 이름 (필수).
- **USER_FULL_NAME**: 사용자의 새 전체 이름 (필수).
  
#### 옵션  
  
- `--is_superuser`, `-su`: 사용자를 슈퍼유저로 설정하여 권한을 상승시킵니다. 이 플래그는 값이 필요하지 않습니다.  
- `--valid_until`, `-vu`: 계정 만료 날짜를 YYYY-MM-DD HH:MI:SS 형식으로 설정합니다. 제공되지 않으면 계정은 무기한 유효합니다.  
  
#### 예제
  
사용자 `jdoe`의 전체 이름을 “Johnathan Doe”로 변경하고 해당 사용자를 슈퍼유저로 설정하려면:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd` 명령어는 ***digna*** CLI에서 기존 사용자의 비밀번호를 변경하는 데 사용됩니다.
  
#### 명령 사용법
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### 인수
  
- **USER_NAME**: 비밀번호를 변경할 사용자의 사용자 이름 (필수).
- **USER_PWD**: 사용자의 새 비밀번호 (필수).
  
#### 예제
  
사용자 `jdoe`의 비밀번호를 `newpassword123` 으로 변경하려면:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users` 명령어는 ***digna*** CLI에서 등록된 모든 사용자 목록을 표시합니다.

#### 명령 사용법

```bash
dignacli list-users
```

이 명령어를 실행하면 ***digna*** 리포지토리에 연결하여 모든 사용자를 나열하고, 각 사용자의 ID, 사용자 이름, 전체 이름, 슈퍼유저 상태 및 만료 타임스탬프를 보여줍니다.

## 리포지토리 관리

### upgrade-repo
  
`upgrade-repo` 명령어는 ***digna*** CLI에서 ***digna*** 리포지토리를 업그레이드하거나 초기화하는 데 사용됩니다. 이 명령어는 업데이트를 적용하거나 리포지토리 인프라를 처음 설정할 때 필수적입니다.
  
#### 명령 사용법

```bash
dignacli upgrade-repo [options]
```
  
#### 옵션
  
- `--simulation-mode`, `-s`: 활성화하면 명령어를 시뮬레이션 모드로 실행하여 실제로 SQL 문을 실행하지 않고 실행될 SQL 문들을 출력합니다. 변경 사항을 미리 확인할 때 유용합니다.  

  
#### 예제
  
옵션 없이 ***digna*** 리포지토리를 업그레이드하려면:
  
```bash
dignacli upgrade-repo
```  
시뮬레이션 모드로 업그레이드를 실행하여(실제로 적용하지 않고 SQL 문만 확인) 보려면:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
이 명령어는 데이터베이스 스키마 및 기타 리포지토리 구성 요소가 소프트웨어의 최신 버전과 일치하도록 유지하는 데 중요합니다.

### encrypt
  
`encrypt` 명령어는 비밀번호를 암호화하는 데 사용됩니다.
  
#### 명령 사용법
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### 인수
- **PASSWORD**: 암호화할 비밀번호 (필수).
  
#### 예제
  
비밀번호를 암호화하려면 비밀번호를 인수로 제공해야 합니다.  
예를 들어 비밀번호 `mypassword123` 을 암호화하려면:
```bash
dignacli encrypt mypassword123
```
이 명령어는 제공된 비밀번호의 암호화된 버전을 출력하며, 이후 안전한 환경에서 사용할 수 있습니다. 비밀번호 인수가 제공되지 않으면 CLI는 누락된 인수에 대한 오류를 표시합니다.

### generate-key
  
`generate-key` 명령어는 Fernet 키를 생성하는 데 사용되며, 이는 ***digna*** 리포지토리에 저장된 비밀번호를 보호하는 데 필수적입니다.
  
#### 명령 사용법
```bash
dignacli generate-key
```
  
## 데이터 관리

### clean-up

`clean-up` 명령어는 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로필, 예측 및 트래픽 라이트 시스템 데이터를 제거하는 데 사용됩니다. 이 명령어는 데이터 수명주기 관리를 위해 중요하며, 오래되었거나 불필요한 데이터를 정리하여 정리되고 효율적인 데이터 환경을 유지하는 데 도움을 줍니다.

#### 명령 사용법

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 인수
  
- **PROJECT_NAME**: 데이터를 제거할 프로젝트 이름 (필수). 이 인수에 all-projects 키워드를 사용하면 ***digna***가 모든 기존 프로젝트를 반복 처리하여 이 명령을 적용합니다.
- **FROM_DATE**: 데이터 제거의 시작 날짜 및 시간. 허용되는 형식은 %Y-%m-%d, %Y-%m-%dT%H:%M:%S, 또는 %Y-%m-%d %H:%M:%S 입니다 (필수).
- **TO_DATE**: 데이터 제거의 종료 날짜 및 시간으로 FROM_DATE와 동일한 형식을 따릅니다 (필수).
  
#### 옵션
  
- `--table-name`, `-tn`: 정리 작업을 프로젝트 내 특정 테이블로 제한합니다.
- `--table-filter`, `-tf`: 이름에 지정된 부분 문자열을 포함하는 테이블로만 정리를 제한하는 필터입니다.
- `--timing`, `-tm`: 완료 후 정리 프로세스의 소요 시간을 표시합니다.
- `--help`: clean-up 명령어에 대한 도움말을 표시하고 종료합니다.
  
#### 예제
  
프로젝트 ProjectA에서 2023년 1월 1일부터 2023년 6월 30일까지의 데이터를 제거하려면:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
특정 테이블 `Table1`의 데이터만 제거하려면:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
이 명령어는 데이터 저장을 관리하고 리포지토리에 관련 없는 정보만 남지 않도록 하는 데 도움이 됩니다.

### remove-orphans
  
`remove-orphans` 명령어는 ***digna*** 리포지토리의 정리 작업에 사용됩니다.  
사용자가 프로젝트나 데이터 소스를 삭제할 때 프로필과 예측이 리포지토리에 남아 있을 수 있습니다. 이 명령어를 사용하면 그러한 고아 행(orphans)이 리포지토리에서 제거됩니다.
  
#### 명령 사용법
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects` 명령어는 ***digna*** CLI에서 사용 가능한 모든 프로젝트 목록을 표시하는 데 사용됩니다.
  
#### 명령 사용법
  
```bash
dignacli list-projects
```

이 명령어는 여러 프로젝트를 관리하는 관리자 및 사용자에게 특히 유용하며, ***digna*** 리포지토리에서 사용 가능한 프로젝트를 빠르게 개관할 수 있게 해줍니다.

### list-ds

`list-ds` 명령어는 지정된 프로젝트 내 사용 가능한 모든 데이터 소스 목록을 표시하는 데 사용됩니다. 이 명령어는 분석 및 관리에 사용할 수 있는 데이터 자산을 파악하는 데 유용합니다.

#### 명령 사용법
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### 인수
- **PROJECT_NAME**: 데이터 소스를 나열할 프로젝트 이름 (필수).
  
#### 예제
  
프로젝트 `ProjectA` 내 모든 데이터 소스를 나열하려면:
  
```bash
dignacli list-ds ProjectA
```
  
이 명령어는 프로젝트 내 사용 가능한 데이터 소스에 대한 개요를 제공하여 데이터 환경을 보다 효과적으로 탐색하고 관리할 수 있게 합니다.


### inspect

`inspect` 명령어는 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로필, 예측 및 트래픽 라이트 시스템 데이터를 생성하는 데 사용됩니다. 이 명령어는 정의된 기간 동안 데이터를 분석하고 모니터링하는 데 도움을 줍니다. 검사 완료 후 계산된 트래픽 라이트 시스템의 값이 반환됩니다:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### 명령 사용법

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 인수
  
- **PROJECT_NAME**: 검사를 수행할 프로젝트 이름 (필수). 이 인수에 all-projects 키워드를 사용하면 ***digna***가 모든 기존 프로젝트를 반복 처리하여 이 명령을 적용합니다.
- **FROM_DATE**: 데이터 검사의 시작 날짜 및 시간. 허용되는 형식은 %Y-%m-%d, %Y-%m-%dT%H:%M:%S, 또는 %Y-%m-%d %H:%M:%S 입니다 (필수).
- **TO_DATE**: 데이터 검사의 종료 날짜 및 시간으로 FROM_DATE와 동일한 형식을 따릅니다 (필수).
  
#### 옵션

- `--table-name`, `-tn`: 검사를 프로젝트 내 특정 테이블로 제한합니다.
- `--table-filter`, `-tf`: 이름에 지정된 부분 문자열을 포함하는 테이블만 검토하도록 필터링합니다.
- `--enable_notification`, `-en`: 경고가 발생한 경우 알림 전송을 활성화합니다.
- `--bypass-backend`, `-bb`: 백엔드를 우회하고 CLI에서 직접 검사를 실행합니다(테스트 목적으로만 사용!).

  
#### 예제
  
프로젝트 `ProjectA`의 데이터를 2024년 1월 1일부터 2024년 1월 31일까지 검사하려면:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
특정 테이블만 검사하고 예측을 재계산하도록 강제하려면:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
이 명령어는 업데이트된 프로필 및 예측을 생성하고, 데이터 무결성을 모니터링하며, 지정된 프로젝트 기간 내에 경고 시스템을 관리하는 데 유용합니다.

### inspect-async

`inspect-async` 명령어는 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로필, 예측 및 트래픽 라이트 시스템 데이터를 생성하는 데 사용됩니다. 이 명령어는 정의된 기간 동안 데이터를 분석하고 모니터링하는 데 도움을 줍니다. `inspect-async` 명령어와 달리 이 명령어는 검사 완료를 기다리지 않습니다.  
대신 제출된 검사 요청에 대한 요청 ID를 반환합니다. 검사 진행 상황을 조회하려면 `inspect-status` 명령어를 사용하십시오.

#### 명령 사용법

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 인수
  
- **PROJECT_NAME**: 검사를 수행할 프로젝트 이름 (필수). 이 인수에 all-projects 키워드를 사용하면 ***digna***가 모든 기존 프로젝트를 반복 처리하여 이 명령을 적용합니다.
- **FROM_DATE**: 데이터 검사의 시작 날짜 및 시간. 허용되는 형식은 %Y-%m-%d, %Y-%m-%dT%H:%M:%S, 또는 %Y-%m-%d %H:%M:%S 입니다 (필수).
- **TO_DATE**: 데이터 검사의 종료 날짜 및 시간으로 FROM_DATE와 동일한 형식을 따릅니다 (필수).
  
#### 옵션

- `--table-name`, `-tn`: 검사를 프로젝트 내 특정 테이블로 제한합니다.
- `--table-filter`, `-tf`: 이름에 지정된 부분 문자열을 포함하는 테이블만 검토하도록 필터링합니다.
- `--enable_notification`, `-en`: 경고가 발생한 경우 알림 전송을 활성화합니다.

  
#### 예제
  
프로젝트 `ProjectA`의 데이터를 2024년 1월 1일부터 2024년 1월 31일까지 비동기 검사하려면:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status` 명령어는 비동기 검사 요청의 진행 상태를 요청 ID 기반으로 확인하는 데 사용됩니다.

#### 명령 사용법

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### 인수
  
- **REQUEST_ID**: `inspect-async` 명령어가 반환한 요청 ID 
  
#### 예제
  
요청 ID 12345 인 검사의 진행 상태를 확인하려면:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel` 명령어는 요청 ID 기반으로 검사를 취소하거나 현재 모든 요청을 취소하는 데 사용됩니다.

#### 명령 사용법

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### 인수
  
- **REQUEST_ID**: `inspect-async` 명령어가 반환한 요청 ID 
  
#### 예제
  
요청 ID 12345 인 검사를 취소하려면:
  
```bash
dignacli inspect-cancel 12345
```

현재 실행 중이거나 대기 중인 모든 요청을 취소하려면:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds` 명령어는 ***digna*** 리포지토리에서 데이터 소스를 내보내기 위해 사용됩니다. 기본적으로 지정된 프로젝트의 모든 데이터 소스가 내보내집니다.

#### 명령 사용법
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### 인수
- **PROJECT_NAME**: 데이터 소스를 내보낼 프로젝트 이름.

#### 옵션

- `--table_name`, `-tn`: 프로젝트에서 특정 데이터 소스만 내보냅니다.
- `--exportfile`, `-ef`: 내보내기 파일 이름을 지정합니다.
    
#### 예제
  
프로젝트 `ProjectA`의 모든 데이터 소스를 내보내려면:
  
```bash
dignacli export-ds ProjectA
```
  
이 명령어는 `ProjectA`의 모든 데이터 소스를 JSON 문서로 내보내며, 이를 다른 프로젝트나 ***digna*** 리포지토리로 가져올 수 있습니다.


### import-ds

`import-ds` 명령어는 데이터 소스를 대상 프로젝트로 가져오고 가져오기 보고서를 생성하는 데 사용됩니다.

#### 명령 사용법
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 인수
- **PROJECT_NAME**: 데이터 소스를 가져올 대상 프로젝트 이름.
- **EXPORT_FILE**: 가져올 데이터 소스 내보내기 파일 이름.

#### 옵션

- `--output-file`, `-o`: 가져오기 보고서를 저장할 파일 (지정하지 않으면 터미널에 표 형태로 출력).
- `--output-format`, `-f`: 가져오기 보고서를 저장할 형식 (json, csv).
    
#### 예제
  
내보내기 파일 `my_export.json` 의 모든 데이터 소스를 `ProjectB` 로 가져오려면:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
가져오기 후 이 명령어는 가져온 객체와 건너뛴 객체에 대한 보고서도 표시합니다. `ProjectB` 에 새 데이터 소스만 가져오며, 어떤 객체가 가져와지고 건너뛰어질지 확인하려면 `plan-import-ds` 명령어를 사용할 수 있습니다.

### plan-import-ds

`plan-import-ds` 명령어는 대상 프로젝트로 데이터를 가져오기 전에 어떤 데이터 소스가 가져와지고 건너뛰어질지 분석하는 데 사용됩니다.

#### 명령 사용법
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 인수
- **PROJECT_NAME**: 데이터 소스가 가져와질 대상 프로젝트 이름.
- **EXPORT_FILE**: 가져오기 전에 분석할 데이터 소스 내보내기 파일 이름.

#### 옵션

- `--output-file`, `-o`: 가져오기 계획 보고서를 저장할 파일 (지정하지 않으면 터미널에 표 형태로 출력).
- `--output-format`, `-f`: 가져오기 계획 보고서를 저장할 형식 (json, csv).
    
#### 예제
  
내보내기 파일 `my_export.json` 를 `ProjectB` 로 가져올 때 어떤 데이터 소스가 가져와지고 건너뛰어질지 확인하려면:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
이 명령어는 가져올 객체와 건너뛸 객체에 대한 가져오기 계획만 표시합니다.