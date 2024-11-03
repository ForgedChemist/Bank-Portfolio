import sqlite3
import json
import customtkinter as ctk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from config import load_config, save_config
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class BankAccount:
    def __init__(self, account_type, currency, exchange_rate, income_percentage=None):
        self.account_type = account_type
        self.currency = currency
        self.exchange_rate = exchange_rate
        self.income_percentage = income_percentage

    def calculate_monthly_income(self, balance):
        if self.income_percentage:
            return balance * (self.income_percentage / 100)
        return 0

class CreditCardOutcome:
    def __init__(self, account_id, amount, description, account_distributions=None):
        self.account_id = account_id
        self.amount = amount
        self.description = description
        self.account_distributions = account_distributions or {}

class Asset:
    def __init__(self, name, quantity, price_per_unit):
        self.name = name
        self.quantity = quantity
        self.price_per_unit = price_per_unit

def create_database():
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            account_type TEXT NOT NULL,
            currency TEXT NOT NULL,
            exchange_rate REAL NOT NULL,
            income_percentage REAL,
            date TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credit_card_outcomes (
            id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            account_distributions TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price_per_unit REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_account(account):
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO accounts (account_type, currency, exchange_rate, income_percentage, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (account.account_type, account.currency, account.exchange_rate, account.income_percentage, current_date))
    conn.commit()
    conn.close()

def get_accounts():
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts')
    accounts = cursor.fetchall()
    conn.close()
    return accounts

def update_account(account_id, account):
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE accounts
        SET account_type = ?, currency = ?, exchange_rate = ?, income_percentage = ?
        WHERE id = ?
    ''', (account.account_type, account.currency, account.exchange_rate, account.income_percentage, account_id))
    conn.commit()
    conn.close()

def delete_account(account_id):
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
    conn.commit()
    conn.close()

def add_credit_card_outcome(outcome):
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO credit_card_outcomes (account_id, amount, description, account_distributions)
        VALUES (?, ?, ?, ?)
    ''', (outcome.account_id, outcome.amount, outcome.description, json.dumps(outcome.account_distributions)))
    conn.commit()
    conn.close()

def get_credit_card_outcomes():
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM credit_card_outcomes')
    outcomes = cursor.fetchall()
    conn.close()
    return outcomes

def update_credit_card_outcome(outcome_id, outcome):
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE credit_card_outcomes
        SET account_id = ?, amount = ?, description = ?, account_distributions = ?
        WHERE id = ?
    ''', (outcome.account_id, outcome.amount, outcome.description, json.dumps(outcome.account_distributions), outcome_id))
    conn.commit()
    conn.close()

def delete_credit_card_outcome(outcome_id):
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT account_distributions FROM credit_card_outcomes WHERE id = ?', (outcome_id,))
    outcome = cursor.fetchone()
    if outcome:
        account_distributions = json.loads(outcome[0])
        for account_id, amount in account_distributions.items():
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, account_id))
    cursor.execute('DELETE FROM credit_card_outcomes WHERE id = ?', (outcome_id,))
    conn.commit()
    conn.close()

def add_asset(asset):
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO assets (name, quantity, price_per_unit)
        VALUES (?, ?, ?)
    ''', (asset.name, asset.quantity, asset.price_per_unit))
    conn.commit()
    conn.close()

def get_assets():
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM assets')
    assets = cursor.fetchall()
    conn.close()
    return assets

