from pyasn1.type import useful
from main import db
import models
'''
user=models.User(full_name="Nguyen Huu Thua",email="admin@thispage.com",role="manager")
user.set_password("admin")
db.session.add(user)
db.session.commit()
user=db.session.query(models.User).filter_by(email="admin@thispage.com").first()
db.session.add(models.Phone(user_id=user.user_id,phonenumber="0123456789"))
db.session.add(models.Address(user_id=user.user_id,address="My address"))
db.session.commit()'''
import fireStore

#fireStore.putProductImg(1)
#print(fireStore.getProductImg(1))


order=db.session.query(models.Order).filter_by(order_id=12).first()

print()