<div align="center">

<br/>

<h1>E R A &nbsp; &amp; &nbsp; B A N K &nbsp; R E C O N C I L I A T I O N</h1>
<sub>— &nbsp; R C M  F I N A N C E  P I P E L I N E &nbsp; —</sub>

<br/><br/>

![Status](https://img.shields.io/badge/STATUS-COMPLETE-217346?style=for-the-badge&labelColor=000000)
![Stack](https://img.shields.io/badge/STACK-PYTHON_%7C_MySQL_%7C_PowerBI-217346?style=for-the-badge&labelColor=000000)
![Python](https://img.shields.io/badge/PYTHON-3.12-217346?style=for-the-badge&logo=python&labelColor=000000&logoColor=217346)
![MySQL](https://img.shields.io/badge/MySQL-InnoDB-217346?style=for-the-badge&logo=mysql&labelColor=000000&logoColor=217346)
![Pandas](https://img.shields.io/badge/Pandas-ETL-217346?style=for-the-badge&logo=pandas&labelColor=000000&logoColor=217346)
![PowerBI](https://img.shields.io/badge/Power_BI-DirectQuery-217346?style=for-the-badge&logo=powerbi&labelColor=000000&logoColor=217346)

<br/>



</div>

---
  <br>
  
  <div>
    <img src="https://raw.githubusercontent.com/Muntasirzx/era-bank-reconciliation/refs/heads/main/Data/Adobe%20Express%20-%2019.04.2026_00.06.10_REC%20-%20Trim.gif" width="49%"/>
    <img src="https://raw.githubusercontent.com/Muntasirzx/era-bank-reconciliation/refs/heads/main/Data/555555.png" width="49%"/>
  </div>
  
  <br>
  
---


## `〉` Overview

This project is an end-to-end ETL pipeline and Business Intelligence dashboard built to automate ERA-to-bank reconciliation in a healthcare Revenue Cycle Management context.

The pipeline ingests synthetic Electronic Remittance Advice (ERA) data alongside a simulated banking feed, applies relational SQL architecture to identify cash variances, and surfaces findings through an interactive Power BI dashboard designed for financial operations teams.

---

## `〉` The Problem

When a hospital bills an insurance payer, the reconciliation process involves two distinct data streams that must be matched: the **ERA (835 file)** stating the intended payment, and the **EFT** — the actual wire that lands in the bank account. The gap between these two is where cash leakage occurs.

<br/>

| Failure Mode | Description |
|---|---|
| **Missing Transfers** | Payer generates an ERA, but the EFT never arrives. The accounting system records the claim as settled; the cash does not exist. |
| **Short Pays** | Intermediary bank deducts a wire processing fee (1–3%). The deposited amount is fractionally less than the ERA amount, breaking exact-match lookups. |
| **Feed Noise** | A hospital bank account receives hundreds of unrelated deposits daily. Isolating ERA-related EFTs from cafeteria receipts, payroll reversals, and vendor refunds creates an operational bottleneck. |

<br/>

Large hospital systems write off material sums annually due to the absence of database infrastructure capable of tracking uncleared cash at scale.

---

## `〉` Solution Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│              ERA & BANK RECONCILIATION PIPELINE                   │
├──────────────────┬────────────────────────────────────────────────┤
│  PHASE 1         │  Python (Pandas)                               │
│  Data Generation │  Synthetic ERA + bank feed with injected       │
│                  │  variance: 65% match · 20% short pay ·         │
│                  │  15% missing · +150 noise transactions         │
├──────────────────┼────────────────────────────────────────────────┤
│  PHASE 2         │  MySQL (InnoDB)                                │
│  Relational Load │  LOAD DATA LOCAL INFILE with on-the-fly        │
│                  │  string cleaning · DECIMAL(15,2) enforcement   │
│                  │  Star-schema: tbl_era_summary + tbl_bank_feed  │
├──────────────────┼────────────────────────────────────────────────┤
│  PHASE 3         │  SQL View: vw_reconciliation_command_center    │
│  Recon Engine    │  LEFT JOIN anchored to ERA · COALESCE for      │
│                  │  nulls · CASE WHEN triage routing              │
├──────────────────┼────────────────────────────────────────────────┤
│  PHASE 4         │  Power BI (DirectQuery)                        │
│  BI Dashboard    │  KPI cards · Donut chart · Payer leakage bar   │
│                  │  Conditional formatting · Operational matrix   │
└──────────────────┴────────────────────────────────────────────────┘
```

---

## `〉` Technology Stack

<br/>

<div align="center">

**— Ingestion & Simulation —**

![Python](https://img.shields.io/badge/Python_3.12-217346?style=for-the-badge&logo=python&logoColor=217346&labelColor=000000)
![Pandas](https://img.shields.io/badge/Pandas-217346?style=for-the-badge&logo=pandas&logoColor=217346&labelColor=000000)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-217346?style=for-the-badge&logo=sqlalchemy&logoColor=217346&labelColor=000000)

**— Relational Warehouse —**

![MySQL](https://img.shields.io/badge/MySQL_InnoDB-217346?style=for-the-badge&logo=mysql&logoColor=217346&labelColor=000000)
![Schema](https://img.shields.io/badge/Star_Schema-217346?style=for-the-badge&logo=databricks&logoColor=217346&labelColor=000000)
![Views](https://img.shields.io/badge/SQL_Views_%26_CTEs-217346?style=for-the-badge&logo=postgresql&logoColor=217346&labelColor=000000)

**— Business Intelligence —**

![PowerBI](https://img.shields.io/badge/Power_BI_DirectQuery-217346?style=for-the-badge&logo=powerbi&logoColor=217346&labelColor=000000)
![DAX](https://img.shields.io/badge/DAX_Measures-217346?style=for-the-badge&logo=microsoftexcel&logoColor=217346&labelColor=000000)

</div>

<br/>

---

## `〉` Data Schema

**`tbl_era_summary`** — Anchor / Dimension Table

| Column | Type | Description |
|---|---|---|
| `Check_EFT_Number` | VARCHAR · PK | Unique 9-digit trace number from the Payer |
| `Check_Date` | DATE | Date the Payer generated the remittance |
| `Payer` | VARCHAR | Insurance company (Medicare, Blue Cross, Aetna, etc.) |
| `Expected_Bank_Deposit` | DECIMAL(15,2) | Dollar amount expected to land in the bank |

**`tbl_bank_feed`** — Fact Table

| Column | Type | Description |
|---|---|---|
| `Bank_Txn_ID` | VARCHAR · PK | Unique identifier assigned by the banking institution |
| `Deposit_Date` | DATE | Date funds cleared |
| `Check_EFT_Number` | VARCHAR · FK | Join key back to the ERA anchor |
| `Deposit_Amount` | DECIMAL(15,2) | Actual cash deposited |

**`tbl_era_claims`** — Granular Fact Table

| Column | Type | Description |
|---|---|---|
| `Claim_ID` | VARCHAR · PK | Individual patient visit identifier |
| `Check_EFT_Number` | VARCHAR · FK | Links claim to the parent check |
| `Procedure_Code` | VARCHAR | CPT / HCPCS clinical procedure code |
| `Billed_Amount` / `Allowed_Amount` | DECIMAL | Used for contractual yield calculations |

---

## `〉` Phase 1 — Data Simulation (Python)

The bank feed was generated programmatically with controlled probability distributions to stress-test the SQL engine against realistic noise conditions.

| Distribution | Share | Logic |
|---|---|---|
| **Perfect Match** | 65% | Deposit equals ERA to the penny |
| **Short Pay** | 20% | Random 1–3% wire fee deducted from expected amount |
| **Missing** | 15% | Check excluded from bank feed entirely |
| **Noise** | +150 rows | Unrelated transactions injected to validate LEFT JOIN filtering |

```python
for i, check in enumerate(checks):
    if i < match_target:
        deposit_amt = check['Expected_Bank_Deposit']
    elif i < (match_target + short_target):
        fee = round(check['Expected_Bank_Deposit'] * random.uniform(0.01, 0.03), 2)
        deposit_amt = round(check['Expected_Bank_Deposit'] - fee, 2)
    else:
        continue  # Missing — excluded from bank feed
```

---

## `〉` Phase 2 — Relational Load (MySQL)

Rather than staging raw CSVs, data was loaded directly into InnoDB with on-the-fly string cleaning to strip dollar signs and commas, and enforced `DECIMAL(15,2)` constraints.

```sql
TRUNCATE TABLE tbl_era_summary;

LOAD DATA LOCAL INFILE 'era_summary_load.csv'
INTO TABLE tbl_era_summary
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Check_EFT_Number, @raw_date, Payer, Total_Claims,
 @raw_billed, @raw_allowed, @raw_gross, @raw_adj, @raw_deposit)
SET
    Check_Date             = STR_TO_DATE(@raw_date, '%m/%d/%y'),
    Total_Billed           = CAST(REPLACE(REPLACE(@raw_billed,  '$',''),',','') AS DECIMAL(15,2)),
    Expected_Bank_Deposit  = CAST(REPLACE(REPLACE(@raw_deposit, '$',''),',','') AS DECIMAL(15,2));
```

Payer assignment was applied via ranged UPDATE statements across the full table after disabling safe-update mode:

```sql
SET SQL_SAFE_UPDATES = 0;
UPDATE tbl_era_summary SET Payer = 'BLUE CROSS' WHERE RIGHT(Check_EFT_Number, 1) IN ('1', '5');
UPDATE tbl_era_summary SET Payer = 'AETNA'      WHERE RIGHT(Check_EFT_Number, 1) IN ('2', '6');
SET SQL_SAFE_UPDATES = 1;
```

---

## `〉` Phase 3 — Reconciliation Engine (SQL View)

The engine is implemented as a SQL View, not a static table. It recalculates against the live bank feed on every query — no manual refresh required.

```sql
CREATE OR REPLACE VIEW vw_reconciliation_command_center AS
SELECT
    e.Check_EFT_Number,
    e.Payer,
    e.Expected_Bank_Deposit                           AS Expected_Amount,
    COALESCE(b.Deposit_Amount, 0)                     AS Actual_Bank_Amount,
    (COALESCE(b.Deposit_Amount, 0)
        - e.Expected_Bank_Deposit)                    AS Variance_Amount,
    CASE
        WHEN b.Deposit_Amount IS NULL
            THEN 'ESCALATE: Missing Check'
        WHEN b.Deposit_Amount = e.Expected_Bank_Deposit
            THEN 'Matched - Cleared'
        WHEN b.Deposit_Amount < e.Expected_Bank_Deposit
            THEN 'Partial: Review Short Pay'
        WHEN b.Deposit_Amount > e.Expected_Bank_Deposit
            THEN 'Audit: Overpayment'
    END AS Triage_Queue_Status
FROM tbl_era_summary e
LEFT JOIN tbl_bank_feed b
    ON e.Check_EFT_Number = b.Check_EFT_Number;
```

**Procedure-Level Yield Analysis** — CTE with window function to rank clinical procedures by contractual write-off volume:

```sql
WITH Procedure_Yield AS (
    SELECT
        Procedure_Code,
        COUNT(Claim_ID)                                              AS Volume,
        SUM(Billed_Amount)                                           AS Total_Billed,
        SUM(Allowed_Amount)                                          AS Total_Allowed,
        ROUND((SUM(Allowed_Amount) / SUM(Billed_Amount)) * 100, 2)  AS Yield_Percentage
    FROM tbl_era_claims
    GROUP BY Procedure_Code
)
SELECT
    Procedure_Code,
    Volume,
    CONCAT('$', FORMAT(Total_Billed, 2))             AS Total_Billed,
    CONCAT(Yield_Percentage, '%')                    AS Collection_Yield,
    RANK() OVER (ORDER BY SUM(Contractual_Adj) DESC) AS Leakage_Rank
FROM Procedure_Yield
LIMIT 5;
```

---

## `〉` Phase 4 — Power BI Dashboard

The dashboard connects to MySQL via **DirectQuery**, ensuring the report reflects the live database state without duplicating data into an import model.

**Data Model**

A strict `1:*` relationship is established between `vw_reconciliation_command_center` and `tbl_era_claims` on `Check_EFT_Number`, enabling bidirectional cross-filtering across all visuals.

**DAX Measures**

```dax
-- Executive KPI Cards
Total Expected Cash  = SUM('vw_reconciliation_command_center'[Expected_Amount])
Total Cleared Cash   = SUM('vw_reconciliation_command_center'[Actual_Bank_Amount])
Total Cash Variance  = SUM('vw_reconciliation_command_center'[Variance_Amount])

-- Pipeline Health
Match Rate % =
DIVIDE(
    CALCULATE(
        COUNTROWS('vw_reconciliation_command_center'),
        'vw_reconciliation_command_center'[Triage_Queue_Status] = "Matched - Cleared"
    ),
    COUNTROWS('vw_reconciliation_command_center')
)
```

**Visual Layout**

| Layer | Visual | Purpose |
|---|---|---|
| KPI Row | Card visuals | Expected cash · Cleared cash · Total variance · Match rate |
| Analytical | Donut chart | Triage status distribution by check count |
| Analytical | Clustered bar | Payer-level cash leakage ranking |
| Operational | Matrix | Daily work queue with conditional formatting on variance column |

Selecting a triage slice (e.g. `ESCALATE: Missing Check`) filters the matrix to the exact affected checks for immediate follow-up.

---

## `〉` Local Setup

### 1 · Clone the repository

```bash
git clone https://github.com/YourUsername/rcm-finance-reconciliation.git
cd rcm-finance-reconciliation
```

### 2 · Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3 · Create the database schema

```sql
CREATE DATABASE Enterprise_Recon_DB;
-- Then execute: 01_table_schemas.sql
```

### 4 · Generate and load data

```bash
python scripts/generate_realistic_bank_feed.py
python scripts/import_bank_feed.py
```

### 5 · Deploy the reconciliation view

```bash
-- Execute: 02_reconciliation_views.sql
```

### 6 · Connect Power BI

```
Open RCM_Payment_Variance_Dashboard.pbix
→ Edit Data Source Settings
→ Point to localhost:3306 / Enterprise_Recon_DB
```

---

## `〉` File Structure

```
rcm-finance-reconciliation/
├── README.md                                   # Project documentation
├── data/
│   ├── era_summary_load.csv                    # Parsed ERA header data
│   ├── era_claims_load.csv                     # Parsed granular claims data
│   └── bank_feed_load.csv                      # Simulated banking data feed
├── scripts/
│   ├── 01_generate_synthetic_era.py            # Generates initial expected ERA CSVs
│   ├── 02_generate_realistic_bank_feed.py      # Injects probability-based variance
│   └── 03_import_to_mysql.py                   # SQLAlchemy DB bulk ingestion
├── sql/
│   ├── 01_schema_creation.sql                  # Star-schema DDL scripts
│   ├── 02_reconciliation_engine.sql            # Core views and triage logic
│   └── 03_analytical_queries.sql               # RCM Yield CTEs and window functions
├── dashboard/
│   └── RCM_Payment_Variance_Dashboard.pbix     # Interactive DirectQuery dashboard
└── requirements.txt                            # Python dependencies (pandas, sqlalchemy)
```

---

## `〉` Potential Extensions

| Extension | Approach |
|---|---|
| **Cloud Migration** | Transition InnoDB to Snowflake or AWS Redshift for parallel processing at multi-million row scale |
| **API Ingestion** | Replace CSV parsers with direct connections to clearinghouse APIs (Change Healthcare, Waystar) for live 835 EDI feeds |
| **Predictive Write-Offs** | Train a classification model on historical short-pay patterns to auto-approve variances below a defined threshold |

---

<div align="center">

<br/>

![Footer](https://img.shields.io/badge/ERA_%26_Bank_Reconciliation-RCM_Finance_Pipeline-217346?style=for-the-badge&labelColor=000000&logoColor=white)

</div>
