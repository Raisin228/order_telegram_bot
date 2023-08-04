string = input()

print(all([1 if i == '.' or i.isdigit() else 0 for i in string]))
