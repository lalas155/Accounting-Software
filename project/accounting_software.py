import os
import mysql.connector
import logging
from dotenv import load_dotenv
from mysql.connector.errors import DatabaseError
from datetime import datetime
import xlrd
import requests
from mysql.connector import errorcode
import pandas as pd
import pymysql
import pandas.io.sql as sql


def read_query(action):
    project_directory = os.path.dirname(os.path.realpath(__file__))
    try:
        reading_query = open(project_directory + f'\{action}.sql','r')
        sql_query = reading_query.read()
        reading_query.close
    except FileNotFoundError:
        logging.error(f'Could not find {action}.sql file.')
    return sql_query

def create_database(company_host, company_user, company_password, company_db_name):
    mydb = mysql.connector.connect(
                                    host = company_host,
                                    user = company_user,
                                    password = company_password
                                    )
    company_cursor = mydb.cursor()
    company_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {company_db_name};")
    return print("Database succesfully created!")

def delete_database(company_host, company_user, company_password, company_db_name):
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

def connect_and_execute_query(company_host, company_user, company_password, company_db_name, query_action, results:bool):

    """
    This function will attempt to connect to MySQL database using company host, user, password and database name as inputs.\n 
    After that, it will execute a MySQL query which name has the format 'action_that_query_will_perform.sql'. If 'results' is set to 'True', results from query, if there is any, will be returned.
    """

    sql_query = read_query(query_action)
    con = pymysql.connect(user=company_user, password=company_password, database=company_db_name, host=company_host)
    if results == True:
        output = sql.read_sql(sql_query, con)
        return  output

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
        database_name = input("Please insert Database name: ")
        return ["with env", env_file_name, database_name]
    elif use_env_file == "No":
        try:
            sv_data = ask_for_sv_data()
            database_name = input("Please insert Database name: ")
            return ["without env", sv_data,database_name]
        except DatabaseError as er:
            return print(er)
    return

def get_correct_number(information_about_number, max_digits:int):
            """
            Information about number: a description of what kind of information the input you are asking for represents.
            Asks for an integer input and checks if it is. Keeps asking for it as long as it is not an integer.
            Finally, checks if the input length is larger than the 'max_digits' available for that number.
            Returns the number as a string.
            """
            while True:
                try:
                    user_input = input(f"Please insert {information_about_number}: ")
                    int(user_input)
                except ValueError:
                    print(f"{user_input} is not a valid {information_about_number}!")
                    continue
                if len(user_input) > max_digits:
                    print(f"{user_input} is not a valid {information_about_number}!")
                else:
                    break
            return user_input

