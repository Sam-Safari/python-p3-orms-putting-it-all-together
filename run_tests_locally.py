from lib.dog import Dog, CONN, CURSOR

# Simple runner to validate core behaviors from the pytest suite

def reset_db():
    CURSOR.execute("DROP TABLE IF EXISTS dogs")
    CONN.commit()


def assert_eq(a, b, msg=None):
    if a != b:
        raise AssertionError(msg or f"Assertion failed: {a} != {b}")


# Test init
reset_db()
d = Dog("joey", "cocker spaniel")
assert_eq((d.name, d.breed), ("joey", "cocker spaniel"))

# create_table and drop_table
reset_db()
Dog.create_table()
# ensure table exists
CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dogs'")
rows = CURSOR.fetchall()
assert_eq(len(rows), 1, "dogs table should exist after create_table")

Dog.drop_table()
CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dogs'")
rows = CURSOR.fetchall()
assert_eq(len(rows), 0, "dogs table should not exist after drop_table")

# save and create
Dog.create_table()
joey = Dog("joey", "cocker spaniel")
joey.save()
CURSOR.execute("SELECT * FROM dogs WHERE name='joey' LIMIT 1")
row = CURSOR.fetchone()
assert_eq(row, (1, 'joey', 'cocker spaniel'))

# create classmethod
Dog.drop_table(); Dog.create_table()
joey = Dog.create('joey', 'cocker spaniel')
assert_eq((joey.id, joey.name, joey.breed), (1, 'joey', 'cocker spaniel'))

# new_from_db
Dog.drop_table(); Dog.create_table()
CURSOR.execute("INSERT INTO dogs (name, breed) VALUES ('joey', 'cocker spaniel')")
CURSOR.execute("SELECT * FROM dogs WHERE name='joey' LIMIT 1")
row = CURSOR.fetchone()
joey = Dog.new_from_db(row)
assert_eq((joey.id, joey.name, joey.breed), (1, 'joey', 'cocker spaniel'))

# get_all
Dog.drop_table(); Dog.create_table()
Dog.create('joey', 'cocker spaniel')
Dog.create('fanny', 'cockapoo')
dogs = Dog.get_all()
assert_eq((dogs[0].id, dogs[0].name, dogs[0].breed), (1, 'joey', 'cocker spaniel'))
assert_eq((dogs[1].id, dogs[1].name, dogs[1].breed), (2, 'fanny', 'cockapoo'))

# find_by_name and find_by_id
Dog.drop_table(); Dog.create_table()
Dog.create('joey', 'cocker spaniel')
joey = Dog.find_by_name('joey')
assert_eq((joey.id, joey.name, joey.breed), (1, 'joey', 'cocker spaniel'))

joey = Dog.find_by_id(1)
assert_eq((joey.id, joey.name, joey.breed), (1, 'joey', 'cocker spaniel'))

# find_or_create_by existing
Dog.drop_table(); Dog.create_table()
Dog.create('joey', 'cocker spaniel')
joey = Dog.find_or_create_by('joey', 'cocker spaniel')
assert_eq((joey.id, joey.name, joey.breed), (1, 'joey', 'cocker spaniel'))

# find_or_create_by new
Dog.drop_table(); Dog.create_table()
joey = Dog.find_or_create_by('joey', 'cocker spaniel')
assert_eq((joey.id, joey.name, joey.breed), (1, 'joey', 'cocker spaniel'))

# save sets id
Dog.drop_table(); Dog.create_table()
joey = Dog('joey', 'cocker spaniel')
joey.save()
assert_eq((joey.id, joey.name, joey.breed), (1, 'joey', 'cocker spaniel'))

# update
Dog.drop_table(); Dog.create_table()
joey = Dog.create('joey', 'cocker spaniel')
joey.name = 'joseph'
joey.update()
assert_eq(Dog.find_by_id(1).name, 'joseph')
assert_eq(Dog.find_by_name('joey'), None)

print('All local checks passed')
