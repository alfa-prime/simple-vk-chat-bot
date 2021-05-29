data = dict(age=dict(value=None, message='Возраст'), city=dict(value='Мурманск', message='Город'))

print(data)

temp = {key: value['message'] for key, value in data.items() if value['value'] is None}
print(temp)