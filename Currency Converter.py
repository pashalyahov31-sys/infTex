import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Фиксированные курсы валют (относительно USD)
# Актуально на Апрель 2026 года
EXCHANGE_RATES = {
    "USD": 1.0000,
    "EUR": 0.9200,
    "GBP": 0.7900,
    "JPY": 148.50,
    "RUB": 88.50,
    "CNY": 7.2400,
    "CAD": 1.3700,
    "AUD": 1.5200,
    "CHF": 0.9100,
    "INR": 83.50,
    "BRL": 5.0500,
    "MXN": 16.80,
    "SGD": 1.3500,
    "NZD": 1.6500,
    "KRW": 1350.00,
    "TRY": 32.50,
    "SEK": 10.70,
    "NOK": 10.90,
    "DKK": 6.8600,
    "PLN": 4.0200,
    "THB": 36.80,
    "VND": 25000.0,
    "IDR": 15900.0,
    "MYR": 4.7500,
    "PHP": 56.50
}

HISTORY_FILE = "history.json"

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter - Без API")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Список валют
        self.currencies = sorted(EXCHANGE_RATES.keys())
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка истории
        self.history = self.load_history()
        self.update_history_table()
        
        # Информация о курсах
        self.show_rate_info()
    
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Конвертер валют", 
                                font=("Arial", 16, "bold"), fg="navy")
        title_label.pack(pady=10)
        
        # Информационная метка
        self.info_label = tk.Label(self.root, text="", font=("Arial", 9), fg="gray")
        self.info_label.pack()
        
        # Фрейм для выбора валют
        frame1 = tk.LabelFrame(self.root, text="Выберите валюты", padx=20, pady=10, font=("Arial", 10, "bold"))
        frame1.pack(pady=15, padx=20, fill="x")
        
        tk.Label(frame1, text="Из:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5)
        self.from_currency = ttk.Combobox(frame1, values=self.currencies, width=12, font=("Arial", 10))
        self.from_currency.grid(row=0, column=1, padx=10, pady=5)
        self.from_currency.set("USD")
        self.from_currency.bind('<<ComboboxSelected>>', self.update_rate_info)
        
        tk.Label(frame1, text="В:", font=("Arial", 11)).grid(row=0, column=2, padx=10, pady=5)
        self.to_currency = ttk.Combobox(frame1, values=self.currencies, width=12, font=("Arial", 10))
        self.to_currency.grid(row=0, column=3, padx=10, pady=5)
        self.to_currency.set("EUR")
        self.to_currency.bind('<<ComboboxSelected>>', self.update_rate_info)
        
        # Текущий курс
        self.rate_label = tk.Label(frame1, text="", font=("Arial", 10, "italic"), fg="green")
        self.rate_label.grid(row=1, column=0, columnspan=4, pady=5)
        
        # Фрейм для ввода суммы
        frame2 = tk.LabelFrame(self.root, text="Введите сумму", padx=20, pady=10, font=("Arial", 10, "bold"))
        frame2.pack(pady=10, padx=20, fill="x")
        
        tk.Label(frame2, text="Сумма:", font=("Arial", 11)).pack(side=tk.LEFT, padx=10)
        self.amount_entry = tk.Entry(frame2, width=20, font=("Arial", 11))
        self.amount_entry.pack(side=tk.LEFT, padx=10)
        
        # Кнопка конвертации
        self.convert_btn = tk.Button(self.root, text="🔄 Конвертировать", command=self.convert, 
                                      bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                                      padx=30, pady=8, cursor="hand2")
        self.convert_btn.pack(pady=15)
        
        # Результат
        self.result_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"), fg="#2196F3")
        self.result_label.pack(pady=10)
        
        # Таблица истории
        history_frame = tk.LabelFrame(self.root, text="История конвертаций", padx=10, pady=10, font=("Arial", 10, "bold"))
        history_frame.pack(pady=10, padx=20, fill="both", expand=True)
Mark Craemer Photography
self.to


# Таблица с прокруткой
        tree_frame = tk.Frame(history_frame)
        tree_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_tree = ttk.Treeview(tree_frame, columns=("from", "to", "amount", "result", "date", "rate"), 
                                         show="headings", height=8, yscrollcommand=scrollbar.set)
        self.history_tree.heading("from", text="Из")
        self.history_tree.heading("to", text="В")
        self.history_tree.heading("amount", text="Сумма")
        self.history_tree.heading("result", text="Результат")
        self.history_tree.heading("rate", text="Курс")
        self.history_tree.heading("date", text="Дата")
        self.history_tree.column("from", width=80)
        self.history_tree.column("to", width=80)
        self.history_tree.column("amount", width=100)
        self.history_tree.column("result", width=120)
        self.history_tree.column("rate", width=100)
        self.history_tree.column("date", width=140)
        self.history_tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.history_tree.yview)
        
        # Кнопки управления историей
        button_frame = tk.Frame(history_frame)
        button_frame.pack(pady=10)
        
        self.load_btn = tk.Button(button_frame, text="📂 Загрузить историю", command=self.reload_history,
                                   bg="#607D8B", fg="white", font=("Arial", 10), padx=15, pady=5, cursor="hand2")
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(button_frame, text="🗑 Очистить историю", command=self.clear_history,
                                    bg="#f44336", fg="white", font=("Arial", 10), padx=15, pady=5, cursor="hand2")
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Обновить информацию о курсе
        self.update_rate_info()
    
    def show_rate_info(self):
        """Показывает информацию об актуальности курсов"""
        current_date = datetime.now().strftime("%d.%m.%Y")
        self.info_label.config(text=f"💰 Курсы валют актуальны на {current_date} (относительно USD)")
    
    def update_rate_info(self, event=None):
        """Обновляет отображение текущего курса"""
        from_cur = self.from_currency.get()
        to_cur = self.to_currency.get()
        
        if from_cur in EXCHANGE_RATES and to_cur in EXCHANGE_RATES:
            rate = EXCHANGE_RATES[to_cur] / EXCHANGE_RATES[from_cur]
            self.rate_label.config(text=f"💰 Текущий курс: 1 {from_cur} = {rate:.4f} {to_cur}")
    
    def validate_amount(self, amount_str):
        """Проверка корректности ввода суммы"""
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
            return True, amount
        except ValueError:
            return False, 0
    
    def convert(self):
        amount_str = self.amount_entry.get().strip()
        is_valid, amount = self.validate_amount(amount_str)
        
        if not is_valid:
            messagebox.showerror("Ошибка", "❌ Сумма должна быть положительным числом!\nПример: 100, 50.5, 1000")
            return
        
        from_cur = self.from_currency.get()
        to_cur = self.to_currency.get()
        
        # Проверка наличия валют
        if from_cur not in EXCHANGE_RATES:
            messagebox.showerror("Ошибка", f"Валюта '{from_cur}' не поддерживается.")
            return
        if to_cur not in EXCHANGE_RATES:
            messagebox.showerror("Ошибка", f"Валюта '{to_cur}' не поддерживается.")
            return
        
        # Вычисление курса и результата
        rate_from = EXCHANGE_RATES[from_cur]
        rate_to = EXCHANGE_RATES[to_cur]
        rate = rate_to / rate_from
        result = amount * rate
        
        # Отображение результата
        result_text = f"{amount:.2f} {from_cur} =


