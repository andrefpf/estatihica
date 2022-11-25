import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


class Dados(list):
    def tamanho(self):
        return len(self)

    def media(self):
        return sum(self) / len(self)

    def mediana(self):
        half = len(self) // 2
        return sorted(self)[half]

    def moda(self):
        counter = defaultdict(lambda: 0)
        # talvez precise quebrar em grupinhos
        for i in self:
            counter[i] += 1
        repetitions = lambda x: counter[x]
        return max(self, key=repetitions)

    def variancia(self):
        media_ = self.media()
        sum_ = 0
        for i in self:
            sum_ += (i - media_) ** 2
        return sum_ / len(self)

    def desvio_padrao(self):
        return np.sqrt(self.variancia())

    def erro_padrao(self):
        return self.desvio_padrao() / np.sqrt(len(self))

    def coeficiente_variacao(self):
        return self.desvio_padrao() / self.media() * 100

    def quartis_1(self):
        half = len(self) // 2
        array = sorted(self)[:half]
        return Dados(array).mediana()

    def quartis_3(self):
        half = len(self) // 2
        array = sorted(self)[half:]
        return Dados(array).mediana()

    def assimetria(self):
        a = self.quartis_3() + self.quartis_1() - 2 * self.mediana()
        b = self.quartis_3() - self.quartis_1()
        return a / b

    def curtose(self):
        return 0.0

    def box_info(self):
        q1 = self.quartis_1()
        q3 = self.quartis_3()

        iqr = q3 - q1
        minimum = q1 - iqr * 1.5
        maximum = q3 + iqr * 1.5

        extreme_max = q1 - iqr * 3
        extreme_min = q3 + iqr * 3

        ok = set()
        outliers = set()
        extreme = set()
        for i in self:
            if minimum < i < maximum:
                ok.add(i)
            elif extreme_min < i < extreme_max:
                outliers.add(i)
            else:
                extreme.add(i)

        minimum = min(ok)
        maximum = max(ok)
        return minimum, maximum, outliers, extreme

    def __str__(self):
        minimum, maximum, outliers, extreme = self.box_info()

        string = ""
        string += "Tamanho da amostra {} \n".format(len(self))
        string += "Média:   {:.4} \n".format(self.media())
        string += "Mediana: {:.4} \n".format(self.mediana())
        string += "Moda:    {:.4} \n".format(self.moda())
        string += "Assimetria:  {:.4} \n".format(self.assimetria())
        string += "Curtose:     {:.4} \n".format(self.curtose())
        string += "Variância:       {:.4} \n".format(self.variancia())
        string += "Desvio padrão:   {:.4} \n".format(self.desvio_padrao())
        string += "Erro padrão:     {:.4} \n".format(self.erro_padrao())
        string += "Coeficiente de variação: {:.4} \n".format(
            self.coeficiente_variacao()
        )
        string += "Qi: {:.4} \n".format(self.quartis_1())
        string += "Qs: {:.4} \n".format(self.quartis_3())
        string += "Mínimo: {:.4} \n".format(minimum)
        string += "Máximo: {:.4} \n".format(maximum)
        string += "Outliers: {} \n".format(outliers)
        string += "Outliers Extremos: {} \n".format(extreme)
        return string


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

    return Dados(spaten), Dados(heineken)


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


def main():
    spaten, heineken = extrair_dados()

    print("# ESTATÍSTICAS SPATEN:")
    print(spaten)

    print("# ESTATÍSTICAS HEINEKEN:")
    print(heineken)

    histograma_cervejas(spaten, heineken)
    boxplot_cervejas(spaten, heineken)


if __name__ == "__main__":
    main()
