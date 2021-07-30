# -*- coding: utf-8 -*-
import cython

@cython.locals(
    A=str,
    B=str,
    largo_A=int,
    largo_B=int,
    matriz=list,
    i=int,
    j=int,
    costo_de_sustitucion=int,
)
def levenshtein(A, B):
    largo_A = len(A)
    largo_B = len(B)

    matriz = [[0] * (largo_B + 1) for _ in range(largo_A + 1)]

    for i in range(largo_A + 1):
        matriz[i][0] = i
    for j in range(largo_B + 1):
        matriz[0][j] = j

    for i in range(1, largo_A + 1):
        for j in range(1, largo_B + 1):

            if A[i - 1] == B[j - 1]:
                costo_de_sustitucion = 0
            else:
                costo_de_sustitucion = 1

            matriz[i][j] = min(
                matriz[i - 1][j - 1] + costo_de_sustitucion,
                matriz[i - 1][j] + 1,
                matriz[i][j - 1] + 1,
            )

    return matriz[largo_A][largo_B]