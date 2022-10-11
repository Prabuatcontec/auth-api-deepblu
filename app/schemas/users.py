from app.ma import ma
from app.models.users import UsersModel


class UsersSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = UsersModel
        fields = ('username', 'roles', 'active')
        load_instance = True
        include_fk = True
