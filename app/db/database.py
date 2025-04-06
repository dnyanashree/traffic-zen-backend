from db.config import get_cassandra_session


def get_all_users():
   
    session = get_cassandra_session()
    rows = session.execute('SELECT * FROM user_login')
    for row in rows:
        print(row.userid, row.email, row.password_hash, row.last_login, row.failed_login_attempts, row.last_failed_login, row.is_account_locked)
    return {"Hello": "World"}

def add_user(user):
    print("Adding user to db",user)
    session = get_cassandra_session()
    session.execute(
        """
        INSERT INTO user_signup (email, created_at, first_name, is_active, last_name, password_hash, verification_token, verification_token_expiration) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    ,
        (user.email, user.created_at, user.first_name, user.is_active, user.last_name, user.password, user.verification_token, user.verification_token_expiration)
    )

def check_user_exists(email):
    session = get_cassandra_session()
    rows = session.execute('SELECT * FROM user_signup WHERE email = %s', (email,))
    if rows:
        return True
    else:
        return False

    # session.execute(
    #     """
    #     INSERT INTO user_login (userid, email, password_hash, last_login, failed_login_attempts, last_failed_login, is_account_locked)
    #     VALUES (%s, %s, %s, %s, %s, %s, %s)
    #     """,
    #     (user.userid, user.email, user.password_hash, user.last_login, user.failed_login_attempts, user.last_failed_login, user.is_account_locked)
    # )
    # session.commit()
    # user.password = 'hashed'
