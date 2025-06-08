#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    char *input = argv[1];
    char *output = argv[2];
    float factor = atof(argv[3]);

    FILE *inptr = fopen(input, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", input);
        return 1;
    }

    FILE *outptr = fopen(output, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", output);
        return 1;
    }

    BYTE header[44];
    fread(header, sizeof(BYTE), 44, inptr);
    fwrite(header, sizeof(BYTE), 44, outptr);

    int16_t buffer;
    while (fread(&buffer, sizeof(int16_t), 1, inptr) == 1)
    {
        buffer = buffer * factor;
        fwrite(&buffer, sizeof(int16_t), 1, outptr);
    }

    fclose(inptr);
    fclose(outptr);

    return 0;
}
