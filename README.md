<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/pprandel/aoi-simulator">
    <img src="images/logo.svg" alt="Logo" width="400">
  </a>

  <p align="center">
    Uma ferramenta de simulação para a Age Of Information
    <br />
    <br />
    <a href="https://github.com/pprandel/aoi-simulator">Vídeo demonstrativo</a>
    ·
    <a href="https://github.com/pprandel/aoi-simulator/issues/new">Reporte um Bug</a>
    ·
    <a href="https://github.com/pprandel/aoi-simulator/issues">Solicite uma funcionalidade</a>
  </p>
</div>


## Sumário
- [Sumário](#sumário)
- [Sobre o projeto](#sobre-o-projeto)
  - [Construído com](#construído-com)
- [Instalação](#instalação)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalando a ferramenta](#instalando-a-ferramenta)
- [Utilização](#utilização)
  - [Plotando os resultados](#plotando-os-resultados)
- [Contribuindo](#contribuindo)
- [Referências Acadêmicas](#referências-acadêmicas)
  - [Conceitos básicos](#conceitos-básicos)
  - [Modelo computacional do aoi-simulator](#modelo-computacional-do-aoi-simulator)
  - [Referências para os exemplos](#referências-para-os-exemplos)
    - [Exemplos 1 e 2:](#exemplos-1-e-2)
    - [Exemplo 3:](#exemplo-3)
- [Licença](#licença)
- [Contatos](#contatos)
  
<!-- ABOUT THE PROJECT -->
## Sobre o projeto 

O simulador para a Age of Information (AoI) surgiu da necessidade de se possuir uma ferramenta capaz de simular um sistema ciberfísico utilizando os conceitos e as métricas relacionadas a essa área. 

O modelo computacional por trás desta ferramenta está descrito no artigo [Computational Modeling of Age of Information for Cyber-physical Systems](https://ieeexplore.ieee.org/document/9647854).

Para mais conteúdo sobre o conceito e a aplicação da AoI, recomenda-se a exploração da seção [referências acadêmicas](#referências-acadêmicas).

Este projeto é parte de uma pesquisa de mestrado sendo desenvolvida pelo autor no programa de Pós-Graduação em Computação Aplicada da Universidade de Brasília (UnB).

<!-- BUILTED WITH -->
### Construído com 

Este projeto utiliza:

* [Python](https://www.python.org/)
* [Queueing Tool](https://github.com/djordon/queueing-tool)
* [Matplot Lib](https://matplotlib.org/)

>Link para o projeto no [PyPi](https://pypi.org/project/aoi-simulator/)


<p align="right">(<a href="#top">voltar ao início</a>)</p>



<!-- GETTING STARTED -->
## Instalação

Este tutorial iŕa guiá-lo através dos processos de instalação e utilização da ferramenta.

### Pré-requisitos

O aoi-simulator é um pacote Python, logo sua utilização independe do sistema operacional utilizado. Os pré requisitos para a instalação são:
* Python 3.7
* Conhecimento básico na linguagem Python
  
>:warning: Para SO Windows instale estritamente o Python 3.7! Para SO Linux você pode instalar uma versão superior.

Para instalar o Python, utilize os links abaixo. 
* [Linux](https://python.org.br/instalacao-linux/)
* [Windows](https://www.python.org/downloads/release/python-370/)

### Instalando a ferramenta

Após a instalação do Python:

1. Abra o terminal de comando

2. Confira a versão instalada do Python:
    ```sh
    python --version
    ```
    > :warning: Caso o comando não execute ou a versão não corresponda à instalada, verifique a configuração do seu `PATH`!

3. Atualize o instalador de pacotes `PIP`:
    ```sh
    python -m pip install --upgrade pip
    ```

4. Instale o aoi-simulator através do `PIP`:
    ```sh
    python -m pip install aoi-simulator
    ```


<p align="right">(<a href="#top">voltar ao início</a>)</p>


<!-- USAGE EXAMPLES -->
## Utilização

Uma vez finalizada a instalação, identifique no repositório uma pasta chamada `sim_exemplos`. Essa pasta contém diversos exemplos de utilização desta ferramenta. Todos os exemplos estão com o código comentado, explicando a finalidade de cada passo do script de simulação.

Para rodar os exemplos, execute os seguintes passos:

1. Escolha o editor de código de sua preferência e crie um arquivo python `.py`.
2. Copie todo o conteúdo de um dos exemplos para dentro do seu arquivo recém criado.
3. Salve o arquivo em uma pasta de sua preferência.
4. Execute a simulação através do comando:
   ```sh
   python CAMINHO/DO/ARQUIVO/exemplo_x.py
   ```
   substituindo `CAMINHO/DO/ARQUIVO` pelo diretório da pasta e `exemplo_x.py` pelo nome do arquivo que você criou.

    > :bulb: Se você já estiver no diretório do arquivo basta executá-lo com o comando `python exemplo_x.py`
5. Durante a simulação, você verá alguns resultados sendo exibidos na tela. Observe também que duas pastas serão criadas no mesmo diretório do arquivo executado:
   * `sim_data`: contém os dados gerados pela simulação
   * `resultados`: contém os resultados da simulação
  
    A descrição do conteúdo dessas pastas pode ser encontrada nos arquivos exemplo.

Cada um dos exemplos fornecios na pasta `sim_exemplos` aborda um caso de uso diferente da ferramenta. Em resumo, os casos são os seguintes:

* `exemplo_1.py`: simula uma fila simples do tipo M/M/1 com regime de serviço (First Come - First Served) FCFS e carga no servidor $\rho=0,5$.
  
*  `exemplo_2.py`: Realiza diversas simulações de uma fila simples do tipo M/M/1 com regime de serviço (First Come - First Served) FCFS. Para cada simulação é utilizada uma carga $\rho$ diferente.

*  `exemplo_3.py`: Realiza diversas simulações de uma fila simples do tipo M/M/1 com regime de serviço (First Come - First Served) FCFS para 2 fontes.

### Plotando os resultados
Para facilitar o trabalho de visualização dos resultados, este repositório fornece também uma pasta chamada `plota_exemplos`, dentro da qual você encontrará alguns scripts para plotar os resultados obtidos nas simulações. 

A execução desses exemplos segue os mesmos passos mostrados anteriormente para a execução das simulações, bastando copiar o conteúdo do arquivo e executá-lo. Os exemplos dessa pasta são os seguintes:

* `plota_exemplo_2.py`: gera um gráfico mostrando os resultados da simulação do `exemplo_2.py`, mostrando a AoI média _vs_ as cargas $\rho$. Esses resultados simulados são comparados com os resultados previstos pelo modelo analítico (ver referências).
  
* `plota_exemplo_3.py`: gera um gráfico mostrando os resultados da simulação do `exemplo_3.py`, mostrando a evolução da AoI média para as 2 fontes em diferentes cargas $\rho$. Esses resultados simulados são comparados com os resultados previstos pelo modelo analítico (ver referências).


<p align="right">(<a href="#top">voltar ao início</a>)</p>

<!-- CONTRIBUTING -->
## Contribuindo

Todas as contribuições a este projeto serão muito bem vindas! 
Se você tem alguma sugestão para a melhoria deste projeto e deseja implementá-la você mesmo, faça um `fork` e crie um `pull request`.  Você pode também abrir uma `issue` ou solicitar um  `enhancement`. Exemplo:

1. Faça um `fork` do projeto
2. Crie sua `Branch` (`git checkout -b feature/MinhaFeature`)
3. Faça o `Commit` das suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça o `Push` da sua `Branch` (`git push origin feature/MinhaFeature`)
5. Abra um `Pull Request`

Não esqueça de nos dar uma :star:, clicando no botão no canto superior direito da tela! Obrigado!

<p align="right">(<a href="#top">voltar ao início</a>)</p>

<!-- REFERENCES -->
## Referências Acadêmicas

Aqui você encontrará uma lista de referências acadêmicas sobre a área Age of Information. Boa leitura!

### Conceitos básicos
* [Age of Information: A New Concept, Metric, and Tool](https://ieeexplore.ieee.org/document/8187436)
* [Age of Information: An Introduction and Survey](https://ieeexplore.ieee.org/document/9380899)
  
### Modelo computacional do aoi-simulator
* [Computational Modeling of Age of Information for Cyber-physical Systems](https://ieeexplore.ieee.org/document/9647854)

### Referências para os exemplos
#### Exemplos 1 e 2:
* [Real-time status: How often should one update?](https://ieeexplore.ieee.org/document/6195689)
  
#### Exemplo 3:
[The Age of Information: Real-Time Status
Updating by Multiple Sources](https://ieeexplore.ieee.org/document/8469047)
<!-- 
#### Exemplo 4:
* [On The Age Of Information In Status Update
Systems With Packet Management](https://ieeexplore.ieee.org/document/7415972?arnumber=7415972) -->



<p align="right">(<a href="#top">voltar ao início</a>)</p>


<!-- LICENSE -->
## Licença

Este projeto utiliza a licença MIT. Veja `LICENSE` para mais informações.

<p align="right">(<a href="#top">voltar ao início</a>)</p>



<!-- CONTACT -->
## Contatos

Paulo Prandel - pauloprandel@hotmail.com ou paulo.prandel@aluno.unb.br

Priscila Barreto - pris@unb.br

<p align="right">(<a href="#top">voltar ao início</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/pprandel/aoi-simulator?style=for-the-badge
[contributors-url]: https://github.com/pprandel/aoi-simulator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/pprandel/aoi-simulator?style=for-the-badge
[forks-url]: https://github.com/pprandel/aoi-simulator/network/members
[issues-shield]: https://img.shields.io/github/issues/pprandel/aoi-simulator?style=for-the-badge
[issues-url]: https://github.com/pprandel/aoi-simulator/issues
[license-shield]: https://img.shields.io/github/license/pprandel/aoi-simulator?style=for-the-badge
[license-url]: https://github.com/pprandel/aoi-simulator/blob/master/LICENSE
