import pandas as pd
import subprocess
from chardet import detect

def detect_encoding(file_path):
    """
    Detecta a codificação de um arquivo para evitar erros de leitura.
    """
    with open(file_path, "rb") as f:
        result = detect(f.read(10000))  # Analisa os primeiros 10KB
    return result["encoding"]

def load_csv(file_path):
    """
    Carrega um arquivo CSV usando pandas e retorna o DataFrame.
    """
    try:
        encoding = detect_encoding(file_path)  # Detecta a codificação do arquivo
        dataframe = pd.read_csv(file_path, encoding=encoding)
        print(f"Arquivo '{file_path}' carregado com sucesso!")
        print("Exemplo dos dados:")
        print(dataframe)  
        return dataframe
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
    return None

def ask_llama(question, context):
    """
    Envia uma pergunta ao modelo Llama3.1:8b e retorna a resposta.
    """
    try:
        # Prepara o comando para chamar o modelo localmente
        prompt = f"Contexto: {context}\n\nPergunta: {question}"
        result = subprocess.run(
            ["ollama", "run", "llama3.1:8b"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding='utf-8',  # Força a codificação UTF-8
            errors='replace'   # Substitui caracteres inválidos
        )
        # Verifica se houve erro na execução do comando
        if result.returncode != 0:
            print(f"Erro ao chamar o modelo: {result.stderr}")
            return "Houve um erro ao processar sua pergunta. Tente novamente."

        # Retorna a resposta do modelo com tratamento de caracteres
        return result.stdout.strip()
    except Exception as e:
        print(f"Erro ao processar a pergunta: {e}")
        return "Ocorreu um erro inesperado ao consultar a IA."

def main():
    # Carregar o arquivo CSV
    file_path = "veiculos_movida.csv"
    dataframe = load_csv(file_path)
    
    if dataframe is None:
        print("Não foi possível carregar os dados. Encerrando o programa.")
        return
    
    # Gerar um contexto básico para o modelo
    context = dataframe.to_string(index=False)  # Converte as primeiras linhas do CSV para texto
    
    print("\nO arquivo foi carregado e está pronto para perguntas!")
    print("Digite 'sair' para encerrar o programa.")
    
    while True:
        question = input("\nFaça uma pergunta sobre os dados: ")
        if question.lower() == "sair":
            print("Encerrando o programa. Até logo!")
            break
        
        # Consultar o modelo e exibir a resposta
        response = ask_llama(question, context)
        print(f"\nResposta da IA: {response}")

if __name__ == "__main__":
    main()
