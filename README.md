# 🚀 Automated Database Normalizer

A Python-based web application that automates database normalization up to Third Normal Form (3NF). The application allows users to provide a flat JSON record and functional dependencies, then automatically generates a normalized database schema along with SQL scripts.

---

## 📌 Features

- Accepts raw data in JSON format
- Accepts user-defined Functional Dependencies (FDs)
- Automatically decomposes data into 3NF tables
- Displays normalized tables in an interactive interface
- Generates SQL CREATE TABLE statements
- Generates SQL INSERT statements
- Download complete SQL schema as a `.sql` file

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- JSON
- SQL

---

## 🚀 How to Run

1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/automated-database-normalizer.git
```

2. Navigate to the project

```bash
cd automated-database-normalizer
```

3. Create a virtual environment

```bash
python -m venv venv
```

4. Activate the environment

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Run the application

```bash
streamlit run app.py
```

---

## 📷 Example Input

### JSON Record

```json
{
  "StudentID": "101",
  "StudentName": "Alice",
  "CourseID": "CS101",
  "CourseName": "Intro to CS",
  "Grade": "A"
}
```

### Functional Dependencies

```
StudentID -> StudentName
CourseID -> CourseName
StudentID, CourseID -> Grade
```

---

## 📊 Output

The application automatically:

- Creates normalized tables
- Displays each relation
- Identifies primary keys
- Generates SQL scripts
- Allows SQL download

---

## 🎯 Project Motivation

Database normalization is often performed manually during academic exercises and database design. This project automates the process by converting a flat record into a normalized schema, making it easier to understand normalization concepts while reducing manual effort.

---

## 🔮 Future Improvements

- Candidate Key Detection
- Minimal Cover Generation
- BCNF Normalization
- Foreign Key Generation
- CSV Upload Support
- ER Diagram Generation
- Better SQL Type Inference

---

## 👨‍💻 Author

**SAHIL JANGRA**
