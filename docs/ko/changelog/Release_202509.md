---
title: digna 릴리스 2025.09 | 모듈형 설계, 다섯 개의 새 모듈, OIDC 기반 MFA
description: digna 릴리스 2025.09의 신규 사항을 확인하세요. 이번 버전에서는 모듈형 아키텍처, 다섯 개의 전문 모듈, OIDC 기반 다중 요소 인증(MFA), 모듈별 알림 기능이 도입되었습니다.
keywords: digna Release 2025.09, digna 변경 로그, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna 모듈형 설계, digna OIDC MFA
image: /assets/logo_square.png
---

# 변경 로그 – 릴리스 2025.09

릴리스 2025.09에서 digna는 새로운 **모듈형 아키텍처**를 도입하고 데이터 품질 및 관측성(Observability)을 위한 **다섯 개의 전문 모듈**을 출시합니다.  
이번 릴리스는 또한 인증을 강화하고 플랫폼 전반의 알림 처리 방식을 개선합니다.

---

## 🚀 새로운 기능

### 모듈형 설계
- digna가 이제 **모듈형 아키텍처**를 따릅니다.  
- 고객은 필요한 모듈만 활성화하고 요구사항이 커지면 추가할 수 있습니다.  
- 이전 기능들은 이제 **digna Data Anomalies**의 일부로 통합되었습니다.  

### 새 모듈
- **digna Data Anomalies** – 데이터 볼륨, 분포, 결측값 등에서 이상을 감지하는 AI 기반 탐지 기능.  
- **digna Data Analytics** – 관측성 메트릭의 시계열 평가를 통해 장기 추세와 변동성을 탐지합니다.  
- **digna Data Timeliness** – 예상 데이터 도착 시간 모니터링(규칙 기반 및 AI 기반 모두 지원).  
- **digna Data Validation** – 비즈니스 규칙 준수를 보장하는 레코드 수준의 규칙 기반 검사.  
- **digna Data Schema Tracker** – 모니터링 대상 데이터베이스의 스키마 변경(DDL 수정) 감지.  

### OIDC 기반 MFA
- OIDC 싱글 사인온으로 **다중 요소 인증(MFA)**을 지원합니다.  
- 모든 사용자 로그인을 위한 엔터프라이즈급 보안을 제공합니다.  

### 모듈별 알림 이메일
- 알림이 이제 **모듈별로** 전송되어 Data Anomalies, Data Analytics 등 각 모듈의 경고를 쉽게 구분할 수 있습니다.  

---

## 🛠 CLI 업데이트

- **새 명령: `inspect-cancel`** – 요청 ID로 검사를 취소하거나 활성 요청을 모두 종료합니다.  
- **새 명령: `check-config`** – 시작 전 구성 파일을 검증합니다.  
- **새 명령: `remove-orphans`** – 고아화된 리포지토리 항목을 정리합니다.  
- **강화된 `inspect` 명령** – 새로운 옵션 `--bypass-backend` (`-bb`)와 표준화된 반환 코드 (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 문서
- 신규 가이드:  
  - Single Sign-On 통합 가이드