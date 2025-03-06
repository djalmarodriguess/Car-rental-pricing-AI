# 🚗 Análise de Precificação de Aluguel de Veículos com uso de IA
![5](https://github.com/user-attachments/assets/b60cff9d-cb85-4412-bf12-0688f5665f4b)

## **Visão Geral**
Este projeto tem como objetivo realizar uma análise de precificação para comparar valores de aluguel de veículos entre duas empresas do setor: **Movida** e uma segunda locadora (a ser definida na próxima etapa).  
A abordagem inicial foca em utilizar **web scraping** para capturar informações estruturadas sobre os veículos de cada empresa, armazenar os dados em um arquivo CSV e integrar um agente de **inteligência artificial** localmente para responder perguntas e tirar conclusões com base nos dados extraídos.

---

## **Primeira Etapa - Web Scraping da Movida**
Na primeira etapa, foi realizado:
1. **Extração de Dados:** Captura de informações da Movida, como nome dos veículos, preços (à vista e sem desconto) e características (ar-condicionado, transmissão, bagagem, etc.).
![2](https://github.com/user-attachments/assets/6d1dd12d-68db-48bb-8c6d-55ff44e30b60)
![1](https://github.com/user-attachments/assets/edfbe0bc-e2ee-4723-959b-86e453ee63db)

2. **Armazenamento Estruturado:** Os dados foram organizados em um arquivo CSV para facilitar análises futuras.
![3](https://github.com/user-attachments/assets/c68a0226-c9c0-4916-a8d7-f73241ecf5d2)

3. **Criação de um Agente de IA:** Um modelo de IA (LLama 3.1) localmente foi integrado ao projeto para responder perguntas relacionadas ou não do dataset, como:
   - Qual é preço médio dos veículos?
   - Quais veículos oferecem melhor custo-benefício para famílias?
   - Faça uma pesquisa em sites de classificação de veiculos ou em concessionárias e me retorne o consumo médio de combustivel de cada veiculo, destaque a fonte de onde você pesquisou os valores.
![4](https://github.com/user-attachments/assets/145942b3-862c-4d31-b36e-24dcb6e93cc0)

---

## **Próximos Passos**
1. **Segunda Etapa - Coleta de Dados de Outra Empresa**
   - Realizar web scraping de outra locadora de veículos (por exemplo, Localiza).
   - Estruturar os dados em um novo arquivo CSV com o mesmo padrão da Movida.

2. **Comparação Entre Locadoras**
   - Desenvolver análises comparativas entre as duas empresas, como:
     - Diferenças de preços por categoria de veículo.
     - Benefícios oferecidos (ex.: ar-condicionado, transmissão automática).
     - Melhor custo-benefício em períodos específicos.

3. **Interações com o Agente de IA**
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
