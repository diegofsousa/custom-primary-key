from dao import Students, list_all

diego = Students("Diego Fernando", "AC", 1)
diego.save()

a = list_all()
print(a)
