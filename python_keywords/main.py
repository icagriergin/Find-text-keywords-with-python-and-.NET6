from flask import Flask, request
from flask_restful import Api
import yake
from keybert import KeyBERT
from textrank4zh import TextRank4Keyword
from rakun2 import RakunKeyphraseDetector
import re
import heapq

app = Flask(__name__)
api = Api(app)

def purePythonExtractor(sourceText):
    min_keywords = 2
    max_keywords = 3

    sentences = re.split(r' *[\.\?!][\’”\)\]]* *', sourceText)
    clean_text = sourceText.lower()
    word_tokenize = clean_text.split()

    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                  'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                  'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                  'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                  'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                  'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                  'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
                  'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                  'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                  'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should',
                  'now']
    word2count = {}
    # for word in word_tokenize:
    for word in word_tokenize:
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1

    for key in word2count.keys():
        word2count[key] = word2count[key] / max(word2count.values())

    candidates = []
    sl = sourceText.lower().split()

    for num_keywords in range(min_keywords, max_keywords + 1):
        # Until the third-last word
        for i in range(0, len(sl) - num_keywords):
            if sl[i] not in stop_words:
                candidate = sl[i]
                j = 1
                keyword_counter = 1
                contains_stopword = False

                while keyword_counter < num_keywords and i + j < len(sl):
                    candidate = candidate + ' ' + sl[i + j]
                    if sl[i + j] not in stop_words:
                        keyword_counter += 1
                    else:
                        contains_stopword = True
                    j += 1

                if contains_stopword and candidate.split()[-1] not in stop_words and keyword_counter == num_keywords:
                    candidates.append(candidate)
    key2score = {}
    for key_phrase in candidates:
        for keyword in key_phrase.split():
            if keyword in word2count.keys():
                if key_phrase not in key2score.keys():
                    key2score[key_phrase] = word2count[keyword]
                else:
                    key2score[key_phrase] += word2count[keyword]

    bestTenKeyphrases = heapq.nlargest(10, key2score, key=key2score.get)

    keywordLists = []

    for kw in bestTenKeyphrases:
        keywordLists.append(kw)

    return ','.join(keywordLists)

def rakunAlgorithm(sourceText):
    hyperParameters = {"num_keywords": 10,
                       "merge_threshold": 1.1,
                       "alpha": 0.3,
                       "token_prune_len": 3}

    keyword_detector = RakunKeyphraseDetector(hyperParameters)
    out_keywords = keyword_detector.find_keywords(sourceText, input_type="string")

    keywordLists = []

    for kw in out_keywords:
        keywordLists.append(kw[0])

    return ','.join(keywordLists)


def textRank4ZhAlgorithm(sourceText):
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=sourceText, lower=True, window=2)

    keywordLists = []

    for kw in tr4w.get_keywords(20, word_min_len=1):
        keywordLists.append(kw.word)

    return ','.join(keywordLists)


def keybertAlgorithm(sourceText):
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(sourceText)
    keywordLists = []

    for kw in keywords:
        keywordLists.append(kw[0])

    return ','.join(keywordLists)


def yakeAlgorithm(sourceText):
    text = sourceText

    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)

    keywordLists = []

    for kw in keywords:
        keywordLists.append(kw[0])

    return ','.join(keywordLists)


@app.route('/runPurePythonExtractor', methods=['POST', 'GET'])
def runPurePythonExtractor():
    data = request.json
    sourceText = data["SourceText"]

    return {"SourceText": purePythonExtractor(sourceText)}, 200


@app.route('/runYakeAlgorithm', methods=['POST', 'GET'])
def runYakeAlgorithm():
    data = request.json
    sourceText = data["SourceText"]

    return {"SourceText": yakeAlgorithm(sourceText)}, 200


@app.route('/runKeybertAlgorithm', methods=['POST', 'GET'])
def runKeybertAlgorithm():
    data = request.json
    sourceText = data["SourceText"]

    return {"SourceText": keybertAlgorithm(sourceText)}, 200


@app.route('/runTextRank4ZhAlgorithm', methods=['POST', 'GET'])
def runTextRank4ZhAlgorithm():
    data = request.json
    sourceText = data["SourceText"]

    return {"SourceText": textRank4ZhAlgorithm(sourceText)}, 200


@app.route('/runRakunAlgorithm', methods=['POST', 'GET'])
def runRakunAlgorithm():
    data = request.json
    sourceText = data["SourceText"]

    return {"SourceText": rakunAlgorithm(sourceText)}, 200


if __name__ == '__main__':
    #     app.run(host="0.0.0.0", port=5000)
    app.run(port=5001)
