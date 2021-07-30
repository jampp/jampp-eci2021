# -*- coding: utf-8 -*-

import sys


def levenshtein(A, B):
    largo_A = len(A)
    largo_B = len(B)

    # matriz[i][j] = distancia entre A[0:i) y B[0:j)
    matriz = [[0] * (largo_B + 1) for _ in range(largo_A + 1)]

    # cadenas de largo cero
    for i in range(largo_A + 1):
        matriz[i][0] = i
    for j in range(largo_B + 1):
        matriz[0][j] = j

    # se suma 1 por la cadena de longitud 0 que contemplamos arriba
    for i in range(1, largo_A + 1):
        for j in range(1, largo_B + 1):

            # comparo el lugar de A que corresponde con |A[0:i)| = i - 1 contra
            # el lugar de B que corresponde con |B[0:j)| = j - 1
            if A[i - 1] == B[j - 1]:
                costo_de_sustitucion = 0
            else:
                costo_de_sustitucion = 1

            matriz[i][j] = min(
                # sustitucion de algun caracter (o no)
                matriz[i - 1][j - 1] + costo_de_sustitucion,

                # eliminacion sobre A, no usa el caracter A[i - 1] de la cadena A[0:i)
                # corresponde a no usar la cadena A[0:i) pero si A[0:i-1)
                # en ambos casos contra B[0:j)
                matriz[i - 1][j] + 1,

                # insercion sobre A, poner el caracter B[j - 1] al final de la cadena A[0:i)
                # resultando de la cadena A[0:i+1) = A[0:i) + B[j - 1]
                # corresponde a comparar la cadena A[0:i) con B[0:j - 1) porque la cadena B[0:j)
                # la usamos para poner B[j - 1] en A
                matriz[i][j - 1] + 1,
            )

    return matriz[largo_A][largo_B]


def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as input_file:
            file_content = input_file.readlines()
            file_content = map(lambda line: line.strip(), file_content)
            do_logic_file(file_content)
    else:
        l = levenshtein(sys.argv[1], sys.argv[2])
        print(l)


def do_logic_file(file_content, print_=False):
    L = [input_line.strip().split(",") for input_line in file_content]
    for i in range(100):
        for string1, string2 in L:
            l = levenshtein(string1, string2)
            if print_:
                print(l)


if __name__ == "__main__":
    main()
