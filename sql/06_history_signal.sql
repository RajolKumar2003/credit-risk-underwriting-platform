SELECT
    CASE
        WHEN bureau_credit_count = 0 THEN 'no bureau record'
        WHEN inst_late_share IS NULL THEN 'no instalment history'
        WHEN inst_late_share = 0 THEN 'never late'
        WHEN inst_late_share < 0.2 THEN 'late on under 20%'
        ELSE 'late on 20% or more'
    END                              AS history_group,
    COUNT(*)                         AS applicants,
    ROUND(AVG(target), 4)            AS default_rate,
    ROUND(AVG(pd), 4)                AS mean_pd
FROM applicants
WHERE split = 'valid'
GROUP BY history_group
ORDER BY default_rate;
