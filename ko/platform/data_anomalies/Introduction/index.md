# Data Anomalies – Automated Detection
<h1 style="display:none;">AI 기반 데이터 품질 및 관측성 모듈 – digna Data Anomalies</h1>

---

## Purpose

The **Data Anomalies** 모듈은 규칙을 작성할 필요 없이 데이터셋의 불규칙성을 자동으로 식별합니다.  
지속적으로 **데이터 전달 품질**을 모니터링하며, “정상”이 무엇인지 학습하고 실시간으로 편차를 감지합니다.

AI 기반 탐지를 사용하여 digna는 리포트, ML 모델 및 대시보드를 왜곡시킬 수 있는 누락, 중복 또는 손상된 기록과 같은 *무언의 데이터 오류(silent data errors)*를 인식합니다.

---

## Technical Overview

### Metrics analyzed

digna는 다음과 같은 데이터 측면을 지속적으로 프로파일링합니다:

- **레코드 볼륨** – 전체 행 수, 일별 또는 배치 기반  
- **결측값** – null 또는 빈 필드 탐지  
- **분포 및 히스토그램** – 데이터 형태 변화 모니터링  
- **값 범위** – 범위를 벗어난 값 또는 극단값 자동 식별  
- **유일성** – 중복 키 또는 반복 항목 검사  

### Intelligent anomaly detection

- **히스토리컬 러닝**을 사용하여 예상 경계(dynamic boundaries)를 동적으로 정의  
- **볼륨, 값 분포 또는 논리적 관계**의 편차를 감지  
- 시간대나 계절 패턴에 따라 임계값을 자동으로 조정하기 위해 AI를 활용  
- **통계적 변동**과 실제 이상치(Anomaly)를 구분  
- 데이터셋 및 컬럼별로 상세한 메트릭과 신뢰도 점수 제공  

---

## Detection Scenarios

아래는 **Data Anomalies** 모듈이 자동으로 포착하는 실제 문제 예시입니다:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | 일별 거래의 절반이 누락되거나, 배치 로드가 중복되었거나, 갑작스러운 데이터 급증 |
| **Missing or null values** | 데이터 추출은 완료되었으나 중요 컬럼이 비어 있음 |
| **Distribution drifts** | 평균 구매 금액이나 지역별 거래 수가 예기치 않게 변경 |
| **Column swaps** | ETL 과정에서 *first_name*과 *last_name* 같은 컬럼이 실수로 서로 바뀜 |
| **Unexpected categorical values** | 예: 오스트리아 도시 목록에 “Zurich”가 나타남 |
| **Sudden uniqueness loss** | 이전에 유일하던 ID가 상류 조인 오류로 인해 중복 발생 |

---

## Architecture and Execution

- **In-database execution:** 모든 이상 탐지 로직은 *데이터베이스 엔진 내부에서 실행*됩니다 (Teradata, Snowflake, Databricks, PostgreSQL 등)  
- **No data movement:** digna는 메트릭만 읽으며 원시 데이터를 외부로 전송하지 않습니다  
- **Incremental updates:** 효율성을 위해 실행마다 새 데이터 세그먼트만 분석  
- **Configurable inspection frequency:** 시간별, 일별 또는 상류 프로세스에 의해 트리거 가능  
- **Result storage:** 메트릭 및 이상 플래그는 시각화 및 알림을 위해 digna의 관측성 스키마에 기록됨  

---

## Benefits

| Area | Benefit |
|------|----------|
| **Automation** | 수백 건의 수동 SQL 또는 규칙 정의를 제거 |
| **Precision** | 고정 임계값이 놓치기 쉬운 문제들을 탐지 |
| **Scalability** | 테이블당 수백만 건의 레코드를 효율적으로 모니터링 |
| **Integration** | 추세 분석을 위해 *digna Data Analytics*와 원활하게 통합 |
| **Compliance** | **데이터의 품질 및 관측성**에 대한 지속적인 통제 보장 |
| **Transparency** | 모든 이상에 대해 신뢰도 점수, 타임스탬프 및 이유 코드 제공 |

---

## How digna Learns “Normal”

1. **프로파일링 단계:** digna가 과거 데이터셋에서 메트릭을 수집합니다.  
2. **학습 단계:** AI 모델이 계절성, 주간·일간 패턴 등 반복되는 패턴을 식별합니다.  
3. **모니터링 단계:** 이후 데이터셋은 동적으로 학습된 임계값과 비교됩니다.  
4. **알림 단계:** 통계적 신뢰 경계를 벗어나는 편차는 이상으로 제기됩니다.  

모든 모델은 설명 가능하고(deteministic), 엔터프라이즈 데이터 볼륨에 최적화되어 있습니다.

---

## Example Use Cases

- **은행 거래 시스템**의 데이터 품질 모니터링  
- **ETL 또는 데이터 웨어하우스 작업**의 로드 실패 감지  
- **통신 기록**에서 비정상 고객 활동 식별  
- **헬스케어 분석 파이프라인**에서 임상 데이터 일관성 관찰  
- **BI 및 리포팅 환경**에서 깨진 대시보드 방지

---

## Frequently Asked Questions

**Does Data Anomalies require predefined rules?**  
아니요 — 모듈이 데이터 동작으로부터 자동으로 학습합니다.

**Can I still define specific thresholds if needed?**  
예. digna는 AI 기반 탐지와 규칙 기반 탐지(*Data Validation*을 통해)를 결합할 수 있습니다.

**How are false positives minimized?**  
모듈은 적응형 학습과 통계적 신뢰도 점수를 사용하여 정상적인 계절 변동을 무시합니다.

**Where does computation happen?**  
모든 처리는 귀하의 데이터베이스 내에서 실행되며 — digna는 원시 데이터를 추출하지 않습니다.

**Is it suitable for sensitive or regulated data?**  
예. digna는 완전히 **on-premises or in private cloud**에서 실행되며 유럽 규정 준수 기준을 준수합니다.

---