def load_document_to_database(server_data, database_name):
    my_database = mysql.connector.connect(
                                            host = server_data[0],
                                            user = server_data[1],
                                            password = server_data[2],
                                            database = database_name
                                        )
    company_cursor = my_database.cursor()
    print("Welcome to Documentation load to database! Please fill in the fields.")
    document_information = ["", "", "", "", "", "", ""]
    loading = True
    while loading:
        vat_base_105 = 0
        vat_base_21 = 0
        vat_base_27 = 0
        vat_105 = 0
        vat_21 = 0
        vat_27 = 0
        vat_withholdings = 0
        gross_income_withholdings = 0
        other_withholdings = 0
        other_amounts_not_tax_base = 0
        doc_table = "sales_docs"
        table = ""
        prefix = "20222222223"
        name = ""
        initial_info = True
        amounts_info = True
        afip_doc_type = ["", ""]
        while ("" in document_information) or (initial_info):
            vendor_or_client = "Vendor/Client"
            if document_information[1] in ["FCV","TIV","NCV","NDV"]:
                vendor_or_client = "Client"
            elif document_information[1] in ["FCC","TIC","NCC","NDC"]:
                vendor_or_client = "Vendor"              
            if vendor_or_client == "Client":
                doc_table = "sales_docs"
                table = "clients"
                prefix = "client_"
            elif vendor_or_client == "Vendor":
                doc_table = "purchase_docs"
                table = "clients"
                prefix = "vendor_"
            print("0- Date: ",document_information[0])
            print("1- Type: ",document_information[1])
            print("2- Letter: ",document_information[2])
            print("3- PoS: ",document_information[3])
            print("4- Number: ",document_information[4])
            print(f"5- {vendor_or_client} ID: ",document_information[5], f"- {vendor_or_client} Name: {name}")
            print("6- AFIP Type: ",document_information[6], F"- {afip_doc_type[1]}")
            if "" in document_information:
                pass
            else:
                print("\n7- Continue to load amounts.")
            print("\n8- Restart load.")
            print("9- Leave.")
            option = input("Please insert the number of the information you would like to load: ")
            if option == "1":
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
                document_information[1] = user_type_input
            elif option == "2":
                doc_letter = None
                while doc_letter not in ["A", "B", "C", "E", "M"]:
                    doc_letter = input("Please insert Document Letter (A/B/C/E/M): ")
                document_information[2] = doc_letter
            elif option == "0":
                pattern = '%d/%m/%Y'
                doc_date = None
                while doc_date is None:
                    user_input = input("Please insert Document Date (Format= DD/MM/YYYY): ")
                    try:
                        doc_date = datetime.strptime(user_input, pattern).date()
                    except ValueError:
                        print(f"{user_input} is not a valid date!")
                document_information[0] = datetime.strftime(doc_date, pattern)
            elif option == "3":
                user_point_of_sale_input = get_correct_number("Document Point of Sale number", 5)
                document_POS = str(user_point_of_sale_input).zfill(5)
                document_information[3] = document_POS
            elif option == "4":
                user_document_numb_input = get_correct_number("Document number", 8)
                document_numb = str(user_document_numb_input).zfill(8)
                document_information[4] = document_numb
            elif option == "5":
                vendor_client_id = get_correct_number(f"{vendor_or_client} ID (11 Int Digits)", 11)
                while len(vendor_client_id) != 11:
                    print(f"{vendor_client_id} is not a valid {vendor_or_client} ID (11 Int Digits)!")
                    vendor_client_id = get_correct_number(f"{vendor_or_client} ID (11 Int Digits)", 11)
                document_information[5] = vendor_client_id
                try:
                    name_query = f"SELECT {prefix}name FROM {table} WHERE {prefix}id = '{vendor_client_id}'"
                    name = company_cursor.execute(name_query)
                    result_from_query = company_cursor.fetchall()
                    if len(result_from_query) != 1:
                        name = f"Could not find {vendor_or_client} ID in Database."
                    if len(result_from_query) == 1:
                        name = result_from_query[0][0]
                except mysql.connector.ProgrammingError as err:
                    if err.errno == errorcode.ER_SYNTAX_ERROR:
                        continue
            elif option == "6":
                def get_afip_doc_types(afip_type):
                    project_directory = os.path.dirname(os.path.realpath(__file__))
                    file_name = "/afip_doc_types.xls"
                    if file_name in project_directory:
                        pass
                    else:
                        afip_doc_types_url = "https://www.afip.gob.ar/fe/documentos/TABLACOMPROBANTES.xls"
                        request=requests.get(afip_doc_types_url)
                        open(project_directory+"/afip_doc_types.xls","wb").write(request.content)
                    workbook = xlrd.open_workbook(project_directory + file_name)
                    sheet = workbook.sheet_by_index(0)
                    row_count = sheet.nrows
                    col_count = sheet.ncols
                    raw_afip_doc_types = []
                    for cur_row in range(0, row_count):
                        for cur_col in range(0, col_count):
                            cell = sheet.cell(cur_row, cur_col)
                            raw_afip_doc_types.append(cell.value)
                    if afip_type in raw_afip_doc_types:
                        return afip_type ,raw_afip_doc_types[raw_afip_doc_types.index(afip_type)+1]
                    else:
                        return "Wrong"
                afip_doc_type_input = input("Please insert AFIP Type of Document: ")
                afip_doc_type = get_afip_doc_types(afip_doc_type_input)
                while afip_doc_type == "Wrong":
                    afip_doc_type_input = input("Please insert valid AFIP Type of Document: ")
                    afip_doc_type = get_afip_doc_types(afip_doc_type_input)
                document_information[6] = afip_doc_type[0]
            elif option == "8":
                return "Restart"
            elif option == "9":
                return "Leave"
            elif option == "7":
                initial_info = False
        if document_information[2] in ("B", "C", "E"):
            other_amounts_not_tax_base = get_correct_number("the total amount of the Document.", 99)
            document_total_amount = other_amounts_not_tax_base
            document_information.append(other_amounts_not_tax_base)
            document_information.append(document_total_amount)
            print(f"Your are about to load the following Document:\n {doc_date} - {user_type_input} - {doc_letter} - {document_POS}-{document_numb}\n {vendor_or_client} ID: {vendor_client_id}    {vendor_or_client} Name: {name}\n AFIP Type: {afip_doc_type[0]}\n Total Document Amount: {document_total_amount}")
            final_check = input("Load to database? ('Yes' or 'Restart'): ")
            while final_check not in ["Yes", "Restart"]:
                final_check = input("Load to database? ('Yes' or 'Restart'): ")
            if final_check == "Restart":
                return "Restart"
            elif final_check == "Yes":
                sql_query = f"INSERT INTO {doc_table} (doc_date, user_type_input, doc_letter, document_POS, document_numb, {prefix}id, {prefix}name, afip_doc_type, other_amounts_not_vat_Base, total_document_amount) VALUES ('{datetime.strftime(doc_date, pattern)}', '{user_type_input}', '{doc_letter}', '{document_POS}', '{document_numb}', '{vendor_client_id}', '{name}', '{document_information[6]}', {other_amounts_not_tax_base}, {document_total_amount})"
                company_cursor.execute(sql_query)
                my_database.commit()
                return "Restart"
        else:
            document_amounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            while amounts_info:
                document_total_amount = 0
                for i in range(0, len(document_amounts) - 1):
                    document_total_amount += document_amounts[i]
                document_amounts[10] = document_total_amount
                print("0- VAT Base 10.5%: ",document_amounts[0])
                print("1- VAT Base 21%: ",document_amounts[1])
                print("2- VAT Base 27%: ",document_amounts[2])
                print("3- VAT 10.5%: ",document_amounts[3])
                print("4- VAT 21%: ",document_amounts[4])
                print("5- VAT 27%: ",document_amounts[5])
                print("6- VAT Withholdings: ",document_amounts[6])
                print("7- Gross Income Withholdings: ",document_amounts[7])
                print("8- Other Withholdings: ",document_amounts[8])
                print("9- Other Amounts: ",document_amounts[9])
                print("Total Amount: ",document_amounts[10])
                if all(amount == 0 for amount in document_amounts):
                    pass
                else:
                    print("\n10- Load Document")
                print("11- Back to previous page.")
                print("12- Restart load.")
                option = input("Please insert the number of the information you would like to load: ")
                if option == "0":
                    vat_base_105 = get_correct_number("the Document 10.5% VAT Base.", 99)
                    document_amounts[0] = int(vat_base_105)
                elif option == "1":
                    vat_base_21 = get_correct_number("the Document 21% VAT Base.", 99)
                    document_amounts[1] = int(vat_base_21)
                elif option == "2":
                    vat_base_27 = get_correct_number("the Document 27% VAT Base.", 99)
                    document_amounts[2] = int(vat_base_27)
                elif option == "3":
                    vat_105 = get_correct_number("the Document 10.5% VAT.", 99)
                    document_amounts[3] = int(vat_105)
                elif option == "4":
                    vat_21 = get_correct_number("the Document 21% VAT.", 99)
                    document_amounts[4] = int(vat_21)
                elif option == "5":
                    vat_27 = get_correct_number("the Document 27% VAT.", 99)
                    document_amounts[5] = int(vat_27)
                elif option == "6":
                    vat_withholdings = get_correct_number("the Document VAT Withholdings.", 99)
                    document_amounts[6] = int(vat_withholdings)
                elif option == "7":
                    gross_income_withholdings = get_correct_number("the Document VAT Withholdings.", 99)
                    document_amounts[7] = int(gross_income_withholdings)
                elif option == "8":
                    other_withholdings = get_correct_number("the Document other Withholdings. If not applicable, enter zero.", 99)
                    document_amounts[8] = int(other_withholdings)
                elif option == "9":
                    other_amounts_not_tax_base = get_correct_number("the Document other amounts that do not match any of the criteria asked above.", 99)
                    document_amounts[9] = int(other_amounts_not_tax_base)
                elif option == "12":
                    return "Restart"
                elif option == "11":
                    amounts_info = False
                    initial_info = True
                elif option == "10":

                    print(f"Your are about to load the following Document:\n {doc_date} - {user_type_input} - {doc_letter} - {document_POS}-{document_numb}\n {vendor_or_client} ID: {vendor_client_id}    {vendor_or_client} Name: {name}\n AFIP Type: {afip_doc_type[0]}\n VAT Base 10.5: {vat_base_105}    VAT 10.5: {vat_105}\n VAT Base 21: {vat_base_21}    VAT 21: {vat_21}\n VAT Base 27: {vat_base_27}    VAT 27: {vat_27}\n VAT Withholdings: {vat_withholdings}\n Gross Income Withholdings: {gross_income_withholdings}\n Other amounts: {other_amounts_not_tax_base}\n Total Document Amount: {document_total_amount}")
                    
                    final_check = input("Are you sure? ('Yes', 'Back' or 'Restart'): ")
                    while final_check not in ["Yes", 'Back', "Restart"]:
                        final_check = input("Load to database? ('Yes', 'Back' or 'Restart'): ")
                    if final_check == "Restart":
                        return "Restart"
                    elif final_check == "Back":
                        initial_info = False
                        amounts_info = True
                    elif final_check == "Yes":
                        sql_query = f"INSERT INTO {doc_table} VALUES ('{datetime.strftime(doc_date, pattern)}', '{user_type_input}', '{doc_letter}', '{document_POS}', '{document_numb}', '{vendor_client_id}', '{name}','{document_information[6]}', {vat_base_105}, {vat_base_21}, {vat_base_27}, {vat_105}, {vat_21}, {vat_27}, {vat_withholdings}, {gross_income_withholdings}, {other_withholdings}, {other_amounts_not_tax_base}, {document_total_amount})"
                        company_cursor.execute(sql_query)
                        my_database.commit()
                        return "Restart"
    return "Restart"

