import numpy as np

fun_salarios = [1066.38, 1281.140, 1495.9, 1710.66, 1925.42]
fun_pesos = [14, 10, 3, 2, 1]

sup_salarios = [2812.033, 4969.1, 7126.167, 9283.233, 11440.3, 13597.367]
sup_pesos = [5, 15, 8, 3, 3, 2]

def media(x, p):
	s = 0
	pesos = sum(p)
	assert len(x) == len(p)

	for i, j in zip(x, p):
		s += i*j
	return s / pesos

def desvio(x, p):
	s = 0
	m = media(x, p)
	pesos = sum(p)

	for i, j in zip(x, p):
		s += (i - m)**2 * j
	s /= pesos
	return np.sqrt(s)

def variacao(x, p):
	return desvio(x, p) / media(x, p)

def assimetria(x, p):
	return (media(x, p) - moda(x, p)) / desvio(x, p)

def erro_padrao(x, p):
	pesos = sum(p)
	return desvio(x, p) / np.sqrt(pesos)

def moda(x, p):
	a = {i:j for i, j in zip(x, p)}
	return max(x, key=a.get)



print("fundamental")
print("media:", media(fun_salarios, fun_pesos))
print("desvio:", desvio(fun_salarios, fun_pesos))
print("variação:", variacao(fun_salarios, fun_pesos))
print("assimetria:", assimetria(fun_salarios, fun_pesos))
print("erro:", erro_padrao(fun_salarios, fun_pesos))
print("moda:", moda(fun_salarios, fun_pesos))

print()

print("superior")
print("media:", media(sup_salarios, sup_pesos))
print("desvio:", desvio(sup_salarios, sup_pesos))
print("variação:", variacao(sup_salarios, sup_pesos))
print("assimetria:", assimetria(sup_salarios, sup_pesos))
print("erro:", erro_padrao(sup_salarios, sup_pesos))
print("moda:", moda(sup_salarios, sup_pesos))
