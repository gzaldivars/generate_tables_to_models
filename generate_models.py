import sqlite3
from pathlib import Path
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
#from sqlalchemy.ext.declarative import declarative_base

database_path = Path("bd_dtgmanager.sqlite3")

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

 #Base = declarative_base()

for table_name in tables:
	# Obtener la información de las columnas
	columns = cursor.execute("PRAGMA table_info({})".format(table_name)).fetchall()

	# Generar la clase
	class_name = table_name.capitalize()
	with open("models.py", "a") as f:
		f.write(f"class {class_name}(Base):\n")
		for column in columns:
			column_name = column[1]
			column_type = convert_sqlite_type_to_sa(column[2])
			primary_key = True if column[5] == 1 else False
			f.write(f"    {column_name} = Column({column_type}, primary_key={primary_key})\n")
	
def convert_sqlite_type_to_sa(sqlite_type):
    if sqlite_type in ("TEXT", "VARCHAR", "CHAR"):
        return String
    elif sqlite_type in ("INTEGER", "REAL"):
        return Float
    elif sqlite_type == "BLOB":
        return Text
    else:
        raise ValueError("Tipo de dato SQLite no compatible: {}".format(sqlite_type))

cursor.close()
connection.close()

