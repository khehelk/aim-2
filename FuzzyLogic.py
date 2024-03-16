import matplotlib.pyplot as plt
from io import BytesIO
import base64


def trapezoidal_mf(x, params):
    a, b, c, d = params
    if x < a or x > d:
        return 0
    elif a <= x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return 1
    elif c <= x <= d:
        return (d - x) / (d - c)


def union(mf1_params, mf2_params, crisp_values):
    union_values = []
    for x in crisp_values:
        membership1 = trapezoidal_mf(x, mf1_params)
        membership2 = trapezoidal_mf(x, mf2_params)
        union_values.append(max(round(membership1, 2), round(membership2, 2)))
    return union_values


def draw_fuzzy_set(mf1_params, mf2_params, crisp_values, result):
    fig, ax = plt.subplots()

    min_crisp = min(crisp_values)
    max_crisp = max(crisp_values)

    plt.tight_layout()

    ax.plot([mf1_params[0], mf1_params[1], mf1_params[2], mf1_params[3], mf1_params[0]], [0, 1, 1, 0, 0], 'b-')
    ax.plot([mf2_params[0], mf2_params[1], mf2_params[2], mf2_params[3], mf2_params[0]], [0, 1, 1, 0, 0], 'r-')

    i = 0
    for val in crisp_values:
        ax.plot([val, val], [0, result[i]], 'g--')
        ax.plot([val, val], [0, 0], 'g--')
        ax.scatter(val, result[i], color='green')
        i += 1

    ax.set_ylim([0, 1.2])
    ax.set_xlim([min(mf1_params[0], mf2_params[0], min_crisp) - 10, max(mf1_params[3], mf2_params[3], max_crisp) + 10])
    ax.set_xlabel('X')
    ax.set_ylabel('Membership')

    plt.grid(True)
    img = BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)
    plt.close()
    return base64.b64encode(img.read()).decode()