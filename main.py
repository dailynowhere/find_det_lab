import sys
import itertools


def create_matrix(rows, cols):
    print("\nВвод элементов матрицы:")
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            while True:
                try:
                    element = float(input(f"Введите элемент [{i}][{j}]: "))
                    row.append(element)
                    break
                except ValueError:
                    print("Ошибка! Пожалуйста, введите число (целое или вещественное).")
        matrix.append(row)
    return matrix


def recursive_method(matrix, n):
    if n < 1:
        raise ValueError("Размерность матрицы должна быть положительной")

    match n:
        case 1:
            return matrix[0][0]
        case 2:
            return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        case _:
            s = 0
            for i in range(n):
                minor = []
                for k in range(1, n):  # Начинаем с 1, так как первую строку пропускаем
                    r = []
                    for j in range(n):
                        if j != i:
                            r.append(matrix[k][j])
                    minor.append(r)
                s += matrix[0][i] * recursive_method(minor, n - 1) * (-1) ** i
            return s


def leibniz_method(matrix, n):
    if n != len(matrix) or n != len(matrix[0]):
        raise ValueError("Матрица должна быть квадратной")

    indices = list(range(n))
    determinant = 0

    for permutation in itertools.permutations(indices):
        # Вычисляем знак перестановки
        sign = -1 if sum(permutation[i] < permutation[j]
                         for i in range(n)
                         for j in range(i + 1, n)) % 2 == 0 else 1

        # Вычисляем произведение элементов для данной перестановки
        product = 1
        for i in range(n):
            product *= matrix[i][permutation[i]]

        determinant += sign * product

    return determinant


def gauss_method(matrix, n):
    print("\nРешение методом Гаусса:")
    # Создаем копию матрицы
    matrix = [row[:] for row in matrix]
    determinant = 1
    epsilon = 1e-10  # Порог для сравнения с нулём

    for i in range(n):
        print(f"\nШаг {i + 1}:")
        print_matrix(matrix)

        # Поиск максимального элемента в столбце для улучшения устойчивости
        max_element = abs(matrix[i][i])
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > max_element:
                max_element = abs(matrix[k][i])
                max_row = k

        # Если максимальный элемент близок к нулю, определитель равен нулю
        if max_element < epsilon:
            print("Определитель равен 0 (найден нулевой столбец)")
            return 0

        # Меняем строки местами, если нужно
        if max_row != i:
            print(f"Меняем местами строки {i + 1} и {max_row + 1}")
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            determinant *= -1
            print("Матрица после перестановки строк:")
            print_matrix(matrix)

        # Обрабатываем строки под текущей
        for j in range(i + 1, n):
            if abs(matrix[j][i]) >= epsilon:
                factor = matrix[j][i] / matrix[i][i]
                print(f"Вычитаем из строки {j + 1} строку {i + 1}, умноженную на {factor:.4f}")
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
                print("Матрица после преобразования:")
                print_matrix(matrix)

    # Вычисляем определитель
    for i in range(n):
        determinant *= matrix[i][i]

    print("\nИтоговая треугольная матрица:")
    print_matrix(matrix)
    print(f"\nОпределитель вычисляется как произведение элементов главной диагонали: {determinant:.4f}")

    return determinant


def print_matrix(matrix):
    for row in matrix:
        for element in row:
            print(f"{element:8.4f}", end=' ')
        print()


try:
    print("Программа для вычисления определителя матрицы различными методами")

    while True:
        try:
            rows = int(input('\nВведите количество строк матрицы: '))
            if rows <= 0:
                print("Размерность матрицы должна быть положительной!")
                continue
            break
        except ValueError:
            print("Ошибка! Введите целое положительное число.")

    while True:
        try:
            cols = int(input('Введите количество столбцов матрицы: '))
            if cols <= 0:
                print("Размерность матрицы должна быть положительной!")
                continue
            break
        except ValueError:
            print("Ошибка! Введите целое положительное число.")

    if rows != cols:
        print('\nОшибка: невозможно вычислить определитель для неквадратной матрицы!')
        sys.exit()

    print("\nДоступные методы вычисления:")
    print("1. рекурсивный - классический метод разложения по первой строке")
    print("2. лейбниц - метод перестановок")
    print("3. гаусс - метод приведения к треугольному виду")

    while True:
        method = input('\nВыберите метод для вычисления определителя (рекурсивный/лейбниц/гаусс): ').lower()
        if method in ['рекурсивный', 'лейбниц', 'гаусс']:
            break
        print("Ошибка! Выберите один из предложенных методов.")

    matrix = create_matrix(rows, cols)

    print("\nИсходная матрица:")
    print_matrix(matrix)

    if method == 'рекурсивный':
        result = recursive_method(matrix, cols)
    elif method == 'лейбниц':
        result = leibniz_method(matrix, cols)
    else:  # гаусс
        result = gauss_method(matrix, cols)

    print(f"\nОпределитель матрицы: {result:.4f}")

except ValueError as e:
    if str(e):
        print(f"Ошибка: {e}")
    else:
        print('Ошибка: необходимо ввести число!')
except KeyboardInterrupt:
    print("\nПрограмма прервана пользователем.")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")

# Примеры использования программы:

"""
Пример 1: Матрица 2x2
Входные данные:
rows = 2
cols = 2
matrix = [
    [4, 3],
    [6, 3]
]
Ожидаемый результат:
Определитель = -6
(4 * 3 - 6 * 3 = 12 - 18 = -6)


Пример 2: Матрица 3x3
Входные данные:
rows = 3
cols = 3
matrix = [
    [2, 5, 3],
    [1, -2, -1],
    [1, 2, -1]
]
Ожидаемый результат:
Определитель = -20


Пример 3: Матрица 4x4
Входные данные:
rows = 4
cols = 4
matrix = [
    [1, 2, 3, 4],
    [2, 3, 4, 1],
    [3, 4, 1, 2],
    [4, 1, 2, 3]
]
Ожидаемый результат:
Определитель = 160


# Особые случаи для тестирования:
'''
# Матрица с нулевым определителем
test_matrix_zero = [
    [1, 2, 3],
    [2, 4, 6],
    [1, 2, 3]
]

# Единичная матрица (определитель = 1)
test_matrix_identity = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
]

# Матрица с дробными числами
test_matrix_float = [
    [1.5, 2.3],
    [3.7, 4.2]
]
'''
"""
