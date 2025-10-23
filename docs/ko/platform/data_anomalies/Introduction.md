---
title: Data Anomalies – Automated Detection | digna Documentation
description: digna Data Anomalies가 수동 규칙 없이 볼륨 감소, 결측값, 분포 변화 및 예상치 못한 패턴을 자동으로 감지하는 방법을 확인하세요. AI 기반 이상 탐지로 데이터 품질을 향상시킵니다.
---

# Data Anomalies – Automated Detection

## Purpose
규칙을 작성하지 않고 이상을 포착합니다.

## Technical Features
### Metrics analyzed
- 레코드 수  
- 결측값  
- 분포 및 히스토그램  
- 값 범위  
- 유일성  

### Intelligent detection
- **과거 학습**을 사용하여 예상 범위를 동적으로 정의합니다  
- 실제 데이터가 예상 범위를 벗어나면 이상으로 표시합니다  

## Detection Scenarios
- **볼륨 감소/급증** → 예: 일일 거래의 절반이 누락됨  
- **열 교환** → 이름(first name)과 성(last name) 컬럼이 뒤바뀜  
- **예상치 못한 값** → 오스트리아 도시 목록에 “Zurich”가 나타남  

## Value
보통 수백 개의 수동 규칙이 필요한 작업을 자동화합니다.