from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    # return "This page will show all my restaurants"
    restaurants = session.query(Restaurant).all()
    # item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))

    else:
            return render_template('newrestaurant.html', Restaurant = Restaurant)

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    editedItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name=request.form['name']
        if request.form['description']:
            editedItem.description=request.form['description']
        if request.form['price']:
            editedItem.price=request.form['price']
        if request.form['course']:
            editedItem.course=request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editrestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    # return "This page will be for deleting restaurant %s" % restaurant_id
    return render_template('deleterestaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    # return "This page is the menu for restaurant %s" % restaurant_id
    return render_template('menu.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    # return "This page is for making a new menu item for restaurant %s" % restaurant_id
    return render_template('newmenuitem.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/menu_id/edit')
def editMenuItem(restaurant_id):
    # return "This page is for editing menu items %s" % menu_id
    return render_template('editmenuitem.html', restaurant=restaurant,
    menu_id=restaurant['id'])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id):
    # return "This page is for deleting menu item %s" % menu_id
    return render_template('deletemenuitem', restaurant=restaurant,
    menu_id=restaurant['id'])


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5000)
