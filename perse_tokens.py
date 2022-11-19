"""
extract tokens from bangla text
"""
import os
import sys
from collections import OrderedDict


SHOR_BORNO_CHARS       = 'অআইঈউঊঋএঐওঔ'
BANJON_BORNO_CHARS     = 'কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়'
BANJON_BORNO_SPATIAL   = 'ং ঃ ৎ'
ENDING_SYMBOLS         = 'ো ৌ ি ী'
AKAR_EKAR_OIKAR        = 'া ে  ৈ'
ENDING_SYMBOLS_SPATIAL = 'ু ূ ৃ ্ ঁ'

CHONDRO_BRINDO = 'ঁ'

# NORMAL_SYMBOLS = 'ক ষ ম র'
NORMAL_SYMBOLS = SHOR_BORNO_CHARS + BANJON_BORNO_CHARS
DUMMY_SYMBOLS = '1234567890' # this is added for handle index out of error
connector = '্'

# define colors
CRED = '\033[91m'
CEND = '\033[0m'

BN_MAX_CLASSES = 904


def get_en_unique_combination():
    # unique_chars_set = [c for c in EN_CHARS_SET]
    unique_chars_set = []
    cls_cnt = 0
    for c in EN_CHARS_SET:
        for ch in EN_CHARS_SET:
            unique_chars_set.append(c + ch)
            cls_cnt += 1
            if cls_cnt == BN_MAX_CLASSES:
                return unique_chars_set


def get_bn_class():
    bn_class = []
    with open(BN_CLASS_FREQUENCY) as f:
        for line in f:
            line = line.strip(' \n')
            _class_name, _ = line.split(' ')
            bn_class.append(_class_name)
    return bn_class


def init_en_bn_maping():
    en_class = get_en_unique_combination()
    bn_class = get_bn_class()
    f_bn_to_en = open('bn_to_en_maping.txt', 'w')
    f_en_to_bn = open('en_to_bn_maping.txt', 'w')

    for en, bn in zip(en_class, bn_class):
        f_en_to_bn.write(en + ' ' + bn + '\n')
        f_bn_to_en.write(bn + ' ' + en + '\n')
        EN_TO_BN_MAP[en] = bn
        BN_TO_EN_MAP[bn] = en


def print_c(log_msg):
	print(CRED + log_msg + CEND)


def read_bangla_corpus(dictionary_path):
    with open(dictionary_path, 'r') as corpus:
        big_line = ''
        big_line_set = set()
        for line in corpus:
            line = line.strip('\n')
            line = line.strip(' ')
            # print(line)
            big_line += line
            big_line_set.add(line)

        print('len big_line', len(big_line))
        print('len big_line_set', len(big_line_set))

        return big_line


def is_normal_char(char):
    if char in NORMAL_SYMBOLS:
        return True
    return False


def is_ending_char(char):
    if char in ENDING_SYMBOLS:
        return True
    return False


def is_ending_char_spatial(char):
    if char in ENDING_SYMBOLS_SPATIAL:
        return True
    return False


def is_spatial_type_banjn_borno(char):
    if char in BANJON_BORNO_SPATIAL:
        return True
    return False


def is_akar_ekar_oikar(char):
    if char in AKAR_EKAR_OIKAR:
        return True
    return False


