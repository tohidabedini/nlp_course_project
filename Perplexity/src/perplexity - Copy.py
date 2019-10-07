import re
import math

# used for unseen words in training vocabularies
UNK = None
# sentence start and end
SENTENCE_START = "<s>"
SENTENCE_END = "</s>"


def read_sentences_from_file(file_path):
    with open(file_path, "r",encoding="utf-8") as f:
        return [re.split("\s+", line.rstrip('\n')) for line in f]


class UnigramLanguageModel:
    def __init__(self, sentences, smoothing=False):
        self.unigram_frequencies = dict()
        self.corpus_length = 0
        for sentence in sentences:
            for word in sentence:
                self.unigram_frequencies[word] = self.unigram_frequencies.get(word, 0) + 1
                if word != SENTENCE_START and word != SENTENCE_END:
                    self.corpus_length += 1
        # subtract 2 because unigram_frequencies dictionary contains values for SENTENCE_START and SENTENCE_END
        self.unique_words = len(self.unigram_frequencies) - 2
        self.smoothing = smoothing

    def calculate_unigram_probability(self, word):
        word_probability_numerator = self.unigram_frequencies.get(word, 0)
        word_probability_denominator = self.corpus_length
        if self.smoothing:
            word_probability_numerator += 1
            # add one more to total number of seen unique words for UNK - unseen events
            word_probability_denominator += self.unique_words + 1
        return float(word_probability_numerator) / float(word_probability_denominator)

    def calculate_sentence_probability(self, sentence, normalize_probability=True):
        sentence_probability_log_sum = 0
        for word in sentence:
            if word != SENTENCE_START and word != SENTENCE_END:
                word_probability = self.calculate_unigram_probability(word)
                sentence_probability_log_sum += math.log(word_probability, 2)
        return math.pow(2, sentence_probability_log_sum) if normalize_probability else sentence_probability_log_sum

    def sorted_vocabulary(self):
        full_vocab = list(self.unigram_frequencies.keys())
        full_vocab.remove(SENTENCE_START)
        full_vocab.remove(SENTENCE_END)
        full_vocab.sort()
        full_vocab.append(UNK)
        full_vocab.append(SENTENCE_START)
        full_vocab.append(SENTENCE_END)
        return full_vocab


class BigramLanguageModel(UnigramLanguageModel):
    def __init__(self, sentences, smoothing=False):
        UnigramLanguageModel.__init__(self, sentences, smoothing)
        self.bigram_frequencies = dict()
        self.unique_bigrams = set()
        for sentence in sentences:
            previous_word = None
            for word in sentence:
                if previous_word != None:
                    self.bigram_frequencies[(previous_word, word)] = self.bigram_frequencies.get((previous_word, word),
                                                                                                 0) + 1
                    if previous_word != SENTENCE_START and word != SENTENCE_END:
                        self.unique_bigrams.add((previous_word, word))
                previous_word = word
        # we subtracted two for the Unigram model as the unigram_frequencies dictionary
        # contains values for SENTENCE_START and SENTENCE_END but these need to be included in Bigram
        self.unique__bigram_words = len(self.unigram_frequencies)

    def calculate_bigram_probabilty(self, previous_word, word):
        bigram_word_probability_numerator = self.bigram_frequencies.get((previous_word, word), 0)
        bigram_word_probability_denominator = self.unigram_frequencies.get(previous_word, 0)
        if self.smoothing:
            bigram_word_probability_numerator += 1
            bigram_word_probability_denominator += self.unique__bigram_words
        return 0.0 if bigram_word_probability_numerator == 0 or bigram_word_probability_denominator == 0 else float(
            bigram_word_probability_numerator) / float(bigram_word_probability_denominator)

    def calculate_bigram_sentence_probability(self, sentence, normalize_probability=True):
        bigram_sentence_probability_log_sum = 0
        previous_word = None
        for word in sentence:
            if previous_word != None:
                bigram_word_probability = self.calculate_bigram_probabilty(previous_word, word)
                bigram_sentence_probability_log_sum += math.log(bigram_word_probability, 2)
            previous_word = word
        return math.pow(2,
                        bigram_sentence_probability_log_sum) if normalize_probability else bigram_sentence_probability_log_sum


