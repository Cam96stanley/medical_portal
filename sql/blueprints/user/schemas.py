from sql.extensions import ma
from sql.models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User
    load_instance = True

user_schema = UserSchema()
return_user_schema = UserSchema(exclude=("password",))