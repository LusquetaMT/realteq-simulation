
total_chamados = 194
chamados_indevidos = 22
chamados_legitimos = total_chamados - chamados_indevidos

dias_observados = 109

taxa_chegada_legitimos = chamados_legitimos / dias_observados
taxa_chegada_indevidos = chamados_indevidos / dias_observados

taxa_demanda_remota = 2.0
taxa_erro_base = taxa_chegada_indevidos / taxa_demanda_remota

horas_disponiveis = 8.0
horas_por_visita = 5.0

coeficiente_cobrancas = 0.1
sensibilidade_erro = 0.01
atraso_cobrancas = 3

eficacia_checklist = 0.5

passo_tempo = 1.0
dias_simulacao = 109

fila_inicial_legitimos = 0.0
fila_inicial_indevidos = 0.0
