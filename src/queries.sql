-- En aktif bölgeler
SELECT region, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY region
ORDER BY quake_count DESC
LIMIT 20;

-- Saatlik deprem yoğunluğu
SELECT strftime('%Y-%m-%d %H:00', timestamp) AS hour,
       COUNT(*) AS quake_count
FROM earthquakes
GROUP BY hour
ORDER BY hour;

-- Magnitude dağılımı
SELECT
  CASE
    WHEN magnitude < 2 THEN '<2.0'
    WHEN magnitude < 4 THEN '2.0-3.9'
    WHEN magnitude < 5 THEN '4.0-4.9'
    WHEN magnitude < 6 THEN '5.0-5.9'
    ELSE '6.0+'
  END AS magnitude_range,
  COUNT(*) AS quake_count
FROM earthquakes
GROUP BY magnitude_range
ORDER BY magnitude_range;

-- Son 24 saatteki deprem sayısı
SELECT COUNT(*) AS last_24h_quakes
FROM earthquakes
WHERE timestamp >= datetime('now', '-1 day');
