---
title: digna CLI Reference 2026.04 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2026.04
image: /assets/logo_square.png
---

# digna CLI Reference 2026.04
**2026-04-08**

이 페이지는 ***digna*** CLI 릴리스 **2026.04**에서 사용 가능한 전체 명령 세트를 사용 예제와 옵션과 함께 문서화합니다.

---

## CLI 기초

---

### help
`--help` 옵션은 사용 가능한 명령과 사용법에 대한 정보를 제공합니다. 이 옵션을 사용하는 주요 방법은 두 가지입니다:

1. **일반 도움말 표시:**
   
   키워드 ***dignacli*** 바로 뒤에 `--help`를 사용합니다.  
   ```bash
   dignacli --help
   ```

2. **특정 명령에 대한 도움말 확인:**  
  
   특정 명령에 대한 자세한 정보를 얻으려면 해당 명령에 `--help`를 추가합니다.  
   예를 들어 `add-user` 명령에 대한 도움말을 얻으려면 다음을 실행합니다:
   ```bash
   dignacli add-user --help
   ```

   ### 출력:
      
   - **명령 설명:** 명령이 수행하는 작업에 대한 자세한 설명.  
   - **구문:** 필수 및 선택 인수를 포함한 정확한 사용 구문.  
   - **옵션:** 명령에 특화된 옵션과 그 설명.  
   - **예제:** 명령을 효과적으로 실행하는 방법에 대한 예제.

### check-config

`check-config` 명령은 ***digna*** 구성 요소가 config.toml에서 필요한 구성 요소를 찾을 수 있는지 테스트하기 위해 설계된 ***digna*** CLI 유틸리티입니다. 이 명령은 구성의 완전성을 확인합니다.

#### 옵션

- `--configpath`, `-cp`: 구성 파일 또는 디렉토리 경로. 생략하면 ../config.toml을 사용합니다.
      
#### 명령 사용법
```bash
dignacli check-config
```

정상적으로 실행되면 명령은 구성의 완전성에 대한 확인을 출력합니다.  
  
구성이 불완전한 경우 누락된 구성 요소들이 나열됩니다.

  
### check-repo-connection

`check-repo-connection` 명령은 지정된 ***digna*** 저장소에 대한 연결 및 접근성을 테스트하도록 설계된 ***digna*** CLI 유틸리티입니다. 이 명령은 CLI가 저장소와 상호작용할 수 있는지를 확인합니다.
      
#### 명령 사용법
```bash
dignacli check-repo-connection
```

정상적으로 실행되면 명령은 연결 확인과 함께 저장소에 대한 세부 정보를 출력합니다: Repository version, Host, Database 및 Schema.  
  
저장소 연결이 성공적이지 않은 경우 config.toml 파일의 설정을 확인하십시오.


### version

설치된 *dignacli* 버전을 확인하려면 `--version` 옵션을 사용하십시오.  
  
#### 명령 사용법
```bash
dignacli --version
```
  
#### 예제 출력
```bash
dignacli version 2026.04
```

### 로깅 옵션
  
기본적으로 ***digna*** 명령의 콘솔 출력은 최소한의 정보만 보이도록 설계되어 있습니다. 대부분의 명령은 다음 옵션을 사용하여 추가 정보를 제공할 수 있습니다:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose”와 “debug”는 상세 수준을 정의하고, “logfile” 스위치는 출력을 콘솔 대신 파일로 스트리밍하도록 리디렉션합니다.

## 사용자 관리

### add-user
  
`add-user` 명령은 ***digna*** 시스템에 신규 사용자를 추가하는 데 사용됩니다.
  
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
- `--valid_until`, `-vu`: `YYYY-MM-DD HH:MI:SS` 형식으로 사용자 계정 만료일을 설정합니다. 설정하지 않으면 계정에 만료일이 없습니다.

#### 예제

사용자 이름이 `jdoe`, 전체 이름이 `John Doe`, 비밀번호가 `password123`인 새 사용자를 추가하려면:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
계정 만료일을 설정하여 새 사용자를 추가하려면:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user` 명령은 ***digna*** 시스템에서 기존 사용자를 삭제하는 데 사용됩니다.
  
#### 명령 사용법
```bash
dignacli delete-user USER_NAME
```
  
#### 인수
- **USER_NAME**: 삭제할 사용자의 사용자 이름 (필수). 이 명령이 요구하는 유일한 인수입니다.

#### 예제
```bash
dignacli delete-user jdoe
```
  
이 명령을 실행하면 사용자 `jdoe`가 ***digna*** 시스템에서 삭제되어 접근 권한이 취소되고 저장소에서 관련 데이터 및 권한이 제거됩니다.

### modify-user

`modify-user` 명령은 ***digna*** 시스템에서 기존 사용자의 세부 정보를 업데이트하는 데 사용됩니다.

#### 명령 사용법
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### 인수
  
- **USER_NAME**: 수정할 사용자의 사용자 이름 (필수).
- **USER_FULL_NAME**: 사용자의 새 전체 이름 (필수).
  
#### 옵션  
  
- `--is_superuser`, `-su`: 사용자를 슈퍼유저로 설정하여 권한을 상승시킵니다. 이 플래그는 값이 필요하지 않습니다.  
- `--valid_until`, `-vu`: 계정 만료일을 YYYY-MM-DD HH:MI:SS 형식으로 설정합니다. 제공하지 않으면 계정은 무기한 유효합니다.  
  
#### 예제
  
사용자 `jdoe`의 전체 이름을 “Johnathan Doe”로 변경하고 슈퍼유저로 설정하려면:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd` 명령은 ***digna*** 시스템에서 기존 사용자의 비밀번호를 변경하는 데 사용됩니다.
  
