from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
# This line defines a route decorator for the /bakeries endpoint. When a GET request is made to this endpoint, the following function, bakeries(), will be executed.
def bakeries():

    bakeries = Bakery.query.all()
    # This line executes a database query using SQLAlchemy's query interface to retrieve all the Bakery objects from the corresponding table in the database. It returns a list of Bakery objects.
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    # to_dict() method is called to serialize the object into a dictionary representation. The resulting dictionaries are collected into a new list called bakeries_serialized.
    response = make_response(
        jsonify(bakeries_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    # response.headers['Content-Type'] = 'application/json' sets the value of the 'Content-Type' header in the HTTP response to 'application/json'.
    # response.headers: This property provides access to the headers of the response. Headers are used to convey additional information about the response to the client.
# 'Content-Type': This is the key of the header that specifies the type of content in the response.
# 'application/json': This is the value assigned to the 'Content-Type' header. It indicates that the content of the response is in JSON format.
    return response



@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    # query: This is a method provided by SQLAlchemy that allows you to construct and execute queries on the database.
    # filter_by(id=id): This is a filtering condition applied to the query. It specifies that the id attribute of the Bakery objects should match the provided id value.
    # first(): This method is used to retrieve the first result from the query. Since id is expected to be unique, first() is commonly used to retrieve a single object based on the filtering condition.
    bakery_serialized = bakery.to_dict()

    response = make_response(
        jsonify(bakery_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    by_price = BakedGood.query.order_by(BakedGood.price).all()
    # order_by(BakedGood.price): This method is used to specify the ordering of the query results. It takes the price attribute of the BakedGood model as the ordering criterion.
    # all(): This method executes the query and retrieves all the results as a list of BakedGood objects.
    by_price_serialized = [bg.to_dict() for bg in by_price]
    
    response = make_response(
        jsonify(by_price_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    # order_by(BakedGood.price.desc()): This method is used to specify the ordering of the query results. It orders the BakedGood objects by their price attribute in descending order (desc() is used to indicate descending order).
    # limit(1): This method limits the number of results returned by the query to 1. It ensures that only the highest-priced BakedGood is retrieved.
    # first(): This method retrieves the first result from the query, which corresponds to the BakedGood object with the highest price.
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        jsonify(most_expensive_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


# Methods for selceting data filte, filter_by, order_by, select, query, scalars

if __name__ == '__main__':
    app.run(port=555, debug=True)