def is_jukto_borno(chars, start_index, log=False):
    if log:
        print('///////// In is_jukto_borno method ////////')
    c = chars[start_index]
    c_next = chars[start_index + 1]
    c_next_next = chars[start_index + 2]
    # variables for 2 connected jukto_borno
    c_next_next_next = chars[start_index + 3]
    c_next_next_next_next = chars[start_index + 4]
    c_next_next_next_next_next = chars[start_index + 5]

    jukto_borno = ''
    is_found_jukto_borno = False
    new_start_index = start_index

    if log:
        print('------> Start index ', start_index)
        print('1', c, ' 2', c_next, ' 3', c_next_next, ' 4', c_next_next_next, ' 5',\
             c_next_next_next_next, ' 5', c_next_next_next_next_next)


    if is_normal_char(c) and is_ending_char_spatial(c_next) and \
        c_next_next == connector and is_normal_char(c_next_next_next):
        # example : গণঅভ্যুত্থানের = গ+ণ+অ+ভ+ু+্+য+ত+্+থ+া+ন+ে+র
        is_found_jukto_borno = True
        jukto_borno = c + c_next + c_next_next + c_next_next_next
        new_start_index = start_index + 4
    # check two connector jukto borno
    # example: ষ + ্ + ক + ্ + র = ষ্ক্র
    elif is_normal_char(c) and c_next == connector and is_normal_char(c_next_next) \
        and c_next_next_next == connector and is_normal_char(c_next_next_next_next): \
        # this is 2 connected juktorborno
        if log:
            print('...In two connector jukto-borno')

        is_found_jukto_borno = True
        # check two connector jukto-borno with 'ENDING SYMBOLS'
        # example: ষ + ্ + ক + ্ + র + া = ষ্ক্রা
        if is_ending_char(c_next_next_next_next_next):
            if log:
                print('In two connector jukto-borno with ending symbols')
            jukto_borno = c + c_next + c_next_next + c_next_next_next + c_next_next_next_next \
                            + c_next_next_next_next_next
            new_start_index = start_index + 6
        else:
            # example: ষ + ্ + ক + ্ + র + া = ষ্ক্র
            if log:
                print('In two connector jukto-borno without ending symbols')
            # this is two connector jukto-borno without 'ENDING SYMBOLS'
            jukto_borno = c + c_next + c_next_next + c_next_next_next + c_next_next_next_next
            new_start_index = start_index + 5
    # check one connector jukto borno
    # example: ক + ্ + ষ = ক্ষ
    elif is_normal_char(c) and c_next == connector and is_normal_char(c_next_next):
        if log:
            print('...In one connector juktoborno')

        is_found_jukto_borno = True
        # chekc jukto borno is with 'ENDING SYMBOLS'
        # example: ক + ্ + ষ + া = ক্ষা
        if is_ending_char(c_next_next_next):
            if log:
                print("This is jukto borno with 'ENDING_SYMBOLS' ")
            jukto_borno = c + c_next + c_next_next + c_next_next_next
            # update start index
            new_start_index = start_index + 4
        else:
            # example: ক + ্ + ষ + া = ক্ষ
            if log:
                print("This is jukto borno without any 'ENDING_SYMBOLS' ")
            jukto_borno = c + c_next + c_next_next
            # update start index
            new_start_index = start_index + 3

    # chech jukto-borno has 'ENDING_SYMBOLS_SPATIAL'
    # example: ক + ্ + ক + ু = ক্কু
    temp_spatial_char = chars[new_start_index]
    if log:
        print('temp_spatial_char', temp_spatial_char)
    if is_ending_char_spatial(temp_spatial_char):
        if log:
            print('This is juktoborno with spatial ending char')
        jukto_borno += temp_spatial_char
        new_start_index = new_start_index + 1

    if log:
        print('////// End of is_jukto_borno method ///////// ', new_start_index)

    return is_found_jukto_borno, jukto_borno, new_start_index


def class_extractor(chars, log=True):
    class_list = []
    len_chars = len(chars)
    chars = chars + DUMMY_SYMBOLS

    i = 0
    while i < len_chars:
        # print('Number of symbols processed', i)
        if log:
            print('i', i)

        if chars[i] == ' ':
            print_c('space found in position: ' + str(i))
            i += 1
            continue

        c = chars[i]
        c_next = chars[i + 1]
        c_next_next = chars[i + 2]
        c_next_next_next = chars[i + 3]

        if log:
            print('1:', c, '2:', c_next, '3:', c_next_next, '4:', c_next_next_next)

        is_found_jukto_borno, jukto_borno, new_start_index = is_jukto_borno(chars, i)
        # print('jukto_borno_found:', is_found_jukto_borno)
        # init
        chunk = ''
        start = i

        if is_spatial_type_banjn_borno(c):
            chunk = c
            start = i + 1
        elif is_found_jukto_borno:
            if log:
                print('jukto-borno', jukto_borno)

            chunk = jukto_borno
            # set start positon for next iteration of i
            start = new_start_index
            if log:
                print('start in is_found_jukto_borno', start)
        elif is_normal_char(c) and is_normal_char(c_next):
            chunk = c
            # set start positon for next iteration of i
            start = i + 1
        elif is_normal_char(c) and is_ending_char(c_next) and is_ending_char(c_next_next):
            chunk = c + c_next + c_next_next
            start = i + 3
        elif is_normal_char(c) and is_spatial_type_banjn_borno(c_next):
            # print('in')
            # example: অংস
            chunk = c
            start = i + 1
        elif is_normal_char(c) and is_ending_char_spatial(c_next) and c_next_next == CHONDRO_BRINDO:
            # example: 'অগ্নিঝুঁকিতে'
            chunk = c + c_next + c_next_next
            start = i + 3
        elif is_spatial_type_banjn_borno(c) and is_normal_char(c_next):
            # example: অংস
            # print('in2')
            chunk = c
            start = i + 1
        elif is_spatial_type_banjn_borno(c) and c_next == CHONDRO_BRINDO:
            # example : হুঁশিয়ার
            chunk = c + c_next
            start = i + 2
        elif is_normal_char(c) and is_ending_char(c_next):
            # chekc it has ENDING_SYMBOLS_SPATIAL
            # example : ক ু  া
            if is_ending_char_spatial(c_next_next):
                if log:
                    print('normal + ending + spatial + ending')
                chunk = c + c_next + c_next_next
                start = i + 3
            else:
                if log:
                    print('normal + ending')
                # ending chars with out spatial ending symbols
                # example : কা = ক + া
                chunk = c + c_next
                # print('chunk is ', chunk)
                # set start positon for next iteration of i
                start = i + 2
        elif is_normal_char(c) and is_ending_char_spatial(c_next):
            # print('ami in ?')
            # check has ending char
            if is_ending_char(c_next_next):
                chunk = c + c_next + c_next_next
                start = i + 3
            else:
                # print('in else')
                chunk = c + c_next
                # print(chunk)
                start = i + 2
        elif is_normal_char(c) and c_next == connector and is_normal_char(c_next_next):
            if is_ending_char(c_next_next_next) or is_ending_char_spatial(c_next_next_next):
                chunk = c + c_next + c_next_next + c_next_next_next
                start = i + 4
            else:
                chunk = c + c_next + c_next_next
                start = i + 3
        elif is_normal_char(c) and c_next == connector:
            # example: অপ্‌
            chunk = c + c_next
            start = i + 2
        elif is_normal_char(c) and c_next == '1':
            # this is the last chars of the line
            chunk = c
            start = i + 1
        elif is_normal_char(c) and is_akar_ekar_oikar(c_next) and c_next_next == CHONDRO_BRINDO:
            chunk = [c + c_next_next, c_next]
            start = i + 3
        elif is_akar_ekar_oikar(c):
            chunk = c
            start = i + 1
        elif is_normal_char(c):
            chunk = c
            start = i + 1
        elif str(c) in DUMMY_SYMBOLS:
            # print('dummy')
            # we reach to end
            # example = হল্‌
            break

        if type(chunk) is list:
            print('chunk is list')
            for item in chunk:
                class_list.append(item)
        else:
            # write data to text file
            # print('chunk is 2', chunk)
            if chunk != '':
                class_list.append(chunk)
            else:
                print_c('chunk is empty for: ' + chars[i])
                # skip this word
                return []
        # updae the start position of i
        i = start

    return class_list


