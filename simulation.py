
import parameters as p

from model import (
    atualizar_filas,
    calcular_cobrancas,
    calcular_taxa_erro,
    calcular_chegada_indevidos
)


def executar_simulacao(
    eficacia_checklist=0.0,
    horas_por_visita=None,
    passo_tempo=None,
    taxa_erro_base=None
):
    if horas_por_visita is None:
        horas_por_visita = p.horas_por_visita

    if passo_tempo is None:
        passo_tempo = p.passo_tempo

    if taxa_erro_base is None:
        taxa_erro_base = p.taxa_erro_base

    if passo_tempo <= 0:
        raise ValueError("O passo temporal deve ser positivo")

    if p.atraso_cobrancas < 0:
        raise ValueError("O atraso não pode ser negativo")

    atraso_passos = round(p.atraso_cobrancas / passo_tempo)

    if abs(atraso_passos * passo_tempo - p.atraso_cobrancas) > 1e-9:
        raise ValueError("O atraso deve ser múltiplo do passo temporal")

    fila_legitimos = p.fila_inicial_legitimos
    fila_indevidos = p.fila_inicial_indevidos

    historico = []
    tempo = 0.0

    historico_filas = [
        (fila_legitimos, fila_indevidos)
    ]

    while tempo < p.dias_simulacao - 1e-9:
        passo = min(passo_tempo, p.dias_simulacao - tempo)

        indice_atrasado = max(
            0,
            len(historico_filas) - 1 - atraso_passos
        )

        fila_legitimos_atrasada, fila_indevidos_atrasada = (
            historico_filas[indice_atrasado]
        )

        cobrancas = calcular_cobrancas(
            fila_legitimos_atrasada,
            fila_indevidos_atrasada,
            p.coeficiente_cobrancas
        )

        taxa_erro = calcular_taxa_erro(
            taxa_erro_base,
            cobrancas,
            p.sensibilidade_erro,
            eficacia_checklist
        )

        taxa_chegada_indevidos = calcular_chegada_indevidos(
            p.taxa_demanda_remota,
            taxa_erro
        )

        resultado = atualizar_filas(
            fila_legitimos=fila_legitimos,
            fila_indevidos=fila_indevidos,
            taxa_chegada_legitimos=p.taxa_chegada_legitimos,
            taxa_chegada_indevidos=taxa_chegada_indevidos,
            horas_disponiveis=p.horas_disponiveis,
            horas_por_visita=horas_por_visita,
            passo_tempo=passo
        )

        tempo += passo

        fila_legitimos = resultado["fila_legitimos"]
        fila_indevidos = resultado["fila_indevidos"]

        historico_filas.append(
            (fila_legitimos, fila_indevidos)
        )

        historico.append({
            "dia": tempo,
            "passo_tempo": passo,
            "cobrancas": cobrancas,
            "taxa_erro": taxa_erro,
            "taxa_chegada_legitimos": p.taxa_chegada_legitimos,
            "taxa_chegada_indevidos": taxa_chegada_indevidos,
            "chegadas_legitimos": p.taxa_chegada_legitimos * passo,
            "chegadas_indevidos": taxa_chegada_indevidos * passo,
            **resultado
        })

    return historico
