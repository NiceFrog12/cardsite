#Импорт
from flask import Flask, render_template,request, redirect, url_for
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app)
#Создание таблицы

class Card(db.Model):
    #Создание полей
    #id
    id = db.Column(db.Integer, primary_key=True)
    #Заголовок
    title = db.Column(db.String(100), nullable=False)
    #Описание
    subtitle = db.Column(db.String(300), nullable=False)
    #Текст
    text = db.Column(db.Text, nullable=False)

    #Вывод объекта и id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Задание №1. Создать таблицу User

class User(db.Model):
    #userid
    id = db.Column(db.Integer, primary_key=True)
    #user email
    email = db.Column(db.String(50), nullable=False)
    #user password
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'





#Запуск страницы с контентом
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_email = request.form['email']
        form_password = request.form['password']
            
        #Задание №4. Реализовать проверку пользователей
        users_db = User.query.all()
        for user in users_db:
            if form_email == user.email and form_password == user.password:
                return redirect('/index')
        
        error = 'Неправильно указан пользователь или пароль'
        return render_template('login.html', error=error)

            
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        
        #Задание №3. Реализовать запись пользователей
        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


#Запуск страницы с контентом
@app.route('/index')
def index():
    #Отображение объектов из БД
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

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

        #Создание объкта для передачи в дб

        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')


@app.route('/delete/<id>', methods= ['POST'])
def form_delete(id):
    #im trying to delete this card, man T-T
    try:
        delete = Card.query.get(id)
        db.session.delete(delete)
        db.session.commit()
        return redirect('/index')
    except:
        pass
    
    return redirect('/index')
    
@app.route("/edit/<int:id>", methods=['POST'])
def cardedit(id):
    card = Card.query.get(id)
    return render_template('card_edit.html', card=card)

@app.route("/editthismf", methods = ['POST'])
def card_edit():
    # getting info out of the form to edit the card
    id = request.form['id']
    title = request.form['title']
    subtitle = request.form['subtitle']
    text = request.form['text']
    # update the card in the database
    card = Card.query.get(id)
    card.title = title
    card.subtitle = subtitle
    card.text = text
    db.session.commit()
    return redirect('/index')


if __name__ == "__main__":
    app.run(debug=True)
