from random import randint
import enchant
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.html import HtmlParser
from sumy.summarizers.text_rank import TextRankSummarizer as TextSummarizer
from sumy.utils import get_stop_words
from Most_Similar import main3
from word_2_vec import main
from years_define import year_definitions
from nltk.stem.snowball import SnowballStemmer


def main2():
    link = input("enter link of text you want to find key words of(HTML): ")
    things = open(link, 'r', encoding='utf-8')
    z = xhtml_to_text(link)
    r = str(z)
    xhtml = things.read()
    summary = get_summary(xhtml)
    # s = input("enter link of text you want to find key words of(TEXT): ")
    # f = open(s, "r")
    # r = f.read()
    text = word_tokenize(r)
    x = main(r, link)
    wordz = list()
    summary_string = ""

    for sentences in summary[1:]:
        summary_string += sentences + " "

    for words in x:
        if words in summary_string:
            wordz.append(words)

    i = input("Press 'm' for multiple choice or 'b' for fill in the blank questions")
    # if i == "b":
    # fill_in_the_blank(wordz, text)

    if i == "m":
        multiple_choices(wordz, summary_string)


def fill_in_the_blank(x, text):
    n = len(x)  # number of questions you want + 1
    words = list()
    end = False
    while n > 0 and end is False:
        random = randint(0, len(x) - 1)
        if x[random] not in words:
            words.append(x[random])
            n -= 1
    for q in words:
        t = False
        y = wn.synsets(q)
        if y:
            sol = y[0].definition()
        while t is False:
            if y and q.isdigit() is False:
                answer = input("Fill in the blank (press 's' to stop, 'n' to skip question): " + sol + " :")
                if answer == q:
                    print("Correct!")
                    t = True
                if answer == "s":
                    end = True
                    break
                if answer == "n":
                    break
                if answer != q and answer != "s" and answer != "n":
                    print("Try again!")
            else:
                definition = year_definitions(q, text)
                answer = input("What year did this happen:  " + definition + "?")
                if answer == "s":
                    end = True
                    break
                if answer == "n":
                    break
                # sim = SequenceMatcher(None, answer, definition).ratio()
                if answer == q:
                    print("Correct!")
                    t = True
                else:
                    print("Try again!")
        if end is True:
            break


