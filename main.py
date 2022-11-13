import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


def media(array):
    return sum(array) / len(array)


def mediana(array):
    half = len(array) // 2
    return sorted(array)[half]


def moda(array):
    counter = defaultdict(lambda: 0)

    # talvez precise quebrar em grupinhos
    for i in array:
        counter[i] += 1

    repetitions = lambda x: counter[x]
    return max(array, key=repetitions)


def variancia(array):
    media_ = media(array)
    sum_ = 0
    size_ = len(array)

    for i in array:
        sum_ += (i - media_) ** 2

    return sum_ / size_


def plot_histogram(array, classes=None):
    if classes is None:
        classes = int(np.sqrt(len(array)))
    plt.hist(array, bins=classes)
    plt.show()


def extrair_dados():
    tabela = pd.read_excel("dados.xlsx")

    marcas = tabela["Marca"]
    latinha_350 = tabela["C16 - LATA – 350 ml"]

    spaten = [
        preco
        for marca, preco in zip(marcas, latinha_350)
        if (preco > 0) and (marca == "SPATEN")
    ]
    heineken = [
        preco
        for marca, preco in zip(marcas, latinha_350)
        if (preco > 0) and (marca == "HEINEKEN")
    ]

    return spaten, heineken


def histograma_cervejas(spaten, heineken):
    fig, (spaten_ax, heineken_ax) = plt.subplots(1, 2, sharex=True, sharey=True)
    fig.suptitle("Preços por latas de 350 ml")

    bins = np.arange(0, 10, 0.5)

    spaten_ax.hist(spaten, bins=bins, color="green")
    heineken_ax.hist(heineken, bins=bins, color="red")

    spaten_ax.set_title("Spaten")
    heineken_ax.set_title("Heineken")

    plt.show()


def boxplot_cervejas(spaten, heineken):
    fig, (spaten_ax, heineken_ax) = plt.subplots(1, 2, sharex=True, sharey=True)
    fig.suptitle("Preços por latas de 350 ml")

    spaten_ax.boxplot(spaten, patch_artist=True)
    heineken_ax.boxplot(heineken, patch_artist=True)

    spaten_ax.set_title("Spaten")
    heineken_ax.set_title("Heineken")

    plt.show()


def valor_central(array):
    string = ""
    string += "Média:   {:.4} \n".format(media(array))
    string += "Mediana: {:.4} \n".format(mediana(array))
    string += "Moda:    {:.4}".format(moda(array))
    return string


def dispersao(array):
    var = variancia(array)
    desvio = np.sqrt(var)
    erro = desvio / np.sqrt(len(array))
    media_ = media(array)
    coeficiente = desvio / media_ * 100

    string = ""
    string += "Variância:       {:.4} \n".format(var)
    string += "Desvio padrão:   {:.4} \n".format(desvio)
    string += "Erro padrão:     {:.4} \n".format(erro)
    string += "Coeficiente de variação: {:.4}".format(coeficiente)
    return string


def forma(array):
    string = ""
    string += "Assimetria:  {:.4} \n".format(0.0)
    string += "Curtose:     {:.4}".format(0.0)
    return string


def boxplot_dados(array):
    half = len(array) // 2
    array = sorted(array)

    q1 = mediana(array[:half])
    q2 = mediana(array)
    q3 = mediana(array[half:])

    iqr = q3 - q1
    minimum = q1 - iqr * 1.5
    maximum = q3 + iqr * 1.5

    ok = set()
    outliers = set()
    for i in array:
        if minimum < i < maximum:
            ok.add(i)
        else:
            outliers.add(i)

    minimum = min(ok)
    maximum = max(ok)

    string = "Min: {:.4} \n".format(minimum)
    string += "Q1: {:.4} \n".format(q1)
    string += "Q2: {:.4} \n".format(q2)
    string += "Q3: {:.4} \n".format(q3)
    string += "Max: {:.4} \n".format(maximum)
    string += "Outliers: {}".format(outliers)
    return string


def main():
    spaten, heineken = extrair_dados()

    print("# ESTATÍSTICAS SPATEN:")
    print(valor_central(spaten))
    print(dispersao(spaten))
    print(forma(spaten))
    print(boxplot_dados(spaten))
    print()

    print("# ESTATÍSTICAS HEINEKEN:")
    print(valor_central(heineken))
    print(dispersao(heineken))
    print(forma(heineken))
    print(boxplot_dados(heineken))
    print()

    histograma_cervejas(spaten, heineken)
    boxplot_cervejas(spaten, heineken)


if __name__ == "__main__":
    main()
