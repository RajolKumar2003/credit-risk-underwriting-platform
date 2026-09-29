WITH ranked AS (
    SELECT
        expected_loss,
        target,
        NTILE(10) OVER (ORDER BY pd DESC) AS risk_decile
    FROM applicants
    WHERE split = 'valid'
),
by_decile AS (
    SELECT
        risk_decile,
        COUNT(*)            AS applicants,
        SUM(expected_loss)  AS expected_loss,
        AVG(target)         AS default_rate
    FROM ranked
    GROUP BY risk_decile
)
SELECT
    risk_decile,
    applicants,
    ROUND(default_rate, 4)                                                           AS default_rate,
    ROUND(100.0 * expected_loss / SUM(expected_loss) OVER (), 1)                     AS pct_of_expected_loss,
    ROUND(100.0 * SUM(expected_loss) OVER (ORDER BY risk_decile) / SUM(expected_loss) OVER (), 1) AS cumulative_pct
FROM by_decile
ORDER BY risk_decile;
