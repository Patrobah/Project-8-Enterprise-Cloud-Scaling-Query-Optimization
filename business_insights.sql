-- ====================================================================
-- PROJECT 8: HIGH-PERFORMANCE EXECUTIVE EXECUTIVE ANALYSIS METRICS
-- WAREHOUSE COMPILED: GOOGLE BIGQUERY
-- ====================================================================

-- Query 1: Calculate Global Plan Performance Metrics
SELECT
    Plan_Type,
    COUNT(Transaction_ID) AS Total_Active_Contracts,
    ROUND(SUM(Normalized_Amount_USD), 2) AS Gross_Generated_Revenue_USD,
    ROUND(AVG(Normalized_Amount_USD), 2) AS Average_Revenue_Per_Account_ARPU
FROM
    `SaaS_Enterprise_Scaling.fact_transactions`
GROUP BY
    Plan_Type
ORDER BY
    Gross_Generated_Revenue_USD DESC;

-- Query 2: Aggregate Dynamic SaaS Monthly Recurring Revenue (MRR)
-- (Applies precise time-scale scaling to annual contract tiers)
WITH PlanMRR AS (
    SELECT
        Plan_Type,
        SUM(Normalized_Amount_USD) AS Raw_Revenue
    FROM
        `SaaS_Enterprise_Scaling.fact_transactions`
    GROUP BY
        Plan_Type
)
SELECT
    ROUND(SUM(
        CASE
            WHEN Plan_Type = 'Basic_Monthly' THEN Raw_Revenue
            WHEN Plan_Type = 'Pro_Monthly' THEN Raw_Revenue
            WHEN Plan_Type = 'Enterprise_Annual' THEN (Raw_Revenue / 12)
            ELSE 0
        END
    ), 2) AS Total_Monthly_Recurring_Revenue_MRR,

    ROUND(SUM(
        CASE
            WHEN Plan_Type = 'Basic_Monthly' THEN Raw_Revenue
            WHEN Plan_Type = 'Pro_Monthly' THEN Raw_Revenue
            WHEN Plan_Type = 'Enterprise_Annual' THEN (Raw_Revenue / 12)
            ELSE 0
        END
    ) * 12, 2) AS Projected_Annual_Recurring_Revenue_ARR
FROM
    PlanMRR;
