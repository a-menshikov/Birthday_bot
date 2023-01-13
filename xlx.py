# file = open('Книга3.xlsx', 'r', encoding='ANSI')
# x = file.readline()

codecs = ["cp1252", "cp437", "utf-16be", "utf-16", "utf-8"]

with open("Книга3.xlsx", "r", encoding="iso_8859_1") as file:
    text = file.read()
print(text)