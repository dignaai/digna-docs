---
title: 데이터베이스 연결 | digna 문서
description: 기존 digna 프로젝트에 데이터베이스를 연결하는 단계별 가이드입니다. 연결 구성, 자격 증명 제공 및 보안 액세스 활성화 방법을 알아보세요.
---

# 데이터베이스 연결

이 가이드는 프로젝트에 데이터베이스 연결을 추가하기 위한 최소 단계들을 보여줍니다.

## 인터랙티브 데모

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="프로젝트에 데이터베이스 연결"
    frameborder="0"
    loading="lazy"
    webkitallowfullscreen
    mozallowfullscreen
    allowfullscreen
    allow="clipboard-write"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;">
  </iframe>
</div>
<!--ARCADE EMBED END-->

---

### 단계

1. **프로젝트 열기**  
   왼쪽 탐색에서 **Projects**를 클릭하고 대상 프로젝트를 선택합니다.

2. **연결 추가**  
   **Connections**로 이동하여 **Add Connection**을 클릭합니다.

3. **데이터베이스 유형 선택**  
   연결할 데이터베이스를 선택합니다(예: PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **연결 세부정보 입력**  
   **Name**, **Host**, **Port**, **Database/Service**, 그리고 **Credentials**(해당하는 경우 username/password 또는 SSO)를 입력합니다.

5. **테스트 및 저장**  
   **Test**를 클릭합니다. 성공하면 **Save**를 클릭합니다. 연결이 프로젝트의 **Connections**에 표시됩니다.