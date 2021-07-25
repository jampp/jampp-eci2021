#!/usr/bin/env python3.7
from subprocess import run, PIPE
import sys

# Modo de uso: python3.7 runner.py SOLUCION.py

TESTS = {
    r'C': '0 0 00 0000 0 00',
    r'CC': '0 0 00 0000 0 000 00 0000 0 00',
    r'%': '00 0 0 0 00 00 0 0 00 0 0 0',
    r'abcdefghijklmnopqrstuvwxyz': '0 00 00 0000 0 000 00 000 0 0 00 0 0 00 00 000 0 0000 00 00 0 0 00 00 0 00 00 00 0 0 00 0 0 000 00 00 0 00 00 0 0 00 00 00 0 00000 00 0 0 0 00 000 0 00 00 0 0 0 00 00 0 000 00 0 0 0 00 0 0 0 00 0 0 00 00 0 0 0 00 0 0 0000 00 0 0 00 00 00 0 00 00 0 0 00 00 0 0 000 00 0 0 000 00 0 0 00 00 0 0 0000000 00 0000 0 000 00 000 0 0000 00 00 0 0 00 0 0 000 00 00 0 00000 00 0 0 0 00 00 0 000 00 0 0 0 00 0 0 0000 00 0 0 00 00 0 0 000 00 0 0 0000000 00 000 0 0000 00 00 0 00000 00 0 0 0 00 0',
    r'!"#$&': '00 0 0 0 00 0000 0 0 00 0 0 0 00 000 0 0 00 00 0 0 00 000 0 00 00 0 0 0 00 00 0 0 00 000 0 0 00 00 0 00 00 0',
    r'&a$z%e*r-t+y?y.u:i=o)p': '00 0 0 0 00 00 0 00 00 0 0 00 00 0000 0 0 00 0 0 0 00 00 0 0 00 00 0 0000 00 0 0 0 00 00 0 0 00 00 0 0 00 0 0 000 00 00 0 0 00 0 0 0 00 0 0 0 00 0 0 0 00 0 0 0 00 0 0 000 00 00 0 0 00 00 0 0 00 0 0 00 00 0 0 0000 00 0 0 0 00 000 0 0 00 0 0 0 00 0 0 000000 00 00 0 0 00 0 0 0000000000 00 00 0 0 00 0 0 0 00 0 0 000 00 0 0 000 00 0 0 0 00 0 0 0 00 0 0 000 00 0 0 0 00 0 0 00 00 0 0 0 00 00 0 0 00 0 0 0000 00 0 0 000 00 0 0 0000 00 0 0 0 00 0 0 0 00 00 0 0000 00 0000',
    r'AaBbCcDdEeFf': '0 0 00 00000 0 000 00 0000 0 00 00 0000 0 0 00 0 0 00 00 000 0 0 00 0 0 0 00 0000 0 0000 00 000 0 000 00 000 0 0 00 00 0 00 00 00 0 0 00 00 0 0 00 000 0 0 00 0 0 000 00 00 0 0 00 0 0 00 00 000 0 00 00 0 0 00 00 00 0 00 00 0',
    r'Bienvenido a la ECI 2021!': '0 0 00 0000 0 0 00 0 0 00 00 0 0 0 00 00 0 000 00 00 0 0 00 0 0 000 00 0 0 000 00 0 0 000 00 0 0 00 00 0 0 00 00 00 0 0 00 0 0 000 00 0 0 000 00 0 0 00 00 0 0 0 00 00 0 000 00 00 0 0 00 00 0 00 00 0 0 0000 00 0 0 0 00 00000 0 00 00 0000 0 0 00 0 0 0 00 00000 0 00 00 0 0 00 00 00 0 00 00 0000 0 0 00 0 0 0 00 00000 0 0 00 000 0 0 00 0 0 00 00 0000 0 000 00 00 0 0 00 00 0 0 00 0 0 0 00 000000 0 00 00 00 0 0 00 00 0 00 00 00000 0 00 00 00 0 0 00 00 0 00 00 000 0 0 00 0 0 0 00 0000 0 0',
    r'**We are hiring**': '00 0 0 0 00 0 0 0 00 0 0 0 00 00 0 0 00 0 0 0 00 0 0 0 00 0 0 0 00 0 0 0 00 0 0 00000 00 00 0 0 00 0 0 0 00 0 0 0 00 00000 0 00 00 0000 0 0000 00 00 0 0 00 0 0 00 00 00 0 0 00 0 0 0 00 0 0 0 00 00000 0 00 00 0 0 0 00 000 0 00 00 0 0 0 00 00 0 0000 00 00 0 0 00 0 0 00 00 0 0 0 00 00 0 000 00 0 0 000 00 0 0 00 00 00 0 000 00 0 0 0 00 0 0 0 00 0 0 0 00 00 0 0 00 0 0 0 00 0 0 0 00 0',
}

ok = True
for t, e in TESTS.items():
    p = run(['python3.7', sys.argv[1]],
        stdout=PIPE,
        input=t, encoding='ascii'
    )
    if p.returncode != 0:
        print("ERROR on test '{}'".format(t))
        ok = False
        break

    output = p.stdout.rstrip()
    if output != e:
        print("FAIL on test '{}', expected_output: '{}' output: '{}'".format(t, e, output))
        ok = False
        break

    print ("PASS test: '{}'".format(t))

if ok:
    code_len = 0
    with open(sys.argv[1], 'r') as fh:
        code_len = len(fh.read())
    print("PASS ALL TESTS!\n\nCODE LENGTH {}".format(code_len))
else:
    print("ERROR")

