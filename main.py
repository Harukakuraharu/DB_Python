import psycopg2

def create_table(conn):
    with conn.cursor() as cur:
        # таблица 1-ая, для ФО и почты
        cur.execute("""
            CREATE TABLE IF NOT EXISTS info_client(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(60) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE);
                    """)
        
        # таблица 2-ая, для номера тел.
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id SERIAL PRIMARY KEY, 
            client_id INTEGER NOT NULL REFERENCES info_client(client_id),
            phone VARCHAR(12));  
                    """)
    return 'Отношения успешно созданы'   


def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO info_client(first_name, last_name, email)
            VALUES (%s, %s, %s)
            RETURNING client_id, first_name, last_name, email;
                    """, (first_name, last_name, email))
        print (cur.fetchone())
    return 'Данные успешно добавлены'


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone(client_id, phone)
            VALUES (%s, %s);
                    """, (client_id, phone))
    return f'Номер телефона {phone} для клиента с айди {client_id} успешно добавлен'    


def change_client(conn, client_id=None, first_name=None, last_name=None, email=None, phone=None):
    id_client = input('Введите айди клиента: ')
    parameters = input('Какие данные клиента нужно изменить? first_name, last_name, email, phone: ')
    correct_params = ['first_name', 'last_name', 'email', 'phone']
    parameters_full = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Почта', 'phone': 'Номер телефона'}
    while parameters not in correct_params:
        return 'Неккоректный ввод. Попробуйте еще раз'
        break 
    else:
        value = input(f'Введите новое значение для {parameters}: ')
        with conn.cursor() as cur:
            cur.execute(f"""
                UPDATE info_client
                SET {parameters} = '{value}'
                WHERE client_id = {id_client};
                        """)
        return f'{parameters_full[parameters]} успешно изменено/изменена на {value}'           


def delete_phone(conn, client_id=None, phone=None):
    id_client = input('Введите айди клиента: ')
    phone_number = input('Введите номер телефона, который нужно удалить: ')
    with conn.cursor() as cur:
        cur.execute(f"""
            DELETE from phone
            WHERE client_id = {id_client} AND phone = '{phone_number}';
                    """)
    return f'Номер телефона {phone_number} успешно удален'


def delete_client(conn, client_id=None):
    with conn.cursor() as cur:
        id_client = input('Введите айди клиента: ')
        cur.execute(f"""
            DELETE from info_client
            WHERE client_id = {id_client};
                    """)
    return f'Клиент с айди {id_client} успешно удален'    


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    parameters = str(input('По каким данным нужно искать клиента? first_name, last_name, email, phone: '))
    correct_params = ['first_name', 'last_name', 'email', 'phone']
    while parameters not in correct_params:
        return 'Неккоректный ввод. Попробуйте еще раз'
        break 
    else:
        value = input(f'Введите значение для {parameters}: ')
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT first_name, last_name, email, phone FROM info_client ic
                FULL OUTER JOIN phone p ON ic.client_id = p.client_id
                WHERE LOWER({parameters}) = LOWER('{value}') """)
            result = cur.fetchall()
            if result:
                print('Данные найдены')
                return result
            else:
                return 'Данные не найдены. Попробуйте еще раз'

with psycopg2.connect(database='netology_db', user='postgres', password='nxso32MI') as conn:
    print(create_table(conn))  
    # print(add_client(conn, first_name=input('Введите имя: '), last_name=input('Введите фамилию: '), 
    #                  email=input('Введите почту: '), phone=None))
    # print(add_phone(conn, client_id=input('Введите айди клиента: '), phone=input('Введите номер телефона: ')))
    # print(change_client(conn, client_id=None, first_name=None, last_name=None, email=None, phone=None))
    # print(delete_phone(conn, client_id=None, phone=None))
    # print(delete_client(conn, client_id=None))
    # print(find_client(conn, first_name=None, last_name=None, email=None, phone=None))
conn.close()
