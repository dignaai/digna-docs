---
title: digna リリース 2026.04 | Analytics Chart、Enumerations、Validation Rule Templates
description: digna リリース 2026.04 の新機能をご紹介します。本バージョンでは Analytics Chart による高度な時系列分析、再利用可能な検証ルールテンプレート、許容値の列挙 (enumerations)、および列単位の関連性条件が導入されます。
keywords: digna リリース 2026.04, digna 更新履歴, digna Data Analytics, 時系列分析, 回帰, データ検証テンプレート, enumerations, 許容値検証, データ品質ルール, データ可観測性
image: /assets/logo_square.png
---

# Changelog – Release 2026.04  

With Release 2026.04, digna significantly enhances its capabilities in analytics and data validation.  
This release introduces advanced time-series analysis, reusable validation components, and centralized value standardization.

---

## New Features  

### Analytics Chart – Time Series Analysis Without Data Science  
- New **Analytics Chart** for interactive time-series analysis  
- Built-in analytical methods:
    - Linear, quadratic and cubic regression  
    - Piecewise regression with configurable breakpoints  
    - Smoothing techniques  
    - Quantile analysis  
- Automatic identification of trends, seasonality, and pattern changes  
- Residual analysis for deeper insight into deviations  
- Time-series are automatically calculated for every dataset  

**Impact:** Enables users to understand complex data behavior over time without requiring data science expertise or external tools.

---

### Enumerations – Central Definition of Allowed Values  
- Define reusable sets of allowed values (e.g., countries, states, status codes)  
- Validate column values against predefined enumerations in **digna Data Validation**  
- Reuse enumerations across projects and data sources  
- Use enumerations everywhere via `#ENUM:MY_ENUM#`  
- All check are executed **directly in the source database**  

**Impact:** Ensures consistent and standardized data values across the organization.

---

### Validation Rule Templates – Reusable Data Quality Logic  
- Define reusable validation rules (e.g., whitespace checks, NOT NULL, format checks)  
- Apply templates across multiple datasets  
- Ensure consistent rule logic across projects  
- Reduce duplication and manual configuration  
- All check are executed **directly in the source database**  

**Impact:** Enables scalable and high-performance data validation without data movement.

---

### Statistic-Level Relevance Conditions  
- Define relevance conditions on **column level for each statistic**  
- Extends the concept of anomaly relevance conditions  
- Control when a statistic should be considered relevant
- Reduce noise by excluding non-critical situations  

**Impact:** Improves signal quality by focusing only on meaningful deviations.

---

## Data Analytics と Data Validation の拡張機能  

With this release, digna expands both **data understanding** and **data validation standardization**:

- Advanced **time-series interpretation** without data science knowledge  
- Centralized definition of **allowed values via enumerations**  
- Reusable **validation logic via templates**  
- Fine-grained control over **relevance of statistics and alerts**  

Together, these capabilities enable organizations to not only detect issues, but also **understand, standardize, and control data quality**.

---

## Who Benefits from This Release  

- **Data Engineers:** Reusable validation logic and improved control over monitoring behavior  
- **Data Quality & Governance Teams:** Standardized rules and consistent data validation across systems  
- **Analytics & BI Teams:** Better understanding of trends and deviations  
- **Platform Owners:** Increased adoption through simplified analytics and scalable validation  

---

## CLI Updates  
- 変更なし  

---