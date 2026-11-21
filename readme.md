# Simulação Computacional — Realteq

Modelo computacional desenvolvido para a disciplina **ELE637 — Pensamento Sistêmico em Engenharia (UFMG)**.

## Objetivo

Simular o processo de triagem e atendimento de chamados técnicos externos da Realteq, investigando como encaminhamentos presenciais desnecessários afetam a capacidade operacional, o acúmulo de chamados e a eficiência do atendimento.

O modelo também avalia os efeitos da implementação de um checklist de triagem técnica.

## Modelo matemático

A simulação utiliza princípios de Dinâmica de Sistemas, baseando-se em um Diagrama de Laços Causais (DLC) e um Diagrama de Estoques e Fluxos (DEF).

São considerados dois estoques:

- **Fila de chamados legítimos:** atendimentos que necessitam de intervenção presencial.
- **Fila de chamados indevidos:** atendimentos encaminhados presencialmente que poderiam ser solucionados remotamente.

A evolução dos estoques segue:

\[
F(t+\Delta t)=F(t)+[\lambda(t)-A(t)]\Delta t
\]

A capacidade de atendimento é determinada por:

\[
C=\frac{H}{h}
\]

As filas compartilham a capacidade disponível de atendimento externo.

### Retroalimentação sistêmica

O modelo representa o laço de reforço R2, no qual o aumento das filas gera mais cobranças dos clientes, elevando a pressão sobre a recepção e a probabilidade de encaminhamentos indevidos.

A implementação de um checklist técnico reduz essa probabilidade e permite avaliar os efeitos da intervenção.

## Estrutura do projeto

```text
realteq-simulation/
├── parameters.py
├── model.py
├── simulation.py
├── visualization.py
├── sensitivity.py
├── validation.py
├── main.py
└── README.md
```

## Tecnologias

- Python
- NumPy
- Pandas
- Matplotlib

## Execução

Instale as dependências:

```bash
python -m pip install numpy pandas matplotlib
```

Execute a simulação principal:

```bash
python main.py
```

Execute a análise de sensibilidade:

```bash
python sensitivity.py
```

Execute as validações matemáticas:

```bash
python validation.py
```

## Dados e parâmetros

O levantamento histórico contempla 194 chamados externos, dos quais 22 foram identificados como potencialmente solucionáveis remotamente (11,34%).

O modelo utiliza parâmetros operacionais hipotéticos, incluindo duração das visitas, intensidade das cobranças e eficácia do checklist.

Esses parâmetros podem ser ajustados em `parameters.py`.

## Experimentos computacionais

Foram implementados:

- Comparação entre operação atual e operação com checklist técnico.
- Análise de sensibilidade da duração das visitas e eficácia do checklist.
- Verificação da conservação dos chamados.
- Análise de convergência numérica.
- Calibração da taxa inicial de erro utilizando os registros históricos.

## Limitações

O simulador é determinístico e utiliza taxas médias de chegada. A capacidade operacional e alguns coeficientes de retroalimentação são hipóteses de modelagem, não medições diretas da empresa.

Os resultados representam cenários simulados e não previsões verificadas do funcionamento real da Realteq.