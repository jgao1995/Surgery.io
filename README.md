# 29-Facilitating-Selection-of-Compatible-Endovascular-Devices-During-Surgery
- Created by Amit Patel, Joseph Gao, Raymond Yin, and Sumit Shyamsukha.

## Setting up
- `pip install` all dependencies in requirements.txt
- migrate database if it's the first time you're using the app

## Important stuff
- Please make sure your `.gitignore` files has the following lines
- `ENV/`
- `*.pyc`
- `db.sqlite3`

## Updating 
- after each major change, make sure you reset and reseed the database. The reseed method is made possible thanks to a generous contribution from Raymond. Here are the steps. 
1. Delete the `db.sqlite3` file from your working directory. 
2. Rerun the migrations (`python manage.py migrate`)
3. Startup the Django console with `python manage.py shell_plus`
4. Import our models using `from plan_surgery.models import *`
5. Finally, run the seed method: `seed_db()`.

You should be set at this point!

## Known Bugs/Missing Features
- (feel free to add/remove from this list as you see fit.)
- meaningful landing page. add some art or something
- i updated the planned surgery page but it has a dead link. That link is to our own 'admin' feature, to add stuff
- all devices literally just displays device information but in no well formatted way. not very helpful
- no way to delete notes/videos after added, except by dropping the DB
- graph visualization/logic for seeing if devices fit within one another
- GUI for visualizing if two devices are compatible
- information on the device specifics page could be more specific. (I did not add dimensions). 
- dynamic search is broken for some reason :( 


