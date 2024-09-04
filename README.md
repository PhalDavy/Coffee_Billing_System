# Coffee_Billing_System

### Objective 
The purpose of this project is to develop a functional and efficient cashier system for a coffee shop, using the MySQL database for data storage and the Flask web framework for application logic and user interface.

### Prerequisites
Before running the script, make sure you have the following installed:
1. **Python 3.6+**
2. **MySQL Workbench**
3. **DBeaver**
   - connect your MySQL Workbench with DBeaver
   - create a database
     Example: billing
    - insert **pos.sql** into your created database
    - run database
5. **Libraries**:
   ```bash
   pip install -r requirement.txt
   ```

### Usage
1. **Clone the repesitory:**
   ```bash
   git clone  https://github.com/PhalDavy/Coffee_Billing_System.git
   ```
2. **Project directory:**
   ```bash
   cd path_to_your_cloned_directory
   ```
3. **Run the script:**
   - download 
   - activate the environment: .venv\Scripts\activate
   - Make some changes in **def get_db_connection()**
     - host: based on your host in DBeaver
     - user: based on user name in DBeaver
     - password: based on your password in MySQL Workbench
     - database: your database name
   - run: python app.py
   
