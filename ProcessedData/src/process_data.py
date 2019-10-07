from __future__ import unicode_literals
from hazm import *

# normalizer.normalize()
# sent_tokenize()
# word_tokenize()
ignore_list = ["،", "»", "«", "؟", "!", "."]

f1_processed = open('../label1.txt', 'w', encoding="utf-8")
f1_data = open('../../Data/label1.txt', 'r', encoding="utf-8")

f2_processed = open('../label2.txt', 'w', encoding="utf-8")
f2_data = open('../../Data/label2.txt', 'r', encoding="utf-8")


def data_processor(input_file, output_file, ignore_list, mode):
    normalizer = Normalizer()
    for line in input_file:
        line = line.replace("خواهی","خواهی_،")
        # print(word_tokenize(line))
        # print(word_tokenize(normalizer.normalize(line)))
        for i in word_tokenize(normalizer.normalize(line)):
            # i = i.translate({ord('،'): None})
            # i = i.translate({ord('_'): None})
            if i in ignore_list:
                continue
            if mode == 0:
                output_file.write(i+"\n")
            elif mode == 1:
                output_file.write(i + " ")
        if mode == 1:
            output_file.write("\n")
    input_file.close()


data_processor(f2_data, f2_processed, ignore_list, 1)
data_processor(f1_data, f1_processed, ignore_list, 1)
