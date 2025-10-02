import os
import re
import argparse
from word_statistics import word_statistics
from pathlib import Path

# Чтение текста в строку
def read_text(path: Path) -> str:
    text: str = ""
    with open(path, "r", encoding="utf-8") as file:
        line: str = file.readline()
        while line != "":
            text += line
            line = file.readline()
    
    return text


def main():
    try:
    # Распаришиваем аргументы 
        parser = argparse.ArgumentParser()
        parser.add_argument("path")
        args = parser.parse_args() 
        path: Path = Path(args.path)
        # Проверяем путь на существование
        if(not path.exists()):
            path = Path(os.path.join(os.path.dirname(__file__), path))
            if (not path.exists()):
                raise Exception("Path was not exist")
            if(not path.is_file()):
                raise Exception("Еhe end of the path must be a file")
            extension: str = re.search(".[A-Za-z]+$", str(path))            
            if(extension != ".txt"):
                raise Exception("The file extension must be .txt")
        
        text:str = read_text(path)
        wordsStatistics: dict[str, int] = word_statistics.get_words_statistics(text)
        print("##############################################")
        print("Статистика слов:\n", wordsStatistics, "\n##############################################")
        sentencesCount: int = word_statistics.get_sentences_count(text)
        print("Количество предложений:", sentencesCount, "\n##############################################")
       # wordsCount: int = word_statistics.get_total_words_count(wordsStatistics)
       # print("Общее количество слов:", wordsCount, "\n##############################################")
        sizeStatistics: dict[int, int] = word_statistics.get_size_statistics(wordsStatistics)
        print("Распределение длин слов:", sizeStatistics, "\n##############################################")
        top10Words: dict[str, int] = word_statistics.get_top10_words(wordsStatistics)
        avgLength, maxLength = word_statistics.get_avg_and_max_word_length(wordsStatistics)
        print("Средняя длина слова:", round(avgLength, 2))
        print("Максимальная длина слова:", maxLength, "\n##############################################")
        print("ТОП 10 частых слов :", top10Words, "\n##############################################")
        top10Bigrams, top10Trigrams = word_statistics.get_top10_ngrams(text)
        print("ТОП 10 биграмм:", top10Bigrams)
        print("ТОП 10 триграмм:", top10Trigrams, "\n##############################################")
        
    except Exception as err:
        print("Error:", err)
    return 0

if __name__ == "__main__":
    main()