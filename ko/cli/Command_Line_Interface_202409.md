# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI 기초

---

###   help

--help 옵션은 사용 가능한 명령과 사용법에 대한 정보를 제공합니다. 이 옵션을 사용하는 주요 방법은 두 가지입니다:

1. **일반 도움말 표시:**
   
    키워드 digna 뒤에 --help를 즉시 사용합니다.  
   bash
   dignacli --help

2. **특정 명령에 대한 도움말 받기:**  
  
    특정 명령에 대한 자세한 정보를 보려면 해당 명령 뒤에 --help를 붙입니다.  
    예를 들어 add-user 명령에 대한 도움말을 얻으려면 다음을 실행합니다:  
     bash
     dignacli add-user --help
     

     ### 출력:
      
     - **명령 설명:** 명령이 수행하는 작업에 대한 상세 설명.  
     - **문법:** 필수 및 선택 인수를 포함한 정확한 문법 표시.  
     - **옵션:** 명령에 특정한 옵션과 그 설명 목록.  
     - **예제:** 명령을 효과적으로 실행하는 방법을 보여주는 예제들.

  
###   check-repo-connection

check-repo-connection 명령은 digna CLI 도구 내에서 지정된 digna 저장소에 대한 연결 및 접근을 테스트하도록 설계된 유틸리티입니다. 이 명령은 CLI가 저장소와 상호작용할 수 있는지 확인합니다.
      
##### 명령 사용법
bash
dignacli check-repo-connection


명령이 성공적으로 실행되면 저장소 버전, 호스트, 데이터베이스 및 스키마에 대한 세부 정보와 함께 연결 확인을 출력합니다.  
  
저장소 연결에 실패할 경우 config.toml 파일에서 올바른 구성 설정이 있는지 확인하십시오.

###   version

설치된 dignacli 버전을 확인하려면 --version 옵션을 사용하십시오.  
  
#### 명령 사용법
bash
dignacli --version

  
#### 예제 출력
bash
dignacli version 2024.09


###   로깅 옵션
  
기본적으로 digna 명령의 콘솔 출력은 최소한으로 설계되어 있습니다. 대부분의 명령은 다음 옵션을 사용하여 추가 정보를 제공할 수 있습니다:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose”와 “debug”는 상세 수준을 정의하고, “logfile” 스위치는 출력을 콘솔 창 대신 파일로 스트리밍하도록 리다이렉트할 수 있게 합니다.

## 사용자 관리

###   add-user
  
add-user 명령은 digna CLI에서 새로운 사용자를 digna 시스템에 추가하는 데 사용됩니다.
  
#### 명령 사용법
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### 인수

- **USER_NAME**: 새 사용자의 사용자명 (필수).
- **USER_FULL_NAME**: 새 사용자의 전체 이름 (필수).
- **USER_PASSWORD**: 새 사용자의 비밀번호 (필수).

#### 옵션

- --is_superuser, -su: 새 사용자를 관리자(슈퍼유저)로 지정하는 플래그.
- --valid_until, -vu: 계정 만료일을 YYYY-MM-DD HH:MI:SS 형식으로 설정합니다. 설정하지 않으면 계정에 만료일이 없습니다.

#### 예제

사용자명 jdoe, 전체 이름 John Doe, 비밀번호 password123인 새 사용자를 추가하려면:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
계정 만료일을 설정하여 새 사용자를 추가하려면:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
delete-user 명령은 digna CLI에서 기존 사용자를 digna 시스템에서 제거하는 데 사용됩니다.
  
##### 명령 사용법
bash
dignacli delete-user USER_NAME

  
#### 인수
- **USER_NAME**: 삭제할 사용자의 사용자명 (필수). 이 명령이 요구하는 유일한 인수입니다.

#### 예제
bash
dignacli delete-user jdoe

  
이 명령을 실행하면 사용자 jdoe의 접근 권한이 해제되고 저장소에서 해당 사용자의 관련 데이터와 권한이 삭제됩니다.

###   modify-user

modify-user 명령은 digna CLI에서 기존 사용자의 세부 정보를 업데이트하는 데 사용됩니다.

##### 명령 사용법
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### 인수
  
- **USER_NAME**: 수정할 사용자의 사용자명 (필수).
- **USER_FULL_NAME**: 사용자의 새 전체 이름 (필수).
  
#### 옵션  
  
- --is_superuser, -su: 사용자를 슈퍼유저로 설정하여 권한을 상승시킵니다. 이 플래그는 값이 필요 없습니다.  
- --valid_until, -vu: 계정 만료일을 YYYY-MM-DD HH:MI:SS 형식으로 설정합니다. 제공하지 않으면 계정은 무기한 유효합니다.  
  
#### 예제
  
사용자 jdoe의 전체 이름을 "Johnathan Doe"로 수정하고 해당 사용자를 슈퍼유저로 설정하려면:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
modify-user-pwd 명령은 digna CLI에서 기존 사용자의 비밀번호를 변경하는 데 사용됩니다.
  
