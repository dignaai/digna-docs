# 매일 실행되는 작업 예약 방법

스케줄링을 통해 수동 개입 없이 검사를 자동으로 실행할 수 있습니다.  
이 가이드에서는 **하루에 한 번** 실행되는 작업을 생성하여 데이터가 지속적으로 모니터링되도록 설정하는 방법을 설명합니다.

---

## 인터랙티브 데모

과정을 직접 확인하려면 인터랙티브 튜토리얼을 따라하세요:  

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/Ra9E19A0QfMpzKqm3Yhu?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a New Data Inspection Job" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## 학습 목표

- digna 대시보드에서 **Scheduling** 섹션에 접근하는 방법  
- 새 예약 작업을 생성하는 방법  
- **일정한 시간에 매일** 실행되도록 구성하는 방법  
- 올바른 프로젝트와 데이터소스를 선택하는 방법  
- 작업이 자동으로 실행되도록 활성화하는 방법  

---

## 일일 작업이 유용한 이유

일일 스케줄은 운영 환경에서 가장 일반적인 설정입니다. 이를 통해 다음을 보장합니다:  

- **신선도(Freshness)** — 매일의 데이터가 검증됩니다.  
- **일관성(Consistency)** — 이상치가 하류로 전파되기 전에 조기에 발견됩니다.  
- **자동화(Automation)** — 검사를 수동으로 트리거할 필요가 없습니다.  

---

## 다음 단계

- 자세한 맞춤 스케줄은 [How to use crontab definition](how_to_use_crontab.md)를 참고하세요.  
- 일일 작업을 **alerting**과 결합하여 이상이 감지되었을 때 알림을 받도록 설정하세요.