# ICARUS – Sala de Situação

Interface web **multimodular** no estilo **sala de situação**, desenvolvida em **Python** utilizando os frameworks **Dash** e **Plotly**, voltada para o **monitoramento e gerenciamento de recursos urbanos durante crises hidrológicas**.

Este projeto está sendo desenvolvido como **Trabalho de Conclusão de Curso (TCC)** do **Bacharelado em Sistemas de Informação** na **Universidade Tecnológica Federal do Paraná (UTFPR)**.

---

## Objetivo

O projeto tem como objetivo oferecer uma ferramenta de apoio à tomada de decisão por órgãos públicos durante **eventos críticos como enchentes e alagamentos**, permitindo:

- Visualização de **eventos hidrológicos em tempo real**;
- Avaliação rápida da **situação urbana** por meio de uma interface interativa;
- **Gerenciamento de recursos urbanos**, como:
  - Linhas de ônibus afetadas;
  - Unidades de saúde próximas às áreas de risco;
  - Sugestões automáticas de medidas corretivas (ex: redirecionamento de rotas, readequação de pacientes etc.);

---

## Tecnologias Utilizadas

- Python 3.11+
- Dash
- Plotly
- Pandas
- OpenStreetMap
- GeoPandas 

---
## Configurações de hardware utilizadas para testes
- Processador: AMD Ryzen 5 5600
- Memoria Ram: 16gb DDR4, 3200 MHz
- Placa de vídeo: NVIDIA GeForce RTX 4060, 8 GB GDDR6
- Armazenamento: SSD de 1 TB, SATA

## Softwares utilizados
- Sistema operacional: Windows 11 Pro, 64 bits
- Python versão 3.11.9
---
## Como executar o projeto
- Clone o repositório https://github.com/GabrielLeao01/ICARUS-Sala-de-Situacao.git
- Caso não tenha todas bibliotecas necessárias, baixe atráves do Pip install do Python
- Crie uma pasta shapefiles e insira os shapefiles desejados
- Execute o arquivo app.py
- Acesse o ip hospedado pela aplicação
- é possivel mudar o ip e a porta através da linha 214 "app.run(debug=True, host="192.168.15.49", port=8050)" na classe app.py
- Criar uma pasta "shapefiles" dentro do repositório.
- Dentro da pasta "shapefiles", criar a pasta situacao.
- Dentro da pasta situação, inserir o shapefile desejado. Após inserir, o shapefile aparecerá na tela inicial de situação atual.
- Para inserir os recursos que deverão aparecer na tela de "gerenciamento de recursos", criar uma pasta com o nome "gerenciamento_recursos" dentro da pasta "shapefiles"
- Dentro da pasta "gerenciamento_recursos", criar uma pasta para cada recurso desejado.
- Dentro da pasta criada para o recurso, criar a pasta "atual", para inserir os shapefiles da situação atual do recurso e a pasta "reestruturada", para inserir dados da solução proposta, caso tenha.
- Para inserir gráficos no sistema, criar a pasta gráfico no repositório
- Após criar a pasta "gráfico", basta inserir o gráfico desejado no formato json

---
## 📂 Estrutura do Repositório

```text
ICARUS-Sala-de-Situacao/
│
├── assets/                  # Front-end (estilização CSS)
├── icarus/                  # Classes da aplicação chamadas pela classe principal
│   ├── alerta.py            # Classe com métodos de exibição dos alertas
│   ├── graficos.py          # Classe com métodos para exibição dos gráficos
│   ├── recursos.py          # Classe com os principais métodos do módulo de gerenciamento de recursos
│   ├── situacao.py          # Classe com os principais métodos do módulo de situação atual
│
├── app.py                   # Classe principal da aplicação
├── .gitignore               # Arquivos/pastas ignoradas pelo Git
├── LICENSE                  # Licença GPLv3
└── README.md                # Documentação do projeto
```
---
## Licença
Este projeto está licenciado sob a [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) – veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor
Gabriel Leão Bernarde
