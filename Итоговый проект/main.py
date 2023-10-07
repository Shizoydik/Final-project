# Импортируем все нужные библиотеки и модули
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Хранение и инициализация объектов графического интерфейса
class MainFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Создание основного интерфейса программы и туллбара
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Конфигурация колонок таблицы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone_number', 'email', 'salary'), height=45, show='headings' )
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone_number', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        # Заголовки колонок таблицы
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone_number', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Заработная плата')
        self.tree.pack(side=tk.LEFT)

        # Создание на туллбаре кнопки добавления сотрудника
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # Создание на туллбаре кнопки обновления сотрудника
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Создание на туллбаре кнопки удаления сотрудника
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete =  tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # Создание на туллбаре кнопки поиска сотрудника
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search =  tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Создание на туллбаре кнопки обновления страницы
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.refresh_img, command=self.refresh_records)
        btn_refresh.pack(side=tk.LEFT)

    # Метод открытия дочернего окна
    def open_dialog(self):
        ChildFrame()

    # Метод внесения данных в базу данных(добавления нового сотрудника)
    def records(self, name, phone_number, email, salary):
        self.db.insert_data(name, phone_number, email, salary)
        self.view_records()

    # Метод отображения записей на главном окне
    def view_records(self):
        self.db.cursor.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    # Метод открытия окна редактирования контакта
    def open_update_dialog(self):
        UpdateEmployeeDataFrame()

    # Метод редактирования контакта
    def update_records(self, name, phone_number, email, salary):
        self.db.cursor.execute(
            '''UPDATE db SET name = ?, phone_number = ?, email = ?, salary = ? WHERE ID = ?''', (name, phone_number, email, salary, self.tree.set(self.tree.selection() [0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления сотрудника
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cursor.execute('''DELETE FROM db WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска сотрудника
    def open_search_dialog(self):
        SearchEmployeeFrame()

    # Метод поиска записи
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cursor.execute('''SELECT * FROM db WHERE name LIKE ?''', (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    # Метод обновления страницы
    def refresh_records(self):
        self.db.cursor.execute('''SELECT * FROM db ''')

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

# Создание дочернего окна добавления
class ChildFrame(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Инициализация окна добавления
        label_name=tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)

        label_phone_number=tk.Label(self, text='Телефон')
        label_phone_number.place(x=50, y=80)

        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)

        label_salary = tk.Label(self, text='Заработная плата')
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_phone_number = ttk.Entry(self)
        self.entry_phone_number.place(x=200, y=110)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        #Создание кнопки закрытия и её функционала
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        #Создание кнопки добавления и её функционала
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_phone_number.get(),
                                                                       self.entry_salary.get()))
        self.btn_ok.bind('<Button-1>', lambda event:
        self.destroy(), add='+')

# Создание окна редактирования сотрудника
class UpdateEmployeeDataFrame(ChildFrame):
    def __init__(self):
        super().__init__()
        self.view = app
        self.db = db
        try:
            self.default_data()

            # Инициализация окна редактирования
            self.title("Редактирование сотрудника")
            btn_edit = ttk.Button(self, text="Редактировать")
            btn_edit.place(x=205, y=170)
            btn_edit.bind(
                "<Button-1>",
                lambda event: self.view.update_records(
                    self.entry_name.get(), self.entry_email.get(), self.entry_phone_number.get(), self.entry_salary.get()
                ),
            )
            btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
            self.btn_ok.destroy()

        except IndexError:
            messagebox.showerror("Сотрудник для редактирования не выбран", "Пожалуйста, выберите сотрудника для редактирования.")
            self.destroy()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_email.get(),
                                              self.entry_phone_number.get(),
                                              self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.cursor.execute(
            'SELECT * FROM db WHERE id=?', (self.view.tree.set(self.view.tree.selection() [0], '#1'),))
        row = self.db.cursor.fetchall()

        self.entry_name.insert(0, row[0][1])
        self.entry_email.insert(0, row[0][2])
        self.entry_phone_number.insert(0, row[0][3])
        self.entry_salary.insert(0, row[0][4])

# Создание окна поиска
class SearchEmployeeFrame(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app
        self.db = db

    # Инициализация окна поиска
    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('350x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск:')
        label_search.place(x=50, y=20)

        self.entry_search = tk.Entry(self)
        self.entry_search.place(x=185, y=50, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=105, y=50)

        btn_search = ttk.Button(self, text='Найти')
        btn_search.place(x=105, y=50)

        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))

        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# Создание базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db (
                id integer primary key,
                name text,
                phone_number text,
                email text,
                salary integer
            )'''
        )
        self.conn.commit()

    # Метод добавления информации в базу данных
    def insert_data(self, name, phone_number, email, salary):
        self.cursor.execute('''INSERT INTO db (name, phone_number, email, salary) VALUES(?,?,?,?)''', (name, phone_number, email, salary))
        self.conn.commit()

# Создание основного окна
if __name__=='__main__':
    root=tk.Tk()
    db = DB()
    app = MainFrame(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('800x450')
    root.resizable(False, False)

    root.mainloop()