def update_asset(asset_id, asset):
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE assets
        SET name = ?, quantity = ?, price_per_unit = ?
        WHERE id = ?
    ''', (asset.name, asset.quantity, asset.price_per_unit, asset_id))
    conn.commit()
    conn.close()

def delete_asset(asset_id):
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
    conn.commit()
    conn.close()

def calculate_total_money():
    accounts = get_accounts()
    total_money = sum(account[3] for account in accounts)  # Assuming the balance is in the 4th column
    return total_money

def calculate_total_outcome():
    outcomes = get_credit_card_outcomes()
    total_outcome = sum(outcome[2] for outcome in outcomes)  # Assuming the amount is in the 3rd column
    return total_outcome

def get_money_over_time():
    conn = sqlite3.connect('bank_portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, SUM(balance) FROM accounts GROUP BY date')
    data = cursor.fetchall()
    conn.close()
    return data

def main():
    create_database()
    ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    root = ctk.CTk()
    root.title("Bank Portfolio Manager")
    root.geometry("1200x800")  # Increased the initial size of the window
    root.minsize(1200, 800)  # Increased the minimum size of the window

    button_width = 250  # Updated button width to better fit the larger window

    # Language dictionary
    lang_dict = {
        "en": {
            "add_account": "Add Account",
            "view_accounts": "View Accounts",
            "update_account": "Update Account",
            "delete_account": "Delete Account",
            "add_credit_card_outcome": "Add Credit Card Outcome",
            "view_credit_card_outcomes": "View Credit Card Outcomes",
            "update_credit_card_outcome": "Update Credit Card Outcome",
            "delete_credit_card_outcome": "Delete Credit Card Outcome",
            "add_asset": "Add Asset",
            "view_assets": "View Assets",
            "update_asset": "Update Asset",
            "delete_asset": "Delete Asset",
            "show_total_money_pie_chart": "Show Total Money Pie Chart",
            "show_total_outcome_pie_chart": "Show Total Outcome Pie Chart",
            "exit": "Exit",
            "switch_language": "Switch Language",
            "info": "Info",
            "error": "Error",
            "account_added_successfully": "Account added successfully",
            "account_updated_successfully": "Account updated successfully",
            "account_deleted_successfully": "Account deleted successfully",
            "credit_card_outcome_added": "Credit card outcome added successfully",
            "credit_card_outcome_updated": "Credit card outcome updated successfully",
            "credit_card_outcome_deleted": "Credit card outcome deleted successfully",
            "asset_added_successfully": "Asset added successfully",
            "asset_updated_successfully": "Asset updated successfully",
            "asset_deleted_successfully": "Asset deleted successfully",
            "invalid_input": "Invalid input",
            "total_money_distribution": "Total Money Distribution",
            "no_data": "No Data",
            "total_outcome_distribution": "Total Outcome Distribution",
            "show_money_distribution_list": "Show Money Distribution List"
        },
        "tr": {
            "add_account": "Hesap Ekle",
            "view_accounts": "Hesapları Görüntüle",
            "update_account": "Hesabı Güncelle",
            "delete_account": "Hesabı Sil",
            "add_credit_card_outcome": "Kredi Kartı Harcaması Ekle",
            "view_credit_card_outcomes": "Kredi Kartı Harcamalarını Görüntüle",
            "update_credit_card_outcome": "Kredi Kartı Harcamasını Güncelle",
            "delete_credit_card_outcome": "Kredi Kartı Harcamasını Sil",
            "add_asset": "Varlık Ekle",
            "view_assets": "Varlıkları Görüntüle",
            "update_asset": "Varlığı Güncelle",
            "delete_asset": "Varlığı Sil",
            "show_total_money_pie_chart": "Toplam Para Pasta Grafiğini Göster",
            "show_total_outcome_pie_chart": "Toplam Harcama Pasta Grafiğini Göster",
            "exit": "Çıkış",
            "switch_language": "Dili Değiştir",
            "info": "Bilgi",
            "error": "Hata",
            "account_added_successfully": "Hesap başarıyla eklendi",
            "account_updated_successfully": "Hesap başarıyla güncellendi",
            "account_deleted_successfully": "Hesap başarıyla silindi",
            "credit_card_outcome_added": "Kredi kartı harcaması başarıyla eklendi",
            "credit_card_outcome_updated": "Kredi kartı harcaması başarıyla güncellendi",
            "credit_card_outcome_deleted": "Kredi kartı harcaması başarıyla silindi",
            "asset_added_successfully": "Varlık başarıyla eklendi",
            "asset_updated_successfully": "Varlık başarıyla güncellendi",
            "asset_deleted_successfully": "Varlık başarıyla silindi",
            "invalid_input": "Geçersiz giriş",
            "total_money_distribution": "Toplam Para Dağılımı",
            "no_data": "Veri Yok",
            "total_outcome_distribution": "Toplam Harcama Dağılımı",
            "show_money_distribution_list": "Para Dağılımını Göster"
        }
    }

    config = load_config()
    current_lang = config.get("language", "en")

    def update_ui_text():
        add_account_button.configure(text=lang_dict[current_lang]["add_account"])
        view_accounts_button.configure(text=lang_dict[current_lang]["view_accounts"])
        update_account_button.configure(text=lang_dict[current_lang]["update_account"])
        delete_account_button.configure(text=lang_dict[current_lang]["delete_account"])
        add_credit_card_outcome_button.configure(text=lang_dict[current_lang]["add_credit_card_outcome"])
        view_credit_card_outcomes_button.configure(text=lang_dict[current_lang]["view_credit_card_outcomes"])
        update_credit_card_outcome_button.configure(text=lang_dict[current_lang]["update_credit_card_outcome"])
        delete_credit_card_outcome_button.configure(text=lang_dict[current_lang]["delete_credit_card_outcome"])
        add_asset_button.configure(text=lang_dict[current_lang]["add_asset"])
        view_assets_button.configure(text=lang_dict[current_lang]["view_assets"])
        update_asset_button.configure(text=lang_dict[current_lang]["update_asset"])
        delete_asset_button.configure(text=lang_dict[current_lang]["delete_asset"])
        exit_button.configure(text=lang_dict[current_lang]["exit"])
        show_distribution_button.configure(text=lang_dict[current_lang]["show_money_distribution_list"])

    def switch_language():
        nonlocal current_lang
        current_lang = "tr" if current_lang == "en" else "en"
        config["language"] = current_lang
        save_config(config)
        update_ui_text()

    def add_account_ui():
        try:
            account_type = simpledialog.askstring("Input", "Enter account type:")
            if not account_type:
                return
            currency = simpledialog.askstring("Input", "Enter currency:")
            if not currency:
                return
            exchange_rate = float(simpledialog.askstring("Input", "Enter exchange rate to Turkish Lira:"))
            income_percentage = simpledialog.askstring("Input", "Enter income percentage (leave blank if not applicable):")
            income_percentage = float(income_percentage) if income_percentage else None
            account = BankAccount(account_type, currency, exchange_rate, income_percentage)
            add_account(account)
            messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["account_added_successfully"])
        except (TypeError, ValueError):
            messagebox.showerror(lang_dict[current_lang]["error"], lang_dict[current_lang]["invalid_input"])

    def view_accounts_ui():
        accounts = get_accounts()
        accounts_str = "\n".join([str(account) for account in accounts])
        messagebox.showinfo(lang_dict[current_lang]["info"], accounts_str)

    def update_account_ui():
        try:
            account_id = int(simpledialog.askstring("Input", "Enter account ID to update:"))
            account_type = simpledialog.askstring("Input", "Enter new account type:")
            if not account_type:
                return
            currency = simpledialog.askstring("Input", "Enter new currency:")
            if not currency:
                return
            exchange_rate = float(simpledialog.askstring("Input", "Enter new exchange rate to Turkish Lira:"))
            income_percentage = simpledialog.askstring("Input", "Enter new income percentage (leave blank if not applicable):")
            income_percentage = float(income_percentage) if income_percentage else None
            account = BankAccount(account_type, currency, exchange_rate, income_percentage)
            update_account(account_id, account)
            messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["account_updated_successfully"])
        except (TypeError, ValueError):
            messagebox.showerror(lang_dict[current_lang]["error"], lang_dict[current_lang]["invalid_input"])

    def delete_account_ui():
        try:
            account_id = int(simpledialog.askstring("Input", "Enter account ID to delete:"))
            delete_account(account_id)
            messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["account_deleted_successfully"])
        except (TypeError, ValueError):
            messagebox.showerror(lang_dict[current_lang]["error"], lang_dict[current_lang]["invalid_input"])

    def add_credit_card_outcome_ui():
        try:
            account_id = int(simpledialog.askstring("Input", "Enter account ID:"))
            amount = float(simpledialog.askstring("Input", "Enter amount:"))
            description = simpledialog.askstring("Input", "Enter description:")
            if not description:
                return
            account_distributions = {}
            while True:
                dist_account_id = simpledialog.askstring("Input", "Enter account ID used to pay (leave blank to finish):")
                if not dist_account_id:
                    break
                dist_amount = float(simpledialog.askstring("Input", "Enter amount taken from this account:"))
                account_distributions[int(dist_account_id)] = dist_amount
            outcome = CreditCardOutcome(account_id, amount, description, account_distributions)
            add_credit_card_outcome(outcome)
            messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["credit_card_outcome_added"])
        except (TypeError, ValueError):
            messagebox.showerror(lang_dict[current_lang]["error"], lang_dict[current_lang]["invalid_input"])

    def view_credit_card_outcomes_ui():
        outcomes = get_credit_card_outcomes()
        outcomes_str = "\n".join([str(outcome) for outcome in outcomes])
        messagebox.showinfo(lang_dict[current_lang]["info"], outcomes_str)

    def update_credit_card_outcome_ui():
        try:
            outcome_id = int(simpledialog.askstring("Input", "Enter outcome ID to update:"))
            account_id = int(simpledialog.askstring("Input", "Enter new account ID:"))
            amount = float(simpledialog.askstring("Input", "Enter new amount:"))
            description = simpledialog.askstring("Input", "Enter new description:")
            if not description:
                return
            account_distributions = {}
            while True:
                dist_account_id = simpledialog.askstring("Input", "Enter new account ID used to pay (leave blank to finish):")
                if not dist_account_id:
                    break
                dist_amount = float(simpledialog.askstring("Input", "Enter new amount taken from this account:"))
                account_distributions[int(dist_account_id)] = dist_amount
            outcome = CreditCardOutcome(account_id, amount, description, account_distributions)
            update_credit_card_outcome(outcome_id, outcome)
            messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["credit_card_outcome_updated"])
        except (TypeError, ValueError):
            messagebox.showerror(lang_dict[current_lang]["error"], lang_dict[current_lang]["invalid_input"])

    def delete_credit_card_outcome_ui():
        try:
            outcome_id = int(simpledialog.askstring("Input", "Enter outcome ID to delete:"))
            delete_credit_card_outcome(outcome_id)
            messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["credit_card_outcome_deleted"])
        except (TypeError, ValueError):
            messagebox.showerror(lang_dict[current_lang]["error"], lang_dict[current_lang]["invalid_input"])

    def add_asset_ui():
        try:
            name = simpledialog.askstring("Input", "Enter asset name:")
            if not name:
                return
            quantity = float(simpledialog.askstring("Input", "Enter quantity:"))
            price_per_unit = float(simpledialog.askstring("Input", "Enter price per unit:"))
            asset = Asset(name, quantity, price_per_unit)
            add_asset(asset)
            messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["asset_added_successfully"])
        except (TypeError, ValueError):
            messagebox.showerror(lang_dict[current_lang]["error"], lang_dict[current_lang]["invalid_input"])

    def view_assets_ui():
        assets = get_assets()
        assets_str = "\n".join([str(asset) for asset in assets])
        messagebox.showinfo(lang_dict[current_lang]["info"], assets_str)

    def update_asset_ui():
        try:
            asset_id = int(simpledialog.askstring("Input", "Enter asset ID to update:"))
            name = simpledialog.askstring("Input", "Enter new asset name:")
            if not name:
                return
            quantity = float(simpledialog.askstring("Input", "Enter new quantity:"))
            price_per_unit = float(simpledialog.askstring("Input", "Enter new price per unit:"))
            asset = Asset(name, quantity, price_per_unit)
            update_asset(asset_id, asset)
            messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["asset_updated_successfully"])
        except (TypeError, ValueError):
            messagebox.showerror(lang_dict[current_lang]["error"], lang_dict[current_lang]["invalid_input"])

    def delete_asset_ui():
        try:
            asset_id = int(simpledialog.askstring("Input", "Enter asset ID to delete:"))
            delete_asset(asset_id)
            messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["asset_deleted_successfully"])
        except (TypeError, ValueError):
            messagebox.showerror(lang_dict[current_lang]["error"], lang_dict[current_lang]["invalid_input"])

    # Create a frame for the charts
    chart_frame = ctk.CTkFrame(root)
    chart_frame.pack(side="right", fill="both", expand=True)

    def show_total_money_pie_chart():
        total_money = calculate_total_money()
        if total_money == 0:
            labels = lang_dict[current_lang]["no_data"],
            sizes = [1]
            autopct = lambda p: '0.0%' if p == 100 else ''
        else:
            labels = lang_dict[current_lang]["total_money_distribution"],
            sizes = [total_money]
            autopct = '%1.1f%%'
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct=autopct, startangle=140)
        ax.set_title(lang_dict[current_lang]["total_money_distribution"])
        return fig

    def show_total_outcome_pie_chart():
        total_outcome = calculate_total_outcome()
        if total_outcome == 0:
            labels = lang_dict[current_lang]["no_data"],
            sizes = [1]
            autopct = lambda p: '0.0%' if p == 100 else ''
        else:
            labels = lang_dict[current_lang]["total_outcome_distribution"],
            sizes = [total_outcome]
            autopct = '%1.1f%%'
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct=autopct, startangle=140)
        ax.set_title(lang_dict[current_lang]["total_outcome_distribution"])
        return fig

    def show_money_distribution_list_ui():
        accounts = get_accounts()
        accounts_str = "\n".join([f"ID: {a[0]}, Type: {a[1]}, Currency: {a[2]}, Exchange Rate: {a[3]}" for a in accounts])
        assets = get_assets()
        assets_str = "\n".join([f"ID: {asset[0]}, Name: {asset[1]}, Quantity: {asset[2]}, Price per Unit: {asset[3]}" for asset in assets])
        distribution = f"Accounts:\n{accounts_str}\n\nAssets:\n{assets_str}"
        messagebox.showinfo(lang_dict[current_lang]["info"], distribution)

    def show_money_over_time_chart():
        try:
            data = get_money_over_time()
            if not data:
                messagebox.showinfo(lang_dict[current_lang]["info"], lang_dict[current_lang]["no_data"])
                return

            dates, balances = zip(*data)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(dates, balances, marker='o')
            ax.set_title("Overall Money Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Total Money")
            ax.grid(True)

            chart_window = ctk.CTkToplevel(root)
            chart_window.title("Overall Money Over Time")
            chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror(lang_dict[current_lang]["error"], str(e))

    # Display the charts in the chart frame
    money_chart = show_total_money_pie_chart()
    outcome_chart = show_total_outcome_pie_chart()

    money_canvas = FigureCanvasTkAgg(money_chart, master=chart_frame)
    money_canvas.draw()
    money_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    outcome_canvas = FigureCanvasTkAgg(outcome_chart, master=chart_frame)
    outcome_canvas.draw()
    outcome_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    add_account_button = ctk.CTkButton(root, text=lang_dict[current_lang]["add_account"], command=add_account_ui, width=button_width)
    add_account_button.pack(pady=10)
    view_accounts_button = ctk.CTkButton(root, text=lang_dict[current_lang]["view_accounts"], command=view_accounts_ui, width=button_width)
    view_accounts_button.pack(pady=10)
    update_account_button = ctk.CTkButton(root, text=lang_dict[current_lang]["update_account"], command=update_account_ui, width=button_width)
    update_account_button.pack(pady=10)
    delete_account_button = ctk.CTkButton(root, text=lang_dict[current_lang]["delete_account"], command=delete_account_ui, width=button_width)
    delete_account_button.pack(pady=10)
    add_credit_card_outcome_button = ctk.CTkButton(root, text=lang_dict[current_lang]["add_credit_card_outcome"], command=add_credit_card_outcome_ui, width=button_width)
    add_credit_card_outcome_button.pack(pady=10)
    view_credit_card_outcomes_button = ctk.CTkButton(root, text=lang_dict[current_lang]["view_credit_card_outcomes"], command=view_credit_card_outcomes_ui, width=button_width)
    view_credit_card_outcomes_button.pack(pady=10)
    update_credit_card_outcome_button = ctk.CTkButton(root, text=lang_dict[current_lang]["update_credit_card_outcome"], command=update_credit_card_outcome_ui, width=button_width)
    update_credit_card_outcome_button.pack(pady=10)
    delete_credit_card_outcome_button = ctk.CTkButton(root, text=lang_dict[current_lang]["delete_credit_card_outcome"], command=delete_credit_card_outcome_ui, width=button_width)
    delete_credit_card_outcome_button.pack(pady=10)
    add_asset_button = ctk.CTkButton(root, text=lang_dict[current_lang]["add_asset"], command=add_asset_ui, width=button_width)
    add_asset_button.pack(pady=10)
    view_assets_button = ctk.CTkButton(root, text=lang_dict[current_lang]["view_assets"], command=view_assets_ui, width=button_width)
    view_assets_button.pack(pady=10)
    update_asset_button = ctk.CTkButton(root, text=lang_dict[current_lang]["update_asset"], command=update_asset_ui, width=button_width)
    update_asset_button.pack(pady=10)
    delete_asset_button = ctk.CTkButton(root, text=lang_dict[current_lang]["delete_asset"], command=delete_asset_ui, width=button_width)
    delete_asset_button.pack(pady=10)
    show_distribution_button = ctk.CTkButton(root, text=lang_dict[current_lang]["show_money_distribution_list"], command=show_money_distribution_list_ui, width=button_width)
    show_distribution_button.pack(pady=10)

    show_money_over_time_button = ctk.CTkButton(root, text="Show Money Over Time", command=show_money_over_time_chart, width=button_width)
    show_money_over_time_button.pack(pady=10)

    language_button = ctk.CTkButton(root, text="Switch Language", command=switch_language, width=button_width)
    language_button.pack(pady=10)

    exit_button = ctk.CTkButton(root, text=lang_dict[current_lang]["exit"], command=root.quit, width=button_width)
    exit_button.pack(pady=32)




    update_ui_text()  # Update UI text based on the loaded language

    root.mainloop()

if __name__ == "__main__":
    main()