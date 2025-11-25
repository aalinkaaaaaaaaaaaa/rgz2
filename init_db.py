from app import app, db
from models import User, Book
import os

def init_database():
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                is_admin=True
            )
            admin.set_password('Admin123!')
            db.session.add(admin)
            db.session.commit()
            print('Администратор создан: admin / Admin123!')
        
        if Book.query.count() == 0:
            real_books = [
                #Классическая литература
                Book(title='Анна Каренина', author='Лев Толстой', pages=864, publisher='Азбука',
                    description='Трагическая история любви замужней женщины.', cover_image='anna-karenina.jpg'),
                Book(title='Белая гвардия', author='Михаил Булгаков', pages=384, publisher='Азбука',
                    description='Роман о Гражданской войне на Украине.', cover_image='white-guard.jpg'),
                Book(title='Братья Карамазовы', author='Федор Достоевский', pages=1024, publisher='АСТ',
                    description='Последний роман Достоевского о вере и сомнении.', cover_image='brothers-karamazov.jpg'),
                Book(title='Война и мир', author='Лев Толстой', pages=1225, publisher='Речь',
                    description='Эпопея о русском обществе во время наполеоновских войн.', cover_image='war-peace.jpg'),
                Book(title='Герой нашего времени', author='Михаил Лермонтов', pages=320, publisher='Эксмо',
                    description='Психологический роман о Печорине.', cover_image='hero-time.jpg'),
                Book(title='Горе от ума', author='Александр Грибоедов', pages=256, publisher='Эксмо',
                    description='Комедия в стихах о конфликте поколений.', cover_image='woe-wit.jpg'),
                Book(title='Доктор Живаго', author='Борис Пастернак', pages=608, publisher='Эксмо',
                    description='Роман о судьбе интеллигенции в революцию.', cover_image='doctor-zhivago.jpg'),
                Book(title='Евгений Онегин', author='Александр Пушкин', pages=288, publisher='АСТ',
                    description='Роман в стихах о любви и судьбе.', cover_image='onegin.jpg'),
                Book(title='Идиот', author='Федор Достоевский', pages=640, publisher='Эксмо',
                    description='Роман о "положительно прекрасном человеке".', cover_image='idiot.jpg'),
                Book(title='Мастер и Маргарита', author='Михаил Булгаков', pages=480, publisher='АСТ',
                    description='Великий роман о любви, искусстве и борьбе добра со злом.', cover_image='master-margarita.jpg'),
                Book(title='Мертвые души', author='Николай Гоголь', pages=352, publisher='АСТ',
                    description='Поэма о русской жизни и характере.', cover_image='dead-souls.jpg'),
                Book(title='Обломов', author='Иван Гончаров', pages=576, publisher='Азбука',
                    description='Роман о русской лени и "обломовщине".', cover_image='oblomov.jpg'),
                Book(title='Отцы и дети', author='Иван Тургенев', pages=320, publisher='Эксмо',
                    description='Роман о конфликте поколений в России XIX века.', cover_image='fathers-sons.jpg'),
                Book(title='Преступление и наказание', author='Федор Достоевский', pages=672, publisher='Эксмо',
                    description='Психологический роман о моральных дилеммах и redemption.', cover_image='crime-punishment.jpg'),
                Book(title='Ревизор', author='Николай Гоголь', pages=192, publisher='Азбука',
                    description='Комедия о чиновничьем произволе.', cover_image='inspector.jpg'),
                Book(title='Тихий Дон', author='Михаил Шолохов', pages=1504, publisher='Эксмо',
                    description='Эпопея о жизни донского казачества.', cover_image='quiet-don.jpg'),

                #Зарубежная классика
                Book(title='1984', author='Джордж Оруэлл', pages=328, publisher='Penguin Books',
                    description='Антиутопия о тоталитарном обществе и контроле над сознанием.', cover_image='1984.jpg'),
                Book(title='451° по Фаренгейту', author='Рэй Брэдбери', pages=256, publisher='Эксмо',
                    description='Антиутопия о обществе, где книги запрещены.', cover_image='fahrenheit451.jpg'),
                Book(title='Великий Гэтсби', author='Фрэнсис Скотт Фицджеральд', pages=256, publisher='АСТ',
                    description='Роман о "американской мечте" и ее иллюзорности.', cover_image='great-gatsby.jpg'),
                Book(title='Гамлет', author='Уильям Шекспир', pages=256, publisher='АСТ',
                    description='Трагедия о датском принце.', cover_image='hamlet.jpg'),
                Book(title='Доктор Фаустус', author='Томас Манн', pages=672, publisher='АСТ',
                    description='Роман о гении, продавшем душу дьяволу.', cover_image='doctor-faustus.jpg'),
                Book(title='Лолита', author='Владимир Набоков', pages=448, publisher='Азбука',
                    description='Скандальный роман о запретной любви.', cover_image='lolita.jpg'),
                Book(title='Маленький принц', author='Антуан де Сент-Экзюпери', pages=96, publisher='Эксмо',
                    description='Философская сказка для детей и взрослых.', cover_image='little-prince.jpg'),
                Book(title='Над пропастью во ржи', author='Джером Сэлинджер', pages=288, publisher='Эксмо',
                    description='История подростка Холдена Колфилда и его бунта против общества.', cover_image='catcher-rye.jpg'),
                Book(title='О дивный новый мир', author='Олдос Хаксли', pages=320, publisher='АСТ',
                    description='Антиутопия о технологическом контроле над обществом.', cover_image='brave-new-world.jpg'),
                Book(title='Повелитель мух', author='Уильям Голдинг', pages=320, publisher='АСТ',
                    description='Роман о группе детей, оставшихся на необитаемом острове.', cover_image='lord-flies.jpg'),
                Book(title='Портрет Дориана Грея', author='Оскар Уайльд', pages=320, publisher='Эксмо',
                    description='Роман о красоте, морали и вечной молодости.', cover_image='dorian-gray.jpg'),
                Book(title='Процесс', author='Франц Кафка', pages=320, publisher='Азбука',
                    description='Абсурдистский роман о бюрократической машине.', cover_image='trial.jpg'),
                Book(title='Ромео и Джульетта', author='Уильям Шекспир', pages=192, publisher='Эксмо',
                    description='История трагической любви.', cover_image='romeo-juliet.jpg'),
                Book(title='Сто лет одиночества', author='Габриэль Гарсиа Маркес', pages=544, publisher='АСТ',
                    description='Магический реализм о семье Буэндиа.', cover_image='hundred-years.jpg'),
                Book(title='Три товарища', author='Эрих Мария Ремарк', pages=480, publisher='АСТ',
                    description='Роман о дружбе и любви в послевоенной Германии.', cover_image='three-comrades.jpg'),
                Book(title='Унесенные ветром', author='Маргарет Митчелл', pages=1024, publisher='Эксмо',
                    description='История жизни Скарлетт О`Хара во время Гражданской войны в США.', cover_image='gone-wind.jpg'),
                Book(title='Цветы зла', author='Шарль Бодлер', pages=256, publisher='Азбука',
                    description='Сборник стихов французского поэта.', cover_image='flowers-evil.jpg'),

                #Фэнтези
                Book(title='Ведьмак: Последнее желание', author='Анджей Сапковский', pages=384, publisher='АСТ',
                    description='Первая книга саги о ведьмаке Геральте.', cover_image='witcher1.jpg'),
                Book(title='Властелин колец: Братство кольца', author='Джон Р. Р. Толкин', pages=576, publisher='АСТ',
                    description='Эпическая фэнтези-сага о Средиземье.', cover_image='lotr1.jpg'),
                Book(title='Властелин колец: Две крепости', author='Джон Р. Р. Толкин', pages=448, publisher='АСТ',
                    description='Вторая часть трилогии "Властелин колец".', cover_image='lotr2.jpg'),
                Book(title='Гарри Поттер и философский камень', author='Джоан Роулинг', pages=432, publisher='Росмэн',
                    description='Первая книга о юном волшебнике Гарри Поттере.', cover_image='harry-potter1.jpg'),
                Book(title='Гарри Поттер и Тайная комната', author='Джоан Роулинг', pages=480, publisher='Росмэн',
                    description='Вторая книга о приключениях Гарри Поттера.', cover_image='harry-potter2.jpg'),
                Book(title='Гарри Поттер и узник Азкабана', author='Джоан Роулинг', pages=528, publisher='Росмэн',
                    description='Третья книга о приключениях Гарри Поттера.', cover_image='harry-potter3.jpg'),
                Book(title='Гарри Поттер и Кубок огня', author='Джоан Роулинг', pages=672, publisher='Росмэн',
                    description='Четвертая книга о приключениях Гарри Поттера.', cover_image='harry-potter4.jpg'),
                Book(title='Гарри Поттер и Орден Феникса', author='Джоан Роулинг', pages=768, publisher='Росмэн',
                    description='Пятая книга о приключениях Гарри Поттера.', cover_image='harry-potter5.jpg'),
                Book(title='Игра престолов', author='Джордж Р. Р. Мартин', pages=864, publisher='Эксмо',
                    description='Первая книга эпической саги "Песнь льда и пламени".', cover_image='game-thrones.jpg'),
                Book(title='Хоббит', author='Джон Р. Р. Толкин', pages=384, publisher='АСТ',
                    description='Приключения Бильбо Бэггинса в поисках сокровищ.', cover_image='hobbit.jpg'),
                Book(title='Хроники Нарнии', author='Клайв Стейплз Льюис', pages=768, publisher='Эксмо',
                    description='Сборник фэнтезийных повестей о волшебной стране.', cover_image='narnia.jpg'),

                #Научная фантастика
                Book(title='Автостопом по галактике', author='Дуглас Адамс', pages=256, publisher='Азбука',
                    description='Юмористическая научно-фантастическая сага.', cover_image='hitchhiker-galaxy.jpg'),
                Book(title='Дюна', author='Фрэнк Герберт', pages=704, publisher='АСТ',
                    description='Эпическая научно-фантастическая сага о планете Арракис.', cover_image='dune.jpg'),
                Book(title='Марсианин', author='Энди Вейер', pages=384, publisher='АСТ',
                    description='Роман о выживании астронавта на Марсе.', cover_image='martian.jpg'),
                Book(title='Основание', author='Айзек Азимов', pages=320, publisher='Эксмо',
                    description='Первая книга цикла о Галактической Империи.', cover_image='foundation.jpg'),
                Book(title='Солярис', author='Станислав Лем', pages=288, publisher='АСТ',
                    description='Философская научная фантастика о контакте с разумным океаном.', cover_image='solaris.jpg'),
                Book(title='Мы', author='Евгений Замятин', pages=288, publisher='Азбука',
                    description='Первая антиутопия в мировой литературе.', cover_image='we.jpg'),

                #Детективы и триллеры
                Book(title='Девушка с татуировкой дракона', author='Стиг Ларссон', pages=542, publisher='Эксмо',
                    description='Первая книга трилогии "Миллениум".', cover_image='dragon-tattoo.jpg'),
                Book(title='Девушка в паутине', author='Давид Лагеркранц', pages=480, publisher='Эксмо',
                    description='Продолжение трилогии "Миллениум".', cover_image='girl-spider.jpg'),
                Book(title='Десять негритят', author='Агата Кристи', pages=256, publisher='Эксмо',
                    description='Детектив о таинственных убийствах на острове.', cover_image='ten-little.jpg'),
                Book(title='Заводной апельсин', author='Энтони Бёрджесс', pages=272, publisher='АСТ',
                    description='Антиутопия о молодежной преступности.', cover_image='clockwork-orange.jpg'),
                Book(title='Исчезнувшая', author='Гиллиан Флинн', pages=512, publisher='Эксмо',
                    description='Психологический триллер о пропавшей жене.', cover_image='gone-girl.jpg'),
                Book(title='Код да Винчи', author='Дэн Браун', pages=544, publisher='АСТ',
                    description='Интеллектуальный детектив о тайнах истории.', cover_image='da-vinci-code.jpg'),
                Book(title='Молчание ягнят', author='Томас Харрис', pages=448, publisher='Эксмо',
                    description='Психологический триллер о серийном убийце.', cover_image='silence-lambs.jpg'),
                Book(title='Убийство в Восточном экспрессе', author='Агата Кристи', pages=320, publisher='Эксмо',
                    description='Знаменитый детектив Эркюля Пуаро расследует убийство в поезде.', cover_image='orient-express.jpg'),
                Book(title='Убийство Роджера Экройда', author='Агата Кристи', pages=320, publisher='Эксмо',
                    description='Один из лучших детективов Кристи.', cover_image='roger-ackroyd.jpg'),
                Book(title='Шерлок Холмс: Собака Баскервилей', author='Артур Конан Дойл', pages=288, publisher='Азбука',
                    description='Самое известное дело Шерлока Холмса.', cover_image='sherlock-holmes.jpg'),

                #Приключения
                Book(title='Граф Монте-Кристо', author='Александр Дюма', pages=1248, publisher='Азбука',
                    description='Роман о мести и справедливости.', cover_image='monte-cristo.jpg'),
                Book(title='Дети капитана Гранта', author='Жюль Верн', pages=640, publisher='АСТ',
                    description='Кругосветное путешествие в поисках пропавшего капитана.', cover_image='captain-grant.jpg'),
                Book(title='Остров сокровищ', author='Роберт Льюис Стивенсон', pages=320, publisher='Эксмо',
                    description='Приключенческий роман о поисках пиратского клада.', cover_image='treasure-island.jpg'),
                Book(title='Робинзон Крузо', author='Даниель Дефо', pages=384, publisher='АСТ',
                    description='История выживания на необитаемом острове.', cover_image='robinson-crusoe.jpg'),
                Book(title='Три мушкетера', author='Александр Дюма', pages=768, publisher='Эксмо',
                    description='Приключения гасконца д`Артаньяна и его друзей.', cover_image='three-musketeers.jpg'),

                #Детская литература
                Book(title='Алиса в Стране чудес', author='Льюис Кэрролл', pages=192, publisher='Эксмо',
                    description='Сказка о приключениях девочки Алисы.', cover_image='alice-wonderland.jpg'),
                Book(title='Винни-Пух и все-все-все', author='Алан Милн', pages=256, publisher='Азбука',
                    description='Приключения медвежонка Винни-Пуха и его друзей.', cover_image='winnie-pooh.jpg'),
                Book(title='Малыш и Карлсон, который живет на крыше', author='Астрид Линдгрен', pages=192, publisher='АСТ',
                    description='История о маленьком пропеллерном человечке.', cover_image='carlson.jpg'),
                Book(title='Пеппи Длинныйчулок', author='Астрид Линдгрен', pages=224, publisher='Эксмо',
                    description='Приключения самой сильной девочки в мире.', cover_image='pippi.jpg'),
                Book(title='Приключения Гекльберри Финна', author='Марк Твен', pages=320, publisher='Эксмо',
                    description='Продолжение приключений друга Тома Сойера.', cover_image='huck-finn.jpg'),
                Book(title='Приключения Тома Сойера', author='Марк Твен', pages=288, publisher='АСТ',
                    description='История о похождениях мальчика из провинциального городка.', cover_image='tom-sawyer.jpg'),

                #Современная проза
                Book(title='Авиатор', author='Евгений Водолазкин', pages=384, publisher='АСТ',
                    description='Роман о человеке, пролежавшем в анабиозе 70 лет.', cover_image='aviator.jpg'),
                Book(title='Атлант расправил плечи', author='Айн Рэнд', pages=1392, publisher='Альпина Паблишер',
                    description='Философский роман об объективизме.', cover_image='atlas-shrugged.jpg'),
                Book(title='Дом в котором...', author='Мариам Петросян', pages=960, publisher='Гаятри',
                    description='Роман о подростках в интернате для детей-инвалидов.', cover_image='house-which.jpg'),
                Book(title='Жизнь Пи', author='Янн Мартел', pages=464, publisher='Азбука',
                    description='История выживания в океане с тигром.', cover_image='life-pi.jpg'),
                Book(title='Зеленая миля', author='Стивен Кинг', pages=384, publisher='АСТ',
                    description='Тюремная драма с элементами фэнтези.', cover_image='green-mile.jpg'),
                Book(title='Зулейха открывает глаза', author='Гузель Яхина', pages=512, publisher='АСТ',
                    description='История раскулаченной татарки.', cover_image='zuleikha.jpg'),
                Book(title='Книжный вор', author='Маркус Зусак', pages=576, publisher='Эксмо',
                    description='История девочки в нацистской Германии.', cover_image='book-thief.jpg'),
                Book(title='Лавр', author='Евгений Водолазкин', pages=448, publisher='АСТ',
                    description='Роман о средневековом целителе.', cover_image='laurel.jpg'),
                Book(title='Метро 2033', author='Дмитрий Глуховский', pages=448, publisher='АСТ',
                    description='Постапокалиптический роман о жизни в московском метро.', cover_image='metro2033.jpg'),
                Book(title='Ночной цирк', author='Эрин Моргенштерн', pages=512, publisher='Эксмо',
                    description='Волшебная история о загадочном цирке.', cover_image='night-circus.jpg'),
                Book(title='Норвежский лес', author='Харуки Мураками', pages=400, publisher='Эксмо',
                    description='История любви и потерь в Японии 1960-х.', cover_image='norwegian-wood.jpg'),
                Book(title='Тень горы', author='Грегори Дэвид Робертс', pages=576, publisher='Азбука',
                    description='Продолжение романа "Шантарам".', cover_image='shadow-mountain.jpg'),
                Book(title='Щегол', author='Донна Тартт', pages=832, publisher='АСТ',
                    description='Роман о мальчике, пережившем теракт.', cover_image='goldfinch.jpg'),

                #Современная русская литература
                Book(title='Generation П', author='Виктор Пелевин', pages=416, publisher='Эксмо',
                    description='Роман о поколении 1990-х.', cover_image='generation-p.jpg'),
                Book(title='Чапаев и Пустота', author='Виктор Пелевин', pages=448, publisher='Эксмо',
                    description='Философский роман о реальности и иллюзиях.', cover_image='chapaev.jpg'),

                #Романы о войне
                Book(title='А зори здесь тихие', author='Борис Васильев', pages=192, publisher='Эксмо',
                    description='Повесть о женщинах-зенитчицах.', cover_image='dawn-quiet.jpg'),
                Book(title='В списках не значился', author='Борис Васильев', pages=224, publisher='АСТ',
                    description='Роман о защитниках Брестской крепости.', cover_image='not-listed.jpg'),
                Book(title='Жизнь и судьба', author='Василий Гроссман', pages=880, publisher='АСТ',
                    description='Эпопея о Сталинградской битве.', cover_image='life-fate.jpg'),
                Book(title='Момент истины', author='Владимир Богомолов', pages=480, publisher='АСТ',
                    description='Роман о работе военной контрразведки.', cover_image='moment-truth.jpg'),
                Book(title='Прокляты и убиты', author='Виктор Астафьев', pages=832, publisher='АСТ',
                    description='Роман о Великой Отечественной войне.', cover_image='cursed-killed.jpg'),

                #Драматургия
                Book(title='Вишневый сад', author='Антон Чехов', pages=128, publisher='Азбука',
                    description='Пьеса о закате дворянской культуры.', cover_image='cherry-orchard.jpg'),
                Book(title='На дне', author='Максим Горький', pages=160, publisher='Эксмо',
                    description='Пьеса о жизни обитателей ночлежки.', cover_image='lower-depths.jpg'),
                Book(title='Три сестры', author='Антон Чехов', pages=144, publisher='АСТ',
                    description='Драма о мечтах и реальности.', cover_image='three-sisters.jpg'),

                #Поэзия
                Book(title='Облако в штанах', author='Владимир Маяковский', pages=192, publisher='АСТ',
                    description='Поэма о любви и революции.', cover_image='cloud-pants.jpg'),
                Book(title='Реквием. Стихотворения и поэмы', author='Анна Ахматова', pages=448, publisher='Эксмо',
                    description='Сборник стихотворений великой поэтессы.', cover_image='akhmatova.jpg'),
                Book(title='Стихотворения', author='Сергей Есенин', pages=384, publisher='АСТ',
                    description='Лирика русского поэта.', cover_image='esenin.jpg'),

                #Психология и саморазвитие
                Book(title='7 навыков высокоэффективных людей. Краткая версия', author='Стивен Кови', pages=384, publisher='Альпина Паблишер',
                    description='Классика литературы по саморазвитию.', cover_image='7-habits.jpg'),
                Book(title='Атомные привычки', author='Джеймс Клир', pages=320, publisher='Манн, Иванов и Фербер',
                    description='Как приобретать хорошие привычки и избавляться от плохих.', cover_image='atomic-habits.jpg'),
                Book(title='Богатый папа, бедный папа', author='Роберт Кийосаки', pages=352, publisher='Попурри',
                    description='Финансовая грамотность для всех.', cover_image='rich-dad.jpg'),
                Book(title='Думай и богатей', author='Наполеон Хилл', pages=352, publisher='Попурри',
                    description='Классика мотивационной литературы.', cover_image='think-grow-rich.jpg'),
                Book(title='Как завоевывать друзей и оказывать влияние на людей', author='Дейл Карнеги', pages=320, publisher='Попурри',
                    description='Бестселлер о навыках общения.', cover_image='how-to-win-friends.jpg'),

                #Научпоп
                Book(title='Космос', author='Карл Саган', pages=528, publisher='Альпина нон-фикшн',
                    description='Исследование Вселенной и места человека в ней.', cover_image='cosmos.jpg'),
                Book(title='Краткая история времени', author='Стивен Хокинг', pages=272, publisher='АСТ',
                    description='От Большого взрыва до черных дыр.', cover_image='brief-history-time.jpg'),
                Book(title='Sapiens: Краткая история человечества', author='Юваль Ной Харари', pages=520, publisher='Синдбад',
                    description='Эволюция человеческого вида.', cover_image='sapiens.jpg'),
                Book(title='Физика невозможного', author='Митио Каку', pages=352, publisher='Альпина нон-фикшн',
                    description='Научный анализ технологий будущего.', cover_image='physics-impossible.jpg'),
                Book(title='Эгоистичный ген', author='Ричард Докинз', pages=512, publisher='АСТ',
                    description='Революционный взгляд на эволюцию.', cover_image='selfish-gene.jpg'),

                #Исторические романы
                Book(title='В круге первом', author='Александр Солженицын', pages=704, publisher='АСТ',
                    description='Роман о жизни в сталинской "шарашке".', cover_image='first-circle.jpg'),
                Book(title='Петр Первый', author='Алексей Толстой', pages=768, publisher='АСТ',
                    description='Исторический роман о первом российском императоре.', cover_image='peter-first.jpg'),
            ]
            
            for book in real_books:
                db.session.add(book)
            
            db.session.commit()
            print(f'Добавлено {len(real_books)} книг')
        
        print('База данных инициализирована успешно')

if __name__ == '__main__':
    init_database()