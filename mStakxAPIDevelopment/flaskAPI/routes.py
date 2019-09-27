from flask import request, jsonify, render_template, url_for, json
import requests
from werkzeug.utils import redirect
from flaskAPI import db, app
from flaskAPI.form import create_form
from flaskAPI.models import Book


@app.route("/api/external-books", methods=['GET'])
def query():
    name = request.args.get('name', type=str)
    url = "https://www.anapioficeandfire.com/api/books?name=" + str(name)
    resp = requests.get(url)
    if resp.status_code != 200:
        resp = {
            "status_code": 200,
            "status": "success",
            "data": []
        }
        return jsonify(resp)
    response = resp.json()
    output = resp.json()
    for index, data in enumerate(response):
        for key in data:
            if key not in ['name', 'isbn', 'authors', 'numberOfPages', 'publisher', 'country', 'released']:
                del output[index][key]
            if key == 'numberOfPages':
                output[index]['number_of_pages'] = output[index].pop('numberOfPages')
            elif key == 'released':
                output[index]['release_date'] = output[index].pop('released')
    return jsonify(output)

#Creation through browser using form (additional)
@app.route("/api/v1/books_", methods=['GET', 'POST'])
def create():
    form = create_form()
    if form.validate_on_submit():
        book = Book(name=form.name.data, isbn=form.isbn.data, authors=form.authors.data, country=form.country.data,
                    numberOfPages=form.numberOfPages.data, publisher=form.publisher.data, release=form.release.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('create'))
    return render_template('create.html', form=form)

#API Funtion
@app.route("/api/v1/books", methods=['POST'])
def create2():
    # data = ast.literal_eval(d.decode("utf-8"))
    # data = (request.data.decode("utf-8"))
    data = json.loads(request.data.decode("utf-8"))
    # print(type(data), "  ", data)

    book = Book(id=data.get('id'), name=data['name'], isbn=data['isbn'], authors=data['authors'],
                country=data['country'], numberOfPages=data['numberOfPages'], publisher=data['publisher'],
                release=data['release'])
    db.session.add(book)
    db.session.commit()
    output = {"status_code": 200, "status": "success", "data": [data]}
    return jsonify(output)

@app.route("/api/v1/books/<int:bid>", methods=['GET'])
@app.route("/api/v1/books", methods=['GET'])
def read(bid=None):
    if bid:
        book = Book.query.filter_by(id=bid).all()
    else:
        book = Book.query.all()
    output = {"status_code": 200, "status": "success", "data": []}
    for item in book:
        data = {}
        data["id"] = item.id
        data["name"] = item.name
        data["isbn"] = item.isbn
        data["authors"] = item.authors
        data["numberOfPages"] = item.numberOfPages
        data["publisher"] = item.publisher
        data["country"] = item.country
        data["release"] = item.release
        output['data'].append(data)
    return jsonify(output)


@app.route("/api/v1/books/<int:bid>", methods=['PATCH'])
def update(bid):
    data = json.loads(request.data.decode("utf-8"))
    book = Book.query.get_or_404(bid)
    #stmt = update(Book).where(Book.id == 2).values(name='abhishek')    #Did not work not sure why!
    for key, value in data.items():
        setattr(book, key, value)
    #db.session.add(book)   #optional
    db.session.commit()
    output = {"status_code": 200, "status": "success", "message": "The book " + book.name + " was updated successfully",
              "data": [data]}
    return jsonify(output)


@app.route("/api/v1/books/<int:bid>", methods=['DELETE'])
def delete(bid):
    book = Book.query.get_or_404(bid)
    db.session.delete(book)
    db.session.commit()
    output = {"status_code": 200, "status": "success", "message": "The book " + book.name + " was deleted successfully",
              "data": []}
    return jsonify(output)
