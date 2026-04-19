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