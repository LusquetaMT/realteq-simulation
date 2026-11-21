
import matplotlib.pyplot as plt
import pandas as pd


def visualizar_simulacoes(historico_base, historico_checklist):
    base = pd.DataFrame(historico_base)
    checklist = pd.DataFrame(historico_checklist)

    for dados in (base, checklist):
        dados["fila_total"] = (
            dados["fila_legitimos"] + dados["fila_indevidos"]
        )

        dados["utilizacao"] = (
            100 * dados["total_atendimentos"] /
            (dados["capacidade_diaria"] * dados["passo_tempo"])
        )

        dados["utilizacao"] = (
            dados["utilizacao"].fillna(0).clip(0, 100)
        )

    fig, eixos = plt.subplots(3, 1, figsize=(12, 12))

    eixos[0].plot(
        base["dia"],
        base["fila_total"],
        label="Cenário atual"
    )

    eixos[0].plot(
        checklist["dia"],
        checklist["fila_total"],
        label="Com checklist"
    )

    eixos[0].set_title("Evolução da fila externa total")
    eixos[0].set_ylabel("Chamados pendentes")

    eixos[1].plot(
        base["dia"],
        base["taxa_erro"] * 100,
        label="Cenário atual"
    )

    eixos[1].plot(
        checklist["dia"],
        checklist["taxa_erro"] * 100,
        label="Com checklist"
    )

    eixos[1].set_title("Probabilidade de erro na triagem")
    eixos[1].set_ylabel("Probabilidade (%)")

    eixos[2].plot(
        base["dia"],
        base["utilizacao"],
        label="Cenário atual"
    )

    eixos[2].plot(
        checklist["dia"],
        checklist["utilizacao"],
        label="Com checklist"
    )

    eixos[2].axhline(
        100,
        linestyle="--",
        label="Capacidade máxima"
    )

    eixos[2].set_title("Utilização da capacidade de campo")
    eixos[2].set_ylabel("Utilização (%)")
    eixos[2].set_ylim(0, 110)

    for eixo in eixos:
        eixo.set_xlabel("Dia")
        eixo.legend()
        eixo.grid(True)

    plt.tight_layout()
    plt.show()
