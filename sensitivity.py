
import pandas as pd
import matplotlib.pyplot as plt

from simulation import executar_simulacao
from validation import calibrar_taxa_erro


def executar_analise_sensibilidade():
    taxa_calibrada = calibrar_taxa_erro()
    duracoes_visita = [3.0, 4.0, 5.0, 6.0]
    eficacias_checklist = [0.0, 0.25, 0.50, 0.75, 1.0]

    resultados = []

    for duracao in duracoes_visita:
        for eficacia in eficacias_checklist:
            historico = executar_simulacao(
                eficacia_checklist=eficacia,
                horas_por_visita=duracao,
                taxa_erro_base=taxa_calibrada
            )

            ultimo_dia = historico[-1]

            fila_final = (
                ultimo_dia["fila_legitimos"] +
                ultimo_dia["fila_indevidos"]
            )

            encaminhamentos_indevidos = sum(
                dia["chegadas_indevidos"]
                for dia in historico
            )

            atendimentos_legitimos = sum(
                dia["atendimentos_legitimos"]
                for dia in historico
            )

            utilizacao_media = sum(
                dia["total_atendimentos"] /
                (dia["capacidade_diaria"] * dia["passo_tempo"])
                for dia in historico
            ) / len(historico) * 100

            resultados.append({
                "horas_por_visita": duracao,
                "eficacia_checklist": eficacia,
                "fila_final": fila_final,
                "encaminhamentos_indevidos": encaminhamentos_indevidos,
                "atendimentos_legitimos": atendimentos_legitimos,
                "utilizacao_media": utilizacao_media
            })

    return pd.DataFrame(resultados)


def visualizar_sensibilidade(resultados):
    indicadores = [
        ("fila_final", "Fila final (chamados)"),
        ("encaminhamentos_indevidos", "Encaminhamentos indevidos"),
        ("atendimentos_legitimos", "Atendimentos legítimos")
    ]

    fig, eixos = plt.subplots(1, 3, figsize=(17, 5))

    for eixo, (coluna, titulo) in zip(eixos, indicadores):
        tabela = resultados.pivot(
            index="horas_por_visita",
            columns="eficacia_checklist",
            values=coluna
        )

        imagem = eixo.imshow(
            tabela.values,
            aspect="auto",
            cmap="viridis"
        )

        eixo.set_xticks(range(len(tabela.columns)))
        eixo.set_xticklabels([
            f"{valor:.0%}" for valor in tabela.columns
        ])

        eixo.set_yticks(range(len(tabela.index)))
        eixo.set_yticklabels([
            f"{valor:g}" for valor in tabela.index
        ])

        eixo.set_xlabel("Eficácia do checklist")
        eixo.set_ylabel("Horas por visita")
        eixo.set_title(titulo)

        for i in range(len(tabela.index)):
            for j in range(len(tabela.columns)):
                eixo.text(
                    j,
                    i,
                    f"{tabela.iloc[i, j]:.1f}",
                    ha="center",
                    va="center",
                    color="white"
                )

        fig.colorbar(imagem, ax=eixo)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    resultados = executar_analise_sensibilidade()

    print(resultados.round(2).to_string(index=False))

    visualizar_sensibilidade(resultados)
