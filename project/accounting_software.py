import os
import mysql.connector
import logging
from dotenv import load_dotenv
from mysql.connector.errors import DatabaseError
from datetime import datetime

def read_query(action):
    project_directory = os.path.dirname(os.path.realpath(__file__))
    try:
        reading_query = open(project_directory + f'\{action}.sql','r')
        sql_query = reading_query.read()
        reading_query.close
    except FileNotFoundError:
        logging.error(f'Could not find {action}.sql file.')
    return sql_query

def create_database(company_host,company_user,company_password,company_db_name):
    mydb = mysql.connector.connect(
                                    host = company_host,
                                    user = company_user,
                                    password = company_password
                                    )
    company_cursor = mydb.cursor()
    company_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {company_db_name};")
    return print("Database succesfully created!")

def delete_database(company_host,company_user,company_password,company_db_name):
    you_sure = input(f"Are you sure u want to delete {company_db_name} forever? (That is a lot of time!). If sure, type Yes, otherwise type anything you want.")
    if you_sure == "Yes":
        mydb=mysql.connector.connect(
                                    host = company_host,
                                    user = company_user,
                                    password = company_password,
                                    database = company_db_name
                                    )
        company_cursor = mydb.cursor()
        company_cursor.execute(f"DROP DATABASE {company_db_name};")
        return print("Database succesfully deleted!")
    else:
        print("Operation Cancelled!")

def connect_and_execute_query(company_host,company_user,company_password,company_db_name,query_action,results:bool):

    """
    This function will attempt to connect to MySQL database using company host, user, password and database name as inputs.\n 
    After that, it will execute a MySQL query which name has the format 'query_that_query_file_will_perform.sql'. If 'results' is ser to 'True', results from query, if there is any, will be returned as a list.
    """

    mydb = mysql.connector.connect(
                                    host = company_host,
                                    user = company_user,
                                    password = company_password,
                                    database = company_db_name
                                    )
    company_cursor = mydb.cursor()
    sql_query = read_query(query_action)
    company_cursor.execute(sql_query)

    if results == True:
        result_from_query = company_cursor.fetchall()
        output_list=[]
        for res in result_from_query:
            output_list.append(res)
        return output_list
    return

def ask_for_sv_data():
    host = input("Please insert host name (default localhost if using XAMPP): ")
    user = input("Please insert username (default root if using XAMPP): ")
    password = input("Please insert password (leave empty if there is no password): ")
    return [host, user, password]

def read_env_file(env_file_name):
    load_dotenv(os.path.dirname(os.path.realpath(__file__))+f"\{env_file_name}.env")
    COMPANY_HOST = os.getenv('COMPANY_HOST')
    COMPANY_USERNAME = os.getenv('COMPANY_USERNAME')
    COMPANY_PASSWORD = os.getenv('COMPANY_PASSWORD')
    return[COMPANY_HOST, COMPANY_USERNAME, COMPANY_PASSWORD]

def import_or_manual_sv_data_gathering():
    use_env_file = input("Would you like to import Server data from .env file? Type 'Yes' if you would like to, otherwise type 'No'.\n Answer: ")
    while use_env_file not in ["Yes", "No"]:
        use_env_file = input("Would you like to import Server data from .env file? Type 'Yes' if you would like to, otherwise type 'No'.\n Answer: ")
    if use_env_file == "Yes":
        env_file_name = input("Insert the name of the .env file: ")
        database_name = input("Please insert desired Database name: ")
        return ["with env", env_file_name, database_name]
    elif use_env_file == "No":
        try:
            sv_data = ask_for_sv_data()
            database_name = input("Please insert desired Database name: ")
            return ["without env", sv_data,database_name]
        except DatabaseError as er:
            return print(er)
    return

