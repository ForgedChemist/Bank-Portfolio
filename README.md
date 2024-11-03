
# Bank Portfolio 

**Bank Portfolio** is a Python-based GUI application designed to help users efficiently see their bank accounts, credit card transactions, and personal assets by entering them mannualy. Leveraging `CustomTkinter` for an enhanced user interface and `SQLite` for reliable data storage, this application offers a comprehensive solution for tracking and visualizing financial information.

---

## Key Features

### Account Management

- **Add, View, Update, and Delete Bank Accounts**
  - Track account types, currencies, exchange rates, and income percentages.

### Credit Card Outcome Tracking

- **Manage Credit Card Transactions**
  - Detailed descriptions.
  - Allocate and distribute expenses across multiple accounts.

### Asset Management

- **Manage Personal Assets**
  - Add, view, update, and delete personal assets.
  - Monitor asset quantities and price per unit.

### Data Visualization

- **Generate Pie Charts**
  - Visualize total money and outcome distributions.
- **Display Comprehensive Lists**
  - Accounts and assets.

### Localization

- **Multi-language Support**
  - English and Turkish languages.
  - Easily switch between supported languages within the application.

### Configuration Management

- **Persistent Configurations**
  - Stored in `config.json`.
- **Easy Setup and Customization**
  - Modify application settings as needed.

---

## Technologies Used

- **Programming Language**: Python
- **GUI Framework**: CustomTkinter
- **Database**: SQLite
- **Data Visualization**: Matplotlib
- **Configuration Management**: JSON

---

## Installation and Setup

### Clone the Repository
```bash
git clone https://github.com/ForgedChemist/Bank-Portfolio.git
cd Bank-Portfolio
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure the Application
```json
{
  "language": "en"
}
```
### Run the Application
```bash
python Bank.py
```

## Usage Guide
**Adding an Account:** Click on "Add Account" and provide the necessary details such as account type, currency, exchange rate, and income percentage.

**Viewing Accounts:** Select "View Accounts" to see a list of all your bank accounts.

**Managing Credit Card Outcomes:** Use the respective buttons to add, view, update, or delete credit card transactions.

**Managing Assets:** Similar to accounts, you can add, view, update, or delete your personal assets.

**Viewing Data Visualizations:** The application displays pie charts representing your total money and outcome distributions.

**Switching Language:** Click on "Switch Language" to toggle between English and Turkish.
