import os
import mysql.connector
import logging
from dotenv import load_dotenv
from mysql.connector.errors import DatabaseError

def read_query(action):
    project_directory=os.path.dirname(os.path.realpath(__file__))
    try:
        reading_query= open(project_directory+f'\{action}.sql','r')
        sql_query = reading_query.read()
        reading_query.close
    except FileNotFoundError:
        logging.error(f'Could not find {action}.sql file.')
    return sql_query

def create_database(company_host:int,company_user,company_password,company_db_name):
    mydb=mysql.connector.connect(
        host=company_host,
        user=company_user,
        password=company_password
    )
    company_cursor=mydb.cursor()
    company_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {company_db_name};")
    return print("Database succesfully created!")

def delete_database(company_host:int,company_user,company_password,company_db_name):
    you_sure=input(f"Are you sure u want to delete {company_db_name} forever? (That is a lot of time!). If sure, type Yes, otherwise type anything you want.")
    if you_sure=="Yes":
        mydb=mysql.connector.connect(
            host=company_host,
            user=company_user,
            password=company_password,
            database=company_db_name
            )
        company_cursor=mydb.cursor()
        company_cursor.execute(f"DROP DATABASE {company_db_name};")
        return print("Database succesfully deleted!")
    else:
        print("Operation Cancelled!")

def create_tables(company_host:int,company_user,company_password,company_db_name):
    create_database(company_host,company_user,company_password,company_db_name)
    mydb=mysql.connector.connect(
        host=company_host,
        user=company_user,
        password=company_password,
        database=company_db_name
    )
    company_cursor=mydb.cursor()
    
    sql_query=read_query("create_tables")
    company_cursor.execute(sql_query)
    return print("Tables succesfuly created!")

def ask_for_data():
    host=input("Please insert host name (default localhost if using XAMPP): ")
    user=input("Please insert username (default root if using XAMPP): ")
    password=input("Please insert password (leave empty if there is no password): ")
    return [host,user,password]

option=(input("Hello, Welcome to this Accounting Software! Please enter the number of the action you would like to do: \n 1- Create New Database. \n 2- Delete an existing Database. \n 3- Operate with an existing Database.\n 4- Close the Program.\n Answer: "))

while option not in ["1","2","3","4"]:
        option=(input("Please enter the number of the action you would like to do: \n 1- Create New Database. \n 2- Delete an existing Database. \n 3- Operate with an existing Database.\n 4- Close the Program.\n Answer: "))

if option=="1":
    use_env_file=input("Would you like to import Server data from .env file? Type 'Yes' if you would like to, otherwise type 'No'.\n Answer: ")
    while use_env_file not in ["Yes","No"]:
        use_env_file=input("Would you like to import Server data from .env file? Type 'Yes' if you would like to, otherwise type 'No'.\n Answer: ")
    if use_env_file=="Yes":
        load_dotenv('server_data.env')
        COMPANY_USERNAME=os.getenv('COMPANY_USERNAME')
        COMPANY_PASSWORD=os.getenv('COMPANY_PASSWORD')
        COMPANY_HOST=os.getenv('COMPANY_HOST')
        database_name=input("Please insert desired Database name (default localhost if using XAMPP): ")
        create_tables(COMPANY_HOST,COMPANY_USERNAME,COMPANY_PASSWORD,f"{database_name}") 
    elif use_env_file=="No":
        try:
            data=ask_for_data()
            database_name=input("Please insert desired Database name: ")
            create_tables(data[0],data[1],data[2],f"{database_name}")
            print(f"{database_name} Database succesfully created!")
        except DatabaseError as er:
            print(er)
    else:
        option=input("Please inser a valid answer: ")
        
elif option=="2":
        try:
            data=ask_for_data()
            database_name=input("Please insert Database name: ")
            delete_database(data[0],data[1],data[2],database_name)
        except DatabaseError as er:
            print(er)
elif option == "4":
    print("Closing program! Have a nice day.")

elif option == "3":
    pass