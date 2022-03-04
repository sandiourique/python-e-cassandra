import pandas as pd
import uuid
from modules.connector import Bancosql
from modules.connector_cassandra import Cassandra
import __main__

class Insert:

    ## 1 passo - Editando os arquivos CSV - SQL 
    def popular_sql():
        try:
            data = pd.read_csv("Sistema_A_SQL.csv", sep=",") 
            data['vendedor'] = data['vendedor'].fillna("Null")
            data['vendedor'] = data['vendedor'].astype('string')  
        except Exception as e:
            print(str(e))
        # 2 passo - popular o banco postgreSQL

        try:
            for index, row in data.iterrows():
                query = (f"INSERT INTO vendas (nota_fiscal, vendedor, total) VALUES ({int(row['nota_fiscal'])}, '{row['vendedor']}', {float(row['total'])})")
                Bancosql.executar(query)
            print("Oldtech Filial - SQL populado com sucesso!")
            __main__.menu()
        except Exception as e:
            print(str(e)) 
            __main__.menu()

    ## 3 Passo - Editando o arquivo CVS - NoSQL
    def popular_nosql():
        try:
            conectar = Cassandra('oldtech')
            data_nosql = pd.read_csv("Sistema_B_NoSQL.csv", sep=",") 
            data_nosql['vendedor'] = data_nosql['vendedor'].fillna("Null")
            data_nosql['vendedor'] = data_nosql['vendedor'].astype('string')  
            # print(data_nosql)
            lista = []
            for index, row in data_nosql.iterrows(): 
                dados = {'id':str(uuid.uuid4()),'nota_fiscal':f"{int(row['nota_fiscal'])}",'vendedor': f"{repr(str(row['vendedor']))}",
                'total':f"{float(row['total'])}"}  
                lista.append(dados)
            # print(lista)
            # 4 - Passo - popular Cassandra
            conectar.inserir('vendas', lista) 
            print("Oldtech Matriz - NoSQL populado com sucesso!")
            __main__.menu()
        except Exception as e:
            print(str(e)) 

    
    ## Passo 5 - Pegar os dados o PostgreSql, tratar, inserir no banco Cassandra    
    def popular_nosql_sql():
        #buscando os dados no SQL e tratando os dados
        try:
            conectar = Cassandra('oldtech')
            query = "SELECT * FROM vendas;"
            dados = Bancosql.buscar(query)
            dados = pd.DataFrame(dados)  
            dados[0] = dados[0].astype('int') 
            dados[1] = dados[1].astype('string') 
            dados[2] = dados[2].astype('float') 
            # print(dados)
            # print(dados.dtypes)
            lista_sql = []
            for index, row in dados.iterrows():
                dados = {'id':str(uuid.uuid4()),'nota_fiscal': f'{row[0]}','vendedor': repr(str(row[1])), 'total':f'{row[2]}'}
                lista_sql.append(dados)
                # print(lista_sql)
            
            conectar.inserir('vendas', lista_sql) 
            print("Dados transferidos com populado com sucesso!")
            __main__.menu() 
            
        except Exception as e:
            print(str(e))
            
    #metodo para mostrar os dados da filial - sql        
    def mostrar_filial():
        query = "SELECT * FROM vendas;"
        dados = Bancosql.buscar(query)
        dados = pd.DataFrame(dados)
        print(dados) 

    # metodo para mostrar os dados da matriz - NoSQL
    def mostrar_matriz():
        conectar = Cassandra('oldtech')
        conectar.buscar('vendas')

 
