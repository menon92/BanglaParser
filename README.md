# BanglaPerser
Parse token from bangla text

Input words and it's parsed token
```
হ্যান্ডব্যাগেই    => ['হ্য', 'া', 'ন্ড', 'ব্য', 'া', 'গ', 'ে', 'ই']
বিশ্ববিদ্যালয়গুলো => ['বি', 'শ্ব', 'বি', 'দ্য', 'া', 'ল', 'য়', 'গু', 'লো']
ইন্টেলিজেন্সের   => ['ই', 'ন্ট', 'ে', 'লি', 'জ', 'ে', 'ন্স', 'ে', 'র']
হিষ্টিরিয়াগ্রস্তের   => ['হি', 'ষ্টি', 'রি', 'য়', 'া', 'গ্র', 'স্ত', 'ে', 'র']
মুক্তিযুদ্ধের     => ['মু', 'ক্তি', 'যু', 'দ্ধ', 'ে', 'র']
```
## Project structure
```sh
├── corpus
│   ├── bangla_golpo_monogram.txt
│   └── BengaliWordList_439.txt
├── data
│   ├── 439Kword_bn_class-frequency_count.txt
│   ├── 439Kword_bn_not-passed.txt
│   ├── 439Kword_bn_unique_class.txt
│   ├── 439Kword_bn_unique_word.txt
│   ├── golpo_bn_class-frequency_count.txt
│   ├── golpo_bn_not-passed.txt
│   └── golpo_bn_unique_word.txt
├── LICENSE
├── perse_tokens.py
└── README.md
```
## How to run
```sh
# set corpus path
corpus_path = 'corpus/BengaliWordList_439.txt'
go(corpus_path)

# now you can run
python perse_tokens.py
```
It will generate the following files

- Class/Token based frequency: `439Kword_bn_class-frequency_count.txt`
- Word that could not process by thie tool: `439Kword_bn_not-passed.txt`
- Unique class: `439Kword_bn_unique_class.txt`
- Unique words: `439Kword_bn_unique_word.txt`
