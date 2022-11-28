import mysql.connector


def db_connection():
    host = '67.205.163.34'
    user = "sohail"
    password = "sohail123"
    database = 'elm1'
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
    return cnx

# def db_connection():
#     host = 'localhost'
#     user = "root"
#     password = ""
#     database = 'elm'
#     cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
#     return cnx

