---
title: Data Validation – 규칙 기반 검사로 컴플라이언스 및 감사 가능성 확보 | digna Documentation
description: digna Data Validation이 임계값, 범위, 참조 목록을 포함한 결정론적 규칙 기반 검사를 어떻게 적용하는지 알아보세요. 금융, 의료 및 기타 데이터 민감 산업에서 컴플라이언스, 감사 가능성 및 규제 보고를 보장합니다.
image: /assets/logo_square.png
keywords:
  - 데이터 유효성 검사
  - 규칙 기반 데이터 검사
  - 데이터 품질
  - 데이터의 품질
  - 데이터 관찰성
  - 임계값 및 범위
  - 참조 목록 검증
  - 감사 가능성
  - 컴플라이언스 모니터링
  - digna data validation
lang: ko
robots: index, follow
og_title: Data Validation – Rule-Based Checks for Compliance & Auditability | digna Documentation
og_description: digna Data Validation은 임계값, 범위, 참조 목록을 사용한 결정론적 규칙 기반 검사를 시행합니다. 규제 산업을 위해 설계되어 컴플라이언스, 투명성 및 감사 가능성을 보장합니다.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Rule-Based Checks
<h1 style="display:none;">AI 기반 Data Validation 모듈 — 데이터 품질 및 관찰성을 위한 digna</h1>

---

## 목적

The **Data Validation** 모듈은 **데이터 품질**을 정밀한 규칙 기반 검사로 보장합니다.  
조직이 결정론적 비즈니스 및 기술 유효성 검사 로직을 정의할 수 있도록 하여, 데이터가 컴플라이언스 표준, 계약상 SLA 및 규제 요구사항을 충족하도록 합니다.

*데이터베이스 내 규칙 실행*, *완전한 감사 추적*, 및 *다른 digna 모듈과의 통합*을 결합함으로써, **Data Validation**은 복잡한 엔터프라이즈 환경 전반에 걸쳐 일관되고 추적 가능한 **데이터 품질 및 관찰성**을 보장합니다.

---

## 기술 개요

### 지원되는 유효성 검사 유형

- **일치 검사**  
  값이 예상 결과와 일치하는지 확인합니다 (예: 참조 코드, Boolean 플래그, 범주 매핑).

- **임계값 및 범위**  
  숫자 측정값 또는 KPI를 정의된 한계(정적 또는 동적으로 도출됨)에 대해 검증합니다.

- **참조 목록 및 조회**  
  필드 값이 승인된 마스터 데이터 세트 내에 존재하는지 확인합니다 (예: VAT 코드, ISO 국가 목록, 제품 카탈로그).

- **열 간 일관성**  
  관계적 정합성을 보장합니다 (예: 통화가 지역과 일치하는지, 리스크 카테고리가 자산 유형과 일치하는지).

- **널 처리 규칙**  
  중요 열에서 예상치 못한 null 또는 빈 값을 감지합니다.

### 실행 및 로깅

- **데이터베이스 내 처리** – 모든 유효성 검사 규칙은 귀하의 데이터베이스(Teradata, Snowflake, Databricks, PostgreSQL 등)에서 직접 실행됩니다.  
- **데이터 추출 없음** – digna는 원시 데이터를 고객 환경 외부로 전송하지 않습니다.  
- **완전한 추적성** – 각 규칙 결과는 타임스탬프, 대상 데이터셋, 레코드 수 및 통과/실패 결과와 함께 기록됩니다.  
- **감사**