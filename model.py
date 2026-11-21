
def atualizar_fila(fila, taxa_chegada, taxa_atendimento, passo_tempo):
    proxima_fila = fila + (
        taxa_chegada - taxa_atendimento
    ) * passo_tempo

    return max(0.0, proxima_fila)


def calcular_capacidade(horas_disponiveis, horas_por_visita):
    if horas_disponiveis < 0:
        raise ValueError("As horas disponíveis não podem ser negativas")

    if horas_por_visita <= 0:
        raise ValueError("As horas por visita devem ser positivas")

    return horas_disponiveis / horas_por_visita


def distribuir_capacidade(fila_legitimos, fila_indevidos, capacidade):
    fila_total = fila_legitimos + fila_indevidos

    if fila_total <= 0 or capacidade <= 0:
        return 0.0, 0.0

    total_atendimentos = min(capacidade, fila_total)

    atendimentos_legitimos = total_atendimentos * (
        fila_legitimos / fila_total
    )

    atendimentos_indevidos = total_atendimentos * (
        fila_indevidos / fila_total
    )

    return atendimentos_legitimos, atendimentos_indevidos


def calcular_cobrancas(fila_legitimos, fila_indevidos, coeficiente):
    if coeficiente < 0:
        raise ValueError("O coeficiente não pode ser negativo")

    fila_total = fila_legitimos + fila_indevidos

    return coeficiente * fila_total


def calcular_taxa_erro(
    taxa_erro_base,
    cobrancas,
    sensibilidade_erro,
    eficacia_checklist
):
    if not 0 <= taxa_erro_base <= 1:
        raise ValueError("A taxa de erro base deve estar entre 0 e 1")

    if not 0 <= eficacia_checklist <= 1:
        raise ValueError("A eficácia deve estar entre 0 e 1")

    if cobrancas < 0 or sensibilidade_erro < 0:
        raise ValueError("Cobranças e sensibilidade não podem ser negativas")

    taxa_erro = taxa_erro_base + sensibilidade_erro * cobrancas

    taxa_erro = min(1.0, max(0.0, taxa_erro))

    return taxa_erro * (1.0 - eficacia_checklist)


def calcular_chegada_indevidos(taxa_demanda_remota, taxa_erro):
    if taxa_demanda_remota < 0:
        raise ValueError("A demanda remota não pode ser negativa")

    return taxa_demanda_remota * taxa_erro


def atualizar_filas(
    fila_legitimos,
    fila_indevidos,
    taxa_chegada_legitimos,
    taxa_chegada_indevidos,
    horas_disponiveis,
    horas_por_visita,
    passo_tempo
):
    if passo_tempo <= 0:
        raise ValueError("O passo temporal deve ser positivo")

    if min(
        fila_legitimos,
        fila_indevidos,
        taxa_chegada_legitimos,
        taxa_chegada_indevidos
    ) < 0:
        raise ValueError("Filas e taxas de chegada não podem ser negativas")

    capacidade_diaria = calcular_capacidade(
        horas_disponiveis,
        horas_por_visita
    )

    chamados_legitimos_disponiveis = (
        fila_legitimos + taxa_chegada_legitimos * passo_tempo
    )

    chamados_indevidos_disponiveis = (
        fila_indevidos + taxa_chegada_indevidos * passo_tempo
    )

    atendimentos_legitimos, atendimentos_indevidos = distribuir_capacidade(
        chamados_legitimos_disponiveis,
        chamados_indevidos_disponiveis,
        capacidade_diaria * passo_tempo
    )

    taxa_atendimento_legitimos = atendimentos_legitimos / passo_tempo
    taxa_atendimento_indevidos = atendimentos_indevidos / passo_tempo

    proxima_fila_legitimos = atualizar_fila(
        fila_legitimos,
        taxa_chegada_legitimos,
        taxa_atendimento_legitimos,
        passo_tempo
    )

    proxima_fila_indevidos = atualizar_fila(
        fila_indevidos,
        taxa_chegada_indevidos,
        taxa_atendimento_indevidos,
        passo_tempo
    )

    return {
        "fila_legitimos": proxima_fila_legitimos,
        "fila_indevidos": proxima_fila_indevidos,
        "atendimentos_legitimos": atendimentos_legitimos,
        "atendimentos_indevidos": atendimentos_indevidos,
        "total_atendimentos": atendimentos_legitimos + atendimentos_indevidos,
        "capacidade_diaria": capacidade_diaria
    }
