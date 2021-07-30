#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MIN3(a, b, c) ((a) < (b) ? ((a) < (c) ? (a) : (c)) : ((b) < (c) ? (b) : (c)))

#define MAX_NUMBER_OF_LINES_IN_FILE 1000000
#define MAX_LINE_LENGTH 256
#define PRINT_OUTPUT 0

int main(int argc, char *argv[])
{

    int i = 0;

    char const *const fileName = argv[1]; /* should check that argc > 1 */
    char **file_content = (char **)malloc(sizeof(char *) * MAX_NUMBER_OF_LINES_IN_FILE);
    FILE *file = fopen(fileName, "r"); /* should check the result */

    for (i = 0; 1; i++)
    {
        file_content[i] = malloc(MAX_LINE_LENGTH);
        if (fgets(file_content[i], MAX_LINE_LENGTH - 1, file) == NULL)
            break;

        /* Get rid of CR or LF at end of line */
        int j = 0;
        for (j = strlen(file_content[i]) - 1; j >= 0 && (file_content[i][j] == '\n' || file_content[i][j] == '\r'); j--)
        {
            i;
        }
        file_content[i][j + 1] = '\0';
    }
    fclose(file);

    for (int j = 0; j < 100; j++)
        do_logic(file_content, i);

    return 0;
}

int do_logic(char **file_content, int max_lines)
{

    char *str1, *str2, *token;
    char *line_content;
    char *saveptr1;
    int i = 0;
    for (i = 0; i < max_lines; i++)
    {
        int first = 1;
        for (line_content = file_content[i];; line_content = NULL)
        {
            token = strtok_r(line_content, ",", &saveptr1);
            if (token == NULL)
                break;
            if (first == 1)
                str1 = token;
            else
                str2 = token;
            first = 0;
        }
        if (PRINT_OUTPUT == 1)
            printf("%s %s %d\n", str1, str2, levenshtein(str1, str2));
        else levenshtein(str1, str2);
    }
    return 1;
}

// taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#C
int levenshtein(char *A, char *B)
{
    unsigned int i, j, lenA, lenB;
    lenA = strlen(A);
    lenB = strlen(B);

    unsigned int** matriz = (unsigned int **)malloc((lenA + 1) * sizeof(unsigned int *));
    for (i = 0; i < lenA + 1; i++) {
        matriz[i] = (unsigned int *)malloc((lenB + 1) * sizeof(unsigned int));
        matriz[i][0] = i;
    }

    for (j = 1; j < lenB + 1; j++)
        matriz[0][j] = j;

    for (i = 1; i < lenA + 1; i++)
        for (j = 1; j < lenB + 1; j++)
            matriz[i][j] = MIN3(
                matriz[i - 1][j] + 1,
                matriz[i][j - 1] + 1,
                matriz[i - 1][j - 1] + (A[i - 1] == B[j - 1] ? 0 : 1));

    unsigned int res = matriz[lenA][lenB];

    for (i = 0; i < lenA; i++)
        free(matriz[i]);
    free(matriz);

    return (res);
}