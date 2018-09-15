# Input data and connection of libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


zone_list = []
meanDeviationGroup = 4  # Среднее отклонение данной выборки
numberOfObjectsGroup = 64  # Количество элементов выборки
meanValueOfTheGroup = 101  # Среднее значение гипотезы Н1
meanValueOfTheHypothesis = 100  # Среднее значение гипотезы Н0
mean_of_global_deviation = 1
z = 0
left_z = 0
RIGHT_EDGE = 3
LEFT_EDGE = -1 * RIGHT_EDGE
RIGHT_ERR_EDGE = 1.96
LEFT_ERR_EDGE = -1 * RIGHT_ERR_EDGE
point_count = 10000
print('enter the desired result (it can be errors, probability_H0_exceed_H1 or probability_H0_not_exceed_H1)')
MODE = str(input())  # can take value: errors, probability_H0_exceed_H1, probability_H0_not_exceed_H1

# Mathematiс block
# Making transformation, determining coordinates, describe the functions for drawing, calculating
# Сarry out z transformation


def z_deter(value, edge, error_edge, mode):
    if mode == 'probability_H0_exceed_H1' or mode == 'probability_H0_not_exceed_H1':
        value = (meanValueOfTheGroup - meanValueOfTheHypothesis) / mean_of_global_deviation
    elif mode == 'errors':
        value = (meanValueOfTheGroup - meanValueOfTheHypothesis) / (meanDeviationGroup / np.sqrt(numberOfObjectsGroup))
    else:
        print('Not enough input data')
        exit()
    if ((value < 0) and (edge > 0)) or ((value > 0) and (edge < 0)):
        value *= -1
    if abs(value) >= abs(edge):
        value = edge
    elif abs(value) <= abs(error_edge):
        value = error_edge
    return value


z = z_deter(z, RIGHT_EDGE, RIGHT_ERR_EDGE, MODE)
left_z = z_deter(left_z, LEFT_EDGE, LEFT_ERR_EDGE, MODE)

# Section for determining the coordinates
fig_size = (10, 7)
fig = plt.figure(figsize=fig_size, facecolor='red', frameon=True)
x = np.linspace(LEFT_EDGE, RIGHT_EDGE, point_count)
y = (1 / (np.sqrt(2 * np.pi))) * (np.exp((-1 * (x ** 2)) / 2))


def y_calc(value):
    return (1 / (np.sqrt(2 * np.pi))) * (np.exp((-1 * (value ** 2)) / 2))


def get_err_interval(x_list, y_list, start, end):
    y_interval = []
    x_interval = []
    counter = 0
    for x_index in range(len(x_list)):
        x_value = x_list[x_index]
        if (x_value >= start) and (x_value <= end):
            x_interval.insert(counter, x_value)
            y_interval.insert(counter, y_list[x_index])
            counter += 1
    np_y = np.array(y_interval)
    np_x = np.array(x_interval)
    y_nul = np_y * 0

    return {
        'y': np_y,
        'x': np_x,
        'z': y_nul
    }


def calculate_zones(params):
    x = params['x']
    y = params['y']
    z = params['z']
    left_z = params['left_z']
    LEFT_EDGE = params['LEFT_EDGE']
    LEFT_ERR_EDGE = params['LEFT_ERR_EDGE']
    RIGHT_EDGE = params['RIGHT_EDGE']
    RIGHT_ERR_EDGE = params['RIGHT_ERR_EDGE']
    zones = []
    if params['mode'] == 'errors':
        zones.extend([
            {
                'zone': get_err_interval(x, y, LEFT_EDGE, left_z),
                'type': 'err_2'
            },
            {
                'zone': get_err_interval(x, y, left_z, LEFT_ERR_EDGE),
                'type': 'err_1'
            },
            {
                'zone': get_err_interval(x, y, RIGHT_ERR_EDGE, z),
                'type': 'err_1'
            },
            {
                'zone': get_err_interval(x, y, z, RIGHT_EDGE),
                'type': 'err_2'
            }
        ])
    elif params['mode'] == 'probability_H0_not_exceed_H1':
       zones.append({
           'zone': get_err_interval(x, y, LEFT_EDGE, z),
           'type': 'probability_pos'
       })
    elif params['mode'] == 'probability_H0_exceed_H1':
        zones.append({
            'zone': get_err_interval(x, y, z, RIGHT_EDGE),
            'type': 'probability_neg'
        })
    else:
        print('Are you ahueli tam?')

    return zones

