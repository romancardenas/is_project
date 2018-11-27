import pandas as pd
from random import randint

pd.options.display.max_rows = None


def fum1(max_power):
    return randint(0, max_power)


def fum2(power, reduce):
    return power * reduce


def fum3(power, offset):
    if power > offset:
        return power - offset
    else:
        return 0


def fu_data(data, failNum=2, minFaulty=4, maxFaulty=7, minBroken=3, maxBroken=5, fum=0, maxPower=7500000, reduce=0.75,
            offset=10000, test=0):
    data0 = data.copy()
    n = failNum
    m = 0
    s = len(data0) / n

    if test == 1:
        faulty_start = 100
        broken_start = randint(minFaulty * 24, maxFaulty * 24) + faulty_start
        broken_end = randint(minBroken * 24, maxBroken * 24) + broken_start

        m = m + 1

        i = 0
        if fum == 0:
            method = randint(1, 3)
        else:
            method = fum

        print("Starting {} iteration of faults. Fault starts at {};".format(m, faulty_start))
        print("the engine breaks at {} and is repaired at {}. Fault type was {}".format(broken_start, broken_end, method))

        for p in data0['output_power']:
            i = i + 1
            if (i > faulty_start) & (i < broken_start):
                if method == 1:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum1(maxPower)                    
                elif method == 2:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum2(p, reduce)
                elif method == 3:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum3(p, offset)
                data0.iloc[i, data0.columns.get_loc('state')] = 'f'
            elif (i >= broken_start) & (i < broken_end):
                data0.iloc[i, data0.columns.get_loc('output_power')] = 0
                data0.iloc[i, data0.columns.get_loc('state')] = 'r'
        return data0
    while n > 0:
        n = n - 1
        faulty_start = randint(300 + m * s, len(data0) - s * n - 300)
        broken_start = randint(minFaulty * 24, maxFaulty * 24) + faulty_start
        broken_end = randint(minBroken * 24, maxBroken * 24) + broken_start

        m = m + 1

        i = 0
        if fum == 0:
            method = randint(1, 3)
        else:
            method = fum

        print("Starting {} iteration of faults. Fault starts at {};".format(m, faulty_start))
        print("the engine breaks at {} and is repaired at {}. Fault type was {}".format(broken_start, broken_end, method))

        for p in data0['output_power']:
            i = i + 1
            if (i > faulty_start) & (i < broken_start):
                if method == 1:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum1(maxPower)
                    data0.iloc[i, data0.columns.get_loc('state')] = 'f'
                elif method == 2:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum2(p, reduce)
                    data0.iloc[i, data0.columns.get_loc('state')] = 'f'
                elif method == 3:
                    data0.iloc[i, data0.columns.get_loc('output_power')] = fum3(p, offset)
                    data0.iloc[i, data0.columns.get_loc('state')] = 'f'
            elif (i >= broken_start) & (i < broken_end):
                data0.iloc[i, data0.columns.get_loc('output_power')] = 0
                data0.iloc[i, data0.columns.get_loc('state')] = 'r'
    return data0


def fault_detected(data, data_r, pos_det, repair_time=3):
    data_f = data.copy()
    gen = (i for i, x in enumerate(data_f['output_power']) if ((i >= pos_det) & (i < pos_det + 24 * repair_time)))
    for i in gen:
        data_f.iloc[i, data_f.columns.get_loc('output_power')] = 0
        data_f.iloc[i, data_f.columns.get_loc('state')] = 'r'
    i = 0
    for s in data_f['state']:
        if i >= pos_det + repair_time * 24:
            if s != 'w':
                data_f.iloc[i, data_f.columns.get_loc('output_power')] = data_r.iloc[
                    i, data_r.columns.get_loc('output_power')]
                data_f.iloc[i, data_f.columns.get_loc('state')] = 'w'
            else:
                return data_f
        i = i + 1
    return data_f


def server_error(data, dataR, pos_det, repair_time=3):  # TODO check this
    data_f = data.copy()
    gen = (i for i, x in enumerate(data_f['output_power']) if ((i >= pos_det) & (i < pos_det + 24 * repair_time)))
    for i in gen:
        data_f.iloc[i, data_f.columns.get_loc('output_power')] = 0
        data_f.iloc[i, data_f.columns.get_loc('state')] = 'r'
    return data_f