##### 명령 사용법
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### 인수
  
- **USER_NAME**: 비밀번호를 변경할 사용자의 사용자명 (필수).
- **USER_PWD**: 사용자의 새 비밀번호 (필수).
  
#### 예제
  
사용자 jdoe의 비밀번호를 newpassword123으로 변경하려면:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

list-users 명령은 digna CLI에서 digna 시스템에 등록된 모든 사용자의 목록을 표시합니다.

##### 명령 사용법

bash
dignacli list-users


이 명령을 실행하면 digna 저장소에 연결하여 모든 사용자를 나열하며, ID, 사용자명, 전체 이름, 슈퍼유저 여부 및 만료 타임스탬프를 표시합니다.

# 저장소 관리

###   upgrade-repo
  
upgrade-repo 명령은 digna CLI에서 digna 저장소를 업그레이드하거나 초기화하는 데 사용됩니다. 이 명령은 업데이트를 적용하거나 저장소 인프라를 처음 설정할 때 필수적입니다.
  
#### 명령 사용법

bash
dignacli upgrade-repo [options]

  
#### 옵션
  
- --simulation-mode, -s: 활성화하면 명령이 시뮬레이션 모드로 실행되어 실제로 SQL을 실행하지 않고 실행될 SQL 문을 출력합니다. 변경 사항을 미리 확인하고 실제 수정 없이 검토할 때 유용합니다.  

  
#### 예제
  
digna 저장소를 업그레이드하려면 옵션 없이 명령을 실행할 수 있습니다:
  
bash
dignacli upgrade-repo
  
시뮬레이션 모드로 업그레이드를 실행하여 SQL 문을 확인하려면:
  
bash
dignacli upgrade-repo --simulation-mode

  
이 명령은 데이터베이스 스키마 및 기타 저장소 구성요소가 소프트웨어의 최신 버전과 일치하도록 유지하는 데 중요합니다.

###   encrypt
  
encrypt 명령은 digna CLI에서 비밀번호를 암호화하는 데 사용됩니다.
  
#### 명령 사용법
  
bash
dignacli encrypt <PASSWORD>

    
#### 인수
- **PASSWORD**: 암호화할 비밀번호 (필수).
  
#### 예제
  
비밀번호를 암호화하려면 비밀번호를 인수로 제공해야 합니다.  
예를 들어 mypassword123을 암호화하려면 다음과 같이 사용합니다:
bash
dignacli encrypt mypassword123

이 명령은 제공된 비밀번호의 암호화된 버전을 출력하며, 이는 보안 컨텍스트에서 사용할 수 있습니다. 비밀번호 인수가 제공되지 않으면 CLI는 누락된 인수에 대한 오류를 표시합니다.

###   generate-key
  
generate-key 명령은 Fernet 키를 생성하는 데 사용되며, 이는 digna 저장소에 저장된 비밀번호를 보호하는 데 필수적입니다.
  
#### 명령 사용법
bash
dignacli generate-key

  
## 데이터 관리

###   clean-up

clean-up 명령은 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로파일, 예측 및 Traffic Light System 데이터(트래픽 라이트 시스템 관련 데이터)를 제거하는 데 사용됩니다. 이 명령은 데이터 수명 주기 관리를 위해 필수적이며, 오래되었거나 불필요한 데이터를 정리하여 조직적이고 효율적인 데이터 환경을 유지하는 데 도움이 됩니다.

#### 명령 사용법

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### 인수
  
- **PROJECT_NAME**: 데이터를 제거할 프로젝트 이름 (필수). 이 인수에 all-projects 키워드를 사용하면 digna가 모든 기존 프로젝트를 반복하며 이 명령을 적용합니다.
- **FROM_DATE**: 데이터 제거의 시작 날짜 및 시간. 허용되는 형식으로는 %Y-%m-%d, %Y-%m-%dT%H:%M:%S, 또는 %Y-%m-%d %H:%M:%S가 있습니다 (필수).
- **TO_DATE**: 데이터 제거의 종료 날짜 및 시간으로 FROM_DATE와 동일한 형식을 따릅니다 (필수).
  
#### 옵션
  
- --table-name, -tn: 클린업 작업을 프로젝트 내 특정 테이블로 제한합니다.
- --table-filter, -tf: 이름에 지정된 하위 문자열이 포함된 테이블로 클린업을 제한하는 필터입니다.
- --timing, -tm: 완료 후 클린업 프로세스의 소요 시간을 표시합니다.
- --help: clean-up 명령에 대한 도움말 정보를 표시하고 종료합니다.
  
#### 예제
  
ProjectA 프로젝트에서 2023년 1월 1일부터 2023년 6월 30일까지의 데이터를 제거하려면:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
특정 테이블 Table1에서만 데이터를 제거하려면:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
이 명령은 저장 공간 관리를 돕고 저장소에 관련 있는 정보만 남도록 보장합니다.

