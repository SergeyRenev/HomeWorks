
# получить словарь из файла
def get_cook_book():
    file = open('../HomeWorks/recipes/recipes.txt', 'r')
    cook_book = {}
    line = '-'
    while line:
        name = file.readline().rstrip('\n') # Название блюда
        num =  file.readline().rstrip('\n') # Количество ингредиентов в блюде
        ingredients = []                    # Список ингредиентов
        for n in range(int(num)):
            list = file.readline().rstrip('\n').split('|') # Читаем ингредиенты и разделяем
            ingredients.append({'ingredient_name': list[0], 'quantity': list[1], 'measure': list[2]})
        cook_book[name] = ingredients
        line = file.readline()
    file.close()
    return cook_book;

# In
# dishes - список блюд
# person_count - количество персон
# Out
# new_ingred - словарь с названием ингредиентов и его количества для блюда
def get_shop_list_by_dishes(dishes, person_count):
    cook_book = GetCookBook()
    new_ingred = {}
    for dish in dishes:
        if cook_book.get(dish, None): #если блюдо есть в списке
            for item in cook_book[dish]:
                ingred = item['ingredient_name']
                if new_ingred.get(ingred,None):
                    new_ingred[ingred]['quantity'] += int(item['quantity'])*person_count
                else:
                    new_ingred[ingred] = {'measure': item['measure'], 'quantity': int(item['quantity'])*person_count}
        else:
            return {} # блюда нет в списке, возвращаем пустой список

    return new_ingred

# запись нового отсортированного файла
def sort_files():
    name_files = ['1.txt', '2.txt', '3.txt']
    data_files = {}
    for name in name_files:
        lines = []
        file = open('../HomeWorks/recipes/' + name, 'r')
        line = file.readline().rstrip('\n')
        while line:
            lines.append(line)
            line = file.readline().rstrip('\n')
        data_files[name] = lines # добавляем строки в словарь
        file.close()
    # сортируем файл
    data_files_sort = sorted(data_files.items(), key=lambda x: len(x[1]))

    # записываем новый файл
    final_file = open('../HomeWorks/recipes/final.txt', 'w')
    for key_vals in data_files_sort:
        #print(key_vals[0])
        final_file.write(key_vals[0] + '\n')            # записываем имя файла
        final_file.write(str(len(key_vals[1])) + '\n')  # записываем число строк
        for line in key_vals[1]:                        # записываем строки
            final_file.write(line + '\n')

    final_file.close()

if __name__ == '__main__':
    print(get_cook_book())
    sort_files()
#new_ingred = get_shop_list_by_dishes(['Запеченный картофель','Запеченный картофель'], 3)
#print(new_ingred)

