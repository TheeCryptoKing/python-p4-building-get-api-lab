from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
# This line sets the naming_convention parameter of the MetaData object to a dictionary representing the custom naming convention for foreign key constraints
# this naming convention will generate foreign key constraint names in the format "fk_<table_name><column_0_name><referred_table_name>", where the placeholders are replaced with the appropriate names from the tables and columns involved in the foreign key relationship.

db = SQLAlchemy(metadata=metadata)
# establishing metadata and putting in a variable 

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    serialize_rules = ('-baked_goods.bakery',)
    # sterilization and set rules for sterilizing, this data wont populate Json  
    # 'baked_goods.bakery': This represents the relationship between the current model (let's assume it's the Bakery model) and the related model (BakedGood). It specifies that the baked_goods attribute, which is a collection of related BakedGood objects, should be excluded from the serialized output. when the to_dict() method (or any serialization method) is called on an instance of the model class, it will exclude the baked_goods relationship from the serialized output. This can be useful when you want to control which attributes or relationships are included or excluded during serialization, providing a more focused or optimized representation of the data.
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    baked_goods = db.relationship('BakedGood', backref='bakery')
    # This line defines the relationship between the Bakery and BakedGood models.
    # is the name of the related model/table that the relationship is established with.
    # backref='bakery' creates a back reference in the BakedGood model. It adds a new attribute called 'bakery' to the BakedGood model, allowing access to the associated Bakery object.
    # Allows bidimensional Data to flow between tables

    def __repr__(self):
        return f'<Bakery {self.name}>'


class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    serialize_rules = ('-bakery.baked_goods',)
    # sterilization and set rules for sterilizing, this data wont populate Json  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    # syntax needs to be like this for updates and creates

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

    def __repr__(self):
        return f'<Baked Good {self.name}, ${self.price}>'
    # representing function, represents the data in inside of retunn (validation i guess??)
    
    #sterilizerMixin = converting data to Json
    #Sterlize_rules = uses class names and sets rules for what will populate db and Json 