###   inspect

inspect 명령은 지정된 프로젝트 내 하나 이상의 데이터 소스에 대해 프로파일, 예측 및 Traffic Light System 데이터를 생성하는 데 사용됩니다. 이 명령은 정의된 기간 동안 데이터를 분석하고 모니터링하는 데 도움이 됩니다.

#### 명령 사용법

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### 인수
  
- **PROJECT_NAME**: 검사를 수행할 프로젝트 이름 (필수). 이 인수에 all-projects 키워드를 사용하면 digna가 모든 기존 프로젝트를 반복하며 이 명령을 적용합니다.
- **FROM_DATE**: 데이터 검사의 시작 날짜 및 시간. 허용되는 형식으로는 %Y-%m-%d, %Y-%m-%dT%H:%M:%S, 또는 %Y-%m-%d %H:%M:%S가 있습니다 (필수).
- **TO_DATE**: 데이터 검사의 종료 날짜 및 시간으로 FROM_DATE와 동일한 형식을 따릅니다 (필수).
  
#### 옵션

- --table-name, -tn: 검사를 프로젝트 내 특정 테이블로 제한합니다.
- --table-filter, -tf: 이름에 지정된 하위 문자열이 포함된 테이블만 검사하도록 필터링합니다.
- --force-profile: 프로파일 재수집을 강제합니다. 기본값은 force-profile입니다.
- --no-force-profile: 프로파일 재수집을 방지합니다.
- --force-prediction: 예측 재계산을 강제합니다. 기본값은 force-prediction입니다.
- --no-force-prediction: 예측 재계산을 방지합니다.
- --force-alert-status: 알림 상태 재계산을 강제합니다. 기본값은 force-alert-status입니다.
- --no-force-alert-status: 알림 상태 재계산을 방지합니다.
- --timing, -tm: 완료 후 검사 프로세스의 소요 시간을 표시합니다.
- --alert-notification, -an: 구독 채널로 알림을 전송합니다.
  
#### 예제
  
ProjectA 프로젝트에서 2024년 1월 1일부터 2024년 1월 31일까지의 데이터를 검사하려면:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
특정 테이블만 검사하고 예측 재계산을 강제하려면:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

이 명령은 업데이트된 프로파일과 예측을 생성하고 데이터 무결성을 모니터링하며 지정된 프로젝트 기간 내에서 알림 시스템을 관리하는 데 유용합니다.

###   tls-status

tls-status 명령은 지정된 프로젝트의 특정 테이블에 대해 주어진 날짜의 Traffic Light System(TLS) 상태를 조회하는 데 사용됩니다. Traffic Light System은 데이터의 상태와 품질에 대한 통찰을 제공하여 주의가 필요한 문제나 알림을 표시합니다.
  
#### 명령 사용법
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### 인수
  
- **PROJECT_NAME**: TLS 상태를 조회할 프로젝트 이름 (필수).
- **TABLE_NAME**: TLS 상태가 필요한 프로젝트 내 특정 테이블 (필수).
- **DATE**: TLS 상태를 조회할 날짜, 일반적으로 %Y-%m-%d 형식 (필수).
  
#### 예제
  
ProjectA 프로젝트의 UserData라는 테이블에 대해 2024년 7월 1일의 TLS 상태를 확인하려면:

bash
dignacli tls-status ProjectA UserData 2024-07-01


이 명령은 사전 정의된 기준에 따라 명확하고 실행 가능한 상태 보고서를 제공하여 사용자가 데이터 품질을 모니터링하고 유지 관리하는 데 도움을 줍니다.

###   list-projects
  
list-projects 명령은 digna CLI에서 사용 가능한 모든 프로젝트 목록을 표시하는 데 사용됩니다.
  
#### 명령 사용법
  
bash
dignacli list-projects


이 명령은 여러 프로젝트를 관리하는 관리자 및 사용자에게 특히 유용하며 digna 저장소에 있는 사용 가능한 프로젝트를 빠르게 개요로 제공합니다.

###   list-ds

list-ds 명령은 지정된 프로젝트 내에서 사용 가능한 모든 데이터 소스 목록을 표시하는 데 사용됩니다. 이 명령은 digna 시스템에서 분석 및 관리를 위해 사용 가능한 데이터 자산을 이해하는 데 유용합니다.

#### 명령 사용법
  
bash
dignacli list-ds <PROJECT_NAME>


#### 인수
- **PROJECT_NAME**: 데이터 소스를 나열할 프로젝트 이름 (필수).
  
#### 예제
  
ProjectA라는 이름의 프로젝트에 있는 모든 데이터 소스를 나열하려면:
  
bash
dignacli list-ds ProjectA

  
이 명령은 프로젝트에서 사용 가능한 데이터 소스에 대한 개요를 제공하여 데이터 환경을 보다 효과적으로 탐색하고 관리할 수 있게 합니다.