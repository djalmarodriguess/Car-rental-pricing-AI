import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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


# @suprimir_erros
def executar_script():
    
    # Variáveis para os elementos interativos
    CIDADE = "São Paulo"
    OPCAO_LOCAL = 'Agencia Aerop Guarulhos'
    
    # Parâmetros das datas 
    DATA_RETIRADA_MES_ANO = "MAR. DE 2025" #formato: MMM. DE YYYY(ex: DEZ. DE 2025)
    DATA_RETIRADA_DIA = "31"
    
    DATA_DEVOLUCAO_MES_ANO = "ABR. DE 2025"
    DATA_DEVOLUCAO_DIA = "4"
    
    
    # Acessar o site da Localiza
    navegador.get("https://www.localiza.com/brasil/pt-br")
    # Maximizar a janela do navegador
    navegador.maximize_window()
    
    print("Site da Localiza carregado com sucesso!")
    time.sleep(3)
    
    
    # Procurar pelo botão de rejeitar cookies, considerando os dois idiomas possíveis
    try:
        # Tentativa 1: Procurar pelo botão com texto "Reject" ou "Rejeitar"
        botao_rejeitar = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.XPATH, 
            "//a[contains(@class, 'cc-dismiss') and (contains(text(), 'Reject') or contains(text(), 'Rejeitar'))]"))
        )
        print("Banner de cookies encontrado. Clicando em 'Reject'/'Rejeitar'...")
        botao_rejeitar.click()
        print("Cookies rejeitados com sucesso!")
        
    except TimeoutException:
        # Tentativa 2: Procurar pelo botão pela classe e posição
        print("Tentando localizar o botão por classe...")
        botao_rejeitar = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.cc-btn.cc-dismiss"))
        )
        print("Botão de rejeitar cookies encontrado. Clicando...")
        botao_rejeitar.click()
        print("Cookies rejeitados com sucesso!")
    
    time.sleep(1)
    
    # Esperar pelo campo de entrada de local estar presente
    campo_local = WebDriverWait(navegador, 15).until(
        EC.presence_of_element_located((By.ID, "mat-input-2"))
    )
    print("Campo de localização encontrado e pronto para inserção!")
    
    # Digitar a cidade no campo de busca
    campo_local.send_keys(f'{CIDADE}')
    # Aguardar o carregamento das opções
    time.sleep(2)
    
    # Selecionar a agência do Aeroporto de Guarulhos
    opcoes = navegador.find_elements(By.CLASS_NAME, "places-list__item__name")
    for opcao in opcoes:
        if f'{OPCAO_LOCAL}' in opcao.text:
            opcao.click()
            break
    print("Agência selecionada com sucesso!")
    
    # Esperar pelo calendário de retirada estar presente
    WebDriverWait(navegador, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mat-datepicker-0"]'))
    )
    print("Calendário de retirada encontrado!")
    
    # Selecionar mês e ano corretos para retirada
    while True:
        mes_ano = navegador.find_element(By.CLASS_NAME, "mat-calendar-period-button").text
        if f'{DATA_RETIRADA_MES_ANO}' in mes_ano:
            break
        botao_proximo = navegador.find_element(By.CLASS_NAME, "mat-calendar-next-button")
        botao_proximo.click()
        time.sleep(1)

    # Selecionar o dia para retirada
    elementos_dia = navegador.find_elements(By.CLASS_NAME, "mat-calendar-body-cell")
    for dia in elementos_dia:
        if dia.text == f'{DATA_RETIRADA_DIA}':
            dia.click()
            break
    print("Data de retirada selecionada!")
  
    # Esperar pelo seletor de hora estar presente
    WebDriverWait(navegador, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mat-select-0-panel"]'))
    )
    print("Seletor de hora encontrado!", flush=True)
     
    # Selecionar hora de retirada
    elementos_hora = navegador.find_elements(By.CLASS_NAME, "mdc-list-item__primary-text")
    for hora in elementos_hora:
        if hora.text == "01:00":
            hora.click()
            break
    
    print("Hora de retirada selecionada!")
    
    # Esperar pelo calendário de devolução estar presente
    WebDriverWait(navegador, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mat-datepicker-1"]'))
    )
    print("Calendário de devolução encontrado!")
    
    # Selecionar mês e ano corretos para devolução
    while True:
        mes_ano = navegador.find_element(By.CLASS_NAME, "mat-calendar-period-button").text
        if f'{DATA_DEVOLUCAO_MES_ANO}' in mes_ano:
            break
        botao_proximo = navegador.find_element(By.CLASS_NAME, "mat-calendar-next-button")
        botao_proximo.click()
        time.sleep(1)

    # Selecionar o dia para devolução
    elementos_dia = navegador.find_elements(By.CLASS_NAME, "mat-calendar-body-cell")
    for dia in elementos_dia:
        if dia.text == f'{DATA_DEVOLUCAO_DIA}':
            dia.click()
            break
    print("Data de devolução selecionada!")
   
    # Garantir que o botão de busca esteja visível e clicável
    botao_busca = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable((By.XPATH, 
        '/html/body/loc-root/app-header/header/div/app-topbar-first-step/div/div/div/div[2]/div[5]'))
    )
    # Garantir visibilidade do botão de busca
    navegador.execute_script("arguments[0].scrollIntoView(true);", botao_busca)
    # Clicar no botão de busca
    botao_busca.click()
    print("Botão de busca de veículos clicado com sucesso!")
    
    try:
        # Esperar até 5 segundos para o popup de diária extra aparecer
        espera_popup = WebDriverWait(navegador, 5)
        
        # Verificar se o popup apareceu usando diferentes abordagens
        # Abordagem 1: Procurar pelo texto da mensagem
        elemento_popup = espera_popup.until(
            EC.visibility_of_element_located((By.XPATH, 
            "//p[contains(text(), 'Deseja acrescentar mais 1 diária a sua reserva')]"))
        )
        print("Popup de diária extra detectado!")
        
        # Procurar pelo botão "Não"
        botao_nao = navegador.find_element(By.XPATH, "//button[contains(text(), 'Não')]")
        print("Botão 'Não' encontrado. Clicando...")
        botao_nao.click()
        print("Diária extra rejeitada com sucesso!")

    except TimeoutException:
        # Abordagem 2: Tentar encontrar o botão diretamente
        try:
            # Procurar usando a classe do botão secundário dentro do modal
            botao_nao = navegador.find_element(
                By.CSS_SELECTOR, ".modal-two-day-incentive_buttons .ds-new-button--secondary button"
            )
            print("Botão 'Não' encontrado. Clicando...")
            botao_nao.click()
            print("Diária extra rejeitada com sucesso!")
        except NoSuchElementException:
            print("Popup de diária extra não apareceu ou não foi detectado.")
    time.sleep(3)
    
    # Alternar para a nova aba
    abas = navegador.window_handles
    navegador.switch_to.window(abas[0])
    print("Alternado para a aba de veículos!")
    time.sleep(2)

    # Função para rolar até o final da página
    def rolar_ate_final(navegador, tempo_pausa=2):
        ultima_altura = navegador.execute_script("return document.body.scrollHeight")
        while True:
            navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(tempo_pausa)
            nova_altura = navegador.execute_script("return document.body.scrollHeight")
            if nova_altura == ultima_altura:
                break
            ultima_altura = nova_altura

    # Rola a página para garantir que todos os veículos sejam carregados
    rolar_ate_final(navegador)

    # Encontre todos os contêineres de veículos
    artigos = navegador.find_elements(By.XPATH, "//article")

    dados_veiculos = {}

    for artigo in artigos:
        try:
            # Extrai o nome do veículo
            elemento_nome = artigo.find_element(By.CLASS_NAME, "car-header-title")
            nome = elemento_nome.text.strip()
            
            # Verifica se o veículo está esgotado
            elementos_esgotado = artigo.find_elements(
                By.XPATH, ".//button[contains(text(), 'Esgotado')]"
            )
            if elementos_esgotado and len(elementos_esgotado) > 0:
                continue  # Pula para o próximo veículo

            # Extrai o preço do veículo
            elemento_preco = artigo.find_element(
                By.CLASS_NAME, "box-group-car-content-box-price-value__rate"
            )
            preco = elemento_preco.text.strip()
            
            # Clica no botão "Mostrar detalhes", se existir
            try:
                botao_detalhes = artigo.find_element(
                    By.CSS_SELECTOR, ".box-group-car-content__show-details button"
                )
                navegador.execute_script("arguments[0].click();", botao_detalhes)
                time.sleep(1)  # Aguarda que os detalhes sejam carregados
            except Exception as e:
                logging.error(f"Botão 'Mostrar detalhes' não encontrado para '{nome}': {e}")
            
            # Aguarda que o container de detalhes apareça
            container_detalhes = WebDriverWait(navegador, 10).until(
                lambda d: artigo.find_element(By.CSS_SELECTOR, "div.box-group-car-details")
            )
            html_detalhes = container_detalhes.get_attribute("outerHTML")
            sopa = BeautifulSoup(html_detalhes, "html.parser")
            elementos_li = sopa.find_all("li")
            textos_detalhes = [
                li.find("p").get_text(strip=True) for li in elementos_li if li.find("p")
            ]
            
            # Armazena os dados, mantendo a ordem conforme aparecem na página
            dados_veiculos[nome] = {"preco": preco, "detalhes": textos_detalhes}
        
        except Exception as e:
            logging.error(f"Erro ao processar veículo '{nome}': {e}")

    # Salva os dados em um CSV, mantendo a ordem dos veículos conforme encontrados
    df = pd.DataFrame([
        {"Veiculo": nome, "Preco": info["preco"], "Detalhes": ", ".join(info["detalhes"])}
        for nome, info in dados_veiculos.items()
    ])
    df.to_csv("veiculos_localiza.csv", index=False)
    print("Dados dos veículos salvos com sucesso no arquivo 'veiculos_localiza.csv'.")


executar_script()