# Lógica de Cálculos

def umidade(peso_inicial, peso_final):
    return ((peso_inicial - peso_final) / peso_inicial) * 100

def cinzas(peso_amostra, peso_residuo):
    return (peso_residuo / peso_amostra) * 100

def proteinas_kjeldahl(volume_acido, fator, peso_amostra):
    return (volume_acido * fator * 1.4007) / peso_amostra

def lipidios_soxhlet(peso_residuo, peso_amostra):
    return (peso_residuo / peso_amostra) * 100

def ph(valor_ph):
    if valor_ph < 7:
        return "Ácida"
    elif valor_ph == 7:
        return "Neutra"
    else:
        return "Básica"

def acidez_titulavel(volume_NaOH, normalidade, fator, peso_amostra):
    return (volume_NaOH * normalidade * fator * 100) / peso_amostra

def densidade(massa, volume):
    return massa / volume