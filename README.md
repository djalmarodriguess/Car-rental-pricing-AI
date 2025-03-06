# 🚗 Análise de Precificação de Aluguel de Veículos com uso de IA
![5](https://github.com/user-attachments/assets/b60cff9d-cb85-4412-bf12-0688f5665f4b)

## **Visão Geral**
Este projeto tem como objetivo realizar uma análise de precificação para comparar valores de aluguel de veículos entre duas empresas do setor: **Movida** e **Localiza**.  
A abordagem inicial foca em utilizar **web scraping** para capturar informações estruturadas sobre os veículos de cada empresa, armazenar os dados em um arquivo CSV e integrar um agente de **inteligência artificial** localmente para responder perguntas e tirar conclusões com base nos dados extraídos.

---

## **Primeira Etapa - Web Scraping da Movida**
Na primeira etapa, foi realizado:
1. **Extração de Dados:** Captura de informações da Movida, como nome dos veículos, preços (à vista e sem desconto) e características (ar-condicionado, transmissão, bagagem, etc.).
### Alterações para Busca dos Dados
![image](https://github.com/user-attachments/assets/d8cfb307-8c92-4e49-b34d-579a157bf993)

A principal mudança no código para controlar a busca dos dados é a **configuração dos parâmetros de localização e datas**. Essa seção define:
- **Localização**:  
  - `CIDADE`: Nome da cidade (ex.: `São Paulo`).  
  - `OPCAO_LOCAL`: Opção detalhada da agência (ex.: `SAO PAULO - GUARULHOS AEROPORTO`). Sugiro entrar no site e copiar o local de retirada conforme está descrito para não haver error na hora da pesquisa.
- **Datas**:  
  - **Data de Retirada**:  
    - `DATA_RETIRADA_ANO`: Ano da retirada (ex.: `2025`).  
    - `DATA_RETIRADA_MES`: Mês da retirada em formato 0-based (ex.:, "0" para Janeiro, "1" para Fevereiro, "2" para Março...).  
    - `DATA_RETIRADA_DIA`: Dia da retirada (ex.: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ...31).
  - **Data de Devolução**:  
    - `DATA_DEVOLUCAO_ANO`: Ano da devolução (ex.: `2025`).  
    - `DATA_DEVOLUCAO_MES`: Mês da devolução em formato 0-based (ex.:, "0" para Janeiro, "1" para Fevereiro, "2" para Março...).  
    - `DATA_DEVOLUCAO_DIA`: Dia da devolução (ex.: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ...31).

Para alterar os dados que serão buscados, basta modificar esses parâmetros conforme sua necessidade. Essa é a parte crucial para ajustar a pesquisa no site.

![2](https://github.com/user-attachments/assets/6d1dd12d-68db-48bb-8c6d-55ff44e30b60)
![1](https://github.com/user-attachments/assets/edfbe0bc-e2ee-4723-959b-86e453ee63db)

3. **Armazenamento Estruturado:** Os dados foram organizados em um arquivo CSV para facilitar análises futuras.
![3](https://github.com/user-attachments/assets/c68a0226-c9c0-4916-a8d7-f73241ecf5d2)

---

## **Segunda Etapa - Web Scraping da Localiza**
Na Segunda etapa, foi realizado:
1. **Extração de Dados:** Captura de informações da Localiza, como nome dos veículos, preços do aluguel e características (ar-condicionado, transmissão, bagagem, etc.).

### Principais Configurações para a Busca
![image](https://github.com/user-attachments/assets/63430dfc-4ac5-4795-b1d2-25f50c25c135)

A principal mudança no código para controlar a busca dos dados é a **configuração dos parâmetros de localização e datas**. Essa seção define:
- **Localização:**
  - `CIDADE`: Define a cidade para a busca (ex.: `"São Paulo"`).
  - `OPCAO_LOCAL`: Especifica a agência ou local detalhado (ex.: `'Agencia Aerop Guarulhos'`).Sugiro entrar no site e copiar o local de retirada conforme está descrito para não haver error na hora da pesquisa.

- **Datas:**
  - **Data de Retirada:**
    - `DATA_RETIRADA_MES_ANO`: Define o mês e ano no formato `MMM. DE YYYY` (ex.: "MAR. DE 2025").
    - `DATA_RETIRADA_DIA`: Define o dia para a retirada (ex.: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ...31).
  - **Data de Devolução:**
    - `DATA_DEVOLUCAO_MES_ANO`: Define o mês e ano no mesmo formato (ex.: `"ABR. DE 2025"`).
    - `DATA_DEVOLUCAO_DIA`: Define o dia para a devolução (ex.: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ...31).

Essas variáveis são responsáveis por orientar o script na seleção correta dos parâmetros de busca no site da Localiza.




![5](https://github.com/user-attachments/assets/ae81ec27-886d-45fe-bd3c-7eaf534b5fb2)
![6](https://github.com/user-attachments/assets/9c106f0c-e1c5-45af-aed9-e49ee967df11)

2. **Armazenamento Estruturado:** Os dados foram organizados em um arquivo CSV para facilitar análises futuras.
![7](https://github.com/user-attachments/assets/14253b0e-f0ac-40c9-b443-e2f381bc584f)



---

## **Terceira Etapa - Uso de IA**
1. **Criação de um Agente de IA:** Um modelo de IA (LLama 3.1) localmente foi integrado ao projeto para responder perguntas relacionadas ou não do dataset, como:
   - Qual é preço médio dos veículos?
   - Quais veículos oferecem melhor custo-benefício para famílias?
   - Faça uma pesquisa em sites de classificação de veiculos ou em concessionárias e me retorne o consumo médio de combustivel de cada veiculo, destaque a fonte de onde você pesquisou os valores.
![4](https://github.com/user-attachments/assets/145942b3-862c-4d31-b36e-24dcb6e93cc0)


## **Próximos Passos**
1. **Comparação Entre Locadoras**
   - Desenvolver análises comparativas entre as duas empresas, como:
     - Diferenças de preços por categoria de veículo.
     - Benefícios oferecidos (ex.: ar-condicionado, transmissão automática).
     - Melhor custo-benefício em períodos específicos.

2. **Interações com o Agente de IA**
   - Configurar o agente de IA localmente para responder perguntas sobre as **diferenças entre as locadoras** e **recomendações personalizadas** baseadas nos dados combinados.
   - Exemplos de perguntas para o agente:
     - "Qual empresa tem o melhor preço para SUVs?"
     - "Quais veículos oferecem o melhor custo-benefício para 5 ocupantes?"
     - "Em qual período os preços são mais baixos?"

---

## **Entregas em Projetos Reais**
Este projeto é um exemplo de como entregas parciais e objetivas são práticas recomendadas em projetos reais.  
- **Iteratividade:** O progresso é contínuo, com validação de cada etapa antes de avançar.  
- **Agilidade:** Entregar uma versão funcional rapidamente é muito mais vantajoso do que levar meses para entregar algo incompleto.  
- **Melhoria Contínua:** O código atual está em evolução, e melhorias serão implementadas em etapas futuras, alinhando-se ao objetivo final.  

---

## **Observações Finais**
- **Flexibilidade:** Esta abordagem permite ajustes e adaptações com base no feedback ao longo do projeto.  
- **Escalabilidade:** O agente de IA e as análises podem ser facilmente expandidos para outras locadoras ou contextos.  
- **Foco no Resultado:** A cada entrega parcial, insights relevantes já podem ser utilizados para tomada de decisão.  

---

## **Contribuições**
Contribuições para o código ou sugestões para o projeto são muito bem-vindas! Este repositório é uma oportunidade de aprendizado e colaboração para otimizar análises de dados no setor de aluguel de veículos.

**🛠️ Projeto em andamento. Vamos construir juntos!**  
