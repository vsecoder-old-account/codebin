import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('readme.js', 'let hi = `Привет, я Всеволод html - разработчик CodeBin,\nэто того рода хранилище для вашего кода, \nкуда Вы можете сохранить код, и поделиться им с друзьями.\nДокументация:\nhttps://codebinpy.herokuapp.com/docs\n  или\nhttps://codebinpy.herokuapp.com/2`;\nconsole.log(hi);')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('documentation.js', 'let docs = `\n<h1>Документация:</h1>\n<h2>Всё легко, и поймёт даже ребёнок!</h2>\n<p>\n  Нажми на "+" внизу справа, заполни поля "Заголовок" и "Код", \n  заверши всё нажатием на кнопку "Создать", и с того момента Вы имеете страницу своего кода!\n</p>`;\ndocument.write(docs);')
            )

connection.commit()
connection.close()