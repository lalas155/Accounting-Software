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

def create_database(company_host,company_user,company_password,company_db_name):
    mydb=mysql.connector.connect(
        host=company_host,
        user=company_user,
        password=company_password
    )
    company_cursor=mydb.cursor()
    company_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {company_db_name};")
    return print("Database succesfully created!")

def delete_database(company_host,company_user,company_password,company_db_name):
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

def ask_for_sv_data():
    host=input("Please insert host name (default localhost if using XAMPP): ")
    user=input("Please insert username (default root if using XAMPP): ")
    password=input("Please insert password (leave empty if there is no password): ")
    return [host,user,password]

def read_env_file(env_file_name):
    load_dotenv(os.path.dirname(os.path.realpath(__file__))+f"\{env_file_name}.env")
    COMPANY_HOST=os.getenv('COMPANY_HOST')
    COMPANY_USERNAME=os.getenv('COMPANY_USERNAME')
    COMPANY_PASSWORD=os.getenv('COMPANY_PASSWORD')
    return[COMPANY_HOST,COMPANY_USERNAME,COMPANY_PASSWORD]

def import_or_manual_sv_data_gathering():
    use_env_file=input("Would you like to import Server data from .env file? Type 'Yes' if you would like to, otherwise type 'No'.\n Answer: ")
    while use_env_file not in ["Yes","No"]:
        use_env_file=input("Would you like to import Server data from .env file? Type 'Yes' if you would like to, otherwise type 'No'.\n Answer: ")
    if use_env_file=="Yes":
        env_file_name=input("Insert the name of the .env file: ")
        database_name=input("Please insert desired Database name (default localhost if using XAMPP): ")
        return ["with env",env_file_name,database_name]
    elif use_env_file=="No":
        try:
            sv_data=ask_for_sv_data()
            database_name=input("Please insert desired Database name: ")
            return ["without env",sv_data,database_name]
        except DatabaseError as er:
            return print(er)
    return

option=(input("Hello, Welcome to this Accounting Software! Please enter the number of the action you would like to do: \n 1- Create New Database. \n 2- Delete an existing Database. \n 3- Operate with an existing Database.\n 4- Close the Program.\n Answer: "))

while option not in ["1","2","3","4"]:
        option=(input("Please enter the number of the action you would like to do: \n 1- Create New Database. \n 2- Delete an existing Database. \n 3- Operate with an existing Database.\n 4- Close the Program.\n Answer: "))
if option=="1":
    sv_data_and_db_name=import_or_manual_sv_data_gathering()
    if sv_data_and_db_name[0]=="with env":
        env_data=read_env_file(sv_data_and_db_name[1])
        create_database(env_data[0],env_data[1],env_data[2],f"{sv_data_and_db_name[2]}")
        create_tables(env_data[0],env_data[1],env_data[2],f"{sv_data_and_db_name[2]}")
    else:
        data_list=[]
        for data in sv_data_and_db_name[1]:
            data_list.append(data)
        create_database(data_list[0],data_list[1],data_list[2],f"{sv_data_and_db_name[2]}")
        create_tables(data_list[0],data_list[1],data_list[2],f"{sv_data_and_db_name[2]}")
elif option=="2":
        try:
            data=ask_for_sv_data()
            database_name=input("Please insert Database name: ")
            delete_database(data[0],data[1],data[2],database_name)
        except DatabaseError as er:
            print(er)
elif option == "4":
    print("Closing program! Have a nice day.")
elif option == "3":
    import_or_manual_sv_data_gathering()
    