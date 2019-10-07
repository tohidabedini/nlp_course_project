from __future__ import unicode_literals
from hazm import *
import copy
from persian_wordcloud.wordcloud import PersianWordCloud, add_stop_words
import arabic_reshaper
from bidi.algorithm import get_display

f1_processed = open('../../ProcessedData/label1.txt', 'r', encoding="utf-8")
f2_processed = open('../../ProcessedData/label2.txt', 'r', encoding="utf-8")


def input_full_tokenizer(input):
    out_list = []
    # counter = 0
    for line in input:
        for i in word_tokenize(line):
            out_list.append(i)
            # out_list[counter] = i
            # counter += 1
    return out_list


out_1 = input_full_tokenizer(f1_processed)
out_2 = input_full_tokenizer(f2_processed)


def frequency_finder(input):
    frequencies = {}
    for word in input:
        if word not in frequencies:
            frequencies[word] = 0
        frequencies[word] += 1
    return frequencies


def relative_normal_freq(input, relative, normal):
    output = copy.deepcopy(input)
    if normal == 1:
        min_value = abs(output[min(output, key=output.get)])
        for i in output:
            output[i] += min_value

    if relative == 1:
        max_value = output[max(output, key=output.get)]
        for i in output:
            output[i] /= max_value
    return output


freq_1 = frequency_finder(out_1)
freq_2 = frequency_finder(out_2)


def freq_subtracted(first_in, second_in):
    first = copy.deepcopy(first_in)
    second = copy.deepcopy(second_in)
    for word in first:
        if word in second:
            first[word] -= second[word]
    return first


freq_just_1 = freq_subtracted(freq_1, freq_2)
freq_just_2 = freq_subtracted(freq_2, freq_1)

stop_words_file = open('../stopwords.txt', 'r', encoding="utf-8")


def file_to_list(input):
    out = []
    for line in input:
        out.append(line[:-1])
    return out


stop_words = file_to_list(stop_words_file)


def stop_words_deleter(stop_words, input):
    output = copy.deepcopy(input)
    for i in stop_words:
        if i in output:
            del output[i]
    return output


def text_reshaper(input):
    output = {}
    for i, j in input.items():
        output[get_display(arabic_reshaper.reshape(i))] = j
    return output


freq_1_rel = text_reshaper(relative_normal_freq(freq_1, 1, 0))
freq_2_rel = text_reshaper(relative_normal_freq(freq_2, 1, 0))

freq_just_1_normal_relative = text_reshaper(relative_normal_freq(freq_just_1, 1, 1))
freq_just_2_normal_relative = text_reshaper(relative_normal_freq(freq_just_2, 1, 1))

freq_1_rel_stop = text_reshaper(relative_normal_freq(stop_words_deleter(stop_words, freq_1), 1, 0))
freq_2_rel_stop = text_reshaper(relative_normal_freq(stop_words_deleter(stop_words, freq_2), 1, 0))

freq_just_1_normal_relative_stop = text_reshaper(relative_normal_freq(stop_words_deleter(stop_words, freq_just_1), 1, 1))
freq_just_2_normal_relative_stop = text_reshaper(relative_normal_freq(stop_words_deleter(stop_words, freq_just_2), 1, 1))


def word_cloud_generator(input, name):
    wordcloud = PersianWordCloud(
        only_persian=True,
        max_words=100,
        stopwords=stop_words,
        margin=0,
        width=800,
        height=800,
        min_font_size=1,
        max_font_size=500,
        background_color="black"
    ).generate_from_frequencies(input)

    image = wordcloud.to_image()
    # image.show()
    image.save("../out/"+name+'.png')


word_cloud_generator(freq_1_rel, "1")
word_cloud_generator(freq_2_rel, "2")

word_cloud_generator(freq_just_1_normal_relative, "3")
word_cloud_generator(freq_just_2_normal_relative, "4")

word_cloud_generator(freq_1_rel_stop, "5")
word_cloud_generator(freq_2_rel_stop, "6")

word_cloud_generator(freq_just_1_normal_relative_stop, "7")
word_cloud_generator(freq_just_2_normal_relative_stop, "8")