def operate_on_database(server_data, database_name):
    while True:
        option = input(f"What action would you like to perform on database {database_name}?\n 1- Load Bills/Invoices/Other Docs.\n 2- Get Sales / Purchase Reports.\n 3- (Incoming) Other option\n Answer: ")
        while option not in ["1", "2", "3", "4"]:
            option = input(f"What action would you like to perform on database {database_name}?\n 1- Load Bills/Invoices/Other Docs.\n 2- (Incoming) Other option\n Answer: ")
        if option == "1":
            answer = load_document_to_database(server_data,database_name)
            while answer == "Restart":
                answer = load_document_to_database(server_data,database_name)
            if answer == "Leave":
                continue
        if option == "2":
            sales_or_purchase_report = input("Please indicate if you would like to get Sales('S') or Purchase('P') report.\nTo go back type 'Back'.\n -Answer: ")
            while sales_or_purchase_report not in ["S", "P", "Back"]:
                sales_or_purchase_report = input("Please indicate if you would like to get Sales('S') or Purchase('P') report.")
            if sales_or_purchase_report == "Back":
                continue
            elif sales_or_purchase_report == "S":
                sales_report = connect_and_execute_query(server_data[0], server_data[1], server_data[2], database_name, "get_sales_report", True)
                sales_report.to_excel("Sales_Report.xlsx", index=False)




