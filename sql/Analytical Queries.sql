USE Enterprise_Recon_DB;

-- Query 1: The Executive Summary (The "CFO View")
SELECT 
    Triage_Queue_Status,
    COUNT(Check_EFT_Number) AS Total_Checks,
    CONCAT('$', FORMAT(SUM(Expected_Amount), 2)) AS Total_Expected_Cash,
    CONCAT('$', FORMAT(SUM(Actual_Bank_Amount), 2)) AS Total_Cleared_Cash,
    CONCAT('$', FORMAT(SUM(Variance_Amount), 2)) AS Total_Variance
FROM vw_reconciliation_command_center
GROUP BY Triage_Queue_Status
ORDER BY SUM(Variance_Amount) ASC;


-- Query 2: Revenue Leakage by Procedure Code (The "RCM Yield View")
WITH Procedure_Yield AS (
    SELECT 
        Procedure_Code,
        COUNT(Claim_ID) AS Volume,
        SUM(Billed_Amount) AS Total_Billed,
        SUM(Allowed_Amount) AS Total_Allowed,
        SUM(Contractual_Adj) AS Total_Write_Off,
        
        -- Calculate the Yield Percentage
        ROUND((SUM(Allowed_Amount) / SUM(Billed_Amount)) * 100, 2) AS Yield_Percentage
    FROM tbl_era_claims
    GROUP BY Procedure_Code
)
SELECT 
    Procedure_Code,
    Volume,
    CONCAT('$', FORMAT(Total_Billed, 2)) AS Total_Billed,
    CONCAT('$', FORMAT(Total_Write_Off, 2)) AS Contractual_Write_Off,
    CONCAT(Yield_Percentage, '%') AS Collection_Yield,
    RANK() OVER (ORDER BY Total_Write_Off DESC) AS Leakage_Rank
FROM Procedure_Yield
LIMIT 10;


-- Query 3: The Actionable Work Queue (The "Billing Team View")
SELECT 
    cmd.Triage_Queue_Status,
    cmd.Check_EFT_Number,
    cmd.Variance_Amount,
    c.Claim_ID,
    c.Procedure_Code,
    c.Billed_Amount,
    c.Provider_Paid AS Expected_Claim_Cash
FROM vw_reconciliation_command_center cmd
INNER JOIN tbl_era_claims c 
    ON cmd.Check_EFT_Number = c.Check_EFT_Number
WHERE cmd.Triage_Queue_Status IN ('Partial: Review Short Pay', 'ESCALATE: Missing Check')
ORDER BY cmd.Variance_Amount ASC, cmd.Check_EFT_Number;