# The function definition block for drawing


def fill_between(zone, colour='green'):
    plt.fill_between(zone['x'], zone['z'], zone['y'], color=colour, alpha=0.25)


def calculation_of_integrals(mode):
    if mode == 'errors':
        i_first_left = quad(y_calc, LEFT_EDGE, left_z)
        i_second_left = quad(y_calc, left_z, LEFT_ERR_EDGE)
        i_first_right = quad(y_calc, z, RIGHT_EDGE)
        i_second_right = quad(y_calc, RIGHT_ERR_EDGE, z)
        integral = abs(i_first_left[0]) + abs(i_second_left[0]) + abs(i_first_right[0]) + abs(i_second_right[0])
    elif mode == 'probability_H0_not_exceed_H1':
        integral_number = quad(y_calc, LEFT_EDGE, z)
        integral = abs(integral_number[0])
    elif mode == 'probability_H0_exceed_H1':
        integral_number = quad(y_calc, z, RIGHT_EDGE)
        integral = abs(integral_number[0])
    percent = round(integral * 100, 4)
    s_persent = str(percent) + '%'
    return s_persent


def draw(mode):
    plt.plot(x, y, 'r', label='функция нормального распределения')
    plt.xlabel('Признак')
    plt.ylabel('Распределение или частота встречи')
    plt.grid()
    plt.title("График нормального распределения после преобразования в единицы стандартного отклонения")
    plt.legend(loc='upper left')
    fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    if mode == 'errors':
        plt.text(-3.1, 0.05, u"зелёное 1 рода", family="verdana")
        plt.text(2.1, 0.05, u"зелёное 1 рода", family="verdana")
        plt.text(0.9, 0.03, u"красное 2 рода", family="verdana")
        plt.text(-1.95, 0.03, u"красное 2 рода", family="verdana")
        plt.text(-0.9, 0.15, "Общий процент ошибок составляет", family="verdana")
        plt.text(-0.16, 0.13, str_percent, family="verdana")
    elif mode == 'probability_H0_not_exceed_H1':
        plt.text(-0.9, 0.15, u"Вероятность того, что Н0<H1", family="verdana")
        plt.text(-0.16, 0.13, str_percent, family="verdana")
    elif mode == 'probability_H0_exceed_H1':
        plt.text(-0.9, 0.15, u"Вероятность того, что Н0>H1", family="verdana")
        plt.text(-0.16, 0.13, str_percent, family="verdana")


str_percent = calculation_of_integrals(MODE)
zones_list = calculate_zones({
    'mode': MODE,
    'x': x,
    'y': y,
    'z': z,
    'left_z': left_z,
    'LEFT_EDGE': LEFT_EDGE,
    'LEFT_ERR_EDGE': LEFT_ERR_EDGE,
    'RIGHT_EDGE': RIGHT_EDGE,
    'RIGHT_ERR_EDGE': RIGHT_ERR_EDGE,
})

# Drawing a Graph
for i in range(len(zones_list)):
    fill_params = zones_list[i]
    type = fill_params['type']
    color = 'green'
    if (type == 'probability_neg') or (type == 'err_2'):
        color = 'red'
    fill_between(fill_params['zone'], color)
draw(MODE)

# Output data and save Graph
plt.savefig(r'C:\Users\Figure')
plt.show()
