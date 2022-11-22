import matplotlib.pyplot as plt
from datetime import datetime
from database.db_handler import get_cursor
import config

def get_incomes_by_month(month:int=datetime.now().month, year:int=datetime.now().year): 
    #узнать доход за месяц или год. Если пользователь ничего не указывает, то получает данные за текущий месяц и год
    
    result = get_cursor(f"""
    SELECT MONEY
    FROM OPERATIONS
    WHERE MONEY > 0
    AND DATE LIKE '%.{month}.{year}' 
    """).fetchall()
    return result


def get_expences_by_month(month:int=datetime.now().month, year:int=datetime.now().year): 
    #узнать расход за месяц или год. Если пользователь ничего не указывает, то получает данные за текущий месяц и год
    
    result = get_cursor(f"""
    SELECT MONEY
    FROM OPERATIONS
    WHERE MONEY < 0
    AND DATE LIKE '%.{month}.{year}' 
    """).fetchall()
    return result

def bars_by_year(year:int=datetime.now().year):
    labels = ['Янв', 'Фев','Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
    fig = plt.figure()

    result_incomes = []
    result_expenses = []

    def get_values(array):
        value = 0
        for i in array:
            value += i[0]
        return abs(value)

    for i in range(1, 13):
        incomes = get_incomes_by_month(month=i)
        expenses = get_expences_by_month(month=i)

        result_incomes.append(get_values(incomes))
        result_expenses.append(get_values(expenses))
        
    incomes_bar = plt.bar(
        x=labels, 
        height=result_incomes, 
        color = config.incomes_bar_color, 
        width = 0.5
    )
    expenses_bar = plt.bar(
        x=labels, 
        height=result_expenses, 
        color = config.expenses_bar_color, 
        width = 0.5
    )
    plt.legend(([incomes_bar, expenses_bar]), ('Доходы', 'Расходы'))
    plt.title(f"График доходов/расходов за {year} год") 

    plt.savefig('pic.png')

bars_by_year() 
