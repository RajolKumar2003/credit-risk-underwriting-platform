WITH cutoffs(cutoff) AS (
    VALUES (0.06), (0.10), (0.16), (0.20), (1.00)
)
SELECT
    c.cutoff,
    ROUND(AVG(CASE WHEN a.pd <= c.cutoff THEN 1.0 ELSE 0 END), 3)                          AS approval_rate,
    ROUND(1.0 * SUM(CASE WHEN a.pd <= c.cutoff THEN a.target END)
          / SUM(CASE WHEN a.pd <= c.cutoff THEN 1 END), 4)                                 AS default_rate_approved,
    ROUND(SUM(CASE WHEN a.pd <= c.cutoff AND a.target = 0 THEN a.credit * 0.08
                   WHEN a.pd <= c.cutoff AND a.target = 1 THEN -a.credit * 0.45
                   ELSE 0 END) / 1e6, 1)                                                   AS net_value_millions
FROM applicants a
CROSS JOIN cutoffs c
WHERE a.split = 'valid'
GROUP BY c.cutoff
ORDER BY c.cutoff;
