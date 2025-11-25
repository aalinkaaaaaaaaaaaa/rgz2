from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Book
from config import Config
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

#Создаем папки для загрузок
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#Декораторы контроля доступа
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему.', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('У вас нет прав доступа к этой странице.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

#Проверка файлов
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

#Передача данных во все шаблоны (тек пользователь и студент)
@app.context_processor
def inject_user_info():
    user_info = {}
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            user_info = {
                'username': user.username,
                'is_admin': user.is_admin
            }
    
    student_info = {
        'fio': 'Геворкян Алина Константиновна',
        'group': 'ФБИ-33'
    }
    
    return dict(user_info=user_info, student_info=student_info)

#Главная страница - список книг с фильтрацией
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    #Получаем параметры фильтрации
    title_filter = request.args.get('title', '')
    author_filter = request.args.get('author', '')
    publisher_filter = request.args.get('publisher', '')
    min_pages = request.args.get('min_pages', type=int)
    max_pages = request.args.get('max_pages', type=int)
    sort_by = request.args.get('sort_by', 'title')
    sort_order = request.args.get('sort_order', 'asc')
    
    #Базовый запрос
    books_query = Book.query
    
    #Применяем фильтры
    if title_filter:
        books_query = books_query.filter(Book.title.ilike(f'%{title_filter}%'))
    if author_filter:
        books_query = books_query.filter(Book.author.ilike(f'%{author_filter}%'))
    if publisher_filter:
        books_query = books_query.filter(Book.publisher.ilike(f'%{publisher_filter}%'))
    if min_pages:
        books_query = books_query.filter(Book.pages >= min_pages)
    if max_pages:
        books_query = books_query.filter(Book.pages <= max_pages)
    
    #Применяем сортировку
    if sort_order == 'desc':
        books_query = books_query.order_by(getattr(Book, sort_by).desc())
    else:
        books_query = books_query.order_by(getattr(Book, sort_by).asc())
    
    #Пагинация
    books = books_query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('index.html', books=books, filters=request.args)

#Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    #Валидация
    if not username or not password:
        flash('Все поля обязательны для заполнения', 'danger')
        return render_template('register.html')
    
    if password != confirm_password:
        flash('Пароли не совпадают', 'danger')
        return render_template('register.html')
    
    #Проверка валидности логина и пароля
    if not User.is_valid_username(username):
        flash('Логин должен содержать только латинские буквы, цифры и знаки препинания', 'danger')
        return render_template('register.html')
    
    if not User.is_valid_password(password):
        flash('Пароль должен содержать только латинские буквы, цифры и знаки препинания', 'danger')
        return render_template('register.html')
    
    #Проверка существующего пользователя
    if User.query.filter_by(username=username).first():
        flash('Пользователь с таким именем уже существует', 'danger')
        return render_template('register.html')
    
    #Создание пользователя
    user = User(username=username)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
    return redirect(url_for('login'))

#Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        session['user_id'] = user.id
        flash(f'Добро пожаловать, {username}!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Неверное имя пользователя или пароль', 'danger')
        return render_template('login.html')

#Выход
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('index'))

#Профиль пользователя
@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

#Удаление аккаунта
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(session['user_id'])
    
    #Администратор не может удалить себя через эту функцию
    if user.is_admin:
        flash('Администратор не может удалить свою учетную запись', 'danger')
        return redirect(url_for('profile'))
    
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id', None)
    flash('Ваш аккаунт был успешно удален', 'info')
    return redirect(url_for('index'))

#Админ-панель - главная
@app.route('/admin')
@admin_required
def admin_dashboard():
    stats = {
        'total_books': Book.query.count(),
        'total_users': User.query.count(),
        'total_admins': User.query.filter_by(is_admin=True).count()
    }
    return render_template('admin/dashboard.html', stats=stats)

#Админ-панель - список книг
@app.route('/admin/books')
@admin_required
def admin_books():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    books = Book.query.order_by(Book.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/books.html', books=books)

#Админ-панель - добавление книги
@app.route('/admin/books/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'GET':
        return render_template('admin/add_book.html')
    
    title = request.form.get('title')
    author = request.form.get('author')
    pages = request.form.get('pages', type=int)
    publisher = request.form.get('publisher')
    description = request.form.get('description')
    
    #Валидация
    if not title or not author or not pages or not publisher:
        flash('Все обязательные поля должны быть заполнены', 'danger')
        return render_template('admin/add_book.html')
    
    if pages <= 0:
        flash('Количество страниц должно быть положительным числом', 'danger')
        return render_template('admin/add_book.html')
    
    book = Book(
        title=title,
        author=author,
        pages=pages,
        publisher=publisher,
        description=description
    )
    
    #Обработка загрузки обложки
    if 'cover_image' in request.files:
        file = request.files['cover_image']
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                book.cover_image = filename
            else:
                flash('Недопустимый формат файла. Разрешены: png, jpg, jpeg, gif', 'warning')
    
    db.session.add(book)
    db.session.commit()
    
    flash('Книга успешно добавлена!', 'success')
    return redirect(url_for('admin_books'))

#Админ-панель - редактирование книги
@app.route('/admin/books/edit/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'GET':
        return render_template('admin/edit_book.html', book=book)
    
    book.title = request.form.get('title')
    book.author = request.form.get('author')
    book.pages = request.form.get('pages', type=int)
    book.publisher = request.form.get('publisher')
    book.description = request.form.get('description')
    
    #Валидация
    if not book.title or not book.author or not book.pages or not book.publisher:
        flash('Все обязательные поля должны быть заполнены', 'danger')
        return render_template('admin/edit_book.html', book=book)
    
    if book.pages <= 0:
        flash('Количество страниц должно быть положительным числом', 'danger')
        return render_template('admin/edit_book.html', book=book)
    
    #Обработка загрузки обложки
    if 'cover_image' in request.files:
        file = request.files['cover_image']
        if file and file.filename != '':
            if allowed_file(file.filename):
                #Удаляем старую обложку если она не дефолтная
                if book.cover_image != 'default-cover.jpg':
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], book.cover_image)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                book.cover_image = filename
            else:
                flash('Недопустимый формат файла. Разрешены: png, jpg, jpeg, gif', 'warning')
    
    db.session.commit()
    flash('Книга успешно обновлена!', 'success')
    return redirect(url_for('admin_books'))

#Админ-панель - удаление книги
@app.route('/admin/books/delete/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    #Удаляем файл обложки если он не дефолтный
    if book.cover_image != 'default-cover.jpg':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], book.cover_image)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(book)
    db.session.commit()
    
    flash('Книга успешно удалена!', 'success')
    return redirect(url_for('admin_books'))

if __name__ == '__main__':
    app.run(debug=True)