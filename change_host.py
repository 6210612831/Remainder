with open('./task/views_fronts.py', 'r') as file:
    data = file.readlines()

if data[11] == 'HOST = "https://reminder-white.herokuapp.com"\n':
    data[11] = 'HOST = "http://127.0.0.1:8000"\n'
else:
    data[11] = 'HOST = "https://reminder-white.herokuapp.com"\n'

with open('./task/views_fronts.py', 'w') as file:
    file.writelines( data )



with open('./task/templates/task/index.html', 'r') as file:
    data = file.readlines()

if data[110] == 'var HOST = "https://reminder-white.herokuapp.com"\n':
    data[110] = 'var HOST = "http://127.0.0.1:8000"\n'
else:
    data[110] = 'var HOST = "https://reminder-white.herokuapp.com"\n'

with open('./task/templates/task/index.html', 'w') as file:
    file.writelines( data )