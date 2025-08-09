import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.utils import secure_filename

# App and Database Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_key_that_should_be_changed')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    itemNumber = db.Column(db.String(50), unique=True, nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    imageUrl = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"Item('{self.name}', '{self.itemNumber}', '{self.brand}')"

# --- Routes ---
ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Initial page load shows all items
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/search')
def search():
    search_query = request.args.get('search_query', '')
    query = Item.query
    if search_query:
        query = query.filter(or_(
            Item.name.ilike(f'%{search_query}%'),
            Item.itemNumber.ilike(f'%{search_query}%'),
            Item.brand.ilike(f'%{search_query}%'),
            Item.description.ilike(f'%{search_query}%')
        ))
    items = query.all()
    # Render only the item grid partial
    return render_template('_item_grid.html', items=items)

@app.route('/item/<int:id>')
def item_detail(id):
    item = Item.query.get_or_404(id)
    return render_template('item_detail.html', item=item)

@app.route('/manage')
def manage_items():
    items = Item.query.all()
    return render_template('manage_items.html', items=items)

@app.route('/manage/search')
def manage_search():
    search_query = request.args.get('search_query', '')
    query = Item.query
    if search_query:
        query = query.filter(or_(
            Item.name.ilike(f'%{search_query}%'),
            Item.itemNumber.ilike(f'%{search_query}%'),
            Item.brand.ilike(f'%{search_query}%')
        ))
    items = query.all()
    return render_template('_manage_item_list.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    new_item = Item(
        name=request.form['name'],
        itemNumber=request.form.get('itemNumber'),
        brand=request.form.get('brand'),
        description=request.form.get('description'),
        imageUrl=request.form.get('imageUrl')
    )
    try:
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding item: {e}', 'danger')
    return redirect(url_for('manage_items'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.itemNumber = request.form.get('itemNumber')
        item.brand = request.form.get('brand')
        item.description = request.form.get('description')
        item.imageUrl = request.form.get('imageUrl')
        try:
            db.session.commit()
            flash('Item updated successfully!', 'success')
            return redirect(url_for('item_detail', id=item.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating item: {e}', 'danger')
    return render_template('add_edit_item.html', title='Edit Item', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting item: {e}', 'danger')
    
    # Check if the request came from the manage page
    if request.referrer and 'manage' in request.referrer:
        return redirect(url_for('manage_items'))
    return redirect(url_for('index'))


@app.route('/import', methods=['POST'])
def import_json():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        try:
            data = json.load(file.stream)
            if not isinstance(data, list):
                flash('Invalid JSON format: must be a list of items.', 'danger')
                return redirect(request.url)
            for item_data in data:
                new_item = Item(
                    name=item_data.get('name'),
                    itemNumber=item_data.get('itemNumber'),
                    brand=item_data.get('brand'),
                    description=item_data.get('description'),
                    imageUrl=item_data.get('imageUrl')
                )
                db.session.add(new_item)
            db.session.commit()
            flash(f'Successfully imported {len(data)} items!', 'success')
        except json.JSONDecodeError:
            flash('Invalid JSON file.', 'danger')
            db.session.rollback()
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
            db.session.rollback()
    else:
        flash('Invalid file type. Please upload a .json file.', 'danger')
    return redirect(url_for('manage_items'))

# Create database tables
with app.app_context():
    db.create_all()
