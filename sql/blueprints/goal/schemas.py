from sql.extensions import ma
from sql.models import Goal

class GoalSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Goal

goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)