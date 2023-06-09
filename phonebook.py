# Создать телефонный справочник с возможностью импорта и экспорта
# данных в формате .txt. Фамилия, имя, отчество, номер телефона - данные,
# которые должны находиться в файле.
# 1.Программа должна выводить данные
# 2.Программа должна сохранять данные в текстовом файле
# 3.Пользователь может ввести одну из характеристик для поиска
# определенной записи(Например имя или фамилию человека)
# 4.Использование функций. Ваша программа не должна быть линейной
# 5. Дополнить телефонный справочник возможностью изменения и удаления
# данных. Пользователь также может ввести имя или фамилию, и Вы должны реализовать
# функционал для изменения и удаления данных.

# ВАЖНО!
# Команды должны вводиться с большой буквы (как в запросе доступных действий)
# Манипуляции с записью телефонной книги "Изменить", "Удалить" доступны только после поиска
# нужного контакта
# При поиске контакта после двоеточия не надо делать пробел
# Файл необходимо обязательно экспортировать, чтобы изменения сохранились


import re


def creating(file='phone.txt'):
    with open(file, 'w', encoding='utf-8') as data:
        data.write(f'Фамилия,Имя,Номер\n')


def writing_txt(info, file='phone.txt'):
    with open(file, 'w', encoding='utf-8') as data:
        data.write(f'Фамилия,Имя,Номер\n{info}')
        print("Файл успешно экспортирован.")


def reading_txt(file):
    # возвращает данные в виде строки
    with open(file, encoding='utf-8') as f:
        content = re.search('(?<=Фамилия,Имя,Номер\n)(.*\n*)*', f.read())
        return content.group(0).lstrip()


def get_info():
    last_name = input("Введите фамилию: ")
    first_name = input("Введите имя: ")

    phone_number = ''
    flag = False
    while not flag:
        try:
            phone_number = input("Введите номер: ")
            if len(phone_number) != 11:
                print("В номере должно быть 11 цифр")
            else:
                phone_number = int(phone_number)
                flag = True
        except:
            print("В номере должны быть только цифры")
    return ",".join([last_name, first_name, f"{phone_number}"])


def record_info():
    info = get_info()
    writing_txt(info)


def start_user_process(file, users, user):
    menu_variants = ['Изменить', 'Удалить', 'Назад']
    choice = input(f"Доступные действия: {menu_variants}\n")

    if choice == 'Назад':
        start_file_dialog(file, users)
    elif choice == 'Удалить':
        start_file_dialog(file, users.replace(f"{user}\n", ''))
    elif choice == 'Изменить':
        new_user = start_edition_dialog(user.split(","))
        start_file_dialog(file, users.replace(user, new_user))
    else:
        print('Неправильный выбор действия, попробуйте еще раз')
        start_user_process(file, users, user)


def start_edition_dialog(user_data):
    new_user = ''
    edition_object = input('Выберите что хотите изменить: [\'Имя\', \'Фамилия\', \'Телефон\']\n')
    if edition_object == 'Фамилия':
        surname = input('Введите фамилию:\n')
        new_user = f"{surname},{user_data[1]},{user_data[2]}"
    elif edition_object == 'Имя':
        name = input('Введите имя:\n')
        new_user = f"{user_data[0]},{name},{user_data[2]}"
    elif edition_object == 'Телефон':
        phone = input('Введите телефон:\n')
        new_user = f"{user_data[0]},{user_data[0]},{phone}"
    else:
        print('Неправильный выбор действия, попробуйте еще раз')
        start_edition_dialog(user_data)
    return new_user


def construct_user(surname, name, phone):
    return f"{surname},{name}, {phone}"


def start_nothing_found_dialog(file, users):
    choice = input("Пользователей не найдено, доступные действия: ['Поиск', 'Назад']\n")
    if choice == 'Поиск':
        start_search_process(file, users)
    elif choice == 'Назад':
        start_file_dialog(file, users)
    else:
        print('Неправильный выбор действия, попробуйте еще раз')
        start_nothing_found_dialog(file, users)


def start_search_process(file, users):
    criteria = input(f"Введите критерий поиска:")
    found_users = [user for idx, user in enumerate(users.split('\n')) if criteria in user]
    print(f"Найденные пользователи:\n {found_users}")

    if len(found_users) == 0:
        start_nothing_found_dialog(file, users)
    elif len(found_users) > 1:
        while True:
            user_num = input('Выберите номер желаемого пользователя\n')
            if int(user_num) < 1 or int(user_num) > len(found_users):
                print("Неправильно указан номер пользователя")
            else:
                break
        start_user_process(file, users, found_users[int(user_num) - 1])
    else:
        start_user_process(file, users, found_users[0])


def start_file_dialog(file, users):
    menu_variants = ['Показать список', 'Поиск', 'Добавить пользователя', 'Экспорт', 'Назад']

    choice = input(f"Доступные действия: {menu_variants}\n")
    if choice == 'Показать список':
        print(users.strip())
        start_file_dialog(file, users)
    elif choice == 'Поиск':
        start_search_process(file, users)
    elif choice == 'Добавить пользователя':
        start_file_dialog(file, f"{users.strip()}\n{get_info()}\n")
        start_menu()
    elif choice == 'Экспорт':
        try:
            writing_txt(users, input('Введите имя файла\n'))
        except FileNotFoundError:
            print("Проверьте корректность названия файла и попробуйте еще раз")
            start_file_dialog(file, users)
    elif choice == 'Назад':
        start_menu()
    else:
        print('Неправильный выбор действия, попробуйте еще раз')
        start_file_dialog(file, users)


def start_import_process(file):
    start_file_dialog(file, reading_txt(file))


def start_creation_process():
    creating(input('Введите имя файла\n'))
    start_menu()


def start_menu():
    menu_variants = ['Создать новый файл', 'Открыть']
    choice = input(f"Доступные действия: {menu_variants}\n")
    if choice == 'Создать новый файл':
        start_creation_process()
    elif choice == 'Открыть':
        try:
            start_import_process(input('Введите имя файла\n'))
        except FileNotFoundError:
            print("Файл не найден, попробуйте еще раз")
            start_menu()
    else:
        print('Неправильный выбор действия, попробуйте еще раз')
        start_menu()


def main():
    start_menu()


if __name__ == "__main__":
    main()
