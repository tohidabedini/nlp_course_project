import math


def calculate_number_of_ngrams(input_model_dir):
    f_in_model = open(input_model_dir, 'r', encoding="utf-8")
    count = 0
    for i in f_in_model:
        count += 1
    f_in_model.close()
    return count


def calculate_unigram_probabilty(word,input_model_dir):
    f_in_model = open(input_model_dir, 'r', encoding="utf-8")
    for i in f_in_model:
        if i.split("|")[0] == word:
            # print(i.split("|"))
            return float(i.split("|")[1])


def calculate_ngram_sentence_probability(sentence,n,input_model_dir):
    if n == 1:
        f_in_model = open(input_model_dir, 'r', encoding="utf-8")

        sentence_probability_log_sum = 0.0
        for word in sentence:
            if word != "<s>" and word != "</s>":
                word_probability = calculate_unigram_probabilty(word,input_model_dir)
                sentence_probability_log_sum += math.log(word_probability, 2)
        f_in_model.close()
        return math.pow(2, sentence_probability_log_sum)


    # elif n == 2:
    #     f_in_model = open(input_model_dir, 'r', encoding="utf-8")
    #
    #     bigram_sentence_probability_log_sum = 0
    #     previous_word = None
    #     for word in sentence:
    #         if previous_word != None:
    #             unigram_word_probability = calculate_bigram_probabilty(word)
    #             unigram_sentence_probability_log_sum += math.log(unigram_word_probability, 2)
    #         previous_word = word
    #     return math.pow(2,unigram_sentence_probability_log_sum)
    #
    #     f_in_model.close()
    #
    # elif n == 3:
    #     f_in_model = open(input_model_dir, 'r', encoding="utf-8")
    #
    #     unigram_sentence_probability_log_sum = 0
    #     previous_word = None
    #     for word in sentence:
    #         if previous_word != None:
    #             unigram_word_probability = calculate_trigram_probabilty(word)
    #             unigram_sentence_probability_log_sum += math.log(unigram_word_probability, 2)
    #         previous_word = word
    #     return math.pow(2,unigram_sentence_probability_log_sum)
    #
    #     f_in_model.close()


def ngram_perplexity_calculator(input_model_dir,input_text_dir,n):
    f_in_model = open(input_model_dir, 'r', encoding="utf-8")
    f_in_text = open(input_text_dir, 'r', encoding="utf-8")
    ngram_count = calculate_number_of_ngrams(input_model_dir)
    sentence_probability_log_sum = 0
    for i in f_in_text:
        # sentence_probability_log_sum -= math.log(float(i.split("|")[-1]), 10)
        sentence_probability_log_sum -= math.log(calculate_ngram_sentence_probability(i,n,input_model_dir), 10)

    f_in_model.close()
    f_in_text.close()
    return math.pow(10, sentence_probability_log_sum / ngram_count)


in_model_uni_1 = "../../Model/label1.1gram.lm"
in_model_bi_1 = "../../Model/label1.2gram.lm"
in_model_tri_1 = "../../Model/label1.3gram.lm"

in_model_uni_2 = "../../Model/label2.1gram.lm"
in_model_bi_2 = "../../Model/label2.2gram.lm"
in_model_tri_2 = "../../Model/label2.3gram.lm"

in_text_1_train = "../../SplitData/train/label1.txt"
in_text_2_train = "../../SplitData/train/label2.txt"
in_text_1_test = "../../SplitData/test/label1.txt"
in_text_2_test = "../../SplitData/test/label2.txt"

# 1
print(ngram_perplexity_calculator(in_model_uni_1,in_text_1_train,1))
# print(ngram_perplexity_calculator(in_model_uni_1,in_text_1_test,1))

# print(ngram_perplexity_calculator(in_model_bi_1,in_text_1_train,2))
# print(ngram_perplexity_calculator(in_model_bi_1,in_text_1_test,2))
#
# print(ngram_perplexity_calculator(in_model_tri_1,in_text_1_train,3))
# print(ngram_perplexity_calculator(in_model_tri_1,in_text_1_test,3))
#
# # 2
# print(ngram_perplexity_calculator(in_model_uni_2,in_text_2_train,1))
# print(ngram_perplexity_calculator(in_model_uni_2,in_text_2_test,1))
#
# print(ngram_perplexity_calculator(in_model_bi_2,in_text_2_train,2))
# print(ngram_perplexity_calculator(in_model_bi_2,in_text_2_test,2))
#
# print(ngram_perplexity_calculator(in_model_tri_2,in_text_2_train,3))
# print(ngram_perplexity_calculator(in_model_tri_2,in_text_2_test,3))

in_model_uni_test = "../../Model/test/out.1gram.lm"
in_model_bi_test = "../../Model/test/out.2gram.lm"
in_model_tri_test = "../../Model/test/out.3gram.lm"
in_text_test = "../../Model/test/in.1gram"
# print(ngram_perplexity_calculator(in_model_uni_test,in_text_test,1))
# print(ngram_perplexity_calculator(in_model_bi_test,in_text_test,2))
# print(ngram_perplexity_calculator(in_model_tri_test,in_text_test,3))
