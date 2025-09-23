import re
import pymorphy2


# Получение общей статистики слов
def get_words_statistics(text: str) -> dict[str, int]:
    allWords = re.findall(r'\w+', text)
    wordsStat: dict = {}
    for word in allWords:
        wordsStat[word] = wordsStat.get(word, 0) + 1;
         
    return wordsStat

# Получение общего колличества слов
def get_total_words_count(wordsStatistics: dict[str, int]) -> int:
    count: int = 0
    for word in wordsStatistics:
        count += wordsStatistics[word]
    
    return count

# Получение статистики размеров слов
def get_size_statistics(wordsStatistics: dict[str, int]) -> dict[int, int]:
    sizeStatistics: dict[int, int] = {}
    wordSize: int = 0
    for word in wordsStatistics:
        wordSize = len(word)
        sizeStatistics[wordSize] = sizeStatistics.get(wordSize, 0) + wordsStatistics[word]
    
    return sizeStatistics

# Получение 10 самых частых слов без учёта союзов и предлогов
def get_top10_words(wordsStatistics:dict[str, int]) -> dict[str, int]:
    sortedDict: dict[str, int] = dict(sorted(wordsStatistics.items(), key=lambda item: item[1], reverse=True))
    top10Dict: dict[str, int] = {}
    FUNCTION_WORDS_RU = {
        'и', 'а', 'но', 'да', 'или', 'либо', 'то', 'не', 'ни', 'как', 'что',
        'чтобы', 'потому', 'поскольку', 'если', 'хотя', 'когда', 'где', 'куда',
        'в', 'на', 'за', 'под', 'над', 'перед', 'с', 'со', 'из', 'от', 'до', 
        'по', 'к', 'у', 'о', 'об', 'обо', 'про', 'при', 'через', 'сквозь'
    }
    
    count: int = 0
    for word in sortedDict:
        try: 
            if (word not in FUNCTION_WORDS_RU and len(word) > 3):
                top10Dict[word] = sortedDict[word]
                count += 1
            if count >= 10:
                break
        except Exception as e:
            print("Error:", e)
            continue

    return top10Dict
