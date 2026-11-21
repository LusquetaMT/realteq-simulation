
import parameters as p

from simulation import executar_simulacao


def calcular_indicadores(historico):
    chegadas_legitimos = sum(
        registro["chegadas_legitimos"]
        for registro in historico
    )

    chegadas_indevidos = sum(
        registro["chegadas_indevidos"]
        for registro in historico
    )

    atendimentos_legitimos = sum(
        registro["atendimentos_legitimos"]
        for registro in historico
    )

    atendimentos_indevidos = sum(
        registro["atendimentos_indevidos"]
        for registro in historico
    )

    fila_final_legitimos = historico[-1]["fila_legitimos"]
    fila_final_indevidos = historico[-1]["fila_indevidos"]

    return {
        "chegadas_legitimos": chegadas_legitimos,
        "chegadas_indevidos": chegadas_indevidos,
        "atendimentos_legitimos": atendimentos_legitimos,
        "atendimentos_indevidos": atendimentos_indevidos,
        "fila_final_legitimos": fila_final_legitimos,
        "fila_final_indevidos": fila_final_indevidos,
        "fila_final_total": (
            fila_final_legitimos + fila_final_indevidos
        )
    }


def calibrar_taxa_erro(tolerancia=1e-6, max_iteracoes=100):
    alvo = p.chamados_indevidos

    def calcular_chegadas(taxa):
        historico = executar_simulacao(
            eficacia_checklist=0.0,
            taxa_erro_base=taxa
        )

        return calcular_indicadores(historico)["chegadas_indevidos"]

    minimo = 0.0
    maximo = 1.0

    chegadas_minimas = calcular_chegadas(minimo)
    chegadas_maximas = calcular_chegadas(maximo)

    if not chegadas_minimas - tolerancia <= alvo <= chegadas_maximas + tolerancia:
        raise ValueError(
            "O alvo não pode ser reproduzido com os parâmetros atuais"
        )

    for _ in range(max_iteracoes):
        meio = (minimo + maximo) / 2
        chegadas = calcular_chegadas(meio)

        if abs(chegadas - alvo) <= tolerancia:
            return meio

        if chegadas < alvo:
            minimo = meio
        else:
            maximo = meio

    return (minimo + maximo) / 2


def validar_conservacao(historico, tolerancia=1e-8):
    indicadores = calcular_indicadores(historico)

    erro_legitimos = abs(
        p.fila_inicial_legitimos
        + indicadores["chegadas_legitimos"]
        - indicadores["atendimentos_legitimos"]
        - indicadores["fila_final_legitimos"]
    )

    erro_indevidos = abs(
        p.fila_inicial_indevidos
        + indicadores["chegadas_indevidos"]
        - indicadores["atendimentos_indevidos"]
        - indicadores["fila_final_indevidos"]
    )

    for registro in historico:
        capacidade_passo = (
            registro["capacidade_diaria"] * registro["passo_tempo"]
        )

        assert registro["total_atendimentos"] <= capacidade_passo + tolerancia
        assert registro["fila_legitimos"] >= -tolerancia
        assert registro["fila_indevidos"] >= -tolerancia

    return {
        "erro_legitimos": erro_legitimos,
        "erro_indevidos": erro_indevidos,
        "aprovado": max(erro_legitimos, erro_indevidos) <= tolerancia
    }


def analisar_convergencia(taxa_erro_base):
    resultados = []

    for passo in [1.0, 0.5, 0.25, 0.125]:
        historico = executar_simulacao(
            passo_tempo=passo,
            taxa_erro_base=taxa_erro_base
        )

        indicadores = calcular_indicadores(historico)

        resultados.append({
            "passo": passo,
            "fila_final": indicadores["fila_final_total"],
            "chegadas_indevidas": indicadores["chegadas_indevidos"]
        })

    referencia = resultados[-1]

    for resultado in resultados:
        resultado["diferenca_fila"] = abs(
            resultado["fila_final"] - referencia["fila_final"]
        )

        resultado["diferenca_indevidos"] = abs(
            resultado["chegadas_indevidas"]
            - referencia["chegadas_indevidas"]
        )

    return resultados


def executar_validacao():
    taxa_calibrada = calibrar_taxa_erro()

    historico = executar_simulacao(
        taxa_erro_base=taxa_calibrada
    )

    indicadores = calcular_indicadores(historico)
    conservacao = validar_conservacao(historico)
    convergencia = analisar_convergencia(taxa_calibrada)

    print("\n=== CALIBRAÇÃO ===")
    print(f"Taxa de erro inicial: {taxa_calibrada:.6f}")
    print(f"Encaminhamentos simulados: {indicadores['chegadas_indevidos']:.4f}")
    print(f"Encaminhamentos observados: {p.chamados_indevidos}")

    print("\n=== CONSERVAÇÃO ===")
    print(f"Erro legítimos: {conservacao['erro_legitimos']:.10f}")
    print(f"Erro indevidos: {conservacao['erro_indevidos']:.10f}")
    print(f"Teste aprovado: {conservacao['aprovado']}")

    print("\n=== CONVERGÊNCIA ===")

    for resultado in convergencia:
        print(
            f"Passo: {resultado['passo']:.3f} | "
            f"Fila: {resultado['fila_final']:.4f} | "
            f"Indevidos: {resultado['chegadas_indevidas']:.4f} | "
            f"Δ fila: {resultado['diferenca_fila']:.6f} | "
            f"Δ indevidos: {resultado['diferenca_indevidos']:.6f}"
        )

    return taxa_calibrada


if __name__ == "__main__":
    executar_validacao()
