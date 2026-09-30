---
title: digna 릴리스 2026.06 | Python SDK, Docker 배포 및 향상된 검증 관리
description: digna 릴리스 2026.06의 변경사항을 확인하세요. 이번 버전은 새로운 digna Python SDK, Docker 배포 지원, 새로워진 대시보드 경험, 그리고 검증 규칙 관리의 향상된 이식성을 도입합니다.
keywords: digna Release 2026.06, digna Python SDK, digna Docker support, 데이터 품질 자동화, 데이터 프로파일링, 검증 규칙 가져오기 내보내기, digna 대시보드, 데이터 관측성 플랫폼, Python API, 메타데이터 자동화
image: /assets/logo_square.png
---

# 변경 로그 – 릴리스 2026.06  

릴리스 2026.06을 통해 digna는 자동화, 확장성 및 플랫폼 사용성 측면에서 큰 진전을 이루었습니다.  
이번 버전은 새로운 **digna Python SDK**, 공식 **Docker 배포 지원**, 새로워진 대시보드 경험, 그리고 검증 규칙 관리를 위한 향상된 이식성을 제공합니다.

---

## 릴리스 영상 보기

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — digna YouTube 채널에서 이번 릴리스를 살펴봅니다.*

---

## 새로운 기능  

### digna Python SDK – Python으로 모든 것을 자동화  
- 설치 방법:
  ```bash
  pip install digna-sdk
  ```
- Python으로 digna를 프로그래밍 방식으로 관리하고 자동화  
- 코드로 프로젝트 생성 및 구성  
- 검사 및 모니터링 실행 트리거  
- 데이터셋, 규칙 및 구성의 프로그래밍적 관리  
- 테이블 프로파일링 및 메타데이터 인사이트 추출  
- 프로파일링 및 데이터 품질 결과를 외부 리포지토리 및 시스템으로 내보내기  
- 노트북, 오케스트레이션 도구 및 CI/CD 파이프라인과 통합  

**영향:** Python을 사용한 인프라스트럭처 코드(Infrastructure-as-Code)와 데이터 품질 및 관측성 워크플로의 심층 자동화를 가능하게 합니다.

---

### Docker 지원 – 간소화된 배포 및 운영  
- digna 공식 Docker 이미지 지원  
- 환경 전반에 걸친 빠르고 일관된 설정  
- 개발, 테스트 및 프로덕션의 간소화된 온보딩  
- Kubernetes 및 컨테이너 플랫폼과의 쉬운 통합  
- 배포의 이식성 및 재현성 향상  

**영향:** 현대 클라우드 네이티브 아키텍처에서 digna를 더 쉽게 배포하고 운영할 수 있게 합니다.

---

### QueryMode – 유연한 SQL 실행 전략

쿼리 실행 전략 구성: **Single** 또는 **Combined** 모드

**Single Mode**: 각 통계는 전용 SQL 쿼리 하나로 계산됩니다

  - 메모리 제약이 있는 대형 데이터 소스에 이상적
  - 결합 쿼리로 인한 리소스 고갈(메모리 부족, 스풀 한도 등)을 방지
  - 쿼리 수는 많아지지만 쿼리당 메모리 사용량은 낮음

**Combined Mode**: 모든 통계가 단일 SQL 쿼리 내에서 계산됩니다

  - 전체 쿼리 수 및 네트워크 오버헤드 감소
  - 데이터 소스를 메모리에서 관리할 수 있을 때 성능 최적화
  - 빈번하고 병렬 실행되는 작업에 더 효율적

**영향:** 사용자가 데이터 소스 특성에 따라 성능, 리소스 사용량 및 메모리 안정성의 균형을 맞출 수 있도록 세밀한 쿼리 실행 제어를 제공합니다.

---

### 구성 가능한 예측 모델

이상 탐지의 기반이 되는 모델은 이제 각 계열에 대해 경쟁하는 여러 설명(패턴과 최근 관측값에 대한 해석의 조합)을 비교 평가하고, 각 설명이 얼마나 강하게 뒷받침되는지에 따라 예측을 혼합합니다. 단일 극단값이 이후 예측으로 번지는 일은 더 이상 없습니다.

