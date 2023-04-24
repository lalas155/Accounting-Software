import os
import mysql.connector
import logging
from dotenv import load_dotenv
from mysql.connector.errors import DatabaseError
from datetime import datetime
import xlrd
import requests

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

def get_correct_number(information_about_number,max_digits:int):
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

def load_document_to_database():
    print("Welcome to Documentation load to database! Please fill in the fields.")
    document_information = ["", "", "", "", "", ""]
    loading = True
    while loading:
        while "" in document_information:
            vendor_or_client = "Vendor/Client"
            if document_information[1] in ["FCV","TIV","NCV","NDV"]:
                vendor_or_client = "Client"
            elif document_information[1] in ["FCC","TIC","NCC","NDC"]:
                vendor_or_client = "Vendor"
            print("0- Date: ",document_information[0])
            print("1- Type: ",document_information[1])
            print("2- Letter: ",document_information[2])
            print("3- PoS: ",document_information[3])
            print("4- Number: ",document_information[4])
            print(f"5- {vendor_or_client} ID: ",document_information[5])
            print("6- AFIP Type: ",document_information[6])
            print("Restart load.")
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
                date = None
                while date is None:
                    user_input = input("Please insert Document Date (Format= DD/MM/YYYY): ")
                    try:
                        date = datetime.strptime(user_input, pattern)
                    except ValueError:
                        print(f"{user_input} is not a valid date!")
                document_information[0] = date
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
            elif option == "6":
                def get_afip_doc_types():
                    project_directory = os.path.dirname(os.path.realpath(__file__))
                    file_name = "/afip_doc_types.xls"
                    if file_name in project_directory:
                        pass
                    else:
                        afip_doc_types_url = "https://www.afip.gob.ar/fe/documentos/TABLACOMPROBANTES.xls"
                        request=requests.get(afip_doc_types_url)
                        open(project_directory+"/afip_doc_types.xls","wb").write(request.content)
                    workbook = xlrd.open_workbook(project_directory+file_name)
                    sheet = workbook.sheet_by_index(0)
                    row_count = sheet.nrows
                    col_count = sheet.ncols
                    raw_afip_doc_types = []
                    for cur_row in range(0, row_count):
                        for cur_col in range(0, col_count):
                            cell = sheet.cell(cur_row, cur_col)
                            raw_afip_doc_types.append(cell.value)
                    afip_doc_types = []
                    for type in raw_afip_doc_types:
                        if len(str(type)) == 3:
                            afip_doc_types.append(type)
                        else:
                            continue
                    return afip_doc_types
                types = get_afip_doc_types()
                afip_doc_type_input = input("Please insert AFIP Type of Document: ")
                while afip_doc_type_input not in types:
                    afip_doc_type_input = input("Please insert valid AFIP Type of Document: ")
                document_information[6] == afip_doc_type_input
            elif option == "Restart":
                return "Restart"
        if doc_letter == "B" or "C" or "E":
            other_amounts_not_tax_base = get_correct_number("the total amount of the Document.")
            document_total_amount = other_amounts_not_tax_base
            document_information.append(other_amounts_not_tax_base)
            document_information.append(document_total_amount)
            print(f"Your are about to load the following Document:\n {date} {user_type_input} {doc_letter} {document_POS}-{document_numb}\n {vendor_or_client} ID: {vendor_client_id}\n AFIP Type: {afip_doc_type_input}\n Total Document Amount: {document_total_amount}")
            final_check = input("Load to database? ('Yes' or 'Restart'): ")
            while final_check != "Yes" or "Restart":
                final_check = input("Load to database? ('Yes' or 'Restart'): ")
            if final_check == "Restart":
                return "Restart"
            elif final_check == "Yes":
                return document_information
        else:
            document_amounts = ["","","","","","","","","",""]
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
            option = input("Please insert the number of the information you would like to load: ")
            if option == "0":
                tax_base_105 = get_correct_number("the Document 10.5% VAT Base. If not applicable, enter zero.", 99)
                document_amounts[0] = tax_base_105
            elif option == "1":
                tax_base_21 = get_correct_number("the Document 21% VAT Base. If not applicable, enter zero.", 99)
                document_amounts[1] = tax_base_21
            elif option == "2":
                tax_base_27 = get_correct_number("the Document 27% VAT Base. If not applicable, enter zero.", 99)
                document_amounts[2] = tax_base_27
            elif option == "3"_
                vat_105 = get_correct_number("the Document 10.5% VAT. If not applicable, enter zero.", 99)
                document_amounts[3] = vat_105
            elif option == "4":
                vat_21 = get_correct_number("the Document 21% VAT. If not applicable, enter zero.", 99)
                document_amounts[4] = vat_21
            elif option == "5":
                vat_27 = get_correct_number("the Document 27% VAT. If not applicable, enter zero.", 99)
                document_amounts[5] = vat_27
            elif option == "6":
                vat_withholdings = get_correct_number("the Document VAT Withholdings. If not applicable, enter zero.", 99)
                document_amounts[6] = vat_withholdings
            
            gross_income_withholdings = get_correct_number("the Document Gross Income Withholdings. If not applicable, enter zero.", 99)
            other_withholdings = get_correct_number("the Document other Withholdings. If not applicable, enter zero.", 99)
            other_amounts_not_tax_base = get_correct_number("the Document other amounts that do not match any of the criteria asked above.", 99)
            document_total_amount = tax_base_105 + tax_base_21 + tax_base_27 + vat_105 + vat_21 + vat_27 + vat_withholdings + gross_income_withholdings + other_withholdings + other_amounts_not_tax_base
            document_amounts.append(document_total_amount)
            
            final_check = print(f"Your are about to load the following Document:\n {date} {user_type_input} {doc_letter} {document_POS}-{document_numb}\n AFIP Type: {afip_doc_type_input}\n VAT Base 10.5: {tax_base_105}    VAT 10.5: {vat_105}\n VAT Base 21:{tax_base_21}    VAT 21:{vat_21}\n VAT Base 27: {tax_base_27}    VAT 27: {vat_27}\n VAT Withholdings: {vat_withholdings}\n Gross Income Withholdings: {gross_income_withholdings}\n Other amounts: {other_amounts_not_tax_base}\n Total Document Amount: {document_total_amount}")

        return

def operate_on_database(database):
    option = input(f"What action would you like to perform on database {database}?\n 1- Load Bills/Invoices/Other Docs.\n 2- (Incoming) Other option\n Answer: ")
    while option not in ["1", "2", "3", "4"]:
        option = input(f"What action would you like to perform on database {database}?\n 1- Load Bills/Invoices/Other Docs.\n 2- (Incoming) Other option\n Answer: ")
    if option == "1":
        answer = load_document_to_database()
        while answer == "Restart":
            answer = load_document_to_database()
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