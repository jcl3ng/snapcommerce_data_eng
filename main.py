import pandas as pd


def clean_word_helper(s):
    return ''.join([i for i in s if i.isalpha()])


def get_first_valid(flight_code_lst):
    for i, code in enumerate(flight_code_lst):
        if code != '':
            return i, int(float(code))
    return -1, None


def clean_flight_code(flight_code_lst):
    pos, code = get_first_valid(flight_code_lst)

    if pos == -1:
        return False
    start = code if pos == 0 else code - (pos * 10)

    clean_lst = []
    for i, f_code in enumerate(flight_code_lst):
        if f_code == '':
            clean_lst.append(int(start + i*10))
            print(int(start + i*10))
        elif int(float(f_code)) != start + i*10:
            clean_lst.append(start + i*10)
        else:
            clean_lst.append(int(float(flight_code_lst[i])))
    return clean_lst


def clean_to_lst_from_lst(lst):
    for i, city in enumerate(lst):
        lst[i] = clean_word_helper(city).upper()


def clean_airline_code(airline_lst):
    for i, code in enumerate(airline_lst):
        lst = code.split(' ')
        temp = []
        for ele in lst:
            word = clean_word_helper(ele)
            if word != '':
                temp.append(word)
        airline_lst[i] = ' '.join(temp)


def get_data(data):
    air_code_lst = []
    delay_times = []
    flight_code_lst = []
    to_lst = []
    from_lst = []
    for row in data.split('\n')[1:]:
        col = row.split(';')
        if len(col) == 4:
            air_code_lst.append(col[0])
            delay_times.append(col[1])
            flight_code_lst.append(col[2])
            temp = col[3].split('_')
            to_lst.append(temp[0])
            from_lst.append(temp[1])
    return air_code_lst, delay_times, flight_code_lst, to_lst, from_lst


def etl(data):
    air_code_lst, delay_times, flight_code_lst, to_lst, from_lst = get_data(data)
    airplane_dict = {'Airline Code': air_code_lst, 'DelayTimes': delay_times, 'FlightCodes': flight_code_lst,
                     'To': to_lst, 'From': from_lst}
    clean_airline_code(airplane_dict['Airline Code'])
    clean_to_lst_from_lst(airplane_dict['To'])
    clean_to_lst_from_lst(airplane_dict['From'])

    check = clean_flight_code(airplane_dict['FlightCodes'])
    if not check:
        airplane_dict['FlightCodes'] = list(map(lambda x: 0, airplane_dict['FlightCodes']))
    else:
        airplane_dict['FlightCodes'] = check

    return pd.DataFrame.from_dict(airplane_dict)


