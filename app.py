import streamlit as st
import sqlite3

# Подключение к базе
conn = sqlite3.connect('tasks.db')
c = conn.cursor()

# Создание таблицы задач, если она еще не существует
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              description TEXT NOT NULL,
              status TEXT NOT NULL,
              executor TEXT NOT NULL)''')
conn.commit()

# Добавление задачи в базу данных
def add_task(name, description, status, executor):
    try:
        c.execute("INSERT INTO tasks (name, description, status, executor) VALUES (?, ?, ?, ?)",
                  (name, description, status, executor))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error adding task: {e}")
        return False

# Получение всех задач из базы данных
def get_tasks():
    c.execute("SELECT * FROM tasks")
    return c.fetchall()

# Форма новой задачи

with st.sidebar:
    with st.form("add_task_form"):
        st.text("Создать новую задачу")
        task_name = st.text_input("Введите имя задачи")
        task_description = st.text_area("Введите описание задачи")
        task_status = st.selectbox("Выберите статус", ["In Progress", "Review", "Deploy", "Done", "Denied"])
        task_executor = st.selectbox("Select Task Executor", ["Alexander", "Evgeny"])
        submitted = st.form_submit_button("Добавить")

        # Проверяем, была ли отправлена форма
        if submitted:
            if task_name.strip() and task_description.strip() and task_status.strip() and task_executor.strip():
                if add_task(task_name, task_description, task_status, task_executor):
                    st.success("Задача добавлена успешно!")
            else:
                st.warning("Не все поля заполнены!")

# Центральная часть страницы: отображение списка задач
st.header("Список задач")
tasks = get_tasks()
if tasks:
    st.data_editor(tasks, column_config={
        "id": "ID",
        "name": "Task Name",
        "description": "Description",
        "status": "Status",
        "executor": "Executor"
    }, key="task_editor")
else:
    st.info("Список пуст добавте задачу.")

conn.close()