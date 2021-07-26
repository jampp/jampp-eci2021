# Code Golf Challenge - Core Team

## Consigna

Llamaremos mensajes **unarios**, aquellos que solo están compuestos por el carácter **0**. El objetivo es escribir un programa en Python que sea capas de transformar un mensaje en esta codificación utilizando la **menor cantidad de caracteres posible**.

Las reglas de codificación son:

- La entrada consiste en caracteres ASCII (7-bits).
- El mensaje codificado de salida consiste en bloques de 0s.
- Cada bloque de 0s es separado de otro bloques por un espacio.
- Dos bloques consecutivos son utilizados para producir una series de valores con el mismo bit (0 o 1):
   - Primer Bloque: es siempre **0** o **00**. Si es **0**, entonces la serie contiene 1s, sino, contiene 0s.
   - Segundo Bloque: el número de 0s de este bloque representa la cantidad de bits en la serie.

Primer ejemplo: *C* (**1000011**)

- **0 0** (corresponde al primer **1**)
- **00 0000** (corresponden a los cuatro **0** consecutivos).
- **0 00** (consiste al último par de **1**s)

El mensaje codificado sería: **0 0 00 0000 0 00**

Segundo ejemplo: *CC* (**10000111000011**)

- **0 0** (un simple **1**)
- **00 0000** (cuatro **0**s)
- **0 000** (tres **1**s)
- **00 0000** (cuatro **0**s)
- **0 00** (dos **1**s)

El mensaje codificado sería: **0 0 00 0000 0 000 00 0000 0 00**

## Reglas

- El input será una cadena de N caracteres ASCII (sin fin de línea).
- Restricciones: 0 < N < 100
- Escribir un programa compatible con Python 3.7.
- La solución deberá ser 100% Python, no se aceptarán solución que combinen otro lenguaje/comando.
- **El programa con menor cantidad de caracteres será el ganador (en caso de empate, el enviado primero)**.
- Se pueden entregar varias soluciones por persona (solo se considerará la mejor).
- La tabla de resultados parcial se publicarán todos los días a las 19hs en el siguiente link: https://share.geckoboard.com/dashboards/WK7QXYNUBY5OZNIE.
- Al finalizar la competencia, publicaremos las mejores 3 soluciones.
- [test_solution.py](https://github.com/jampp/jampp-eci2021/blob/master/Challenges/Code%20Golf%20Challenge%20-%20Core%20Team/test_solution.py) Script para testear la solución y obtener su puntaje.
- Subir solo el archivo .py
- Se aceptarán soluciones hasta el **viernes 30/07/2021 a las 12hs**.

Ejemplo:

- Input: *C*
- Output: **0 0 00 0000 0 00**

## Carga de soluciones

https://forms.gle/xR6JgDgugXvgNcjB7