def multiple_choices(x, text):
    stemmer = SnowballStemmer("english")
    d = enchant.Dict("en_US")
    wrong = 0
    incorrect = list()
    n = len(x)  # number of questions you want + 1
    m = 4  # number of multiple choice questions + 1
    tester = m
    words = list()
    end = False
    iterations = 0
    while n > 0 and end is False:
        random = randint(0, len(x) - 1)
        if x[random] not in words:
            words.append(x[random])
            n -= 1
        iterations += 1
        if iterations > 100:
            n -= 1
            iterations = 0
    print("Length:")
    print(len(words))
    for w in words:
        # print(w)
        count = 0
        a = []
        correct_answer = " "
        answers = [None] * (tester + 1)
        answers[randint(0, 4)] = w
        if w.isdigit() is False and d.check(w.lower()):
            a = main3(w)
        else:
            if w.isdigit():
                it = 0
                while it < 4:
                    a.append(str(randint(int(w) - 50, int(w) + 50)))
                    it += 1
        lgth = 3
        wd = 2
        stemmed = list()
        if len(a) > 2:
            while lgth >= 0:
                r = randint(0, 4)
                while wd > 0 and answers[r] is None:
                    rand = randint(0, len(words) - 1)
                    if stemmer.stem(words[rand].lower()) != stemmer.stem(w.lower()) and stemmer.stem(
                            words[rand].lower()) not in stemmed and w.isdigit() is False and words[
                        rand].isdigit() is False:
                        answers[r] = words[rand].lower()
                        stemmed.append(stemmer.stem(words[rand].lower()))
                        lgth -= 1
                    wd -= 1
                if answers[r] is None and a[lgth] not in answers:
                    answers[r] = a[lgth]
                    lgth -= 1
                if a[lgth] in answers:
                    answers[r] = a[lgth + 1]
        cnt = 0
        output = list()
        if len(a) > 1:
            while cnt < len(answers):
                if cnt == 0:
                    output.append(" " + answers[cnt])
                    if answers[cnt] == w:
                        correct_answer = "a"
                    cnt += 1
                if cnt == 1:
                    output.append("\n " + answers[cnt])
                    if answers[cnt] == w:
                        correct_answer = "b"
                    cnt += 1
                if cnt == 2:
                    output.append("\n " + answers[cnt])
                    if answers[cnt] == w:
                        correct_answer = "c"
                    cnt += 1
                if cnt == 3:
                    output.append("\n " + answers[cnt])
                    if answers[cnt] == w:
                        correct_answer = "d"
                    cnt += 1
                if cnt == 4:
                    output.append("\n " + answers[cnt])
                    if answers[cnt] == w:
                        correct_answer = "e"
                    cnt += 1
        t = False
        while t is False:
            # y = wn.synsets(w)
            y = True
            all_words = word_tokenize(text)
            index = 0
            adds = 0
            info = 0
            keyz = ""
            sol = ""
            if y:
                # sol = y[0].definition()
                for wordz in all_words:
                    sol = ""
                    index += 1
                    if wordz.lower() == w.lower():
                        keyz = wordz.lower()
                        index -= 1
                        point = "o"
                        instance = 0
                        while point != "." and point != "?" and instance < 2 and "." not in wordz:
                            point = all_words[index - adds]
                            if point == ":":
                                instance += 1
                            info = index - adds
                            adds += 1

                        final_words = ""
                        adds = 0
                        info += 1
                        instance = 0
                        while final_words != "." and final_words != "?" and instance < 2 and "." not in words:
                            if final_words == ":" or final_words == ";":
                                instance += 1
                            sol += all_words[info + adds].lower() + " "
                            final_words = all_words[info + adds].lower()
                            adds += 1

                        break

                check = word_tokenize(sol)
                if len(check) < 1:
                    break
                if "[" in check[0].lower() or "identify" in check[0].lower() or "what" in check[
                    0].lower() or "explain" in check[0].lower() or "how" in check[0].lower():
                    break
                xy = 0
                while xy < len(check):
                    if check[xy] == keyz:
                        if check[xy - 1] == "a" or check[xy - 1] == "an":
                            check[xy - 1] = "a(n)"
                    xy += 1
                xy = 0
                while keyz in check:
                    while xy < len(check):
                        if check[xy] == keyz:
                            check[xy] = "-----?-----"
                            break
                        xy += 1

                solution = ""
                b = 0
                while b < len(check) - 1:
                    if check[b + 1] is "." or check[b + 1] is "," or check[b + 1] is ")" or check[b + 1] == '"':
                        solution += check[b]
                    else:
                        solution += check[b] + " "
                    b += 1

                if len(a) > 1:
                    ans = input(
                        "Enter the correct letter answer (or 's' to stop, 'n' to skip): " + solution + " : \n" + ''.join(
                            output))
                else:
                    correct_answer = w
                    ans = input("TYPE down the correct word (or 's' to stop, 'n' to skip): " + solution)

                if ans.lower() == correct_answer.lower():
                    print("Nice!")
                    t = True
                if ans == "n":
                    break
                if ans == "s":
                    end = True
                    break
                if ans != "s" and ans != correct_answer:
                    print("Try again!")
                    if count < 1:
                        count += 1
                        wrong += 1
                        incorrect.append(w)

            else:
                break
        if end is True:
            break
    print("Good Job, you finished this automated test. You incorrectly answered questions " + str(wrong) + " times.")
    print("Given your performance in this test, you should practice learning more about:")
    for words in incorrect:
        print("- " + words)


def xhtml_to_text(xhtml):
    html = open(xhtml).read()
    soup = BeautifulSoup(html, "lxml")
    return soup.get_text()


def get_summary(xhtml):
    summary_algorithm = TextSummarizer
    LANGUAGE = "english"
    REVIEW_COUNT = 20
    # SENTENCES_COUNT = 30

    parser = HtmlParser.from_string(xhtml, None, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = summary_algorithm(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summaries = []
    for sentence in summarizer(parser.document, REVIEW_COUNT):
        sentence = str(sentence).strip()
        if sentence not in summaries and '?' not in sentence:
            summaries.append(sentence)

    return summaries

    # print(categories)


# def year_definitions(year, text):


main2()

