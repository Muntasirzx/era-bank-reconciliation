-- Create the Database
CREATE DATABASE IF NOT EXISTS Enterprise_Recon_DB;
USE Enterprise_Recon_DB;

-- 1. Dimension Table: Expected ERA Summary
CREATE TABLE IF NOT EXISTS tbl_era_summary (
    Check_EFT_Number VARCHAR(50) PRIMARY KEY,
    Check_Date DATE,
    Payer VARCHAR(100),
    Total_Claims INT,
    Total_Billed DECIMAL(15, 2),
    Total_Allowed DECIMAL(15, 2),
    Gross_Provider_Paid DECIMAL(15, 2),
    Provider_Adjustment DECIMAL(15, 2),
    Expected_Bank_Deposit DECIMAL(15, 2)
);

-- 2. Fact Table: Raw Bank Feed
CREATE TABLE IF NOT EXISTS tbl_bank_feed (
    Bank_Txn_ID VARCHAR(50) PRIMARY KEY,
    Deposit_Date DATE,
    Check_EFT_Number VARCHAR(50),
    Payer_Name VARCHAR(100),
    Deposit_Amount DECIMAL(15, 2),
    Transaction_Type VARCHAR(50),
    Status VARCHAR(50)
);

-- 3. Granular Fact Table: Claim Lines
CREATE TABLE IF NOT EXISTS tbl_era_claims (
    Claim_ID VARCHAR(50) PRIMARY KEY,
    Check_EFT_Number VARCHAR(50),
    Procedure_Code VARCHAR(20),
    Billed_Amount DECIMAL(15, 2),
    Allowed_Amount DECIMAL(15, 2),
    Contractual_Adj DECIMAL(15, 2),
    Provider_Paid DECIMAL(15, 2)
);