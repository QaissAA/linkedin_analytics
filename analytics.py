import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl.formatting.rule import ColorScaleRule
from config import DB_CONFIG

# ======================
# Загрузка SQL-запросов
# ======================
def load_queries(sql_file="queries.sql"):
    queries = {}
    with open(sql_file, "r", encoding="utf-8") as f:
        content = f.read()
    raw_queries = [q.strip() for q in content.split(";") if q.strip()]
    for i, query in enumerate(raw_queries, start=1):
        queries[f"query_{i}"] = query
    return queries


# ======================
# Экспорт в Excel с форматированием
# ======================
def export_to_excel(dataframes_dict, filename):
    export_dir = "exports"
    os.makedirs(export_dir, exist_ok=True)
    filepath = os.path.join(export_dir, filename)

    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        for sheet_name, df in dataframes_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            ws = writer.sheets[sheet_name]
            ws.freeze_panes = "B2"
            ws.auto_filter.ref = ws.dimensions

            for col_idx, col in enumerate(df.columns, 1):
                if pd.api.types.is_numeric_dtype(df[col]):
                    col_letter = ws.cell(row=1, column=col_idx).column_letter
                    cell_range = f"{col_letter}2:{col_letter}{len(df)+1}"
                    rule = ColorScaleRule(
                        start_type="min", start_color="FFAA0000",
                        mid_type="percentile", mid_value=50, mid_color="FFFFFF00",
                        end_type="max", end_color="FF00AA00"
                    )
                    ws.conditional_formatting.add(cell_range, rule)

    print(f" Excel-отчёт создан: {filepath}")


# ======================
# Графики
# ======================
charts_dir = os.path.join(os.getcwd(), "charts")
os.makedirs(charts_dir, exist_ok=True)

GRAPH_MAP = {
    "query_1": {"type": "hbar", "title": "Топ-10 компаний по числу сотрудников", "xlabel": "Сотрудники", "ylabel": "Компания"},
    "query_2": {"type": "bar", "title": "Средний возраст по национальностям", "xlabel": "Национальность", "ylabel": "Возраст"},
    "query_3": {"type": "bar", "title": "Топ-10 национальностей по пользователям", "xlabel": "Национальность", "ylabel": "Пользователи"},
    "query_4": {"type": "pie", "title": "Распределение по полу"},
    "query_5": {"type": "line", "title": "Средний стаж по компаниям", "xlabel": "Компания", "ylabel": "Стаж"},
    "query_6": {"type": "bar", "title": "Счастье по полу", "xlabel": "Пол", "ylabel": "Уровень счастья"},
    "query_7": {"type": "hbar", "title": "Самые счастливые компании", "xlabel": "Счастье", "ylabel": "Компания"},
    "query_8": {"type": "scatter", "title": "Подписчики vs Счастье по компаниям", "xlabel": "Подписчики", "ylabel": "Счастье"},
    "query_9": {"type": "bar", "title": "Этнические вероятности", "xlabel": "Группа", "ylabel": "Среднее значение"},
    "query_10": {"type": "hist", "title": "Beauty Score (топ пользователей)", "xlabel": "Оценка", "ylabel": "Частота"}
}

# ======================
# Построение разных графиков
# ======================
def plot_pie(df, title):
    if df.empty:
        return
    plt.figure(figsize=(6, 6))
    plt.pie(df.iloc[:, 1], labels=df.iloc[:, 0], autopct="%1.1f%%")
    plt.title(title)

def plot_bar(df, meta):
    if df.empty:
        return
    df.plot(kind="bar", x=df.columns[0], y=df.columns[1], legend=False, color="skyblue")
    plt.xlabel(meta["xlabel"]); plt.ylabel(meta["ylabel"]); plt.title(meta["title"])

def plot_hbar(df, meta):
    if df.empty:
        return
    df.plot(kind="barh", x=df.columns[0], y=df.columns[1], legend=False, color="green")
    plt.xlabel(meta["xlabel"]); plt.ylabel(meta["ylabel"]); plt.title(meta["title"])

def plot_line(df, meta):
    if df.empty:
        return
    df.plot(kind="line", x=df.columns[0], y=df.columns[1], marker="o", color="blue")
    plt.xlabel(meta["xlabel"]); plt.ylabel(meta["ylabel"]); plt.title(meta["title"])

def plot_hist(df, meta, bins=10):
    if df.empty:
        return
    col = df.select_dtypes(include=["number"]).columns[-1]
    plt.hist(df[col], bins=bins, color="purple", alpha=0.7)
    plt.xlabel(meta["xlabel"]); plt.ylabel(meta["ylabel"]); plt.title(meta["title"])

def plot_scatter(df, meta):
    if df.empty:
        return
    xcol, ycol = df.select_dtypes(include=["number"]).columns[:2]
    plt.scatter(df[xcol], df[ycol], color="red")
    plt.xlabel(meta["xlabel"]); plt.ylabel(meta["ylabel"]); plt.title(meta["title"])


# ======================
# Основная функция
# ======================
def run_analytics():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        queries = load_queries("queries.sql")
        report_dfs = {}

        for qname, meta in GRAPH_MAP.items():
            if qname not in queries:
                print(f" {qname} не найден в queries.sql")
                continue

            print(f"\n {meta['title']}")
            df = pd.read_sql(queries[qname], conn)
            report_dfs[qname] = df

            if df.empty:
                print(f" {qname}: результат пустой, график не создан")
                continue

            # Сохраняем CSV отдельно
            csv_path = os.path.join("exports", f"{qname}.csv")
            os.makedirs("exports", exist_ok=True)
            df.to_csv(csv_path, index=False, encoding="utf-8")
            print(f" Сохранён CSV: {csv_path}")

            # Графики
            plt.figure(figsize=(10, 6))
            try:
                if meta["type"] == "bar": plot_bar(df, meta)
                elif meta["type"] == "hbar": plot_hbar(df, meta)
                elif meta["type"] == "pie": plot_pie(df, meta["title"])
                elif meta["type"] == "line": plot_line(df, meta)
                elif meta["type"] == "hist": plot_hist(df, meta)
                elif meta["type"] == "scatter":
                    num_cols = df.select_dtypes(include=["number"]).columns
                    if len(num_cols) >= 2:
                        plot_scatter(df, meta)
                    else:
                        print(f" {qname}: недостаточно числовых колонок для scatter")
                        plt.close()
                        continue

                file_path = os.path.join(charts_dir, f"{qname}.png")
                plt.tight_layout(); plt.savefig(file_path); plt.close()
                print(f" Сохранён график: {file_path}")

            except Exception as plot_err:
                print(f" Ошибка при построении {qname}: {plot_err}")
                plt.close()

        conn.close()

        # Экспорт всего в Excel
        if report_dfs:
            export_to_excel(report_dfs, "linkedin_report.xlsx")
        else:
            print(" Нет данных для экспорта в Excel")

        print("\n Аналитика завершена, отчёты в папках charts/ и exports/")

    except Exception as e:
        print(" Ошибка при выполнении аналитики:", e)


# ======================
# Запуск
# ======================
if __name__ == "__main__":
    run_analytics()