데이터 소스의 새 **Model** 탭에 있는 두 가지 설정으로 모델을 조정하며, 각 설정의 범위는 `0.0`에서 `1.0`이고 기본값은 `0.5`입니다:

- **Break Sensitivity** – 새로운 수준으로의 도약이나 추세 전환을 이상값으로 처리하지 않고 실제 변화로 받아들이는 속도
- **Model Complexity** – 모델이 찾는 구조의 정도. 달력 효과와 단일 수준 이동부터 알려지지 않은 주기, 월중 일자 효과, 월별 리셋까지

두 설정 모두 언제든지 기본값으로 되돌릴 수 있습니다. 각 설정의 작동 방식은 [모델 설정](../platform/data_anomalies/how_it_works.md#model-settings)을 참조하십시오.

**영향:** 허용 구간에 대한 기존 Sensitivity 및 Memory 설정(이제 **Thresholds** 탭에 있음)과 함께, 예측 모델 자체에 대한 제어 권한을 사용자에게 제공합니다.

---

### 이상 알림 제어

- 데이터 소스의 이상 설정에 새 **Notifications** 탭 추가:
  - **Minimum Alerts** – 알림이 전송되기 전에 한 검사에서 필요한 실패한 체크(불확실한 체크 제외) 수(기본값 `1`)
  - **Pause After Notification (Days)** – 데이터 소스에 대해 알림을 보낸 후 구독이 알림을 보내지 않는 기간(기본값 `0`, 일시 중지 없음)
- 이제 검사 자체가 실패하면 구독자에게 알림이 전송됩니다(**Notify Inspection Errors**)
- 모든 알림은 해당 페이지, 즉 검사의 실패한 체크 또는 Schema Tracker 및 Timeliness 보기로 바로 연결됩니다
- 더 명확해진 구독 스위치: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

**알림 작동 방식:** 알림은 **알림 채널**(Email(SMTP 연결 사용), Slack 또는 Jira)을 통해 전송되며, 알림 채널은 관리자가 설정하고 **Test Notification Channel**로 확인할 수 있습니다. **구독**은 채널을 프로젝트에 연결합니다. 구독은 모든 데이터 소스 또는 선택한 데이터 소스를 대상으로 하며, 스위치로 무엇을 보고할지 선택합니다. 각 모듈(Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker 및 데이터 볼륨 체크), 완전히 실패한 검사, 그리고 선택적으로 통과한 검사까지 포함할 수 있습니다.

**영향:** 알림은 줄고 더 실행 가능해집니다. 고립된 편차와 지속되는 이상이 더 이상 채널을 가득 채우지 않습니다.

---

### 새로워진 대시보드 경험  
- 현대화된 UI/UX 디자인  
- 더 명확한 내비게이션 및 구조  
- 모니터링 결과 및 데이터 품질 인사이트의 가시성 향상  
- 알림, 통계 및 대시보드의 가독성 개선  
- 주요 운영 정보에 대한 더 빠른 접근성  

**영향:** 모든 사용자의 사용성 및 일상 생산성을 향상시킵니다.

---

### 검증 규칙의 확장된 가져오기 및 내보내기  
- 검증 규칙에 대한 향상된 가져오기/내보내기 기능  
- 환경 및 프로젝트 간 마이그레이션 용이성  
- 표준화된 규칙 세트의 재사용성 향상  
- 규칙 거버넌스 및 라이프사이클 관리 개선  
- 팀 간 협업 단순화  

**영향:** 조직 전반에서 확장 가능하고 일관된 데이터 품질 거버넌스를 가능하게 합니다.

---

## 플랫폼 개선사항  

- 자동화를 위한 전체 Python SDK 통합  
- Docker를 통한 컨테이너화된 배포  
- 새로워진 대시보드를 통한 UX 개선  
- 검증 로직의 이식성 확장  

---

## 이 릴리스의 혜택 대상  

- 데이터 엔지니어: 자동화, SDK 활용, 파이프라인 통합  
- 플랫폼 팀: Docker를 통한 간소화된 배포  
- 데이터 거버넌스 팀: 재사용 가능한 검증 규칙 관리  
- 분석 팀: 향상된 사용성 및 인사이트 가시성  

---

## CLI 업데이트  
- SDK 통합 지원 추가  
- 가져오기/내보내기 워크플로 개선  
- 전반적인 안정성 및 성능 향상