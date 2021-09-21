import csv
import re
import pandas as pd
import numpy as np


def lastname(contacts_list):
    """Обработка фамилии"""

    result = []
    for record in contacts_list:
        pattern = "[\w]+"
        words = re.findall(pattern, record[0])
        if len(words) == 3:
            record[0] = words[0]
            record[1] = words[1]
            record[2] = words[2]
        elif len(words) == 2:
            record[0] = words[0]
            record[1] = words[1]
        result.append(record)

    return result


def firstname(contacts_list):
    """Обработка имени"""

    result = []
    for record in contacts_list:
        pattern = "[\w]+"
        words = re.findall(pattern, record[1])
        if len(words) == 2:
            record[1] = words[0]
            record[2] = words[1]
        result.append(record)

    return result


def phone(contacts_list):
    """Обработка номера телефона"""

    pattern = "[\d]"
    result = []
    for record in contacts_list:
        phone_list = re.findall(pattern, record[5])
        if phone_list:
            if phone_list[0] == '8':
                phone_list[0] = '7'
            if len(phone_list) > 11 and re.findall('доб.', record[5]):
                record[5] = '+' + phone_list[0] + '(' + ''.join(phone_list[1:4]) + ')' + ''.join(phone_list[4:7]) + '-' + ''.join(phone_list[7:9]) + '-' + ''.join(phone_list[9:11]) + ' доб.' + ''.join(phone_list[11:])
            else:
                record[5] = '+' + phone_list[0] + '(' + ''.join(phone_list[1:4]) + ')' + ''.join(phone_list[4:7]) + '-' + ''.join(phone_list[7:9]) + '-' + ''.join(phone_list[9:11])
        result.append(record)

    return result


if __name__ == "__main__":

    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    contacts_list = lastname(contacts_list)
    contacts_list = firstname(contacts_list)
    contacts_list = phone(contacts_list)
    contacts_list = pd.DataFrame(contacts_list).replace('', np.NaN).groupby([0, 1]).first()
    contacts_list.to_csv("phonebook.csv", header=False)
