import sqlite3

arquivo = r''

def sqlite(func):

	def operação(**kwargs):

		if not arquivo:
			raise Exception("""O endereço do banco não foi apontado, utilize a função "conectar" para apontar o endereço do banco a ser utilizado.""")

		conexão = sqlite3.connect(arquivo)
		cursor = conexão.cursor()
		
		a = func(cursor=cursor, **kwargs)

		conexão.commit()
		conexão.close()

		if a:
			return a

	return operação

def formatação(valores):

	saida = ''

	if type(valores) == list:
		for A in valores:
		
			if type(A) == str: saida += f"'{A}', "
			elif type(A) == int: saida += f'{A}, '

		saida = saida[:-2]

	else:
		saida = str(valores) if type(valores) == int else f"'{valores}'"
	return saida

def conectar(endereço:str="database.db"):
	global arquivo
	arquivo = endereço

@sqlite
def inserir(**kwargs):
	"""
	tabela = tabela a inserir,
	valores = lista de valores a ser inserida.
	"""

	valores = formatação(kwargs.get("valores"))
	tabela = kwargs.get("tabela")
	cursor = kwargs.get("cursor")

	cursor.execute(f"INSERT INTO {tabela} VALUES({valores})")

@sqlite
def atualizar(**kwargs):
	"""
	tabela = tabela a procurar,
	v1 = Célula a ser alterada,
	v2 = valor a inserir na célula,
	v3 = célula de checagem,
	v4 = valor esperado na célula de checagem.
	"""


	cursor = kwargs.get("cursor")
	tabela = kwargs.get("tabela")

	v1 = kwargs.get("v1")  ;  v2 = formatação(kwargs.get("v2"))
	v3 = kwargs.get("v3")  ;  v4 = formatação(kwargs.get("v4"))

	cursor.execute(f"UPDATE {tabela} SET {v1} = {v2} WHERE {v3} = {v4}")

@sqlite
def deletar(**kwargs):
	"""
	tabela = tabela a procurar,
	v1 = célula a procurar,
	v2 = valor esperado na célula.
	"""

	cursor = kwargs.get("cursor")
	tabela = kwargs.get('tabela')

	v1 = kwargs.get("v1")
	v2 = formatação(kwargs.get("v2"))

	cursor.execute(f"DELETE FROM {tabela} WHERE {v1} = {v2}")

@sqlite
def selecionar(**kwargs):
	"""
	tabela = tabela a procurar,
	v1 = célula(s) a ser selecionada,
	v2 = célula a procurar,
	v3 = valor esperado no v2.
	ATENÇÃO: Ao usar mais de um valor no V1, formate corretamente!!!
	"""
	
	cursor = kwargs.get("cursor")
	tabela = kwargs.get('tabela')

	v1 = kwargs.get("v1")
	v2 = kwargs.get("v2")
	v3 = formatação(kwargs.get("v3"))

	cursor.execute(f"SELECT {v1} FROM {tabela} WHERE {v2} = {v3}")
	
	res = cursor.fetchone()
	if res:
		if len(res) > 1:
			return list(cursor.fetchone())
		else:
			return res[0]
	else:
		return None




#sqlite3.IntegrityError = nome já existente
#selecionar retorna None: nenhum valor encontrado

#deletar(tabela="users", v1='nome', v2='gabriel')
#atualizar(tabela='users', v1="num", v2=999, v3='nome', v4="gabriel")
#inserir(tabela='users', valores=['gabriel', 1234])
#print(selecionar(tabela="users", v1='num', v2='nome', v3='gabriel'))