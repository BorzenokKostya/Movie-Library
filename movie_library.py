import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Личная кинотека")
        self.movies = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Ввод данных о фильме
        form_frame = tk.Frame(self.root)
        form_frame.pack(padx=10, pady=10, fill='x')

        tk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky='e')
        self.title_entry = tk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Жанр:").grid(row=0, column=2, sticky='e')
        self.genre_entry = tk.Entry(form_frame)
        self.genre_entry.grid(row=0, column=3, padx=5)

        tk.Label(form_frame, text="Год выпуска:").grid(row=1, column=0, sticky='e')
        self.year_entry = tk.Entry(form_frame)
        self.year_entry.grid(row=1, column=1, padx=5)

        tk.Label(form_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky='e')
        self.rating_entry = tk.Entry(form_frame)
        self.rating_entry.grid(row=1, column=3, padx=5)

        # Кнопки для добавления и сохранения
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        self.add_button = tk.Button(btn_frame, text="Добавить фильм", command=self.add_movie)
        self.add_button.pack(side='left', padx=5)

        self.save_button = tk.Button(btn_frame, text="Сохранить в JSON", command=self.save_data)
        self.save_button.pack(side='left', padx=5)

        self.load_button = tk.Button(btn_frame, text="Загрузить из JSON", command=self.load_data)
        self.load_button.pack(side='left', padx=5)

        # Фильтр
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10, fill='x')

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0)
        self.genre_filter = tk.Entry(filter_frame)
        self.genre_filter.grid(row=0, column=1, padx=5)
        tk.Button(filter_frame, text="Фильтровать", command=self.filter_movies).grid(row=0, column=2, padx=5)
        tk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter).grid(row=0, column=3, padx=5)

        tk.Label(filter_frame, text="Фильтр по году:").grid(row=1, column=0)
        self.year_filter = tk.Entry(filter_frame)
        self.year_filter.grid(row=1, column=1, padx=5)
        tk.Button(filter_frame, text="Фильтровать", command=self.filter_by_year).grid(row=1, column=2, padx=5)
        tk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter_year).grid(row=1, column=3, padx=5)

        # Таблица для отображения данных
        self.tree = ttk.Treeview(self.root, columns=("Название", "Жанр", "Год", "Рейтинг"), show='headings')
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        # Валидация
        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return
        try:
            year_int = int(year)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом.")
            return
        try:
            rating_float = float(rating)
            if not (0 <= rating_float <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": year_int,
            "rating": rating_float
        }
        self.movies.append(movie)
        self.insert_into_tree(movie)
        self.clear_entries()

    def insert_into_tree(self, movie):
        self.tree.insert('', 'end', values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def save_data(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.movies, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Успех", "Данные успешно сохранены.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def load_data(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
                self.refresh_tree()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in self.movies:
            self.insert_into_tree(movie)

    def filter_movies(self):
        genre_filter = self.genre_filter.get().strip().lower()
        self.reset_tree()
        for movie in self.movies:
            if genre_filter in movie["genre"].lower():
                self.insert_into_tree(movie)

    def filter_by_year(self):
        year_str = self.year_filter.get().strip()
        if not year_str:
            self.reset_tree()
            return
        try:
            year_int = int(year_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Год фильтрации должен быть числом.")
            return
        self.reset_tree()
        for movie in self.movies:
            if movie["year"] == year_int:
                self.insert_into_tree(movie)

    def reset_tree(self):
        self.refresh_tree()

    def reset_filter(self):
        self.genre_filter.delete(0, tk.END)
        self.reset_tree()

    def reset_filter_year(self):
        self.year_filter.delete(0, tk.END)
        self.reset_tree()


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()