#### 명령 사용법
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### 인수
  
- **USER_NAME**: 비밀번호를 변경할 사용자의 사용자 이름 (필수).
- **USER_PWD**: 사용자의 새 비밀번호 (필수).
  
#### 예제
  
사용자 `jdoe`의 비밀번호를 `newpassword123`으로 변경하려면:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users` 명령은 ***digna*** 시스템에 등록된 모든 사용자의 목록을 표시합니다.

#### 명령 사용법

```bash
dignacli list-users
```

이 명령을 실행하면 ***digna*** 저장소에 연결되어 모든 사용자의 ID, 사용자 이름, 전체 이름, 슈퍼유저 상태 및 만료 타임스탬프를 표시합니다.

## 저장소 관리

### upgrade-repo
  
`upgrade-repo` 명령은 ***digna*** 저장소를 업그레이드하거나 초기화하는 데 사용됩니다. 이 명령은 업데이트를 적용하거나 저장소 인프라를 처음으로 설정할 때 필수적입니다.
  
#### 명령 사용법

```bash
dignacli upgrade-repo [options]
```
  
#### 옵션
  
- `--simulation-mode`, `-s`: 활성화하면 시뮬레이션 모드로 명령을 실행하여 실제로 SQL을 실행하지 않고 실행될 SQL 문을 출력합니다. 변경 사항을 미리 확인할 때 유용합니다.  

  
#### 예제
  
옵션 없이 ***digna*** 저장소를 업그레이드하려면 다음을 실행합니다:
  
```bash
dignacli upgrade-repo
```  
시뮬레이션 모드로 업그레이드를 실행하여 SQL 문을 확인하려면:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
이 명령은 데이터베이스 스키마 및 기타 저장소 구성 요소가 소프트웨어의 최신 버전과 일치하도록 유지하는 데 중요합니다.

### encrypt
  
`encrypt` 명령은 비밀번호를 암호화하는 데 사용됩니다.
  
#### 명령 사용법
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### 인수
- **PASSWORD**: 암호화할 비밀번호 (필수).
  
#### 예제
  
비밀번호를 암호화하려면 인수로 비밀번호를 제공해야 합니다.  
예를 들어 비밀번호 `mypassword123`을 암호화하려면:
```bash
dignacli encrypt mypassword123
```
이 명령은 제공된 비밀번호의 암호화된 버전을 출력하며, 이는 보안 문맥에서 사용될 수 있습니다. 비밀번호 인수가 제공되지 않으면 CLI는 누락된 인수에 대한 오류를 표시합니다.

### generate-key
  
`generate-key` 명령은 저장소에 저장된 비밀번호를 보호하는 데 필수적인 Fernet 키를 생성하는 데 사용됩니다.
  
#### 명령 사용법
```bash
dignacli generate-key
```
  
## 데이터 관리

### clean-up

`clean-up` 명령은 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로파일, 예측 및 트래픽 라이트 시스템 데이터를 제거하는 데 사용됩니다. 이 명령은 데이터 수명 주기 관리를 위해 중요하며 오래되거나 불필요한 데이터를 정리하여 조직적이고 효율적인 데이터 환경을 유지하는 데 도움을 줍니다.

#### 명령 사용법

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 인수
  
- **PROJECT_NAME**: 데이터를 제거할 프로젝트 이름 (필수). 이 인수에 all-projects 키워드를 사용하면 ***digna***가 모든 기존 프로젝트를 순회하며 명령을 적용합니다.
- **FROM_DATE**: 데이터 제거 시작 날짜 및 시간. 허용 형식은 %Y-%m-%d, %Y-%m-%dT%H:%M:%S 또는 %Y-%m-%d %H:%M:%S (필수).
- **TO_DATE**: 데이터 제거 종료 날짜 및 시간. FROM_DATE와 동일한 형식 허용 (필수).
  
#### 옵션
  
- `--table-name`, `-tn`: 정리 작업을 프로젝트 내 특정 테이블로 제한합니다.
- `--table-filter`, `-tf`: 이름에 지정한 부분 문자열을 포함하는 테이블로만 정리 대상을 필터링합니다.
- `--timing`, `-tm`: 완료 후 정리 프로세스의 소요 시간을 표시합니다.
- `--help`: clean-up 명령에 대한 도움말을 표시하고 종료합니다.
  
#### 예제
  
ProjectA 프로젝트에서 2023년 1월 1일부터 2023년 6월 30일까지의 데이터를 제거하려면:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
특정 테이블 `Table1`의 데이터만 제거하려면:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
이 명령은 데이터 저장 관리를 도와 저장소에 관련 정보만 남도록 보장합니다.

### remove-orphans
  
`remove-orphans` 명령은 ***digna*** 저장소에서 정리 작업을 수행하는 데 사용됩니다.  
사용자가 프로젝트나 데이터 소스를 삭제할 때 프로파일과 예측이 저장소에 남아 있는 경우가 있습니다. 이 명령은 그러한 고아 행(orphans)을 저장소에서 제거합니다.
  
#### 명령 사용법
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects` 명령은 ***digna*** 시스템 내의 사용 가능한 모든 프로젝트 목록을 표시하는 데 사용됩니다.
  
