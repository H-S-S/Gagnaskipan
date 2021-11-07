import sqlite3

#conn = sqlite3.connect("PreviousLocations.db")
#c = conn.cursor()

def convert_matrix_to_text(matrix1):
    text = ""
    for row in range(len(matrix1)):
        if row !=0:
            text += ";"
        for column in range(len(matrix1[row])):
            if column == len(matrix1[row])-1:
                text += str(matrix1[row][column])
            else:
                text += str(matrix1[row][column]) + ","

    return text


def convert_list_to_text(list1):
    text =""
    for i in range(len(list1)):
        if i == len(list1) - 1:
            text += str(list1[i])
        else:
            text += str(list1[i]) + ","

    return text

def crete_table():
    conn = sqlite3.connect("PreviousLocations.db")
    c = conn.cursor()
    
    c.execute(""" SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'locations' """)

    if c.fetchone()[0] == 1:
        pass
    else:
        c.execute("""CREATE TABLE locations (
        name text,
        loc text,
        loc_between_loc text, 
        distance_between_each_loc text,
        shortest_distance text,
        shortest_distance_km integer
        )""")

    conn.commit()
    conn.close()






def insert_locations(name, loc_text, loc_loc_text, distance_between_loc_text, shortest_distance_text, shortest_distance_km):

    conn = sqlite3.connect("PreviousLocations.db")
    c = conn.cursor()

    c.execute("INSERT INTO locations VALUES (:name, :loc, :loc_between_loc, :distance_between_each_loc, :shortest_distance, :shortest_distance_km)",
              {
                  "name": name,
                  "loc": loc_text,
                  "loc_between_loc": loc_loc_text,
                  "distance_between_each_loc": distance_between_loc_text,
                  "shortest_distance": shortest_distance_text,
                  "shortest_distance_km": shortest_distance_km

              }
              )

    conn.commit()
    conn.close()


def get_location_id(idNumber):
    conn = sqlite3.connect("PreviousLocations.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM locations WHERE oid = :oid",
              {
                  "oid": idNumber}
              )
    records = c.fetchall()

    return records
    conn.commit()
    conn.close()

def get_location_name(name):
    conn = sqlite3.connect("PreviousLocations.db")
    c = conn.cursor()
    c.execute("SELECT * FROM locations WHERE name ="+name)
    records = c.fetchone()

    return records
    conn.commit()
    conn.close()

def remove_location(idNumber):
    conn = sqlite3.connect("PreviousLocations.db")
    c = conn.cursor()

    c.execute("""DELETE from locations WHERE oid = :oid """, {
        "oid":idNumber
    })
    conn.commit()
    conn.close()

def query_all():
    conn = sqlite3.connect("PreviousLocations.db")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM locations")
    records = c.fetchall()

    return records
    conn.commit()
    conn.close()

def query_name():
    conn = sqlite3.connect("PreviousLocations.db")
    c = conn.cursor()

    c.execute("SELECT name, oid FROM locations")
    records = c.fetchall()

    return records
    conn.commit()
    conn.close()



#records = query_all()
#records = get_location_name("'test1'")
#records = get_location_id(1)
#records = query_name()

#for record in records:
    #print(record)