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

## Скриншот аналитики
Аналитика пола

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/7f641358-0289-4aae-8dec-c06bc31196f5" />


Erd Диаграмма

<img width="767" height="711" alt="image" src="https://github.com/user-attachments/assets/7f70454b-40be-4728-900a-797c9fb814a5" />


---

## Как запустить проект

1. Установите PostgreSQL (версия 17+).  

2. Создайте базу данных:
   ```sql
   CREATE DATABASE linkedin_db;

##  Установка и запуск

### 1. Установите зависимости Python:
```bash
pip install -r requirements.txt
2. Запустите скрипт соединения и аналитики:
bash
Копировать код
python sql_connect.py
3. Результаты сохраняются в:
CSV/Excel: .csv, .xlsx файлы

Графики: .png файлы в папке проекта

 Используемые инструменты и ресурсы
PostgreSQL 17 — хранение данных

Python 3.11 — аналитика и визуализация

 Библиотеки:
psycopg2-binary — подключение к PostgreSQL

pandas — обработка данных

matplotlib — построение графиков

openpyxl — экспорт в Excel
```

Датасет:
[LinkedIn Dataset](https://www.kaggle.com/datasets/killbot/linkedin)