option = input("Hello, Welcome to this Accounting Software! Please enter the number of the action you would like to perform: \n 1- Create New Database. \n 2- Delete an existing Database. \n 3- Operate with an existing Database.\n 4- Close the Program.\n Answer: ")

while option not in ["1", "2", "3", "4"]:
        option = input("Please enter the number of the action you would like to do: \n 1- Create New Database. \n 2- Delete an existing Database. \n 3- Operate with an existing Database.\n 4- Close the Program.\n Answer: ")
if option == "1":
    sv_data_and_db_name = import_or_manual_sv_data_gathering()
    if sv_data_and_db_name[0] == "with env":
        env_data = read_env_file(sv_data_and_db_name[1])
        create_database(env_data[0], env_data[1], env_data[2], f"{sv_data_and_db_name[2]}")
        connect_and_execute_query(env_data[0], env_data[1], env_data[2], f"{sv_data_and_db_name[2]}", "create_tables",False)
    else:
        data_list = []
        for data in sv_data_and_db_name[1]:
            data_list.append(data)
        create_database(data_list[0], data_list[1], data_list[2], f"{sv_data_and_db_name[2]}")
        connect_and_execute_query(data_list[0], data_list[1], data_list[2], f"{sv_data_and_db_name[2]}", "create_tables",False)
elif option == "2":
        try:
            data = ask_for_sv_data()
            database_name = input("Please insert Database name: ")
            delete_database(data[0], data[1], data[2], database_name)
        except DatabaseError as er:
            print(er)
elif option == "4":
    print("Closing program! Have a nice day.")
elif option == "3":
    env_or_manual_and_db_name = import_or_manual_sv_data_gathering()
    server_data = []
    if env_or_manual_and_db_name[0] == "with env":
        env_data = read_env_file(env_or_manual_and_db_name[1])
        checking_sv_conn = connect_and_execute_query(env_data[0], env_data[1], env_data[2], f"{env_or_manual_and_db_name[2]}", "check",True)
        for data in env_data:
            server_data.append(data)
    elif env_or_manual_and_db_name[0] == "without env":
        for data in env_or_manual_and_db_name[1]:
            server_data.append(data)
        checking_sv_conn = connect_and_execute_query(server_data[0], server_data[1], server_data[2], f"{env_or_manual_and_db_name[2]}", "check", False)
        operate_on_database(server_data,env_or_manual_and_db_name[2])