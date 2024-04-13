#Импорт
from flask import Flask, render_template,request, redirect
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app )

#Задание №1. Создай таблицу БД

class Card(db.Model):
    #nullable means if its HAS to be filled, false meaning that user HAS TO fill it in
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
            return f'<Card {self.id}>'




#Запуск страницы с контентом
@app.route('/')
def index():
    #Отображение объектов из БД
    #Задание №2. Отоброзить объекты из БД в index.html
    cards = Card.query.all()

    return render_template('index.html',
                           cards = cards
                           )

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    #Задание №2. Отоброзить нужную карточку по id
    card = Card.query.get(id)

    return render_template('card.html', card=card)

def form_delete(id):
    #im trying to delete this card, man T-T
    if request.method == 'SUBMIT':
        cards = Card.query.all()
        card = Card.query.get(id)
        db.session.delete(card)
        db.session.commit()
        return render_template('index.html', cards = cards)
    else:
        #this is more of a fail state
        return redirect ('/')

#Запуск страницы c созданием карты
@app.route('/create')
def create():
    return render_template('create_card.html')

#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        #Задание №2. Создайте сопосб записи данных в БД

        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()       



        return redirect('/')
    else:
        return render_template('create_card.html')





if __name__ == "__main__":
    app.run(debug=True)