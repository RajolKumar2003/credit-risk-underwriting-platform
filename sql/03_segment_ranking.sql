WITH segments AS (
    SELECT
        income_type,
        age_band,
        COUNT(*)            AS applicants,
        AVG(target)         AS default_rate,
        AVG(pd)             AS mean_pd
    FROM applicants
    WHERE split = 'valid'
    GROUP BY income_type, age_band
    HAVING COUNT(*) >= 300
)
SELECT
    income_type,
    age_band,
    applicants,
    ROUND(default_rate, 4)                    AS default_rate,
    ROUND(mean_pd, 4)                         AS mean_pd,
    RANK() OVER (ORDER BY default_rate DESC)  AS risk_rank
FROM segments
ORDER BY risk_rank
LIMIT 10;