#### 명령 사용법
  
```bash
dignacli list-projects
```

이 명령은 여러 프로젝트를 관리하는 관리자 및 사용자에게 특히 유용하며, ***digna*** 저장소에서 사용 가능한 프로젝트를 빠르게 개요로 제공합니다.

### list-ds

`list-ds` 명령은 지정된 프로젝트 내의 사용 가능한 모든 데이터 소스 목록을 표시하는 데 사용됩니다. 이 명령은 분석 및 관리에 사용할 수 있는 데이터 자산을 이해하는 데 유용합니다.

#### 명령 사용법
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### 인수
- **PROJECT_NAME**: 데이터 소스를 나열할 프로젝트 이름 (필수).
  
#### 예제
  
`ProjectA` 프로젝트의 모든 데이터 소스를 나열하려면:
  
```bash
dignacli list-ds ProjectA
```
  
이 명령은 프로젝트에서 사용 가능한 데이터 소스의 개요를 제공하여 데이터 환경을 보다 효과적으로 탐색하고 관리할 수 있도록 도와줍니다.


### inspect

`inspect` 명령은 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로파일, 예측 및 트래픽 라이트 시스템 데이터를 생성하는 데 사용됩니다. 이 명령은 정의된 기간 동안 데이터를 분석하고 모니터링하는 데 도움을 줍니다. 검사 완료 후 계산된 트래픽 라이트 시스템의 값이 반환됩니다:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### 명령 사용법

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 인수
  
- **PROJECT_NAME**: 검사를 수행할 프로젝트 이름 (필수). 이 인수에 all-projects 키워드를 사용하면 ***digna***가 모든 기존 프로젝트를 순회하며 명령을 적용합니다.
- **FROM_DATE**: 검사 시작 날짜 및 시간. 허용 형식은 %Y-%m-%d, %Y-%m-%dT%H:%M:%S 또는 %Y-%m-%d %H:%M:%S (필수).
- **TO_DATE**: 검사 종료 날짜 및 시간. FROM_DATE와 동일한 형식 허용 (필수).
  
#### 옵션

- `--table-name`, `-tn`: 검사를 프로젝트 내 특정 테이블로 제한합니다.
- `--table-filter`, `-tf`: 이름에 지정한 부분 문자열을 포함하는 테이블만 검사하도록 필터링합니다.
- `--enable_notification`, `-en`: 경고 발생 시 알림 전송을 활성화합니다.
- `--bypass-backend`, `-bb`: 백엔드를 우회하고 CLI에서 직접 검사를 실행합니다(테스트 용도로만 사용!).

  
#### 예제
  
`ProjectA` 프로젝트에 대해 2024년 1월 1일부터 2024년 1월 31일까지 데이터를 검사하려면:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
특정 테이블만 검사하고 예측을 강제로 재계산하려면:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
이 명령은 업데이트된 프로파일 및 예측을 생성하고, 데이터 무결성을 모니터링하며, 지정된 프로젝트 기간 내 경고 시스템을 관리하는 데 유용합니다.

### inspect-async

`inspect-async` 명령은 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로파일, 예측 및 트래픽 라이트 시스템 데이터를 생성하는 비동기식 명령입니다. 이 명령은 검사 완료를 기다리지 않고 제출된 검사 요청에 대한 요청 ID를 반환합니다. 검사 진행 상황을 확인하려면 `inspect-status` 명령을 사용하십시오.

#### 명령 사용법

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### 인수
  
