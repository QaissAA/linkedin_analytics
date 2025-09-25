# LinkedIn Analytics Project

##  Компания
**TalentVision Analytics** — консалтинговая компания, которая занимается исследованием профессиональных сетей и карьерных траекторий специалистов на основе открытых данных LinkedIn.  

##  Проект
Цель проекта — построить систему визуализации и аналитики профилей LinkedIn.  
Основные направления анализа:
- Демографический анализ (пол, возраст, национальность).
- Анализ карьерных траекторий и компаний.
- Эмоциональный анализ фотографий профилей.
- Сравнение подписчиков и вовлечённости между компаниями.

---

## 🖼️ Скриншот аналитики
<img width="600" height="400" alt="gender_distribution" src="https://github.com/user-attachments/assets/a773ca88-fd4b-482e-b9a0-a4f7496242e5" />


---

## 🚀 Как запустить проект
1. Установите PostgreSQL (версия 17+).  
2. Создайте базу данных:
   ```sql
   CREATE DATABASE linkedin_db;


Установите зависимости Python:
pip install -r requirements.txt


Запустите скрипт соединения и аналитики:
python sql_connect.py


Результаты сохраняются в:
CSV/Excel (.csv, .xlsx файлы).
PNG-графики в папке проекта.

Используемые инструменты и ресурсы
PostgreSQL 17 — хранение данных.
Python 3.11 — аналитика и визуализация.

Библиотеки:
psycopg2-binary — подключение к PostgreSQL.
pandas — обработка данных.
matplotlib — построение графиков.
openpyxl — экспорт в Excel.

Датасет: LinkedIn Dataset (Kaggle):https://www.kaggle.com/datasets/killbot/linkedin
