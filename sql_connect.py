import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Настройки подключения
DB_NAME = "linkedin_db"
DB_USER = "postgres"
DB_PASSWORD = "1234" # 
DB_HOST = "localhost"
DB_PORT = "5432"

# Подключаемся к базе
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Функция для выполнения SQL и возврата DataFrame
def run_query(query, name):
    df = pd.read_sql(query, conn)
    print(f"\n{name}:\n", df)
    # Сохраняем в CSV и Excel
    df.to_csv(f"{name}.csv", index=False)
    df.to_excel(f"{name}.xlsx", index=False)
    return df

# 🔹 Примеры запросов
queries = {
    "gender_distribution": """
        SELECT gender, COUNT(*) AS total
        FROM members
        GROUP BY gender;
    """,
    "avg_age_by_nationality": """
        SELECT nationality, AVG(age) AS avg_age
        FROM members
        WHERE age IS NOT NULL
        GROUP BY nationality
        ORDER BY avg_age DESC
        LIMIT 10;
    """,
    "top_companies_by_employees": """
        SELECT c.c_name, COUNT(p.m_urn) AS employee_count
        FROM positions p
        JOIN companies c ON p.c_id = c.c_id
        GROUP BY c.c_name
        ORDER BY employee_count DESC
        LIMIT 10;
    """
}

# Выполняем запросы и строим графики
gender_df = run_query(queries["gender_distribution"], "gender_distribution")
age_df = run_query(queries["avg_age_by_nationality"], "avg_age_by_nationality")
companies_df = run_query(queries["top_companies_by_employees"], "top_companies_by_employees")

# Построение графиков

# 1. Распределение по полу
plt.figure(figsize=(6, 4))
plt.bar(gender_df["gender"], gender_df["total"], color="skyblue")
plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("gender_distribution.png")
plt.show()

# 2. Средний возраст по национальностям (топ-10)
plt.figure(figsize=(10, 6))
plt.bar(age_df["nationality"], age_df["avg_age"], color="orange")
plt.title("Average Age by Nationality (Top 10)")
plt.xlabel("Nationality")
plt.ylabel("Average Age")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("avg_age_by_nationality.png")
plt.show()

# 3. Топ-10 компаний по числу сотрудников
plt.figure(figsize=(10, 6))
plt.barh(companies_df["c_name"], companies_df["employee_count"], color="green")
plt.title("Top 10 Companies by Employee Count")
plt.xlabel("Employee Count")
plt.ylabel("Company")
plt.gca().invert_yaxis()  # чтобы топ был сверху
plt.tight_layout()
plt.savefig("top_companies_by_employees.png")
plt.show()

conn.close()
