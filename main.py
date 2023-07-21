from src.classes import HH, Superjob, JSON


def main():

    # Просмотр вакансий
    key = input('Введите поисковый запрос: ')
    hh = HH(key)
    super_job = Superjob(key)

    while True:
        answer = input('Выберите платформу для поиска вакансий:\na.hh.ru\nb.superjob.ru\n')
        if answer == 'a':
            hh.get_request()
            vacansies = hh.get_formatted_vacancies()
            break
        if answer == 'b':
            super_job.get_request()
            vacansies = super_job.get_formatted_vacancies()
            break

    # Сохранение в файл
    js = JSON(f'{key}.json', vacansies)

    # Выборка вакансий
    while True:
        answer = input('1. Вывести всё\n2. Отсортировать по зарплате\n3. Получить топ пять вакансий\n')
        if answer == '1':
            json_all = js.all_data()
            for i in json_all:
                print(i)
        if answer == '2':
            json_sorted = js.sorted_by_salary()
            for i in json_sorted:
                print(i)
        if answer == '3':
            json_sorted = js.get_5()
            for i in json_sorted:
                print(i)


if __name__ == "__main__":
    main()