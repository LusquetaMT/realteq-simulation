"""
Testes de valores extremos e busca dos equilíbrios do modelo.

Uso: python extremos.py
"""

import parameters as p

from simulation import executar_simulacao
from validation import calibrar_taxa_erro, calcular_indicadores


def simular(taxa_erro_base, eficacia_checklist=0.0,
            horas_por_visita=None, **parametros):
    # Troca temporariamente valores de parameters.py e restaura no final
    originais = {nome: getattr(p, nome) for nome in parametros}

    for nome, valor in parametros.items():
        setattr(p, nome, valor)

    try:
        return executar_simulacao(
            eficacia_checklist=eficacia_checklist,
            horas_por_visita=horas_por_visita,
            taxa_erro_base=taxa_erro_base
        )
    finally:
        for nome, valor in originais.items():
            setattr(p, nome, valor)


def fila_total(registro):
    return registro["fila_legitimos"] + registro["fila_indevidos"]


def testar_valores_extremos(taxa_calibrada):
    q0 = taxa_calibrada

    cenarios = [
        ("Cenário atual", dict(taxa_erro_base=q0)),
        ("Checklist 50%", dict(taxa_erro_base=q0, eficacia_checklist=0.5)),
        ("Checklist 90%", dict(taxa_erro_base=q0, eficacia_checklist=0.9)),
        ("Sem laço R2 (k = 0)", dict(taxa_erro_base=q0, sensibilidade_erro=0.0)),
        ("Triagem perfeita (q0 = 0)", dict(taxa_erro_base=0.0)),
        ("Tudo vai a campo (q0 = 1)", dict(taxa_erro_base=1.0)),
        ("Sem horas de campo (H = 0)", dict(taxa_erro_base=q0, horas_disponiveis=0.0)),
        ("Visitas de 1 h (h = 1)", dict(taxa_erro_base=q0, horas_por_visita=1.0)),
    ]

    print("\n=== VALORES EXTREMOS (109 dias) ===")
    print(f"{'Cenário':<28}{'Indevidos':>11}{'Legítimos':>11}"
          f"{'Fila final':>12}{'q final':>10}")

    for nome, ajustes in cenarios:
        historico = simular(**ajustes)
        indicadores = calcular_indicadores(historico)

        print(
            f"{nome:<28}"
            f"{indicadores['chegadas_indevidos']:>11.2f}"
            f"{indicadores['atendimentos_legitimos']:>11.2f}"
            f"{indicadores['fila_final_total']:>12.2f}"
            f"{historico[-1]['taxa_erro'] * 100:>9.1f}%"
        )


def analisar_equilibrios(taxa_calibrada):
    q0 = taxa_calibrada
    capacidade = p.horas_disponiveis / p.horas_por_visita
    folga = capacidade - p.taxa_chegada_legitimos

    # Fila vazia não gera cobranças, então q = (1 - e) * q0.
    # A fila só fica parada em zero se a chegada couber na capacidade:
    #   lambda_L + (1 - e) * q0 * lambda_R <= C
    taxa_erro_maxima = folga / p.taxa_demanda_remota
    eficacia_minima = 1 - taxa_erro_maxima / q0

    horas_maximas = p.horas_disponiveis / (
        p.taxa_chegada_legitimos + q0 * p.taxa_demanda_remota
    )

    horas_maximas_checklist = p.horas_disponiveis / (
        p.taxa_chegada_legitimos
        + (1 - p.eficacia_checklist) * q0 * p.taxa_demanda_remota
    )

    print("\n=== EQUILÍBRIO COM FILA VAZIA ===")
    print(f"Capacidade de campo C: {capacidade:.3f} chamados/dia")
    print(f"Demanda legítima: {p.taxa_chegada_legitimos:.3f} chamados/dia "
          f"({p.taxa_chegada_legitimos / capacidade:.1%} de C)")
    print(f"Erro máximo de triagem para a fila não crescer: {taxa_erro_maxima:.2%}")
    print(f"Eficácia mínima do checklist: {eficacia_minima:.1%}")
    print(f"Horas máximas por visita sem checklist: {horas_maximas:.2f} h")
    print(f"Horas máximas por visita com checklist de "
          f"{p.eficacia_checklist:.0%}: {horas_maximas_checklist:.2f} h")

    print("\nConferência pela simulação:")

    for eficacia in [0.0, 0.5, 0.80, 0.86, 0.88, 0.90, 1.0]:
        historico = simular(q0, eficacia_checklist=eficacia)
        crescimento = fila_total(historico[-1]) - fila_total(historico[-2])

        print(f"Checklist {eficacia:>4.0%} | fila final: "
              f"{fila_total(historico[-1]):6.2f} | "
              f"crescimento no último dia: {crescimento:+.4f}")

    # Com fila F > 0 as cobranças elevam q. A chegada volta a igualar
    # a capacidade em um segundo ponto, F*, que é um equilíbrio instável:
    #   (1 - e) * (q0 + k * c * F*) * lambda_R = C - lambda_L
    print("\n=== EQUILÍBRIO INSTÁVEL (PONTO DE VIRADA) ===")

    for eficacia in [0.90, 0.95]:
        fila_critica = (
            folga / ((1 - eficacia) * p.taxa_demanda_remota) - q0
        ) / (p.sensibilidade_erro * p.coeficiente_cobrancas)

        print(f"\nChecklist {eficacia:.0%}: F* = {fila_critica:.1f} chamados")

        for fila_inicial in [0.5 * fila_critica, 1.5 * fila_critica]:
            historico = simular(
                q0,
                eficacia_checklist=eficacia,
                fila_inicial_legitimos=fila_inicial,
                dias_simulacao=730
            )

            tendencia = fila_total(historico[-1]) - fila_total(historico[-2])
            sentido = "diminui" if tendencia < 0 else "cresce"

            print(f"  Fila inicial {fila_inicial:6.1f} -> após 2 anos: "
                  f"{fila_total(historico[-1]):6.1f} ({sentido})")


def main():
    taxa_calibrada = calibrar_taxa_erro()
    print(f"Taxa de erro calibrada q0: {taxa_calibrada:.4f}")

    testar_valores_extremos(taxa_calibrada)
    analisar_equilibrios(taxa_calibrada)


if __name__ == "__main__":
    main()
