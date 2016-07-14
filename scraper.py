import requests
import sqlite3

API_KEY = "07ad2494eb8df1d0277e159553014444"
ART_URL = "https://api.burningman.org/api/v1/art?year=%d"
BASIC_AUTH = requests.auth.HTTPBasicAuth(API_KEY, '')
DB = None


def create_db(db_path):
    conn = sqlite3.connect(db_path)

    #location: {u'category': None, u'distance': 800, u'string': u"7:15 800'", u'hour': 7, u'gps_latitude': 40.786113813522, u'gps_longitude': -119.20937066261, u'minute': 15}
    conn.execute('''CREATE TABLE IF NOT EXISTS art
                      (category text, location_string text, uid text PRIMARY KEY, artist text, url text, hometown text, description text, donation_link text, program text, contact_email text, year int, name text, loc_category text, loc_distance int, loc_string text, loc_hour int, loc_minute int, loc_latitude real, loc_longitude real)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS images
                      (art_uid text, thumbnail blob, thumbnail_url text)''')

    return conn

def get_art(year):
    resp = requests.get(ART_URL % year, auth=BASIC_AUTH)
    arts = resp.json()
    for art in arts:
        print(art.keys())
        loc = art.get("location",
                {"category": None, "distance": None, "string": None, "hour": None,
                    "minute": None, "gps_latitude": None, "gps_longitude": None})
        DB.execute('''INSERT INTO art(category, location_string, uid, artist, url, hometown, description, donation_link, program, contact_email, year, name, loc_category , loc_distance , loc_string , loc_hour , loc_minute , loc_latitude , loc_longitude )
                      VALUES
                     (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     [art["category"], art.get("location_string", None), art["uid"], art["artist"],
                      art["url"], art["hometown"], art["description"], art["donation_link"],
                      art["program"], art["contact_email"], art["year"], art["name"],
                      loc["category"], loc["distance"], loc["string"], loc["hour"], loc["minute"], 
                      loc["gps_latitude"], loc["gps_longitude"]])

        for image_dict in art.get("images", []):
            url = image_dict["thumbnail_url"]
            if not url or url == "http://" or url == "https://":
                continue
            image_resp = requests.get(url)
            DB.execute("INSERT INTO images(art_uid, thumbnail, thumbnail_url) VALUES (?, ?, ?)",
                       [art["uid"], buffer(image_resp.content), url])
            print("Downloaded image %s" % url)

def main():
    global DB
    year = 2016
    DB = create_db('art-%d.sqlite' % year)
    print("Scraping art for year %d" % year) 
    get_art(year)
    print("Done!")
    DB.commit()
    DB.close()

if __name__ == "__main__":
    main()
