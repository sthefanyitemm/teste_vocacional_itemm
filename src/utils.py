import pymysql
from flask import jsonify, current_app,request
from src.db import  get_mysql_connection

def get_cidade_by_estado(get_cidade):
    connection = get_mysql_connection()
    with connection.cursor() as cur:
        result = cur.execute("SELECT * FROM cidade where CT_UF = %s", [get_cidade])
        print(f"Resultado da consulta SQL: {result}")
        cidade = cur.fetchall()
        print(f"Registros da cidade: {cidade}")
        cidadeArray = []
        for row in cidade:
            cidadeObj = {
                'id': row[0],   # Assumindo que CT_ID é a primeira coluna na sua consulta SQL
                'name': row[1]  # Assumindo que CT_NOME é a segunda coluna na sua consulta SQL
            }
            cidadeArray.append(cidadeObj)
    return jsonify({'cidadeestado': cidadeArray})