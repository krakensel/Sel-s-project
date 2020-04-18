from flask import Flask, request, make_response, jsonify
import sqlite3
import random
conn = sqlite3.connect("materials.db", check_same_thread=False)
cursor = conn.cursor()


app = Flask(__name__)

q = {
    "В каком году было крещение Руси?: а)988 б)899": "а",
    "В каком году было крещение Руси?2: а)988 б)899": "а",
    "В каком году было крещение Руси?2: а)988 б)899": "а",
    "В каком году было крещение Руси?2: а)988 б)899": "а",
}

@app.route('/',)
def all():
    cursor.execute("SELECT * FROM Links ")
    data = cursor.fetchall()

    page = "<table>"
    for row in data:
        page += "<tr>"
        for column in row:
            page += "<td>" + str(column) + "</td>"
        page += "</tr>"
    page += "</table>"
    return page


@app.route('/add', methods=["GET","POST"])
def add():
    if request.method == "POST":
        sphere = request.form ["sphere"]
        level = request.form['level']
        tip = request.form['tip']
        link = request.form['link']
        cursor.execute(f"INSERT INTO Links(sphere, level,type, link) VALUES ('{sphere}','{level}','{tip}','{link}')")
        conn.commit()
        return "Added!"
    else:
        page = '''
        <form method="post">
            <label>Сфера</label> <br>
            <input type='text' name ='sphere' ></input> <br>
            <label>Уровень</label> <br>
            <input type='text'name = 'level' ></input> <br>
            <label>Тип</label> <br>
            <input type='text' name = 'tip'></input> <br>
            <label>Ссылка</label> <br>
            <input type='text' name = 'link'></input> <br>

            <input type = 'submit'>
        </form>
        '''
        return page

@app.route('/delete', methods=["GET","POST"])
def delete():
    if request.method == "POST":
        material_id = request.form['id']

        cursor.execute(f"DELETE FROM Links WHERE id={material_id}")
        conn.commit()
        return "Deleted!"
    else:
        page = '''
        <form method="post">
            <label>Удалить материал</label> <br>
            <input type='number' name ='id' ></input> <br>
            

            <input type = 'submit'>
        </form>
        '''
        return page

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    
    action = req.get('queryResult').get('action')
    

    if action == 'get_material':
        sphr = req.get('queryResult').get('parameters').get('sphere')
        lvl = req.get('queryResult').get('parameters').get('level')
        res = get_material(sphr, lvl)
    elif action == "motivation":
        res = get_motivation()
    elif action == 'birthday':
        date = req.get('queryResult').get('outputContexts')[0].get('parameters').get('date')
        res = count_days(date)
    else:
        res = 'hi'

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))
def count_days(date):

    return date+"!"

def get_motivation():
    frases =[
        "«Если вы не готовы рискнуть обычным, вам придется довольствоваться заурядным», — Джим Рон.",
        "«Нет ничего невозможного. Само слово говорит: „Я возможно!“ (Impossible — I'm possible)», — Одри Хепбёрн.",
        "«Хотите знать, кто вы? Не спрашивайте. Действуйте! Действие будет описывать и определять вас», — Томас Джефферсон.",
        "«Если вы думаете, что способны выполнить что-то, или думаете, что не способны на это, вы правы в обоих случаях», — Генри Форд.",
        "«Великие умы обсуждают идеи. Средние умы обсуждают события. Маленькие умы обсуждают людей», — Элеонора Рузвельт.",
        "«Если вы работаете над тем, что для вас действительно важно, вас не приходится подгонять. Вас тянет вперед ваша мечта», — Стив Джобс.",
        "«А сегодня в завтрашний день не все могут смотреть. Вернее, смотреть могут не только лишь все, мало кто может это делать.» - Кличко.",
        "«В Одесской области город, пятьдесят километров, недалеко… Пятьдесят километров… Знаете, не в километрах расстояние измеряется. Два часа! Пятьдесят километров нужно ехать два часа»."
        ]
    # s = ['','','']
    # res = s[random.randit(0, len(s))]
    #return res
    res = random.choice(frases)
    return res


def get_material(s, lvl, t="-"):
    if t == "-":
        sql = f"SELECT link FROM Links WHERE sphere='{s}' AND level='{lvl}'"
    else:
        sql = f"SELECT link FROM Links WHERE sphere='{s}' AND level='{lvl}' AND type='{t}'"
    cursor.execute(sql)
    if cursor.fetchone() == None:
        card = "К сожалению, в базе нет такого материала."
    else:
        res = cursor.fetchone()[0]
        card = f"Вот материал по теме {s} уровня {lvl}: {res}"
    return card

def quest():
    qst = list(q.keys())[random.randint(0,len(q)-1)]
    print(qst)
    answer(qst)
def answer(qst):
    ans = input("Ответ - ")
    if ans == q[qst]:
        print("Правильно")
    else:
        print("Неправильно")

if __name__ == '__main__':
    app.run(debug=True)
    
