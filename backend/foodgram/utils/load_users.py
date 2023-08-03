from django.contrib.auth.models import User


DATA_USER = (
    ('usr_test_1', 'usr_test_1', 'usr_test_1', '1@1.ru'),
    ('usr_test_2', 'usr_test_2', 'usr_test_2', '2@2.ru'),
    ('usr_test_3', 'usr_test_3', 'usr_test_3', '3@3.ru'),
    ('usr_test_4', 'usr_test_4', 'usr_test_4', '4@4.ru'),
)

for obj in DATA_USER:
    user = User.objects.create_user(
        username=obj[0],
        last_name=obj[1],
        first_name=obj[2],
        email=obj[3]
        password='usr_test_password'
    )
    user.save()
