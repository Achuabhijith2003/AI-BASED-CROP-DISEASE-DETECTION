import sqlite3
import pandas as pd

# Define database connection
DB_PATH = 'DB/Treatment.db'
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

def create_table():
    """Creates the 'treatment' table if it doesn't exist."""
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treatment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_name TEXT,
                causal_organism TEXT,
                symptoms TEXT,
                treatment_control_measures TEXT,
                chemical_treatment TEXT
            )
        ''')
        connection.commit()
        print("Table 'treatment' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def insert_data_from_excel(file_path):
    """Reads data from an Excel file and inserts it into the database."""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        
        print("Columns in Excel file:", df.columns)  # Debugging line
        
        # Correct column names as per the Excel file
        required_columns = {'Disease Name', 'Causal Organism', 'Symptoms', 'Treatment / Control Measures', 'Chemical Treatment (if applicable)'}
        
        if required_columns.issubset(df.columns):
            # Rename columns to match database column names
            df.rename(columns={
                'Disease Name': 'disease_name',
                'Causal Organism': 'causal_organism',
                'Symptoms': 'symptoms',
                'Treatment / Control Measures': 'treatment_control_measures',
                'Chemical Treatment (if applicable)': 'chemical_treatment'
            }, inplace=True)
            
            for _, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO treatment (disease_name, causal_organism, symptoms, treatment_control_measures, chemical_treatment)
                    VALUES (?, ?, ?, ?, ?)''', 
                    (row['disease_name'], row['causal_organism'], row['symptoms'], row['treatment_control_measures'], row['chemical_treatment']))
            connection.commit()
            print("Data inserted successfully.")
        else:
            print(f"Excel file must contain the following columns: {required_columns}")
    except Exception as e:
        print(f"Error inserting data: {e}")
        

def show_treatment_data():
    """Displays all records from the 'treatment' table."""
    try:
        cursor.execute("SELECT * FROM treatment")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")

# Run the functions
# create_table()
# insert_data_from_excel('DB/disease_details.xlsx')
# show_treatment_data()

# Close the database connection

def get_the_treatment(disease_name):
    DB_PATH = 'DB/Treatment.db'
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    """Fetches treatment_control_measures for a given disease_name."""
    try:
        cursor.execute("SELECT treatment_control_measures FROM treatment WHERE disease_name = ?", (disease_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return "No treatment found for the given disease."
    except sqlite3.Error as e:
        return f"Error fetching treatment: {e}"
    
result=get_the_treatment("Blast")
print("Result: ",result)


connection.close()


