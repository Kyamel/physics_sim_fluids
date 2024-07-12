# Simulação 2D de Fluidos com Pygame e Pymunk

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

1. **Intalar Python**: tenha o python 3.12+ instalado na sua máquina https://www.python.org/downloads/.

2. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/Kyamel/physics_sim_fluids.git
   cd physics_sim_fluids

3. **Criar um ambiente virtual**:
   ```bash
   python -m venv venv
   venv/Scripts/activate

4. **Instalar Dependências**:
   ```bash
   pip install pygame
   pip install pymunk