# calculate number of unigrams & bigrams
def calculate_number_of_unigrams(sentences):
    unigram_count = 0
    for sentence in sentences:
        # remove two for <s> and </s>
        unigram_count += len(sentence) - 2
    return unigram_count


def calculate_number_of_bigrams(sentences):
    bigram_count = 0
    for sentence in sentences:
        # remove one for number of bigrams in sentence
        bigram_count += len(sentence) - 1
    return bigram_count


# print unigram and bigram probs
def print_unigram_probs(sorted_vocab_keys, model):
    for vocab_key in sorted_vocab_keys:
        if vocab_key != SENTENCE_START and vocab_key != SENTENCE_END:
            print("{}: {}".format(vocab_key if vocab_key != UNK else "UNK",
                                  model.calculate_unigram_probability(vocab_key)), end=" ")
    print("")


def print_bigram_probs(sorted_vocab_keys, model):
    print("\t\t", end="")
    for vocab_key in sorted_vocab_keys:
        if vocab_key != SENTENCE_START:
            print(vocab_key if vocab_key != UNK else "UNK", end="\t\t")
    print("")
    for vocab_key in sorted_vocab_keys:
        if vocab_key != SENTENCE_END:
            print(vocab_key if vocab_key != UNK else "UNK", end="\t\t")
            for vocab_key_second in sorted_vocab_keys:
                if vocab_key_second != SENTENCE_START:
                    print("{0:.5f}".format(model.calculate_bigram_probabilty(vocab_key, vocab_key_second)), end="\t\t")
            print("")
    print("")


# calculate perplexty
def calculate_unigram_perplexity(model, sentences):
    unigram_count = calculate_number_of_unigrams(sentences)
    sentence_probability_log_sum = 0
    for sentence in sentences:
        try:
            sentence_probability_log_sum -= math.log(model.calculate_sentence_probability(sentence), 2)
        except:
            sentence_probability_log_sum -= float('-inf')
    return math.pow(2, sentence_probability_log_sum / unigram_count)


def calculate_bigram_perplexity(model, sentences):
    number_of_bigrams = calculate_number_of_bigrams(sentences)
    bigram_sentence_probability_log_sum = 0
    for sentence in sentences:
        try:
            bigram_sentence_probability_log_sum -= math.log(model.calculate_bigram_sentence_probability(sentence), 2)
        except:
            bigram_sentence_probability_log_sum -= float('-inf')
    return math.pow(2, bigram_sentence_probability_log_sum / number_of_bigrams)


in_text_1_train = "../../SplitData/train/label1.txt"
in_text_2_train = "../../SplitData/train/label2.txt"
in_text_1_test = "../../SplitData/test/label1.txt"
in_text_2_test = "../../SplitData/test/label2.txt"


in_text_1_train_file = read_sentences_from_file(in_text_1_train)
in_text_1_test_file = read_sentences_from_file(in_text_1_test)
in_text_1_train_model_smoothed = BigramLanguageModel(in_text_1_train_file, smoothing=True)
print("PERPLEXITY of train1")
print("unigram: ", calculate_unigram_perplexity(in_text_1_train_model_smoothed, in_text_1_train_file))
print("bigram: ", calculate_bigram_perplexity(in_text_1_train_model_smoothed, in_text_1_train_file))

print("")

print("PERPLEXITY of test1")
print("unigram: ", calculate_unigram_perplexity(in_text_1_train_model_smoothed, in_text_1_test_file))
print("bigram: ", calculate_bigram_perplexity(in_text_1_train_model_smoothed, in_text_1_test_file))

# -----------------------
print("")

in_text_2_train_file = read_sentences_from_file(in_text_2_train)
in_text_2_test_file = read_sentences_from_file(in_text_2_test)
in_text_2_train_model_smoothed = BigramLanguageModel(in_text_2_train_file, smoothing=True)
print("PERPLEXITY of train2")
print("unigram: ", calculate_unigram_perplexity(in_text_2_train_model_smoothed, in_text_2_train_file))
print("bigram: ", calculate_bigram_perplexity(in_text_2_train_model_smoothed, in_text_2_train_file))

print("")

print("PERPLEXITY of test2")
print("unigram: ", calculate_unigram_perplexity(in_text_2_train_model_smoothed, in_text_2_test_file))
print("bigram: ", calculate_bigram_perplexity(in_text_2_train_model_smoothed, in_text_2_test_file))
