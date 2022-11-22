import matplotlib.pyplot as plt
from datetime import datetime
from database.db_handler import get_cursor
import config   


def get_category_expenses_by_month(month:int=datetime.now().month, year:int=datetime.now().year):
    # находим расходы с id категории по месяцу
    result = get_cursor(f"""
                SELECT CATEGORYID, MONEY
                FROM OPERATIONS
                WHERE MONEY < 0
                AND DATE LIKE '%.{month}.{year}'
                """).fetchall()
    return result


# суммируем значения с одинаковой категорией
def sum_samecategories(list, y):
    sum = 0
    for i in list:
        if y == i[0]:
            sum += i[1]
        else:
            sum == i[1]
    return (y, abs(sum))

# выводим словарь id категории - название
find_category= get_cursor("""SELECT * FROM CATEGORIES""").fetchall()
category_dict = dict(find_category)
print(category_dict)

# Выводим суммы расходов по категориям (по месяцу)
result_categories = []
for i in range (1, 11):
    x = sum_samecategories(get_category_expenses_by_month(), i)
    result_categories.append(x)
dict1 = dict(result_categories)
print(dict1)


#строим круговую диаграмму
def pie_by_categories(month:int=datetime.now().month, year:int=datetime.now().year):

    fig, axes = plt.subplots()

    
    labels = category_dict.values()
    data = dict1.values()

    axes.pie(data, labels=labels, autopct='%.2f%%')

    plt.title(f"Расходы по категориям за {month} {year} года") 

    plt.savefig('pie.png')

pie_by_categories()





