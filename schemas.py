from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class PlainCourseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    grade = fields.Float(required=True)
    points = fields.Integer(required=True)
    user_id = fields.Integer(dump_only=True)


class UpdateCourseSchema(Schema):
    name = fields.String(required=True)
    grade = fields.Float(required=True)
    points = fields.Integer(required=True)


class GpaSchema(Schema):
    gpa = fields.Float(dump_only=True)


class UserSchema(PlainUserSchema):
    courses = fields.List(fields.Nested(PlainCourseSchema()), dump_only=True)


class CourseSchema(PlainCourseSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)