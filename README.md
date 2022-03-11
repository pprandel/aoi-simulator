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
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/pprandel/AoI">
    <img src="images/logo.svg" alt="Logo" width="400">
  </a>

  <p align="center">
    Uma ferramenta de simulação para a Age Of Information
    <br />
    <br />
    <a href="https://github.com/pprandel/AoI">Vídeo demonstrativo</a>
    ·
    <a href="https://github.com/pprandel/AoI">Reporte um Bug</a>
    ·
    <a href="https://github.com/pprandel/AoI/issues">Solicite uma funcionalidade</a>
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
- [Licença](#licença)
- [Contatos](#contatos)
- [Agradecimentos](#agradecimentos)
  
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


<p align="right">(<a href="#top">voltar ao início</a>)</p>



<!-- GETTING STARTED -->
## Instalação

Este tutorial iŕa guiá-lo através dos processos de instalação e utilização da ferramenta.

### Pré-requisitos

O aoi-simulator é um pacote Python, logo sua utilização independe do sistema operacional utilizado. Os pré requisitos para a instalação são:
* Python 3.8 ou superior
* Conhecimento básico na linguagem Python

Para instalar o Python, utilize os tutoriais abaixo. 
* [Linux](https://python.org.br/instalacao-linux/)
* [Windows](https://python.org.br/instalacao-windows/)
* [Mac OS](https://python.org.br/instalacao-mac/)

Usuários Windows devem instalar adicionalmente o Visual Studio Build Tools.
* [Download VS Build Tools](https://visualstudio.microsoft.com/pt-br/thank-you-downloading-visual-studio/?sku=BuildTools)
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

### Plotando os resultados
Para facilitar a visualização dos resultados, este repositório fornece também uma pasta chamada `plota_exemplos`, dentro da qual você encontrará alguns scripts para plotar os resultados obtidos nas simulações. 

A execução desses exemplos segue os mesmos passos mostrados anteriormente para a execução das simulações, bastando copiar o conteúdo do arquivo e executá-lo. Os exemplos dessa pasta são os seguintes:

* `plota_exemplo_2.py`: gera um gráfico mostrando os resultados da simulação do `exemplo_2.py`, mostrando a AoI média _vs_ as cargas $\rho$. Esses resultados simulados são comparados com os resultados previstos pelo modelo analítico (ver referências).


<p align="right">(<a href="#top">voltar ao início</a>)</p>

<!-- CONTRIBUTING -->
## Contribuindo

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">voltar ao início</a>)</p>

<!-- REFERENCES -->
## Referências Acadêmicas

Aqui você encontrará uma lista de referências acadêmicas sobre a área Age of Information. Boa leitura!

<p align="right">(<a href="#top">voltar ao início</a>)</p>


<!-- LICENSE -->
## Licença

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">voltar ao início</a>)</p>



<!-- CONTACT -->
## Contatos

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">voltar ao início</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Agradecimentos

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#top">voltar ao início</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
