import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    database = []
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            database.append(row)

    with open(sys.argv[2], "r") as file:
        dna = file.read()

    str_counts = {}
    str_sequences = list(database[0].keys())[1:]
    for STR in str_sequences:
        str_counts[STR] = longest_match(dna, STR)

    for person in database:
        match = True
        for STR in str_sequences:
            if int(person[STR]) != str_counts[STR]:
                match = False
                break
        if match:
            print(person["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    longest_run = 0
    subseq_len = len(subsequence)
    seq_len = len(sequence)

    for i in range(seq_len):
        count = 0
        while True:
            start = i + count * subseq_len
            end = start + subseq_len
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()
