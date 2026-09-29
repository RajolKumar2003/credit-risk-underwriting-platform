SELECT
    band,
    COUNT(*)                                                   AS applicants,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)         AS pct_of_applicants,
    ROUND(AVG(target), 4)                                      AS default_rate,
    ROUND(100.0 * SUM(target) / SUM(SUM(target)) OVER (), 1)   AS pct_of_defaulters
FROM applicants
WHERE split = 'valid'
GROUP BY band
ORDER BY band_order;
