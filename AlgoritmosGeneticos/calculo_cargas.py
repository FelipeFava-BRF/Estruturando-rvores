# pegando de exemplo esse código
# usaremos ele para calcularmos as alterações que tivermos de peso
# Dados base
cargas = {
    "C1": {"m3_por_ton": 480, "peso": 18, "lucro_por_ton": 310},
    "C2": {"m3_por_ton": 650, "peso": 15, "lucro_por_ton": 380},
    "C3": {"m3_por_ton": 580, "peso": 23, "lucro_por_ton": 350},
    "C4": {"m3_por_ton": 390, "peso": 12, "lucro_por_ton": 285},
}

def calcular(cargas, variacoes_peso):
    """
    variacoes_peso: dict com percentual de variação por carga (positivo = aumenta, negativo = reduz)
    Ex.: {"C1": 20, "C2": -10} -> C1 aumenta 20%, C2 reduz 10%
    """

    resultado = {}
    for carga, dados in cargas.items():
        peso_original = dados["peso"]
        m3_por_ton = dados["m3_por_ton"]
        lucro_por_ton = dados["lucro_por_ton"]


        variacao = variacoes_peso.get(carga, 0) / 100  # converte para fração
        novo_peso = peso_original * (1 + variacao)


        # Calcula novos valores
        novo_volume = m3_por_ton * novo_peso
        novo_lucro = lucro_por_ton * novo_peso

        resultado[carga] = {
            "peso_original": peso_original,
            "novo_peso": round(novo_peso, 2), # arredonda para o número mais próximo com até 2 casas decimais
            "novo_volume": round(novo_volume, 2),
            "novo_lucro": round(novo_lucro, 2)
        }
    return resultado

# reducoes = {} -> para cada nova população vamos colocar um valor de redução aleatório entre 0% a 20%
# Exemplo: aumentar C1 em 15%, C2 em 10%, C3 em 5%, C4 em 8%
variacoes = {"C1": 15, "C2": 10, "C3": 5, "C4": 8}
res = calcular(cargas, variacoes)


# essa função de calcular passando como variacoes_peso um valor que seja negativo, isso é, queremos reduzir o valor.
# usaremos isso no fitness como penalidade, caso mesmo com a tentativa de alocação das cargas não for suficiente para
# os compartimentos do avião, podemos fazer atribuindo um range de -10% a -20% de redução nas cargas para o próximo indivíduo na população.
# bem como, para maximizar os resultados, aos indivíduos que ficam na função elitismo (os melhores da população), vamos
# tentar aumentar a variação atribuindo um range de 5% a 10% para maximizarmos os resultados e passar para a próxima geração.


# Mostrar resultado
for carga, valores in res.items():
    print(f"{carga}: Peso={valores['novo_peso']} ton, Volume={valores['novo_volume']} m³, Lucro=R$ {valores['novo_lucro']}")