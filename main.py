import psycopg2
import pandas as pd
import os

DB_NAME = "linkedin_db"
DB_USER = "postgres"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

def load_queries(sql_file="queries.sql"):
    queries = {}
    with open(sql_file, "r", encoding="utf-8") as f:
        content = f.read()

    raw_queries = [q.strip() for q in content.split(";") if q.strip()]
    for i, query in enumerate(raw_queries, start=1):
        queries[f"query_{i}"] = query
    return queries

def run_queries():
    try:
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)

        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        print(" Успешное подключение к базе данных")

        queries = load_queries("queries.sql")
        print("Загруженные запросы:", list(queries.keys()))

        for name, query in queries.items():
            try:
                print(f"\n Выполняется запрос: {name}")
                df = pd.read_sql(query, conn)
                print(df.head())

                file_path = os.path.join(output_dir, f"{name}.csv")
                df.to_csv(file_path, index=False, encoding="utf-8")

                print(f"Сохранено: {file_path} | Строк: {len(df)}")

            except Exception as qe:
                print(f" Ошибка в запросе '{name}':", qe)

        conn.close()
        print("\n Все запросы выполнены")

    except Exception as e:
        print(" Ошибка подключения или выполнения:", e)

if __name__ == "__main__":
    run_queries()
