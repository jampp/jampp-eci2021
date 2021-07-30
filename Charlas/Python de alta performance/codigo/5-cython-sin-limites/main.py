# -*- coding: utf-8 -*-

import sys
import array
from difference import levenshtein


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
