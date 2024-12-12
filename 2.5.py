import pulp

# Матрица стоимостей
C = [
    [2, 3, 4, 3, 0],
    [5, 3, 1, 2, 0],
    [2, 1, 4, 2, 0]
]

# Запасы на складах
supply = [180, 60, 80]

# Потребности магазинов
demand = [120, 40, 60, 80, 20]

# Количество складов и магазинов
num_suppliers = len(supply)
num_demands = len(demand)

# Создаем модель
model = pulp.LpProblem("TransportationProblem", pulp.LpMinimize)

# Переменные
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(num_suppliers) for j in range(num_demands)), lowBound=0, cat='Continuous')

# Целевая функция
model += pulp.lpSum(C[i][j] * x[i, j] for i in range(num_suppliers) for j in range(num_demands))

# Ограничения на запасы
for i in range(num_suppliers):
    model += pulp.lpSum(x[i, j] for j in range(num_demands)) == supply[i]

# Ограничения на потребности
for j in range(num_demands):
    model += pulp.lpSum(x[i, j] for i in range(num_suppliers)) == demand[j]

# Решение задачи
model.solve()

# Результаты
if pulp.LpStatus[model.status] == 'Optimal':
    print("Оптимальный план перевозок:")
    for i in range(num_suppliers):
        for j in range(num_demands):
            print(f"x{i}{j} = {pulp.value(x[i, j])}")
    print("Минимальная стоимость перевозок:", pulp.value(model.objective))
else:
    print("Решение не найдено. Проверьте ограничения и данные.")
