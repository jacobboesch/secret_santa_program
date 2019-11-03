import sys
from secret_santa.database import init_db, Base, engine

arg_skip_confirm = False
for arg in sys.argv:
    if arg == "-y":
        arg_skip_confirm = True

if not arg_skip_confirm:
    print("This script will drop ALL data from the database!")
    answer = input("Continue? [y/N]: ")
else:
    answer = "y"

if answer is not "y":
    sys.exit()

# Drop any data that's in there
Base.metadata.bind = engine
Base.metadata.drop_all()

init_db()