def load_document_to_database():
    print("Welcome to Docs. load to database! Please fill in the fields to load documentation.")
    def type_input():
        user_type_input = input(" Please insert Document Type.\n If you would like to see the available options, type 'Options'; otherwise input the Doc. Type: ")
        while (user_type_input not in ["FCV", "FCC", "TIV", "TIC", "NCC", "NCV", "NDC", "NDV"]) and (user_type_input != "Options"):
            user_type_input = input("Please insert valid Document Type.\n If you would like to see the available options, type 'Options'; otherwise input the Doc. Type: ")
        type_options = "\n FCV = Sale doc.\n FCC = Purchase doc.\n TIV = Sale Ticket.\n TIC = Purchase Ticket.\n NCC: Purchase Credit Note.\n NCV: Sale Credit Notes.\n NDC: Purchase Debit Note.\n NDV: Sale Debit Note."
        if user_type_input == "Options":
            print(type_options)
        if user_type_input not in ["FCV", "FCC", "TIV", "TIC", "NCC", "NCV", "NDC", "NDV"]:
            type_input()
        return user_type_input
    user_type_input = type_input()
    print(user_type_input) 
    pattern = '%d/%m/%Y'
    date=None
    while date is None:
        user_input = input("Please insert Invoice/Ticket Date (Format= DD/MM/YYYY): ")
        try:
            date = datetime.strptime(user_input, pattern)
        except ValueError:
            print(f"{user_input} is not a valid date!")
    doc_letter = None
    while doc_letter not in ["A", "B", "C", "E", "M"]:
        doc_letter = input("Please insert Document Letter (A/B/C/E/M): ")
    def get_correct_number(type_of_number_information,max_digits:int):
        while True:
            try:
                user_input = input(f"Please insert {type_of_number_information}: ")
                int(user_input)
            except ValueError:
                print(f"{user_input} is not a valid {type_of_number_information}!")
                continue
            if len(user_input) > max_digits:
                print(f"{user_input} is not a valid {type_of_number_information}!")
            else:
                break
        return user_input
    
    user_point_of_sale_input = get_correct_number("Document Point of Sale number", 5)
    document_POS = str(user_point_of_sale_input).zfill(5)

    user_document_numb_input = get_correct_number("Document number", 8)
    document_numb = str(user_document_numb_input).zfill(8)

    def vendor_ID_number():
        vendor_id = input("Please insert Vendor ID. (11 integer digits): ")
        try:
            int(vendor_id)
        except ValueError:
            return print(f"{vendor_id} is not a valid Vendor ID!"), vendor_ID_number()
        while len(vendor_id) != 11 or vendor_id == "":
            vendor_id = input("Please insert valid Vendor ID. (11 integer digits): ")
        return vendor_id
    vendor_id = print(vendor_ID_number())
    afip_type = input("Please insert AFIP Type of Invoice/Ticket: ")
    "Tax Base",
    "VAT Tax",
    "VAT Withholdings",
    "Gross Income Withholdings",
    "Other Withholdings",
    "Other imports(not Tax Base)",
    "Total Invoice/Ticket Amount"
    return

def operate_on_database(database):
    option = input(f"What action would you like to perform on database {database}?\n 1- Load Bills/Invoices/Other Docs.\n 2- (Incoming) Other option\n Answer: ")
    while option not in ["1", "2", "3", "4"]:
        option = input("What would you like to do? 1- Load Bills/Invoices/Other Docs. \n 2- (Incoming) Other option")
    if option == "1":
        load_document_to_database()
    return

operate_on_database("coca")


# option = input("Hello, Welcome to this Accounting Software! Please enter the number of the action you would like to perform: \n 1- Create New Database. \n 2- Delete an existing Database. \n 3- Operate with an existing Database.\n 4- Close the Program.\n Answer: ")

# while option not in ["1", "2", "3", "4"]:
#         option = input("Please enter the number of the action you would like to do: \n 1- Create New Database. \n 2- Delete an existing Database. \n 3- Operate with an existing Database.\n 4- Close the Program.\n Answer: ")
# if option == "1":
#     sv_data_and_db_name = import_or_manual_sv_data_gathering()
#     if sv_data_and_db_name[0] == "with env":
#         env_data = read_env_file(sv_data_and_db_name[1])
#         create_database(env_data[0], env_data[1], env_data[2], f"{sv_data_and_db_name[2]}")
#         connect_and_execute_query(env_data[0], env_data[1], env_data[2], f"{sv_data_and_db_name[2]}", "create_tables",False)
#     else:
#         data_list = []
#         for data in sv_data_and_db_name[1]:
#             data_list.append(data)
#         create_database(data_list[0], data_list[1], data_list[2], f"{sv_data_and_db_name[2]}")
#         connect_and_execute_query(data_list[0], data_list[1], data_list[2], f"{sv_data_and_db_name[2]}", "create_tables",False)
# elif option == "2":
#         try:
#             data = ask_for_sv_data()
#             database_name = input("Please insert Database name: ")
#             delete_database(data[0], data[1], data[2], database_name)
#         except DatabaseError as er:
#             print(er)
# elif option == "4":
#     print("Closing program! Have a nice day.")
# elif option == "3":
    # sv_data_and_db_name = import_or_manual_sv_data_gathering()
    # if sv_data_and_db_name[0] == "with env":
    #     env_data = read_env_file(sv_data_and_db_name[1])
    #     checking_sv_conn = connect_and_execute_query(env_data[0], env_data[1], env_data[2], f"{sv_data_and_db_name[2]}", "check",True)
    # else:
    #     data_list = []
    #     for data in sv_data_and_db_name[1]:
    #         data_list.append(data)
    #     checking_sv_conn = connect_and_execute_query(data_list[0], data_list[1], data_list[2], f"{sv_data_and_db_name[2]}", "check", True)
    # if len(checking_sv_conn) == 0:
    #     print("Connection Error!")
    # else:
    #     operate_on_database(sv_data_and_db_name[2])