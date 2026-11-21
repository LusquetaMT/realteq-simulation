# Simulação Computacional — Realteq

Modelo computacional desenvolvido para a disciplina **ELE637 — Pensamento Sistêmico em Engenharia (UFMG)**.

## Objetivo

Simular o processo de triagem e atendimento de chamados técnicos externos da Realteq, investigando como encaminhamentos presenciais desnecessários afetam a capacidade operacional, o acúmulo de chamados e a eficiência do atendimento.

O modelo também avalia os efeitos da implementação de um checklist de triagem técnica.

## Modelo matemático

A simulação utiliza princípios de **Dinâmica de Sistemas**, baseando-se em um Diagrama de Laços Causais (DLC) e um Diagrama de Estoques e Fluxos (DEF).

São considerados dois estoques:

- **Fila de chamados legítimos:** atendimentos que necessitam de intervenção presencial.
- **Fila de chamados indevidos:** atendimentos encaminhados presencialmente que poderiam ser solucionados remotamente.

A evolução dos estoques segue:

$$
F(t+\Delta t)=F(t)+[\lambda(t)-A(t)]\Delta t
$$

Onde:

- $F(t)$: quantidade de chamados na fila.
- $\lambda(t)$: taxa de chegada de chamados.
- $A(t)$: taxa de atendimento.
- $\Delta t$: passo temporal da simulação.

A capacidade de atendimento é determinada por:

$$
C=\frac{H}{h}
$$

Onde $H$ representa as horas disponíveis de campo por dia e $h$ representa a duração média de uma visita.

As duas filas compartilham a capacidade disponível de atendimento externo, distribuída proporcionalmente à quantidade de chamados pendentes.

### Retroalimentação sistêmica

O modelo representa o **laço de reforço R2**, no qual o aumento das filas gera mais cobranças dos clientes, elevando a pressão sobre a recepção e a probabilidade de encaminhamentos indevidos.

A pressão das cobranças é modelada por:

$$
P(t)=c[F_L(t-\tau)+F_I(t-\tau)]
$$

Onde $c$ representa o coeficiente de cobranças e $\tau$ representa o atraso de retroalimentação.

A probabilidade de erro na triagem é determinada por:

$$
q(t)=(1-e)\min(1,q_0+kP(t))
$$

Onde:

- $q_0$: probabilidade inicial de erro.
- $k$: sensibilidade da triagem às cobranças.
- $e$: eficácia do checklist técnico, entre 0 e 1.

A taxa de encaminhamentos indevidos é calculada por:

$$
\lambda_I(t)=q(t)\lambda_R(t)
$$

Onde $\lambda_R(t)$ representa a taxa de demandas potencialmente solucionáveis remotamente.

A implementação do checklist reduz a probabilidade de encaminhamentos indevidos, permitindo avaliar seus efeitos sobre as filas e a utilização da capacidade de campo.

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

O levantamento histórico contempla **194 chamados externos**, dos quais **22 foram identificados como potencialmente solucionáveis remotamente (11,34%)**.

Os dados correspondem aos atendimentos externos registrados pelo técnico participante da pesquisa, não à totalidade dos chamados recebidos pela empresa.

O modelo utiliza parâmetros operacionais hipotéticos, incluindo:

- Horas disponíveis de campo por dia.
- Duração média das visitas.
- Intensidade das cobranças dos clientes.
- Sensibilidade da triagem à pressão.
- Atraso de retroalimentação.
- Eficácia do checklist técnico.

Esses parâmetros podem ser ajustados em `parameters.py`.

## Experimentos computacionais

Foram implementados:

- **Simulação de cenários:** comparação entre a operação atual e a operação com checklist técnico.
- **Análise de sensibilidade:** avaliação dos efeitos da duração das visitas e da eficácia do checklist.
- **Conservação de chamados:** verificação do equilíbrio entre entradas, atendimentos e estoques.
- **Convergência numérica:** comparação dos resultados com diferentes passos temporais.
- **Calibração:** ajuste da taxa inicial de erro para reproduzir os 22 encaminhamentos indevidos observados no cenário de referência.

## Limitações

O simulador é determinístico e utiliza taxas médias de chegada de chamados.

A capacidade operacional, a demanda potencialmente remota e os coeficientes de retroalimentação são hipóteses de modelagem, não medições diretas da empresa.

Os chamados são representados por quantidades contínuas, podendo assumir valores fracionários.

A calibração reproduz um indicador histórico, mas não constitui validação independente de todos os mecanismos do sistema.

Os resultados representam **cenários simulados**, e não previsões verificadas do funcionamento real da Realteq.