def check_join(id):
    with open('info/doNotSend.txt', 'r') as joined:
        data = joined.readlines()
    if str(id) not in [x.rstrip('\n') for x in data]:
        joined.close()
        with open('info/doNotSend.txt', 'a') as joined:
            joined.write(str(id) + '\n')


def check_teacher(id):
    with open('info/teachers.txt', 'r') as file:
        teachers = file.readlines()
    if id in [int(x.split()[-1].rstrip('\n')) for x in teachers]:
        file.close()
        return True
    else:
        file.close()
        return False


def average(arr_str):
    arr = [int(x) for x in arr_str]
    av = sum(arr) / len(arr)
    return round(av, 2)
