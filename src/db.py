import pymysql
from flask import jsonify, current_app,request



def get_mysql_connection():
    return pymysql.connect(host='localhost', port=3306, user='root', passwd='', database='teste_prod')


def get_estados():
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT UF_ID, UF_NOME FROM estado")
            estados = [{'UF_ID': uf_id, 'UF_NOME': uf_nome} for uf_id, uf_nome in cursor.fetchall()]
            return estados
    except Exception as e:
        print(f"Erro ao obter estados do banco de dados: {e}")
        return []
    finally:
        connection.close()

def get_cidade_by_estado(get_cidade):
    connection = get_mysql_connection()
    with connection.cursor() as cur:
        result = cur.execute("SELECT * FROM cidade where CT_UF = %s", [get_cidade])
        cidade = cur.fetchall()
        cidadeArray = []
        for row in cidade:
            cidadeObj = {
                'id': row[0],   # Assumindo que CT_ID é a primeira coluna na sua consulta SQL
                'name': row[1]  # Assumindo que CT_NOME é a segunda coluna na sua consulta SQL
            }
            cidadeArray.append(cidadeObj)
    return jsonify({'cidadeestado': cidadeArray})


