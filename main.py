
import parameters as p

from simulation import executar_simulacao
from visualization import visualizar_simulacoes
from validation import calibrar_taxa_erro, calcular_indicadores


def imprimir_resumo(nome, indicadores):
    print(f"\n=== {nome} ===")

    print(
        f"Atendimentos legítimos: "
        f"{indicadores['atendimentos_legitimos']:.2f}"
    )

    print(
        f"Atendimentos indevidos: "
        f"{indicadores['atendimentos_indevidos']:.2f}"
    )

    print(
        f"Encaminhamentos indevidos: "
        f"{indicadores['chegadas_indevidos']:.2f}"
    )

    print(
        f"Fila final: "
        f"{indicadores['fila_final_total']:.2f}"
    )


def main():
    taxa_calibrada = calibrar_taxa_erro()

    historico_base = executar_simulacao(
        eficacia_checklist=0.0,
        taxa_erro_base=taxa_calibrada
    )

    historico_checklist = executar_simulacao(
        eficacia_checklist=p.eficacia_checklist,
        taxa_erro_base=taxa_calibrada
    )

    base = calcular_indicadores(historico_base)
    checklist = calcular_indicadores(historico_checklist)

    imprimir_resumo("CENÁRIO ATUAL", base)
    imprimir_resumo("CENÁRIO COM CHECKLIST", checklist)

    encaminhamentos_evitados = (
        base["chegadas_indevidos"]
        - checklist["chegadas_indevidos"]
    )

    reducao_fila = (
        base["fila_final_total"]
        - checklist["fila_final_total"]
    )

    print("\n=== COMPARAÇÃO ===")

    print(
        f"Encaminhamentos evitados: "
        f"{encaminhamentos_evitados:.2f}"
    )

    print(
        f"Redução da fila final: "
        f"{reducao_fila:.2f}"
    )

    visualizar_simulacoes(
        historico_base,
        historico_checklist
    )


if __name__ == "__main__":
    main()