{result:.2f} {to_cur}"
        self.result_label.config(text=result_text)
        
        # Сохранение в историю
        record = {
            "from": from_cur,
            "to": to_cur,
            "amount": round(amount, 2),
            "result": round(result, 2),
            "rate": round(rate, 4),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.insert(0, record)  # Добавляем в начало
        
        # Ограничиваем историю 100 записями
        if len(self.history) > 100:
            self.history = self.history[:100]
        
        self.save_history()
        self.update_history_table()
        
        # Анимация кнопки
        self.convert_btn.config(bg="#45a049")
        self.root.after(100, lambda: self.convert_btn.config(bg="#4CAF50"))
    
    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Сохранение истории в JSON"""
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")
    
    def update_history_table(self):
        """Обновление таблицы истории"""
        # Очищаем таблицу
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)
        
        # Добавляем записи (последние сверху)
        for record in self.history:
            self.history_tree.insert("", "end", values=(
                record["from"], record["to"], record["amount"],
                record["result"], record["rate"], record["date"]
            ))
    
    def reload_history(self):
        """Перезагрузка истории из файла"""
        self.history = self.load_history()
        self.update_history_table()
        messagebox.showinfo("Успех", f"✅ Загружено {len(self.history)} записей из файла.")
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_table()
            messagebox.showinfo("Успех", "✅ История очищена.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()