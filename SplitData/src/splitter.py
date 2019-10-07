import random


def random_generator(start, stop):
    return random.randint(start, stop+1)


def random_list_generator(size, start, stop):
    out = []
    while len(out) < size:
        new = random_generator(start, stop)
        if new in out:
            continue
        else:
            out.append(new)
    return out


def file_line_counter(input):
    counter = 0
    for line in input:
        counter += 1
    return counter


def random_list_make_suitable(input):
    output_1 = [i * 2 for i in input]
    output_2 = []
    for i in output_1:
        output_2.append(i-1)
        output_2.append(i)
    return output_2


input_file_1 = open('../../ProcessedData/label1.txt', 'r', encoding="utf-8")
lines_1 = file_line_counter(input_file_1)
input_file_1.close()

input_file_2 = open('../../ProcessedData/label2.txt', 'r', encoding="utf-8")
lines_2 = file_line_counter(input_file_2)
input_file_2.close()


def file_splitter(input_dir, output_dir, percentage_of_train, lines):
    input_file = open(input_dir, 'r', encoding="utf-8")
    # print(lines)
    lines = int(lines/2)
    # print(lines)
    splitted_file_test = open("../test/"+output_dir, 'w', encoding="utf-8")
    splitted_file_train = open("../train/"+output_dir, 'w', encoding="utf-8")
    line_percentage = int(lines*(percentage_of_train/100))
    # print(line_percentage)
    list = random_list_make_suitable(random_list_generator(line_percentage, 1, lines))
    # print(list)
    # print(len(list))
    counter = 0
    for line in input_file:
        # print(counter)
        # print(line)
        counter += 1
        if counter in list:
            splitted_file_test.write(line)
        else:
            splitted_file_train.write(line)
    splitted_file_test.close()
    splitted_file_train.close()
    input_file.close()


file_splitter('../../ProcessedData/label1.txt', 'label1.txt', 20, lines_1)
file_splitter('../../ProcessedData/label2.txt', 'label2.txt', 20, lines_2)

