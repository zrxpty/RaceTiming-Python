import json
import datetime


def read_competitors(_path):
    with open(_path, 'r', encoding='utf-8') as competitors_file:
        return json.load(competitors_file)


def read_results(_path):
    with open(_path, 'r') as results_file:
        return results_file.readlines()


def process_results(results):
    results_dict = {}
    for result in results:
        result = result.strip().split()
        number = result[0]
        time = result[2]
        if result[1] == 'start':
            results_dict[number] = {'start': time}
        elif result[1] == 'finish':
            if number not in results_dict:
                results_dict[number] = {'start': None}
            results_dict[number]['finish'] = time
    return results_dict


def format_time(start, finish):
    if start and finish:
        time_delta = datetime.datetime.strptime(finish, '%H:%M:%S,%f') - datetime.datetime.strptime(start, '%H:%M:%S,%f')
        result_time = str(time_delta).split('.')[0] + ',' + str(time_delta).split('.')[1][:3]
    else:
        result_time = '00:00:00,000'
    return result_time


def print_results(sorted_results, competitors):
    print('Занятое место  Нагрудный номер  Имя  Фамилия  Результат')
    for i, (number, times) in enumerate(sorted_results):
        name = competitors.get(number, {}).get('Name', '')
        surname = competitors.get(number, {}).get('Surname', '')
        start = times.get('start', None)
        finish = times.get('finish', None)
        result_time = format_time(start, finish)
        print('{:<13} {:<16} {:<5} {:<8} {}'.format(i + 1, number, name, surname, result_time))

def main():
    competitors = read_competitors('competitors2.json')
    results = read_results('results_RUN.txt')
    results_dict = process_results(results)
    sorted_results = sorted(results_dict.items(), key=lambda x: x[1].get('finish', '99:99:99,999999'))
    print_results(sorted_results, competitors)

if __name__ == '__main__':
    main()