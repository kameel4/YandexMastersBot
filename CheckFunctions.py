def check_join(id):
    with open('info/joined.txt', 'r') as joined:
        data = joined.readlines()
    if str(id) not in [x.rstrip('\n') for x in data]:
        joined.close()
        with open('info/joined.txt', 'a') as joined:
            joined.write(str(id) + '\n')


def check_teacher(id):
    with open('info/teachers.txt', 'r') as file:
        teachers = file.readlines()
    if id in [x.split()[-1].rstrip('\n') for x in teachers]:
        return True
    else:
        return False
