from hazm import *

dir1 = "../../SplitData/train/label1.txt"
dir2 = "../../SplitData/train/label2.txt"


def file_to_list(input_dir):
    f_in = open(input_dir, 'r', encoding="utf-8")
    sentences = []
    for line in f_in:
        if line[-1] == "\n":
            sentences.append("<s> " + line[:-1] + " </s>")
        else:
            sentences.append("<s> " + line + " </s>")
    f_in.close()
    return sentences


def input_full_tokenizer(input_dir, mode):
    f_in = open(input_dir, 'r', encoding="utf-8")
    out_list = []
    for line in f_in:
        if mode == 0:
            for i in word_tokenize(line):
                out_list.append(i)
        else:
            if line[-1] == "\n":
                for i in word_tokenize("<s> " + line[:-1] + " </s>"):
                    out_list.append(i)
            else:
                for i in word_tokenize("<s> " + line + " </s>"):
                    out_list.append(i)

    f_in.close()
    return out_list


def frequency_finder(input, gram_num, vocab_len):
    frequencies = {}
    for word in input:
        if word not in frequencies:
            frequencies[word] = 0
        frequencies[word] += 1
    if gram_num > 1:
        frequencies["UNK"] = 1 / vocab_len
    return frequencies


def unigram_writer(freq_in, dest_dir, n):
    v = len(freq_in)
    label_1gram_lm = open(dest_dir, 'w', encoding="utf-8")
    for i, j in freq_in.items():
        p = (j+1)/(v+n+1)
        a = str(i) + "|" + str(format(p, "0.4f"))+"\n"
        label_1gram_lm.write(a)
    label_1gram_lm.close()


def unigram_generator(src_dir, dest_dir):
    out = input_full_tokenizer(src_dir, 0)
    n = len(out)
    unigram_writer(frequency_finder(out,1,0), dest_dir, n)


# unigram_generator(dir1, "../label1.1gram.lm")
# unigram_generator(dir2, "../label2.1gram.lm")
# unigram_generator("../test/in.1gram", "../test/out.1gram.lm")


def line_bigram_generator(input):
    temp = []
    for i in range(len(input)-1):
        sample = []
        sample.append(input[i])
        sample.append(input[i+1])
        temp.append(sample)

    return temp


def make_file_suitable(input_dir):
    temp = file_to_list(input_dir)
    total_bigrams_of_file = []
    counter = 0
    for i in temp:
        line = line_bigram_generator(temp[counter].split())
        for j in line:
            total_bigrams_of_file.append(tuple(j))
        counter += 1
    return total_bigrams_of_file  # , s_total_bigrams_of_file


def bigram_writer(freq_in, dest_dir, v, n_calc):
    label_2gram_lm = open(dest_dir, 'w', encoding="utf-8")
    for i, j in freq_in.items():
        if i[0] in n_calc:
            n = n_calc[i[0]]
        else:
            n = n_calc["UNK"]
        p = (j+1)/(v+n+1)
        if i != "UNK":
            a = str(i[0] + "|" + i[1]) + "|" + str(format(p, "0.4f"))+"\n"
            label_2gram_lm.write(a)
    label_2gram_lm.close()


def bigram_generator(src_dir, dest_dir):
    v = len(frequency_finder(input_full_tokenizer(src_dir, 0),1, 0))
    t = make_file_suitable(src_dir)
    # n = len(s_t)
    # print(t[0][0])
    n_calc = frequency_finder(input_full_tokenizer(src_dir, 1), 2, v)
    bigram_writer(frequency_finder(t,2,v), dest_dir, v, n_calc)


# bigram_generator(dir1, "../label1.2gram.lm")
# bigram_generator(dir2, "../label2.2gram.lm")
# bigram_generator("../test/in.2gram", "../test/out.2gram.lm")


def line_trigram_generator(input):
    temp = []
    for i in range(len(input)-2):
        sample = []
        sample.append(input[i])
        sample.append(input[i+1])
        sample.append(input[i+2])
        temp.append(sample)

    return temp


def make_file_suitable_3(input_dir):
    temp = file_to_list(input_dir)
    total_trigrams_of_file = []
    counter = 0
    for i in temp:
        line = line_trigram_generator(temp[counter].split())
        for j in line:
            total_trigrams_of_file.append(tuple(j))
        counter += 1
    return total_trigrams_of_file


def trigram_writer(freq_in, dest_dir, v, n_calc):
    label_3gram_lm = open(dest_dir, 'w', encoding="utf-8")

    for i, j in freq_in.items():
        if tuple([i[0],i[1]]) in n_calc:
            n = n_calc[tuple([i[0],i[1]])]
        else:
            n = n_calc["UNK"]
        p = (j+1)/(v+n+1)
        if i != "UNK":
            a = str(i[0] + "|" + i[1] + "|" + i[2]) + "|" + str(format(p, "0.4f"))+"\n"
            label_3gram_lm.write(a)
    label_3gram_lm.close()


def trigram_generator(src_dir, dest_dir):
    v = len(frequency_finder(input_full_tokenizer(src_dir, 0),1,0))
    t = make_file_suitable_3(src_dir)
    # n = len(s_t)
    # print(t[0][0])
    # n_calc = frequency_finder(input_full_tokenizer(src_dir, 1),3,v)
    n_calc = frequency_finder(make_file_suitable(src_dir),3,v)
    # n_calc = frequency_finder(input_full_tokenizer_3(src_dir),3,v)
    trigram_writer(frequency_finder(t,3,v), dest_dir, v, n_calc)


trigram_generator(dir1, "../label1.3gram.lm")
trigram_generator(dir2, "../label2.3gram.lm")
trigram_generator("../test/in.3gram", "../test/out.3gram.lm")