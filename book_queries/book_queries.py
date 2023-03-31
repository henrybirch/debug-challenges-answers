# Write a function that takes a list of sentences (a book) and returns a list of (word, word, avg_proximity) tuples
# where avg_proximity is the mean distance (as a float) between two words in all sentences in the entire book.
# Ordered by avg_proximity smallest to largest. In "The red house" the distance between the and house is one.

# Your results should be case insensitive and there should only be one tuple per word-word pair.
# The first word in the tuple should be the smallest alphanumerically out of the pair.
#
# Note that if two words never occured in the same sentence together,
# they will not be in a record together in the list.

# Note that one word can be in a sentence more than once.

# He also wants a function that calculates the average locations of words
# found within a book as a float. e.g. if a word is the first word in a book it
# will have a score of 0.00. If the last, 1.00.
#
# If the word only occurs twice, once as the first word, once as the last.
# It will have a score of 0.50.

from typing import List, Tuple, Set, Dict
import operator

Word = str
Sentence = List[Word]
Book = List[Sentence]
ProximityRecord = Tuple[Word, Word, float]
LocationRecord = Tuple[Word, float]


def get_proximity_records(book: Book) -> List[ProximityRecord]:
    def get_word_distances_for_sentence(
        sentence: Sentence,
    ) -> List[Tuple[Word, Word, int]]:
        word_distances: List[int] = []
        ids_considered: Set[Tuple[int, int]] = set()
        for i in range(len(sentence)):
            for j in range(len(sentence)):
                id = tuple(sorted((i, j)))

                if i == j or id in ids_considered:
                    continue

                ids_considered.add(id)

                word_1 = sentence[i].lower()
                word_2 = sentence[j].lower()

                ordered_words = tuple(sorted((word_1, word_2)))

                distance = abs(i - j) - 1
                word_distances.append(ordered_words + (distance,))
        return word_distances

    def reduce_word_distances(
        word_distances: List[Tuple[Word, Word, int]]
    ) -> List[Tuple[Word, Word, float]]:
        word_pair_counts_distances: Dict[
            Tuple[Word, Word], Tuple[int, int]
        ] = dict()  # {(word_1, word_2) : (count, sum_distance)}
        for record in word_distances:
            (word_1, word_2, distance) = record
            word_pair_counts_distances[(word_1, word_2)] = tuple(
                map(
                    sum,
                    zip(
                        word_pair_counts_distances.get(
                            (word_1, word_2), (0, 0)
                        ),
                        (1, distance),
                    ),
                )
            )
        return [
            (word_1, word_2, sum_distance / count)
            for (
                (word_1, word_2),
                (count, sum_distance),
            ) in word_pair_counts_distances.items()
        ]

    def flatten(l: List[List]):
        return [item for sublist in l for item in sublist]

    return reduce_word_distances(
        flatten(map(get_word_distances_for_sentence, book)),
    )


print(
    get_proximity_records(
        [["dsafsadf", "dsafsadf", "dsafsadf"], ["abba", "dbc", "abba"]]
    )
)
