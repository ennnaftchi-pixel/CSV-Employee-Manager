# Employee Management System (Python & CSV)

A lightweight employee management application developed for the **L1CS course at ISI (2025-2026)**. This project demonstrates how to handle data persistence using CSV files without external libraries like Pandas, and features both a Graphical User Interface (GUI) and a Command Line Interface (CLI).

## 🚀 Features

*   **Dual Interface**: Access the system via a modern Tkinter GUI or a classic terminal-based CLI.
*   **Secure Authentication**: Login system with a maximum of 3 attempts before account lockout.
*   **Full CRUD Operations**: Create, Read, Update, and Delete employee records with data validation (ID uniqueness, positive salaries, etc.).
*   **Advanced Filtering**: Filter employees by department or salary range.
*   **Sorting**: Sort data by salary (ascending/descending) or department (A-Z).
*   **Data Export & Reports**: 
    *   Export high-salary employees (> 4000 DT) to a dedicated CSV.
    *   Generate a statistical report with text-based histograms.
*   **Audit Logging**: Every connection attempt is tracked in a local log file for security.

## 📂 Project Structure

*   `gui_employes.py`: The main application with a Tkinter graphical interface.
*   `projet_csv.py`: The command-line version of the application.
*   `README.md`: Project documentation.
*   `.gitignore`: Prevents sensitive data and logs from being uploaded to GitHub.

## 🛠️ Requirements

*   **Python 3.10+**: Uses `match/case` syntax.
*   **Standard Libraries**: Uses only `csv`, `os`, `datetime`, and `tkinter`.

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone [https://github.com/ennnaftchi-pixel/CSV-Employee-Manager.git](https://github.com/ennnaftchi-pixel/CSV-Employee-Manager.git)
cd CSV-Employee-Manager
```

### 2. Launch the Application

**For the Graphical Interface:**
```bash
python gui_employes.py
```

**For the Terminal Version:**
```bash
python projet_csv.py
```

## 🔒 Security Note
This project is for educational purposes. For security reasons, the data files (`users.csv`, `employes.csv`, `audit.log`) are excluded from this repository via `.gitignore`. Default credentials can be found within the source code initialization functions.

---
**Author:** Mohamed Nafti  
**University:** Institut Supérieur d'Informatique (ISI)  
**Year:** 2025-2026

University: Institut Supérieur d'Informatique (ISI)

Year: 2025-2026
