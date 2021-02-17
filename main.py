import sys
import arrow
import pandas as pd
from collections import defaultdict

import Node
import tree_builder

global right_answers
right_answers = 0


def add_result(probability, expected_result, answers_list):
    global right_answers
    answers_list.append(f"The probability of poisonous: {probability}\n")
    if probability < 0.5 and expected_result == 'e':
        right_answers += 1
    if probability >= 0.5 and expected_result == 'p':
        right_answers += 1


def resolve(sub_questions_list, root):
    answers_list = list()
    for query in sub_questions_list:
        node = root
        while True:
            option = query[node.column]
            if option not in node.nodes:
                add_result(node.result, query['result'], answers_list)

                break
            if not isinstance(node.nodes[option], float):
                next_node = node.nodes[option]
                probability = next_node.result
            else:
                probability = node.nodes[option]
                add_result(probability, query['result'], answers_list)
                break
            if probability >= 1 or probability <= 0:
                add_result(probability, query['result'], answers_list)
                break
            node = next_node
    return answers_list


def main():
    if len(sys.argv) != 4:
        print("Error! Bad number of arguments")
        exit(0)
    data = pd.read_csv(sys.argv[1]).to_dict('records', into=defaultdict(list))
    entropies_for_columns = tree_builder.get_entropies_for_columns(data[:int((len(data))/2)], list())
    min_column_name = tree_builder.get_min_entropy_column_name(entropies_for_columns)

    probability = 0
    for row_ in data:
        probability += 1 if row_["result"] == "p" else 0
    probability = probability / len(data)
    root = Node.Node(min_column_name, probability)
    used_columns = list()
    start_time = arrow.utcnow()
    tree_builder.id3(min_column_name, entropies_for_columns, data, root, used_columns)
    end_time = arrow.utcnow()
    print(f"The time of tree creation: {int((end_time - start_time).total_seconds() * 1000)} ms")

    sub_questions_list = list()
    lines_number = 0
    questions = open(sys.argv[2], "r")
    try:
        while True:
            sub_question = dict()
            line = (questions.readline()).strip('\t\n\r')
            if not line:
                break
            lines_number += 1
            query = line.split(",")
            i = 0
            for column_name in data[0]:
                sub_question[column_name] = query[i]
                i += 1
            sub_questions_list.append(sub_question)
    finally:
        questions.close()

    answers_list = resolve(sub_questions_list, root)
    answers = open(sys.argv[3], "w")
    try:
        answers.writelines(answers_list)
    finally:
        answers.close()
        print("The program finished successfully")
        print(f"Percentage of right answers: {(right_answers/lines_number)*100}%")


if __name__ == '__main__':
    main()
