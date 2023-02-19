import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numbers import Number
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
        string += "Tamanho {} \n".format(self.tamanho())
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

    segmentos = tabela["Seg"]
    marcas = tabela["Marca"]
    latinha_350 = tabela["C16 - LATA – 350 ml"]

    spaten_geral = Dados()
    spaten_as = Dados()
    spaten_mf = Dados()
    spaten_mt = Dados()

    heineken_geral = Dados()
    heineken_as = Dados()
    heineken_mf = Dados()
    heineken_mt = Dados()

    for segmento, marca, preco in zip(segmentos, marcas, latinha_350):
        # não, isso não é o mesmo que preco <= 0
        if not preco > 0:
            continue
        
        if marca == "SPATEN":
            spaten_geral.append(preco)
            if segmento == 1:
                spaten_as.append(preco)
            elif segmento == 2:
                spaten_mf.append(preco)
            elif segmento == 3:
                spaten_mt.append(preco)

        elif marca == "HEINEKEN":
            heineken_geral.append(preco)
            if segmento == 1:
                heineken_as.append(preco)
            elif segmento == 2:
                heineken_mf.append(preco)
            elif segmento == 3:
                heineken_mt.append(preco)

    # desculpe deus por esta aberração
    return spaten_geral, spaten_as, spaten_mf, spaten_mt, heineken_geral, heineken_as, heineken_mf, heineken_mt


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


def boxplot_segmentos(spaten_as, spaten_mf, spaten_mt, heineken_as, heineken_mf, heineken_mt):
    fig, (spaten, heineken) = plt.subplots(2, 3, sharex=True, sharey=True)
    fig.suptitle("Preços por latas de 350 ml")

    spaten_ax_as, spaten_ax_mf, spaten_ax_mt = spaten 
    heineken_ax_as, heineken_ax_mf, heineken_ax_mt = heineken

    spaten_ax_as.boxplot(spaten_as, patch_artist=True)
    spaten_ax_mf.boxplot(spaten_mf, patch_artist=True)
    spaten_ax_mt.boxplot(spaten_mt, patch_artist=True)

    heineken_ax_as.boxplot(heineken_as, patch_artist=True)
    heineken_ax_mf.boxplot(heineken_mf, patch_artist=True)
    heineken_ax_mt.boxplot(heineken_mt, patch_artist=True)

    spaten_ax_as.set_title("Spaten Auto-Serviço")
    spaten_ax_mf.set_title("Spaten Mercado Frio")
    spaten_ax_mt.set_title("Spaten Mercado Tradicional")

    heineken_ax_as.set_title("Heineken Auto-Serviço")
    heineken_ax_mf.set_title("Heineken Mercado Frio")
    heineken_ax_mt.set_title("Heineken Mercado Tradicional")

    plt.show()


# desculpe deus por esta aberração²
def analise_exploratoria():
    spaten_geral, spaten_as, spaten_mf, spaten_mt, heineken_geral, heineken_as, heineken_mf, heineken_mt = extrair_dados()

    print(len(spaten_geral), sum(spaten_geral))
    print(len(heineken_geral), sum(heineken_geral))

    print("# ESTATÍSTICAS SPATEN:")
    print(spaten_geral)

    print("# ESTATÍSTICAS HEINEKEN:")
    print(heineken_geral)

    histograma_cervejas(spaten_geral, heineken_geral)
    boxplot_cervejas(spaten_geral, heineken_geral)
    boxplot_segmentos(spaten_as, spaten_mf, spaten_mt, heineken_as, heineken_mf, heineken_mt)

def gaussiana(x, media, desvio_padrao):
    multi = 1 / (desvio_padrao * np.sqrt(np.pi * 2))
    power = - (x - media)**2 / (2 * desvio_padrao**2)
    return multi * np.e ** power

def dados_histograma(array):
    minimo = np.min(array)
    maximo = np.max(array)
    intervalo = maximo - minimo
    n_classes = int(np.sqrt(len(array)))
    amplitude = intervalo / n_classes

    classes = [0 for i in range(n_classes)]
    for i in array:
        indice = int((i - minimo) / amplitude)

        if indice >= n_classes:
            indice = n_classes - 1
        classes[indice] += 1        
    
    valores = [i for i in np.arange(minimo, maximo, amplitude)]

    return valores, classes
    

def histograma_simples(array):
    classes = int(np.sqrt(len(array)))  
    plt.hist(array, classes)
    plt.show()

def teste_aderencia(dados):
    x, y = dados_histograma(dados)
    plt.fill_between(x,y, color="red", step="pre", alpha=0.4)

    print(x)
    print(y)

    # m = len(dados)
    # gauss_x = np.arange(np.min(dados), np.max(dados), 0.01)
    # gauss_y = [gaussiana(i, dados.media(), dados.desvio_padrao()) * m for i in gauss_x]
    # plt.plot(gauss_x, gauss_y)

    plt.show()


def main():
    spaten_geral, spaten_as, spaten_mf, spaten_mt, heineken_geral, heineken_as, heineken_mf, heineken_mt = extrair_dados()
    # print(spaten_geral)
    # print(heineken_geral)
    # a = spaten_geral
    a = heineken_geral
    print(a)

    # a = np.random.rand(100)
    # for i in range(1000):
    #     a += np.random.rand(100)
    # a = Dados(a)

    # print(a)
    teste_aderencia(a)


    # a = np.random.rand(64)
    # a = Dados(a)
    # print(a)
    # teste_aderencia(a)

    # histograma_simples(a)

if __name__ == "__main__":
    main()
    # analise_exploratoria()
