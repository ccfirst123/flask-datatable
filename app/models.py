from . import db


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(2))
    email = db.Column(db.String(64))
    address = db.Column(db.String(64))

    @property
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'email': self.email,
            'address': self.address
        }

    @staticmethod
    def generate_fake(count=1000):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            s = Student(name=forgery_py.name.full_name(),
                        gender=forgery_py.personal.abbreviated_gender(),
                        email=forgery_py.internet.email_address(),
                        address=forgery_py.address.city()
                        )
            db.session.add(s)
            db.session.commit()




