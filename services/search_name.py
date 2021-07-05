MAX_POINT_NAME = 50

def get_distance(name1, name2):
    # init arr
    list_str_1 = name1.lower().split('.')
    list_str_2 = name2.lower().split('.')

    len_list_1 = len(list_str_1)
    len_list_2 = len(list_str_2)
    
    similar = {}

    for i in range(-1, len_list_1):
        similar[i] = {}
        for j in range(-1, len_list_2):
            similar[i][j] = 0

    # find similar str
    for i in range(0, len_list_1):
        for j in range(0, len_list_2):
            similar[i][j] = max_2_int(similar[i-1][j], similar[i][j-1])
            if (list_str_1[i] == list_str_2[j]):
                similar[i][j] = max_2_int(similar[i][j], similar[i-1][j-1]+1)
    
    global MAX_POINT_NAME

    distance_point = (1 - 2.0 * similar[len_list_1-1][len_list_2-1] / (len_list_1 + len_list_2)) * MAX_POINT_NAME

    print(f'name1 = {name1} ; name2 = {name2} ; similar = {similar[len_list_1-1][len_list_2-1]} ; point = {distance_point}')

    return distance_point


def max_2_int(a, b):
    if a > b:
        return a
    else:
        return b