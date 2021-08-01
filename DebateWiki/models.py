from pydantic import BaseModel
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


# User Models
class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=50, null=True)
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def full_name(self) -> str:
        """
        Returns the best name
        """
        if self.name:
            return f"{self.name}"
        return self.username

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash"]


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)


# Status
class Status(BaseModel):
    message: str
