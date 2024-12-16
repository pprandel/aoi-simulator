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
    A tool for Age Of Information simulation
    <br />
    <br />
    <a href="https://youtu.be/xASlrlQO25o">Demonstration video</a>
    ·
    <a href="https://github.com/pprandel/aoi-simulator/issues/new">Reporte a Bug</a>
    ·
    <a href="https://github.com/pprandel/aoi-simulator/issues">Request a feature</a>
  </p>
</div>


## Summary
- [Summary](#sumário)
- [About the project](#sobre-o-projeto)
  - [Builted with](#construído-com)
- [Instalation](#instalação)
  - [Requirements](#pré-requisitos)
  - [Configuring the tool](#instalando-a-ferramenta)
- [Using the tool](#utilização)
  - [Ploting results](#plotando-os-resultados)
- [Contributing](#contribuindo)
- [References](#referências-acadêmicas)
  - [Basic concepts](#conceitos-básicos)
  - [AoI simulator computational model](#modelo-computacional-do-aoi-simulator)
  - [Example references](#referências-para-os-exemplos)
    - [Examples 1 e 2:](#exemplos-1-e-2)
    - [Example 3:](#exemplo-3)
- [License](#licença)
- [Contact](#contatos)
  
<!-- ABOUT THE PROJECT -->
## About the project 

The Age of Information (AoI) simulator arose from the need to have a tool capable of simulating a cyber-physical system using the concepts and metrics related to this area. 

The computational model behind this tool is described in the article [Computational Modeling of Age of Information for Cyber-physical Systems](https://ieeexplore.ieee.org/document/9647854).

For more content on the concept and application of AoI, it is recommended that you explore the section [academic references](#academic-references).

This project is part of a master's degree research developed by the author in the Postgraduate Program in Applied Computing at the University of Brasília (UnB).

<!-- BUILTED WITH -->
### Builted with 

This project uses:

* [Python](https://www.python.org/)
* [Queueing Tool](https://github.com/djordon/queueing-tool)
* [Matplot Lib](https://matplotlib.org/)

>Link to this project on [PyPi](https://pypi.org/project/aoi-simulator/)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Instalation

This tutorial will guide you through the process of installing and using the tool.

### Requirements

Aoi-simulator is a Python package, so its use does not depend on the operating system used. The prerequisites for installation are:
* Python 3.7
* Basic knowledge of Python
  
>:warning: For Windows OS strictly install Python 3.7! For Linux or Mac OS you can install a higher version.

To install Python, use the links below.
* [Linux](https://python.org.br/instalacao-linux/)
* [Windows](https://www.python.org/downloads/release/python-370/)
* [MacOs](https://python.org.br/instalacao-mac/)

### Configuring the tool

After installing Python:

1. Open command terminal

2. Check your Python version:
    ```sh
    python --version
    ```
    > :warning: If this command does not execute or the version does not match the one installed, check your `PATH` configuration!

3. Update PIP (package installer):
    ```sh
    pip install --upgrade pip
    ```

4. Install aoi-simulator through `PIP`:
    ```sh
    pip install aoi-simulator
    ```


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Using AoI simulator

Once the installation is complete, identify a folder in the repository called `sim_examples`. This folder contains several examples of using this tool. All examples have commented code, explaining the purpose of each step of the simulation script.

To run examples, do the following steps:

1. Choose your preferred code editor and create a python `.py` file.
2. Copy the entire content of one of the examples into your newly created file.
3. Save the file in a folder of your choice.
4. Run the simulation using the command:

   ```sh
   python PATH/TO/FILE/exemplo_x.py
   ```
   replacing `PATH/TO/FILE/` by the folder directory and `example_x.py` by the name of the file you created.

    > :bulb: If you are already in the file directory, just run it with the command `python example_x.py`
    
5. During the simulation, you will see some results displayed on the screen. Also note that two folders will be created in the same directory as the executed file:
   * `sim_data`: contains the data generated by the simulation
   * `results`: contains the simulation results

Description of the contents of these folders can be found in the example files.

Each of the examples provided in the `sim_examples` folder addresses a different use case of the tool. In summary, the cases are as follows:

* `example_1.py`: simulates a M/M/1 simple queue with service regime FCFS (First Come - First Served) and server load &rho;=0.5;
  
* `example_2.py`: performs several simulations of a M/M/1 simple queue with service regime FCFS (First Come - First Served). For each simulation, a different load &rho is used;

* `example_3.py`: performs several simulations of a M/M/1 simple queue with service regime FCFS (First Come - First Served) with 2 sources.


### Ploting results

To help you in the work of visualizing results, this repository also provides a folder called `plot_examples`, within which you will find some scripts to plot the results obtained in the simulations. 

The execution of these examples follows the same steps shown previously for executing the simulations: simply copy the contents of the file and run. Examples of this folder are as follows:

* `plota_example_2.py`: generates a graph showing the simulation results of `example_2.py`, showing the average AoI _vs_ the loads &rho. These simulated results are compared with the results predicted by the analytical model (see references).
  
* `plota_example_3.py`: generates a graph showing the simulation results of `example_3.py`, showing the evolution of the average AoI for the 2 sources at different loads &rho. These simulated results are compared with the results predicted by the analytical model (see references).


<p align="right">(<a href="#top">back to top</a>)</p>

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
