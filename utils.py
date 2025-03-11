# utils.py
from database import get_database_schema, query_database
from cache import salvar_resposta, buscar_resposta_cache

def generate_response(user_question, model):
    """Gera a resposta com base na pergunta do usuário."""
    if model is None:
        return "❌ O modelo não foi carregado corretamente."
    
    if not user_question.strip():
        return "❌ Por favor, insira uma pergunta válida."
    
    # Verifica se já existe a resposta no cache
    resposta_cache = buscar_resposta_cache(user_question)
    if resposta_cache:
        return f"📌 **Resposta recuperada do histórico:**\n\n{resposta_cache}"
    
    # Obtém a estrutura do banco
    schema = get_database_schema()
    if not schema:
        return "❌ Erro ao buscar a estrutura do banco de dados."
    
    # Identifica a tabela mais relevante com base na pergunta
    table_to_query = None
    for table in schema.keys():
        if table.lower() in user_question.lower():
            table_to_query = table
            break
    
    # Se nenhuma tabela for encontrada, lista as tabelas disponíveis
    if not table_to_query:
        return f"📊 O banco contém as seguintes tabelas:\n" + "\n".join([f"- {table}" for table in schema.keys()])
    
    # Consulta otimizada: limita a 5 colunas para desempenho
    columns = ", ".join(schema[table_to_query][:5])
    query = f'SELECT {columns} FROM "{table_to_query}" ORDER BY ROWID DESC LIMIT 5;'
    result = query_database(query)
    
    if isinstance(result, str):
        return result  # Retorna a mensagem de erro da consulta
    
    # Prepara os dados extraídos para o prompt
    dados_texto = "\n".join([", ".join(map(str, row)) for row in result])
    prompt = f"""
    Você é um assistente que responde perguntas sobre um banco de dados.
    Aqui estão os últimos registros extraídos:
    {dados_texto}
    Com base nesses dados, responda à seguinte pergunta de forma clara e objetiva:
    "{user_question}"
    """
    
    try:
        resposta = model.generate(prompt).strip()
        salvar_resposta(user_question, resposta)
        return resposta
    except Exception as e:
        return f"❌ Erro ao processar a solicitação: {str(e)}"
