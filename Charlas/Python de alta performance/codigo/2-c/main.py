# -*- coding: utf-8 -*-

import sys
from ctypes import *

fun = CDLL("/home/vpaz/workspace/ECI-2021/2-c/levenshtein.so")


def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as input_file:
            file_content = input_file.readlines()
            file_content = map(lambda line: line.strip(), file_content)
            do_logic_file(file_content)
    else:
        string1 = create_string_buffer(bytes(sys.argv[1], "ascii"))
        string2 = create_string_buffer(bytes(sys.argv[2], "ascii"))
        l = fun.levenshtein(string1, string2)
        print(l)


def do_logic_file(file_content, print_=False):
    L = [input_line.strip().split(",") for input_line in file_content]
    for i in range(100):
        for string1, string2 in L:
            string1 = create_string_buffer(bytes(string1, "ascii"))
            string2 = create_string_buffer(bytes(string2, "ascii"))
            l = fun.levenshtein(string1, string2)
            if print_:
                print(l)


if __name__ == "__main__":
    main()
