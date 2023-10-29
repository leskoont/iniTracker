
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter import filedialog
import json

class InitiativeTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Battle Tracker")
        self.master.configure(bg='#86656c')

        button_color = "#b99ea1"  # цвет кнопки на 20% светлее
        button_border = "black"  # черная обводка

        # Создаем таблицу для вывода списка персонажей
        self.tree = ttk.Treeview(self.master, columns=("name", "lvl", "hp", "ap", "initiative", "state", "is_enemy", "statuses"), show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("lvl", text="Level")
        self.tree.heading("hp", text="HP")
        self.tree.heading("ap", text="Armor")
        self.tree.heading("initiative", text="Initiative")
        self.tree.heading("state", text="State")
        self.tree.heading("is_enemy", text="Is Enemy")
        self.tree.heading("statuses", text="Statuses")
        self.tree.grid(row=0, column=0, columnspan=1, rowspan=8, padx=5, pady=5, sticky="nsew")

        # Создаем кнопку для добавления нового персонажа
        self.add_button = tk.Button(self.master, text="New Character", command=self.create_character)
        self.add_button.grid(row=0, column=3, sticky="nwe", rowspan=1, padx=5, pady=5)
        self.add_button.config(bg=button_color, fg='white', bd=1, highlightthickness=1,
                               highlightbackground=button_border)

        # Создаем кнопку для добавления пати
        self.add_button = tk.Button(self.master, text="Add Party", command=self.add_characters)
        self.add_button.grid(row=1, column=3, sticky="nwe", rowspan=1, padx=5, pady=5)
        self.add_button.config(bg=button_color, fg='white', bd=1, highlightthickness=1,
                               highlightbackground=button_border)

        # Создаем кнопку для удаления всех персонажей из списка
        self.clear_button = tk.Button(self.master, text="Clear List", command=self.clear_list)
        self.clear_button.grid(row=2, column=3, sticky="nwe", rowspan=1, padx=5, pady=5)
        self.clear_button.config(bg=button_color, fg='white', bd=1, highlightthickness=1,
                               highlightbackground=button_border)

        # Создаем кнопку для удаления всех вражеских персонажей
        self.delete_enemies_button = tk.Button(self.master, text="Delete All Enemies", command=self.delete_all_enemies)
        self.delete_enemies_button.grid(row=3, column=3, sticky="nwe", rowspan=1, padx=5, pady=5)
        self.delete_enemies_button.config(bg=button_color, fg='white', bd=1, highlightthickness=1,
                               highlightbackground=button_border)

        # Создаем кнопку для сохранения персонажей
        self.save_button = tk.Button(self.master, text="Save Party", command=self.save_characters)
        self.save_button.grid(row=4, column=3, sticky="nwe", rowspan=1, padx=5, pady=5)
        self.save_button.config(bg=button_color, fg='white', bd=1, highlightthickness=1,
                               highlightbackground=button_border)

        # Создаем кнопку для загрузки персонажей
        self.load_button = tk.Button(self.master, text="Load Party", command=self.load_characters)
        self.load_button.grid(row=5, column=3, sticky="nwe", rowspan=1, padx=5, pady=5)
        self.load_button.config(bg=button_color, fg='white', bd=1, highlightthickness=1,
                               highlightbackground=button_border)

        self.temp_label_1 = tk.Label(self.master, text="")
        self.temp_label_1.grid(row=6, column=3, sticky="w", padx=5, pady=5)
        self.temp_label_1.config(bg='#86656c', fg='white', bd=1, highlightthickness=1,
                               highlightbackground=button_border)

        self.temp_label_2 = tk.Label(self.master, text="")
        self.temp_label_2.grid(row=7, column=3, sticky="w", padx=5, pady=5)
        self.temp_label_2.config(bg='#86656c', fg='white', bd=1, highlightthickness=1,
                                highlightbackground=button_border)

        # Создаем список для хранения персонажей
        self.characters = []

        # Создаем список для хранения кнопок
        self.buttons = []

        # Задаем параметры макета
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(4, weight=1)


    # Метод для добавления персонажа в список
    def create_character(self):
        character = {"name": "New character", "lvl": 0, "hp": 0, "ap": 0, "initiative": 0, "active": True,
                     "is_enemy": False, "statuses": "", "notes": ""}

        self.characters.append(character)
        self.display_characters()

    def display_characters(self):
        # Очищаем таблицу
        self.tree.delete(*self.tree.get_children())

        # Сортируем список персонажей по значению инициативы от большего к меньшему
        self.characters.sort(key=lambda x: int(x["initiative"]), reverse=True)

        for i, character in enumerate(self.characters):
            self.tree.bind('<Button-3>', lambda event, index=i: self.show_context_menu(event, index))
            active_text = "Active" if character["active"] else "Eliminated"
            enemy_text = "Enemy" if character["is_enemy"] else "Friend"
            self.tree.tag_configure('e', background='red')
            self.tree.tag_configure('f', background='green')
            self.tree.insert("", i, values=(character["name"], character["hp"], character["hp"], character["ap"], character["initiative"], active_text, enemy_text, character["statuses"]))
            item_id = self.tree.get_children()[i]
            self.tree.item(item_id, tags=('e' if (enemy_text == "Enemy") else 'f'))
        self.update_columns_width()

    def update_columns_width(self):
        # Проходим по всем столбцам таблицы
        for col in self.tree["columns"]:
            if col.title() == "Statuses":
                continue
            col_width = tkfont.Font().measure(col.title()) + 5

            # Проходим по всем строкам таблицы
            for row in self.tree.get_children():
                cell_width = tkfont.Font().measure(str(self.tree.item(row, "values")[self.tree["columns"].index(col)]))
                col_width = max(col_width, cell_width)

            # Устанавливаем свойство minwidth для столбца
            self.tree.column(col, width=col_width)

    def show_context_menu(self, event, index):
        # Создаем контекстное меню
        menu = tk.Menu(self.master, tearoff=0)

        # Добавляем пункты меню
        menu.add_command(label="Show Notes", command=lambda: self.show_notes(index))
        menu.add_command(label="Eliminate", command=lambda: self.eliminate_character(index))
        menu.add_command(label="Reactivate", command=lambda: self.reactivate_character(index))
        menu.add_command(label="Edit", command=lambda: self.edit_character(index))
        menu.add_command(label="Delete", command=lambda: self.delete_character(index))

        # Отображаем меню в точке клика
        menu.post(event.x_root, event.y_root)

    def show_notes(self, index):
        # Создаем окно для изменения параметров персонажа
        notes_window = tk.Toplevel(self.master)
        notes_window.title("Notes about {}".format(
            self.characters[index]["name"] if self.characters[index]["name"] != "" else "character"))
        notes_window.configure(bg='#86656c')

        self.notes_list = tk.Text(notes_window, height=40, width=50)
        self.notes_list.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.notes_list.insert("end", self.characters[index]["notes"])  # Исправлено замена 0 на "end"

        # Создаем кнопку для сохранения изменений
        save_button = tk.Button(notes_window, text="Save",
                                command=lambda: self.save_notes(index, self.notes_list.get("1.0", "end"),
                                                                notes_window))  # Исправлено notes_list на self.notes_list
        save_button.grid(row=2, column=1, padx=5, pady=5)

    def save_notes(self, index, notes_list, notes_window):
        self.characters[index]["notes"] = notes_list
        notes_window.destroy()

    # Метод для пометки персонажа как выбывшего
    def eliminate_character(self, index):
        self.characters[index]["active"] = False
        self.display_characters()

    # Метод для реактивации персонажа
    def reactivate_character(self, index):
        self.characters[index]["active"] = True
        self.display_characters()

    # Метод для изменения параметров персонажа
    def edit_character(self, index):
        # Создаем окно для изменения параметров персонажа
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Character")
        edit_window.configure(bg='#86656c')

        # Создаем поле ввода для имени персонажа
        name_label = tk.Label(edit_window, text="Name:", highlightthickness=0, bg=edit_window.cget('background'))
        name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        name_entry.insert(0, self.characters[index]["name"])

        # Создаем поле ввода для уровня
        lvl_label = tk.Label(edit_window, text="Level:", highlightthickness=0,
                            bg=edit_window.cget('background'))
        lvl_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        lvl_entry = tk.Entry(edit_window)
        lvl_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        lvl_entry.insert(0, self.characters[index]["lvl"])

        # Создаем поле ввода для хп
        hp_label = tk.Label(edit_window, text="HP:", highlightthickness=0,
                                    bg=edit_window.cget('background'))
        hp_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        hp_entry = tk.Entry(edit_window)
        hp_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        hp_entry.insert(0, self.characters[index]["hp"])

        # Создаем поле ввода для защиты
        ap_label = tk.Label(edit_window, text="Armor:", highlightthickness=0,
                            bg=edit_window.cget('background'))
        ap_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ap_entry = tk.Entry(edit_window)
        ap_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        ap_entry.insert(0, self.characters[index]["ap"])

        # Создаем поле ввода для инициативы
        initiative_label = tk.Label(edit_window, text="Initiative:", highlightthickness=0,
                                    bg=edit_window.cget('background'))
        initiative_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        initiative_entry = tk.Entry(edit_window)
        initiative_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        initiative_entry.insert(0, self.characters[index]["initiative"])

        # Создаем чекбокс для указания состояния
        is_active_var = tk.BooleanVar()
        is_active_checkbox = tk.Checkbutton(edit_window, text="Active", variable=is_active_var,
                                           highlightthickness=0, bg=edit_window.cget('background'))
        is_active_checkbox.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        is_active_checkbox.select() if self.characters[index]["active"] else is_active_checkbox.deselect()

        # Создаем чекбокс для указания, является ли персонаж врагом
        is_enemy_var = tk.BooleanVar()
        is_enemy_checkbox = tk.Checkbutton(edit_window, text="Is enemy", variable=is_enemy_var,
                                           highlightthickness=0, bg=edit_window.cget('background'))
        is_enemy_checkbox.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        is_enemy_checkbox.select() if self.characters[index]["is_enemy"] else is_enemy_checkbox.deselect()

        # Создаем поле ввода для статусов
        statuses_label = tk.Label(edit_window, text="Statuses:", highlightthickness=0,
                            bg=edit_window.cget('background'))
        statuses_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
        statuses_entry = tk.Entry(edit_window)
        statuses_entry.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        statuses_entry.insert(0, self.characters[index]["statuses"])

        # Создаем кнопку для сохранения изменений
        save_button = tk.Button(edit_window, text="Save",
                                command=lambda: self.save_character(self.characters[index],
                                                                    name_entry.get(), lvl_entry.get(), hp_entry.get(),
                                                                    ap_entry.get(), initiative_entry.get(), is_active_var.get(),
                                                                    is_enemy_var.get(), statuses_entry.get(),
                                                                    edit_window))
        save_button.grid(row=8, column=1, padx=5, pady=5)

    def add_characters(self):
        file_path = filedialog.askopenfilename(defaultextension=".btl",
                                                   filetypes=[("Battle Tracker Files", "*.btl")])
        if file_path:
            with open(file_path, "r") as f:
                self.characters.extend(json.load(f))
            self.display_characters()

    def load_characters(self):
        file_path = filedialog.askopenfilename(defaultextension=".btl",
                                                   filetypes=[("Battle Tracker Files", "*.btl")])
        if file_path:
            with open(file_path, "r") as f:
                self.characters = json.load(f)
            self.display_characters()

    # Метод для сохранения изменений персонажа
    def save_character(self, character, name, lvl, hp, ap, initiative, is_active, is_enemy, statuses, window):
        # Проверяем введенные значения на корректность
        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return
        if not (initiative.isnumeric() or lvl.isnumeric() or hp.isnumeric() or ap.isnumeric()):
            messagebox.showerror("Error", "Level, HP, armor and initiative must be a number.")
            return

        # Сохраняем изменения
        character["name"] = name
        character["lvl"] = int(lvl)
        character["hp"] = int(hp)
        character["ap"] = int(ap)
        character["initiative"] = int(initiative)
        character["is_active"] = is_active
        character["is_enemy"] = is_enemy
        character["statuses"] = statuses

        # Закрываем окно
        self.display_characters()
        window.destroy()

    def delete_character(self, index):
        # Remove the character at the specified index from the list
        del self.characters[index]
        # Redisplay the list of characters
        self.display_characters()

    def delete_all_enemies(self):
        # Удаляем из списка всех вражеских персонажей
        self.characters = [character for character in self.characters if not character.get("is_enemy")]
        self.display_characters()

    # Метод для очистки списка персонажей
    def clear_list(self):
        if tk.messagebox.askyesno("Clear List", "Are you sure you want to clear the character list?"):
            self.characters = []
            self.display_characters()

    def save_characters(self):
        # Открываем диалоговое окно для выбора имени файла
        filename = tk.filedialog.asksaveasfilename(defaultextension=".btl",
                                                   filetypes=[("Battle Tracker Files", "*.btl")])
        if not filename:
            return  # пользователь отменил выбор файла

        # Сохраняем персонажей в файл
        with open(filename, "w") as f:
            json.dump(self.characters, f)

        messagebox.showinfo("Save Characters", "Characters saved successfully!")

root = tk.Tk()
app = InitiativeTracker(root)
root.mainloop()