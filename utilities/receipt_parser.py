from os import listdir

import re

REGISTER_TRANSACTION_PATTERN = "Reg\s#"


def write_lines_to_file(lines, filename):
    with open(filename, 'w+') as file:
        for line in lines:
            file.write("{}\n".format(line))


def main():
    transaction_number = ""
    filenames = listdir('legitimate_receipts/')
    register_transaction_pattern = re.compile(REGISTER_TRANSACTION_PATTERN)
    for filename in filenames:
        legit_filename = "legitimate_receipts/{}".format(filename)
        with open(legit_filename) as legit_file:
            restart_receipt = False
            lines = []
            for line in legit_file:
                line_stripped = line.lstrip().rstrip()
                if register_transaction_pattern.match(line_stripped):
                    line_split = line_stripped.split(' ')
                    transaction_number = line_split[9][1:-1]
                    restart_receipt = True
                lines.append(line)
                if restart_receipt:
                    write_lines_to_file(lines, "legitimate_receipts\{}.txt".format(transaction_number))
                    lines = []
                    restart_receipt = False


if __name__ == '__main__':
    main()