def max_squence_lenght():
    max_len = 0
    min_len = 1000
    avg_len = 0
    with open('corpus/bangla_golpo_monogram.txt', 'r') as corpus:
        total_words = 0
        for line in corpus:
            line = line.strip(' \n')
            word = line.split(' ')[0]
            en_word = convert_bn_to_en(word)
            _len = len(en_word) * 2
            print('bn word', word, ' en word', en_word, ' en len', _len)
            if _len > max_len:
                max_len = _len # each symbol is represented by 2 english chars
            if _len < min_len:
                min_len = _len
            avg_len += _len
            total_words += 1

    print('max squence len:', max_len, ' min len:', min_len, ' avg_len:', avg_len / total_words)


def go(corpus_text):
    f_not_passed = open('data/bn_not-passed.txt', 'w')
    bangla_unique_class = set()
    bangla_unique_word  = set()
    bangla_cls_frequency = {}

    with open(corpus_text, 'r') as f:
    # with open('bn-corpus/utest.txt', 'r') as f:
        line_counter = 0
        for line in f:
            print('line is', line)
            line = line.strip('\n')
            line = line.strip(' ')
            bangla_unique_word.add(line)
            class_list = class_extractor(line)
            # print('class_list', class_list)
            if len(class_list) >= 1:
                for chunk in class_list:
                    # print('chunk is', chunk)
                    bangla_unique_class.add(chunk)
                    # count frequency of a chunk
                    if chunk not in bangla_cls_frequency:
                        bangla_cls_frequency[chunk] = 1
                    else:
                        bangla_cls_frequency[chunk] += 1
            else:
                print_c('can not process word: ' + line + " lc " + str(line_counter))
                f_not_passed.write(line)
                f_not_passed.write('\n')
            line_counter += 1
    f_not_passed.close()

    # sort dictionary by frequency count value
    bangla_cls_frequency = OrderedDict(sorted(bangla_cls_frequency.items(), key=lambda x: x[1], reverse = True))

    print('*' * 35)
    print("Total unique word found     :", len(bangla_unique_word))
    print('Number of unique class found:', len(bangla_unique_class))
    # write unique class to a file
    with open('data/bn_unique_class.txt', 'w') as f_unique:
        for chunk in bangla_unique_class:
            f_unique.write(chunk)
            f_unique.write('\n')

    # write class presence frequency
    with open('data/bn_class-frequency_count.txt', 'w') as f_cls_freqency:
        for key, value in bangla_cls_frequency.items():
            f_cls_freqency.write(key)
            f_cls_freqency.write(' ')
            f_cls_freqency.write(str(value))
            f_cls_freqency.write('\n')

    bangla_unique_word = list(bangla_unique_word)
    bangla_unique_word.sort(key=len)
    with open('data/bn_unique_word.txt', 'w') as w:
        for word in bangla_unique_word:
            w.write(word + '\n')


def debug():
    chars = 'হ্যাঁ'
    class_extractor(chars)
    with open('single_chars.txt', 'w') as f:
        for c in chars:
            print(c)
            f.write(c)
            f.write('\n')

    class_list = class_extractor(chars)
    print(class_list)


def test_words():
    words = ["হ্যান্ডব্যাগেই", "বিশ্ববিদ্যালয়গুলো", "ইন্টেলিজেন্সের","হিষ্টিরিয়াগ্রস্তের","মুক্তিযুদ্ধের"]
    for word in words:
        class_list = class_extractor(word)
        print(f"{word} => {class_list}")


if __name__ == "__main__":
    corpus_path = 'corpus/BengaliWordList_439.txt'
    go(corpus_path)
    # debug()
    # test_words()