from faker import Faker

from users.models import UserModel


class CreateUserFactory:
    @staticmethod
    def create():
        fake: Faker = Faker()
        user = UserModel.objects.create(first_name=fake.first_name(), last_name=fake.last_name(),
                                        mobile=fake.random_number(digits=10), email_id=fake.email())
        user.set_password(fake.password())
        user.save()
        return user
