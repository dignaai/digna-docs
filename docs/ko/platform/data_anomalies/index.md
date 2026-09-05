---
title: digna Data Anomalies | AI 기반 데이터 관찰성
description: digna Data Anomalies는 digna Data Observability Platform의 일부입니다. 이 모듈은 데이터베이스, 데이터 레이크 및 웨어하우스 전반에서 데이터의 패턴을 자동으로 학습하고 이상을 감지하여 데이터 품질과 관찰성을 향상시킵니다.
tags:
  - 데이터 품질
  - 데이터 관찰성
  - 데이터의 품질
  - 데이터의 관찰성
  - AI 기반 모니터링
  - 이상 탐지
  - digna
  - digna 플랫폼
hide:
  - toc                # optional: hide the small top-level TOC if you use inline nav
  - navigation         # optional: hide side navigation for standalone pages
image: /assets/logo_square.png
---


# digna Data Anomalies – AI 기반 데이터 품질 문제 감지

**항상 신뢰할 수 있는 데이터 관찰을 위한 AI 기반 솔루션**

digna Data Anomalies는 **digna Data Observability Platform**의 일부로, 데이터셋이 시간에 따라 어떻게 동작하는지 지속적으로 분석하여 **데이터 품질**을 개선하는 모듈식 솔루션입니다.

이 모듈은 데이터의 “정상” 상태가 어떤지 자동으로 학습하고, 동작이 변할 때 경고를 발생시킵니다 — 정적 임계값을 정의하거나 규칙을 하나도 작성할 필요가 없습니다.  
모듈은 고객 데이터베이스 내부에서 직접 실행되므로 데이터가 환경을 벗어나지 않습니다.

---

## digna Data Anomalies의 목적

**digna Data Anomalies** 모듈은 다음과 같은 사전 정의된 통계 지표를 계산하고 추적하여 지속적인 **데이터 관찰성**을 제공합니다:

- 데이터 볼륨 및 레코드 수  
- 결측값 비율  
- 값 분포 및 히스토그램  
- 수치 범위 및 평균  
- 컬럼 중복성(uniqueness) 및 텍스트 길이  

이 지표들은 모든 데이터셋에 대해 자동으로 수집됩니다.  
digna는 이를 사용해 각 지표의 전형적인 동작을 나타내는 모델을 구축하며 — 일간, 주간 또는 계절적 패턴을 학습합니다.  
모델이 학습된 후에는 새로운 데이터에 대해 예측값을 산출하고, 품질 문제, 프로세스 실패 또는 상류 변경을 나타낼 수 있는 편차를 감지합니다.

---

## 주요 기능

- AI를 사용해 예상되는 데이터 동작을 자동으로 학습 — 임계값 설정 불필요.  
- 데이터 볼륨 및 분포에서의 갑작스런 감소, 급증 또는 드리프트를 감지.  
- 컬럼이 서로 바뀌었거나 속성 간 매핑이 잘못된 경우 식별.  
- 예상치 못한 범주형 값(예: 새로운 지역 또는 코드) 강조.  
- 숫자형, 범주형 또는 지정되지 않은 모든 컬럼 유형 지원.  
- 완전히 고객 환경 내에서 동작 — 데이터 이동 없음.  
- 장기 추세 분석을 위해 **digna Data Analytics**와 통합.

---

## 작동 원리

### Step 1 – Metric calculation
digna는 각 테이블과 컬럼에 대해 프로파일 지표 집합을 계산합니다.  
이 지표들은 데이터의 구조와 통계적 동작을 설명하며 추가 분석을 위해 저장됩니다.

### Step 2 – Model training
과거 지표 값을 바탕으로 digna는 각 지표의 정상 범위를 포착하는 컴팩트한 머신러닝 모델(시그니처 모델)을 학습합니다.

### Step 3 – Automatic thresholding
*conformal inference*을 사용하여 digna는 데이터와 함께 진화하는 적응형 신뢰구간(자동 임계값)을 계산합니다.  
새로운 지표 값이 예측된 범위를 벗어나면 이상으로 표시됩니다.

이 지속적인 피드백 루프는 데이터 볼륨이나 패턴이 자연스럽게 성장하더라도 모니터링이 관련성을 유지하도록 보장합니다.

---

## 예시 시나리오

### 레코드 볼륨의 예상치 못한 감소
어떤 데이터셋은 일반적으로 하루에 약 500,000개의 레코드를 포함합니다.  
새로운 전달이 50,000개의 레코드만 포함한 경우, digna는 이상을 표시하고 학습된 범위에서 얼마나 벗어났는지 보여줍니다.

### 컬럼 스왑 감지
`last_name`의 평균 문자열 길이가 갑자기 `first_name`과 일치합니다.  
digna는 지표 패턴의 편차를 인식하고 컬럼 교환 가능성을 신호로 보냅니다.

### 예상치 못한 범주 감지
오스트리아 도시를 나열하는 컬럼에 갑자기 "Zurich"가 포함됩니다.  
과거 분포를 기반으로 digna는 새로운 값을 예상 밖으로 표시하고 사용자에게 경고합니다.

---

## 다른 모듈과의 통합

- **digna Data Analytics** — 이상 이력과 변동성 지표를 집계하여 장기 추세를 드러냄.  
- **digna Data Validation** — 결정론적 품질 검사를 위한 명시적 비즈니스 규칙 적용.  
- **digna Data Timeliness** — 데이터 도착 시간을 모니터링하고 지연을 이상 발생과 상관시킴.  
- **digna Data Schema Tracker** — 새로운 이상을 설명할 수 있는 구조적 변경 감지.

---

## 전형적인 사용 사례

- 누락되거나 중복된 데이터 로드 감지.  
- 교환되거나 잘린 컬럼 식별.  
- 숫자형 또는 범주형 특성의 분포 드리프트 감지.  
- 예상치 못한 참조 값 또는 코드 발견.  
- 연속 수집 파이프라인의 불규칙성 모니터링.  
- 도메인 전반에 걸친 전체적인 **데이터 품질 및 관찰성** 추적.

---

## 이점

- 비정상적인 데이터 동작의 즉각적 탐지.  
- 수동 임계값 튜닝 제거.  
- 대규모 데이터 환경에서 운영 효율성 감소.  
- 분석 및 리포팅 시스템에 대한 신뢰 구축.  
- **데이터 품질**과 종단간 **데이터 관찰성** 강화.

---

## Related digna Modules

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trend and volatility metrics.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — rule-based data verification.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — monitoring data delivery schedules.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — schema change detection.

---

## 요약

**digna Data Anomalies** 모듈은 digna의 AI 기반 **Data Observability Platform**의 핵심을 형성합니다.  
핵심 지표를 지속적으로 모니터링하고, 패턴을 학습하며, 편차를 식별함으로써 조직이 **데이터 품질**을 신뢰할 수 있고, 안정적이며 설명 가능하도록 유지하는 데 도움을 줍니다 — 수동 구성 없이도.