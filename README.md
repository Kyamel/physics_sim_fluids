# Table of Contents
- [Portuguese](#portuguese)
  - [Simulação 2D de Fluidos com Pygame e Pymunk](#simulação-2d-de-fluidos-com-pygame-e-pymunk)
  - [Descrição do Projeto](#descrição-do-projeto)
  - [Funcionalidades Principais](#funcionalidades-principais)
  - [Instalação](#instalação)
- [English](#english)
  - [2D Fluid Simulation with Pygame and Pymunk](#2d-fluid-simulation-with-pygame-and-pymunk)
  - [Project Description](#project-description)
  - [Key Features](#key-features)
  - [Installation](#installation)

# Portuguese
## Simulação 2D de Fluidos com Pygame e Pymunk

Este repositório contém uma simulação 2D de fluidos desenvolvida como parte de um trabalho de física sobre mecânica dos fluidos. Utilizamos Pygame para a renderização gráfica e Pymunk para simulação física de partículas fluidas.

## Descrição do Projeto

O objetivo deste projeto é simular o comportamento de fluidos em um ambiente 2D interativo. A simulação inclui:

- **Renderização Gráfica**: Utilizamos Pygame para criar uma interface gráfica onde os resultados da simulação são visualizados em tempo real.
  
- **Dinâmica de Fluidos**: Implementamos um modelo simplificado de dinâmica de fluidos baseado em partículas usando Pymunk, permitindo interações entre partículas e com o ambiente.

## Funcionalidades Principais

- **Interatividade**: Os usuários podem interagir com a simulação através de controles simples para modificar parâmetros e observar o comportamento resultante.

- **Visualização em Tempo Real**: A simulação é renderizada em tempo real, proporcionando feedback imediato das mudanças nos parâmetros.

- **Configuração Flexível**: O código permite ajustes e expansões para experimentação e comparação com modelos teóricos.

## Instalação

Para executar a simulação localmente, siga estes passos:

1. **Instalar Python**: Tenha o [Python 3.12+](https://www.python.org/downloads/) instalado na sua máquina.

2. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/Kyamel/physics_sim_fluids
   cd physics_sim_fluids

3. **Criar um ambiente virtual**:
   ```bash
   python -m venv venv
   venv/Scripts/activate

4. **Instalar Dependências**:
   ```bash
   pip install pygame
   pip install pygame_gui
   pip install pymunk

5. **Executar**:
   ```bash
   python src/main.py

# English
## 2D Fluid Simulation with Pygame and Pymunk

This repository contains a 2D fluid simulation developed as part of a physics project on fluid mechanics. We use Pygame for graphical rendering and Pymunk for simulating fluid particle physics.

## Project Description

The objective of this project is to simulate the behavior of fluids in an interactive 2D environment. The simulation includes:

- **Graphical Rendering**: We use Pygame to create a graphical interface where the simulation results are visualized in real-time.
  
- **Fluid Dynamics**: We implement a simplified model of particle-based fluid dynamics using Pymunk, allowing interactions between particles and the environment.

## Key Features

- **Interactivity**: Users can interact with the simulation through simple controls to modify parameters and observe the resulting behavior.

- **Real-Time Visualization**: The simulation is rendered in real-time, providing immediate feedback on parameter changes.

- **Flexible Configuration**: The code allows for adjustments and expansions for experimentation and comparison with theoretical models.

## Installation

To run the simulation locally, follow these steps:

1. **Install Python**: Ensure you have [Python 3.12+](https://www.python.org/downloads/) installed on your machine.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/Kyamel/physics_sim_fluids
   cd physics_sim_fluids

3. **Create a vitual enviroment**:
   ```bash
   python -m venv venv
   venv/Scripts/activate

4. **Install Dependences**:
   ```bash
   pip install pygame
   pip install pygame_gui
   pip install pymunk

5. **Execute**:
   ```bash
   python src/main.py