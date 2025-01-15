import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pyautogui

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
    # Acessar o site da Movida
    navegador.get("https://www.movida.com.br/")
    # Maximizar a janela do navegador
    navegador.maximize_window()
    print("Site carregado com sucesso!")

    # Esperar pelo campo de entrada estar presente
    campo_busca = WebDriverWait(navegador, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Onde você quer alugar?')]"))
    )
    print("Clique no campo Local!")
    # Digitar "São Paulo" no campo de busca
    campo_busca.send_keys("São Paulo")
    # Aguardar o carregamento das opções
    time.sleep(1)

    # Localizar e clicar na opção "SAO PAULO - GUARULHOS AEROPORTO"
    opcao = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'SAO PAULO - GUARULHOS AEROPORTO')]"))
    )
    opcao.click()
    print("Local selecionado com sucesso!", flush=True)

    # Esperar e clicar no botão do calendário
    calendario_btn = WebDriverWait(navegador, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="data_retirada"]'))
    ).click()
    print("Clique no calendario com sucesso!")

    # Executar script JavaScript para selecionar mês e ano
    script1 = """
        var selectMonth = document.querySelector("select.pika-select-month");
        var selectYear = document.querySelector("select.pika-select-year");
        selectMonth.value = '1';  // Fevereiro
        selectYear.value = '2025'; // Ano 2025
        selectMonth.dispatchEvent(new Event('change'));
        selectYear.dispatchEvent(new Event('change'));
    """
    navegador.execute_script(script1)
    print("Mês e ano selecionados com sucesso via JavaScript!")

    # Esperar e clicar no botão do dia específico
    botao_dia = WebDriverWait(navegador, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='pika-button pika-day' and @data-pika-day='8' and @data-pika-month='1' and @data-pika-year='2025']"))
    ).click()

    # Esperar e clicar no botão do calendário de devolução
    calendario_devolucao = WebDriverWait(navegador, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="data_devolucao"]'))
    ).click()
    # Aguardar para garantir que o calendário de devolução esteja aberto
    time.sleep(2)
    print("Calendário de devolução aberto!")

    # Executar script JavaScript para selecionar mês e ano de devolução
    script2 = """
        var selectMonth = document.querySelector("select.pika-select-month");
        var selectYear = document.querySelector("select.pika-select-year");
        selectMonth.value = '1';  // Fevereiro
        selectYear.value = '2025';  // Ano 2025
        selectMonth.dispatchEvent(new Event('change'));
        selectYear.dispatchEvent(new Event('change'));
    """
    navegador.execute_script(script2)
    print("Mês e ano selecionados com sucesso via JavaScript!")

    # Pausar para garantir que o navegador carregue completamente
    time.sleep(2)

    # Coordenadas (X, Y) do botão "Dia 10"
    coordenadas_x = 1318
    coordenadas_y = 545

    # Mover o mouse para as coordenadas e clicar
    pyautogui.moveTo(coordenadas_x, coordenadas_y, duration=0.5)
    pyautogui.click()
    print("Clique realizado com sucesso!")

    # Garantir que o botão de busca esteja visível e clicável
    botao_busca = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="search-content"]/button'))
    )
    # Garantir visibilidade do botão de busca
    navegador.execute_script("arguments[0].scrollIntoView(true);", botao_busca)
    # Clicar no botão de busca
    botao_busca.click()
    print("Botão de busca clicado com sucesso!")

    # Alternar para a nova aba aberta
    abas = navegador.window_handles
    navegador.switch_to.window(abas[0])
    print("Aba alterada!")

    # Encontrar blocos de veículos
    blocos_veiculos = navegador.find_elements(By.CLASS_NAME, "block-select.block-car")
    if blocos_veiculos:
        print("Blocos de veículos encontrados!")
        dados = []

        for bloco in blocos_veiculos:
            try:
                # Encontrar o nome do veículo
                nome_elemento = bloco.find_element(By.XPATH, ".//div[contains(@class, 'text-transform--initial')]//b")
                nome_veiculo = nome_elemento.text.strip()

                # Encontrar os preços
                precos_elementos = bloco.find_elements(By.XPATH, ".//span[contains(@class, 'clube-price__value-discount--size_walk')]")
                preco_a_vista = precos_elementos[0].get_attribute("title").strip() if len(precos_elementos) > 0 else "-"
                preco_sem_desconto = precos_elementos[1].get_attribute("title").strip() if len(precos_elementos) > 1 else "-"

                # Obter o HTML do bloco de veículos
                bloco_html = bloco.get_attribute('outerHTML')
                soup = BeautifulSoup(bloco_html, 'html.parser')

                # Encontrar todos os elementos <div> com a classe 'reserva__item' dentro do bloco
                reserva_items = soup.select('div.reserva__item')

                # Inicializar variáveis
                ar_condicionado = "-"
                transmissao = "-"
                bagagem = "-"
                ocupantes = "-"
                airbag = "-"
                freios_abs = "-"

                # Percorrer cada elemento e extrair o título e o texto do <span>
                for item in reserva_items:
                    span_element = item.select_one('span.reserva__label')
                    title = span_element.get('title', '-')
                    texto = span_element.text.strip()
                    if title == "Ar condicionado":
                        ar_condicionado = texto
                    elif title == "Transmissão":
                        transmissao = texto
                    elif title == "Bagagem":
                        bagagem = texto
                    elif title == "Ocupantes":
                        ocupantes = texto
                    elif title == "Airbag":
                        airbag = texto
                    elif title == "Freios ABS":
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
                logging.error(f"Erro ao processar bloco: {e}")
                pass

        # Criar o DataFrame com os dados extraídos
        colunas = ['Veiculo', 'Preco_a_vista', 'Preco_sem_desconto', 'Ar_condicionado', 'Transmissao', 'Bagagem', 'Ocupantes', 'Airbag', 'Freios_ABS']
        veiculos_movida = pd.DataFrame(dados, columns=colunas)
        veiculos_movida.to_csv("veiculos_movida.csv", index=False)
        print("Dados coletados e salvos com sucesso!")

    else:
        print("Nenhum bloco de veículos encontrado.")

# Executar o script
executar_script()
