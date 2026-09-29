SELECT
    contract_type,
    COUNT(*)                                        AS applicants,
    ROUND(AVG(target), 4)                           AS default_rate,
    ROUND(AVG(pd), 4)                               AS mean_predicted_pd,
    ROUND(SUM(credit) / 1e6, 1)                     AS exposure_millions,
    ROUND(SUM(expected_loss) / 1e6, 1)              AS expected_loss_millions,
    ROUND(SUM(expected_loss) / SUM(credit), 4)      AS expected_loss_rate
FROM applicants
WHERE split = 'valid'
GROUP BY contract_type
ORDER BY exposure_millions DESC;
