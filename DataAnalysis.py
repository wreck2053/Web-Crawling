import re, csv, os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# DEFINE UTILITY FUNCTIONS


# Extract the stopwords
def StopWords():
    temp = []
    for filename in os.listdir("StopWords\\"):
        f = open("StopWords\\" + filename)
        data = f.read().strip().split("\n")
        data = [i[: i.index("|")].strip() if "|" in i else i.strip() for i in data]
        temp.append(data)
        f.close()
    Stopwords = []
    for i in temp:
        Stopwords += i

    return Stopwords


# Cleaning Words
def Clean(words):
    Stopwords = StopWords()
    for i in words[:]:
        if i in Stopwords:
            words.remove(i)
    return words


# Number of syllables
def NoOfSyllables(word_list):
    count = 0
    vowels = ["a", "e", "i", "o", "u"]
    exceptions = ["es", "ed"]
    for i in word_list:
        for j in vowels:
            count += i.count(j)
        if i[-2:] in exceptions:
            count -= 1
    return count


# Positive Score
def PositiveScore(positive_words, words):
    positive_score = 0
    for i in words:
        if i in positive_words:
            positive_score += 1
    return positive_score


# Negative Score
def NegativeScore(negative_words, words):
    negative_score = 0
    for i in words:
        if i in negative_words:
            negative_score += 1
    return negative_score


# Polarity Score
def PolarityScore(positive_score, negative_score):
    polarity_score = (positive_score - negative_score) / (
        (positive_score + negative_score) + 0.000001
    )
    return polarity_score


# Subjectivity Score
def SubjectivityScore(positive_score, negative_score, total_no_of_words):
    subjectivity_score = (positive_score + negative_score) / (
        total_no_of_words + 0.000001
    )
    return subjectivity_score


# Avg Sentence Length
def AvgSentLength(file):
    file.seek(0, 0)
    no_of_words = len(word_tokenize(file.read()))
    file.seek(0, 0)
    no_of_sentences = len(sent_tokenize(file.read()))
    return round(no_of_words / no_of_sentences)


# Percentage of Complex Words
def PerComplexWords(words):
    no_of_complex_words = 0
    for i in words:
        sylcount = 0
        for j in ["a", "e", "i", "o", "u"]:
            sylcount += i.count(j)
        if sylcount > 2:
            no_of_complex_words += 1
    return no_of_complex_words / len(words)


# FOG Index
def FogIndex(x, y):
    return 0.4 * (x + y)


# Complex Word Count
def ComplexWordCount(words):
    return round(PerComplexWords(words) * len(words))


# Word Count
def WordCount(words):
    stop_words = set(stopwords.words("english"))
    filtered_words = [i for i in words if i.lower() not in stop_words]
    count = 0
    for i in filtered_words:
        if "!" in i or "?" in i or "." in i or "," in i:
            pass
        else:
            count += 1
    return count


# Syllable count per word
def SylPerWord(words):
    return round(NoOfSyllables(words) / len(words))


# Personal Pronoun Count
def PersonalPronouns(file):
    file.seek(0, 0)
    pronounRegex = re.compile(r"\b(I|we|my|ours|(?-i:us))\b", re.I)
    pronouns = pronounRegex.findall(file.read())
    return len(pronouns)


# Avg Word Length
def AvgWordLength(words):
    no_of_char = 0
    for i in words:
        no_of_char += len(i)
    return round(no_of_char / len(words))


# Store positive and negative words in lists
f = open("MasterDictionary\\positive-words.txt")
positive_words = f.read().strip().split("\n")
positive_words = Clean(positive_words)
f.close()

f = open("MasterDictionary\\negative-words.txt")
negative_words = f.read().strip().split("\n")
negative_words = Clean(negative_words)
f.close()

# Write into Output.csv as per format of Output_Data_Structure.csv
g = open("Output Data Structure.csv", "r")
h = open("Output.csv", "a", newline="")
Reader = csv.reader(g)
Writer = csv.writer(h)
Writer.writerow(next(Reader))

# Find all the .txt files extracted
files = os.listdir(".")  # current directory
text_files = [file for file in files if file.endswith(".txt")]

# main
for file in text_files:
    f = open(file)
    content = f.read()
    try:
        if not content:
            raise Exception

        words = word_tokenize(content)
        words = Clean(words)

        # Calculate all the variables
        positive_score = PositiveScore(positive_words, words)
        negative_score = NegativeScore(negative_words, words)
        polarity_score = PolarityScore(positive_score, negative_score)
        subjectivity_score = SubjectivityScore(
            positive_score, negative_score, len(words)
        )
        avg_sent_length = AvgSentLength(f)
        per_complex_words = PerComplexWords(words)
        fog_index = FogIndex(avg_sent_length, per_complex_words)
        avg_words_per_sent = avg_sent_length
        complex_word_count = ComplexWordCount(words)
        word_count = WordCount(words)
        syl_per_word = SylPerWord(words)
        personal_pronouns = PersonalPronouns(f)
        avg_word_length = AvgWordLength(words)

        Writer.writerow(
            next(Reader)[:2]
            + [
                positive_score,
                negative_score,
                polarity_score,
                subjectivity_score,
                avg_sent_length,
                per_complex_words,
                fog_index,
                avg_words_per_sent,
                complex_word_count,
                word_count,
                syl_per_word,
                personal_pronouns,
                avg_word_length,
            ]
        )

    except:
        Writer.writerow(next(Reader)[:2] + ([0] * 13))

    f.close()

g.close()
h.close()
