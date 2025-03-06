import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from bs4 import BeautifulSoup

# Configurar o serviço do ChromeDriver
servico = Service(ChromeDriverManager().install())
# Inicializar o navegador Chrome
navegador = webdriver.Chrome(service=servico)

# Configurar o logger para redirecionar os erros para um arquivo de log
logging.basicConfig(filename='erros.log', level=logging.ERROR)

# Função para suprimir erros
def suprimir_erros(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Erro suprimido: {e}")
            pass
    return wrapper

@suprimir_erros
def executar_script():
    
    # Variáveis para os elementos interativos
    CIDADE = "São Paulo"
    OPCAO_LOCAL = 'SAO PAULO - GUARULHOS AEROPORTO'
    
    # Parâmetros das datas (formato: ano, mês 0-based, dia)
    DATA_RETIRADA_ANO = "2025"
    DATA_RETIRADA_MES = "2"  # Janeiro = 0, Fevereiro = 1
    DATA_RETIRADA_DIA = "31"
    
    DATA_DEVOLUCAO_ANO = "2025"
    DATA_DEVOLUCAO_MES = "3"
    DATA_DEVOLUCAO_DIA = "4"

    # Acessar o site da Movida
    navegador.get("https://www.movida.com.br/")
    navegador.maximize_window()
    print("Site da Movida carregado com sucesso!")
    
    # Campo de localização
    campo_local = WebDriverWait(navegador, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Onde você quer alugar?')]")))
    print("Campo de localização encontrado e pronto para inserção!")
    campo_local.send_keys(f'{CIDADE}')
    time.sleep(1)
    
    # Seleção da agência
    opcao_local = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{OPCAO_LOCAL}')]")))
    opcao_local.click()
    print("Agência selecionada com sucesso!")
    
    # Interação com calendário de retirada
    WebDriverWait(navegador, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="data_retirada"]'))).click()
    print("Botão do calendário de retirada clicado com sucesso!")
    
    data_retirada = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, 
            f'(//div[contains(@class, "pika-single")][.//button[@data-pika-year="{DATA_RETIRADA_ANO}" '
            f'and @data-pika-month="{DATA_RETIRADA_MES}"]])[1]//button[@data-pika-day="{DATA_RETIRADA_DIA}"]'
        )))
    data_retirada.click()
    print("Data de retirada selecionada!")
    
    # Interação com calendário de devolução
    WebDriverWait(navegador, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="data_devolucao"]'))).click()
    print("Calendário para seleção da data de devolução aberto!")
    
    data_devolucao = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, 
            f'(//div[contains(@class, "pika-single")][.//button[@data-pika-year="{DATA_DEVOLUCAO_ANO}" '
            f'and @data-pika-month="{DATA_DEVOLUCAO_MES}"]])[2]//button[@data-pika-day="{DATA_DEVOLUCAO_DIA}"]'
        )))
    data_devolucao.click()
    print("Data de devolução selecionada!")

    # Garantir que o botão de busca esteja visível e clicável
    botao_busca = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="search-content"]/button'))
    )
    # Garantir visibilidade do botão de busca
    navegador.execute_script("arguments[0].scrollIntoView(true);", botao_busca)
    # Clicar no botão de busca
    botao_busca.click()
    print("Botão de busca de veículos clicado com sucessos!")

    # Alternar para a nova aba aberta
    abas = navegador.window_handles
    navegador.switch_to.window(abas[0])
    print("Alternado para a aba de veículos!")
    time.sleep(4)

    # Encontrar blocos de veículos
    blocos_veiculos = navegador.find_elements(By.CLASS_NAME, "block-select.block-car")
    if blocos_veiculos:
        dados = []

        for bloco in blocos_veiculos:
            try:
                # Encontrar o nome do veículo
                elemento_nome = bloco.find_element(
                    By.XPATH, ".//div[contains(@class, 'text-transform--initial')]//b"
                )
                nome_veiculo = elemento_nome.text.strip()

                # Encontrar os preços
                elementos_precos = bloco.find_elements(
                    By.XPATH, 
                    ".//span[contains(@class, 'clube-price__value-discount--size_walk')]"
                )
                preco_a_vista = (elementos_precos[0].get_attribute("title").strip() 
                                if len(elementos_precos) > 0 else "-")
                preco_sem_desconto = (elementos_precos[1].get_attribute("title").strip() 
                                     if len(elementos_precos) > 1 else "-")

                # Obter o HTML do bloco de veículos
                html_bloco = bloco.get_attribute('outerHTML')
                soup = BeautifulSoup(html_bloco, 'html.parser')

                # Encontrar todos os elementos <div> com a classe 'reserva__item' dentro do bloco
                itens_reserva = soup.select('div.reserva__item')

                # Inicializar variáveis
                ar_condicionado = "-"
                transmissao = "-"
                bagagem = "-"
                ocupantes = "-"
                airbag = "-"
                freios_abs = "-"

                # Percorrer cada elemento e extrair o título e o texto do <span>
                for item in itens_reserva:
                    elemento_span = item.select_one('span.reserva__label')
                    titulo = elemento_span.get('title', '-')
                    texto = elemento_span.text.strip()
                    if titulo == "Ar condicionado":
                        ar_condicionado = texto
                    elif titulo == "Transmissão":
                        transmissao = texto
                    elif titulo == "Bagagem":
                        bagagem = texto
                    elif titulo == "Ocupantes":
                        ocupantes = texto
                    elif titulo == "Airbag":
                        airbag = texto
                    elif titulo == "Freios ABS":
                        freios_abs = texto

                # Adicionar dados à lista
                dados.append([
                    nome_veiculo,
                    preco_a_vista,
                    preco_sem_desconto,
                    ar_condicionado,
                    transmissao,
                    bagagem,
                    ocupantes,
                    airbag,
                    freios_abs
                ])

            except Exception as e:
                logging.error(f"Erro ao processar informações do veículo: {e}")
                pass

        # Criar o DataFrame com os dados extraídos
        colunas = [
            'Veiculo', 'Preco_a_vista', 'Preco_sem_desconto', 
            'Ar_condicionado', 'Transmissao', 'Bagagem', 
            'Ocupantes', 'Airbag', 'Freios_ABS'
        ]
        veiculos_movida = pd.DataFrame(dados, columns=colunas)
        veiculos_movida.to_csv("veiculos_movida.csv", index=False)
        print("Dados dos veículos salvos com sucesso no arquivo 'veiculos_movida.csv'!")

    else:
        print("Nenhum veículo disponível encontrado para os parâmetros de busca.")

# Executar o script principal
executar_script()