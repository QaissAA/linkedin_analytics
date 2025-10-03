-- 1. Топ-10 компаний по количеству сотрудников (Horizontal bar)
SELECT c.c_name, COUNT(p.m_urn) AS employee_count
FROM positions p
JOIN companies c ON p.c_id = c.c_id
GROUP BY c.c_name
ORDER BY employee_count DESC
LIMIT 10;

-- 2. Средний возраст пользователей по национальности (Bar)
SELECT nationality, AVG(age) AS avg_age
FROM members
WHERE age IS NOT NULL
GROUP BY nationality
ORDER BY avg_age DESC;

-- 3. Топ-10 национальностей по количеству пользователей (Bar)
SELECT nationality, COUNT(*) AS total
FROM members
GROUP BY nationality
ORDER BY total DESC
LIMIT 10;

-- 4. Количество пользователей по полу (Pie)
SELECT gender, COUNT(*) AS total
FROM members
GROUP BY gender;

-- 5. Средняя длина текущего стажа по компаниям (Line)
SELECT c.c_name, AVG(p.tenure_len) AS avg_tenure
FROM positions p
JOIN companies c ON p.c_id = c.c_id
GROUP BY c.c_name
ORDER BY avg_tenure DESC
LIMIT 10;

-- 6. Эмоции: кто чаще улыбается (по полу) (Bar)
SELECT m.gender, AVG(e.emo_happiness) AS avg_happiness
FROM emotions e
JOIN members m ON e.m_urn = m.m_urn
GROUP BY m.gender
ORDER BY avg_happiness DESC;

-- 7. Топ-10 компаний с самыми «счастливыми» профилями (Horizontal bar)
SELECT c.c_name, AVG(e.emo_happiness) AS avg_happiness
FROM emotions e
JOIN positions p ON e.m_urn = p.m_urn
JOIN companies c ON p.c_id = c.c_id
GROUP BY c.c_name
ORDER BY avg_happiness DESC
LIMIT 10;

-- 8. Среднее количество подписчиков по компаниям (Scatter, связать с happiness)
SELECT c.c_name, AVG(m.n_followers) AS avg_followers
FROM members m
JOIN positions p ON m.m_urn = p.m_urn
JOIN companies c ON p.c_id = c.c_id
GROUP BY c.c_name
ORDER BY avg_followers DESC
LIMIT 10;

-- 9. Распределение по этническим вероятностям (Bar)
SELECT AVG(east_asian) AS avg_east_asian,
       AVG(european) AS avg_european,
       AVG(african) AS avg_african
FROM ethnicity_probs;

-- 10. Пользователи с самым высоким уровнем «beauty» (Histogram)
SELECT m.m_urn, m.gender, m.age, f.beauty
FROM face_attributes f
JOIN members m ON f.m_urn = m.m_urn
ORDER BY f.beauty DESC
LIMIT 100;