- **PROJECT_NAME**: 검사를 수행할 프로젝트 이름 (필수). 이 인수에 all-projects 키워드를 사용하면 ***digna***가 모든 기존 프로젝트를 순회하며 명령을 적용합니다.
- **FROM_DATE**: 검사 시작 날짜 및 시간. 허용 형식은 %Y-%m-%d, %Y-%m-%dT%H:%M:%S 또는 %Y-%m-%d %H:%M:%S (필수).
- **TO_DATE**: 검사 종료 날짜 및 시간. FROM_DATE와 동일한 형식 허용 (필수).
  
#### 옵션

- `--table-name`, `-tn`: 검사를 프로젝트 내 특정 테이블로 제한합니다.
- `--table-filter`, `-tf`: 이름에 지정한 부분 문자열을 포함하는 테이블만 검사하도록 필터링합니다.
- `--enable_notification`, `-en`: 경고 발생 시 알림 전송을 활성화합니다.

  
#### 예제
  
`ProjectA` 프로젝트에 대해 2024년 1월 1일부터 2024년 1월 31일까지 비동기 검사를 제출하려면:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  

### inspect-status

`inspect-status` 명령은 비동기 검사 요청의 진행 상태를 요청 ID를 기반으로 확인하는 데 사용됩니다.

#### 명령 사용법

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### 인수
  
- **REQUEST_ID**: `inspect-async` 명령이 반환한 요청 ID
  
#### 예제
  
요청 ID가 12345인 검사의 진행 상태를 확인하려면:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel` 명령은 요청 ID를 기반으로 검사를 취소하거나 현재 실행 중인 모든 요청을 취소하는 데 사용됩니다.

#### 명령 사용법

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### 인수
  
- **REQUEST_ID**: `inspect-async` 명령이 반환한 요청 ID
  
#### 예제
  
요청 ID 12345인 검사를 취소하려면:
  
```bash
dignacli inspect-cancel 12345
```

현재 실행 중이거나 대기 중인 모든 요청을 취소하려면:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds` 명령은 ***digna*** 저장소에서 데이터 소스의 내보내기를 생성하는 데 사용됩니다. 기본적으로 지정된 프로젝트의 모든 데이터 소스가 내보내집니다.

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
  
`ProjectA` 프로젝트의 모든 데이터 소스를 내보내려면:
  
```bash
dignacli export-ds ProjectA
```
  
이 명령은 `ProjectA`의 모든 데이터 소스를 JSON 문서로 내보내며, 이는 다른 프로젝트나 ***digna*** 저장소로 가져오는 데 사용할 수 있습니다.


### import-ds

`import-ds` 명령은 데이터 소스를 대상 프로젝트로 가져오고 가져오기 보고서를 생성하는 데 사용됩니다.

#### 명령 사용법
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 인수
- **PROJECT_NAME**: 데이터 소스를 가져올 대상 프로젝트 이름.
- **EXPORT_FILE**: 가져올 데이터 소스 내보내기 파일 이름.

#### 옵션

- `--output-file`, `-o`: 가져오기 보고서를 저장할 파일(지정하지 않으면 터미널에 표 형식으로 출력).
- `--output-format`, `-f`: 가져오기 보고서를 저장할 형식(json, csv).
    
#### 예제
  
내보내기 파일 `my_export.json`의 모든 데이터 소스를 `ProjectB`로 가져오려면:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
가져오기 후 이 명령은 가져온 객체와 건너뛴 객체에 대한 보고서도 표시합니다. `ProjectB`에는 새로운 데이터 소스만 가져옵니다. 어떤 객체가 가져와지고 건너뛰어질지 확인하려면 `plan-import-ds` 명령을 사용할 수 있습니다.

### plan-import-ds

`plan-import-ds` 명령은 대상 프로젝트로 데이터 소스를 가져오기 전에 어떤 항목이 가져와지고 건너뛰어질지 분석하는 데 사용됩니다.

#### 명령 사용법
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### 인수
- **PROJECT_NAME**: 데이터 소스가 가져와질 대상 프로젝트 이름(예정).
- **EXPORT_FILE**: 가져오기 전 분석할 데이터 소스 내보내기 파일 이름.

#### 옵션

- `--output-file`, `-o`: 가져오기 계획 보고서를 저장할 파일(지정하지 않으면 터미널에 표 형식으로 출력).
- `--output-format`, `-f`: 가져오기 계획 보고서를 저장할 형식(json, csv).
    
#### 예제
  
내보내기 파일 `my_export.json`을 `ProjectB`에 가져올 때 어떤 데이터 소스가 가져와지고 어떤 것이 건너뛰어질지 확인하려면:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
이 명령은 가져올 객체와 건너뛸 객체에 대한 가져오기 계획만 표시합니다.