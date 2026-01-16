# 🛒 Kirana Dukaan

Kirana Dukaan is a **grocery store web application** built as a learning project.  

It helps beginners and intermediate developers understand important concepts in **web development and coding**, including frontend design, backend logic, RESTful Api and database management.


## ✨ Features
- User-friendly interface for browsing grocery items  
- Dynamic product listing using HTML, CSS, and JavaScript  
- Backend powered by **Flask (Python)**  
- Data storage with **SQLite**  
- Simple and modular codebase for easy learning and extension
- Added Flask-RESTful Api Checkpoints

**🔐 Authentication & Authorization**

* Uses Flask’s built-in session login
* Admin routes are only accessible to admins
* Returns clear JSON errors with proper status codes (401, 403)

**📦 Data Handling**

* Sends complete data, including related information
* Formats dates in ISO format for JSON
* Safely handles missing related data

**🧩 API Setup**

* All endpoints start with `/api`
* The API is registered in `app.py`


```bash
# Get all products (requires login)
GET /api/products

# Get specific category (requires login)  
GET /api/categories/1

# Get all users (requires admin login)
GET /api/users

# Get transaction details (requires admin login)
GET /api/transactions/123
```


## 🛠 Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Database:** SQLite  


## 🚀 Getting Started
Type this into your command line where you want to copy the folder.
   ```bash
   git clone https://github.com/CodeNaveen-in/Kirana-Dukaan.git
   cd Kirana-Dukaan
   code .
   ```