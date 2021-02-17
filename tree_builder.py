import math
import copy
from collections import Counter
import Node


def get_entropies_for_columns(rows, used_columns_):
    entropies = dict()
    for column_name in rows[0]:
        if column_name == "result" or column_name in used_columns_:
            continue
        values_in_column = dict()
        rowcount = 0
        for row in rows:
            rowcount += 1
            value = row[column_name]
            if value in values_in_column:
                values_in_column[value] += Counter(row["result"])
            else:
                values_in_column[value] = Counter(row["result"])
        entropy_sum_for_average = 0
        for val in values_in_column:
            e = values_in_column[val]["e"] if "e" in values_in_column[val] else 0
            p = values_in_column[val]["p"] if "p" in values_in_column[val] else 0
            n = p + e
            entropy = 0
            if p > 0:
                entropy += p / n * math.log2(n / p)
            if e > 0:
                entropy += e / n * math.log2(n / e)
            entropy_sum_for_average += entropy * n
        ent = list()
        ent.append(entropy_sum_for_average / rowcount)
        ent.append(len(values_in_column))
        ent.append(list(values_in_column.keys()))
        entropies[column_name] = ent
    return entropies


def get_min_entropy_column_name(entropies):
    return_value = list(entropies.keys())[0]
    for column_name in entropies:
        if entropies[column_name][0] < entropies[return_value][0] or \
                entropies[column_name][0] == entropies[return_value][0] and \
                entropies[column_name][1] < entropies[return_value][1]:
            return_value = column_name
    return return_value


def id3(min_column_name, entropies_for_columns, data, root, used_columns):
    used_columns_ = copy.deepcopy(used_columns)
    used_columns_.append(min_column_name)
    for i in entropies_for_columns[min_column_name][2]:      # possible values in min_column_name
        new_data = list()
        counter = 0
        no_counter = 0
        for row in data:
            no_counter += 1
            if row[min_column_name] == i:
                new_data.append(row)
                counter += 1
        probability = 0
        for row in new_data:
            probability += 1 if row["result"] == "p" else 0
        probability = probability / len(new_data)
        if probability == 1.0:
            root.add_child(i, 1.0)
            continue
        if probability == 0.0:
            root.add_child(i, 0.0)
            continue
        if len(new_data[0].keys()) - len(used_columns_) == 2:
            root.add_child(i, probability)
            continue

        en_ = get_entropies_for_columns(new_data, used_columns_)
        min_column_name_ = get_min_entropy_column_name(en_)
        new_node = Node.Node(min_column_name_, probability)
        id3(min_column_name_, en_, new_data, new_node, used_columns_)
        root.add_child(i, new_node)
