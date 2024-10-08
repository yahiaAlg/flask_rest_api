from marshmallow import fields, Schema


class PlainStoreSchema(Schema):
    # consist of id,name

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(
        fields.Nested(lambda: PlainItemSchema()),
        dump_only=True,
    )
    tags = fields.List(
        fields.Nested(lambda: PlainTagSchema()),
        dump_only=True,
    )


class StoreUpdateSchema(Schema):
    # consist of name
    id = fields.Int(required=True)
    name = fields.Str()


class PlainTagSchema(Schema):
    # consist of id,name

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(lambda: PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(lambda: PlainItemSchema()), dump_only=True)


class TagUpdateSchema(Schema):
    # consist of name
    name = fields.Str()


class PlainItemSchema(Schema):
    # consist of id,name,category,description,price, store_id

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    description = fields.Str(default="")
    price = fields.Float(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(lambda: PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(lambda: PlainTagSchema()), dump_only=True)


class ItemUpdateSchema(Schema):
    # consist of name,category,description,price
    name = fields.Str()
    category = fields.Str()
    description = fields.Str()
    price = fields.Float()


class ItemAndTagSchema(Schema):
    message = fields.Str()

    item = fields.Nested(lambda: ItemSchema())
    tag = fields.Nested(lambda: TagSchema())
