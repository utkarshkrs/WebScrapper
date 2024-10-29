from flask import Flask , request , render_template
from bs4 import BeautifulSoup
import requests
import mysql.connector

app = Flask(__name__)

# Function to scrap data from URL
# url = "https://www.cricbuzz.com/live-cricket-scores/101549/sl-vs-ind-1st-odi-india-tour-of-sri-lanka-2024"
try:
    def scrape_data(url):
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {
            "title": soup.title.string if soup.title else "No Title",
            "meta": [meta.attrs for meta in soup.find_all('meta')],
            # Add more elements to scrape as needed
        }
        return data

except requests.exceptions.RequestException as e:
        print(f"Error: {e}") 
        

# Function to connect to MySQL database and insert data
def save_to_db(data):
    conn = mysql.connector.connect(
        host='localhost',
        port  = 3306,
        user='root',
        password='Msdhoni@1107',
        database='webscraper_db'
    )
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS web_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        meta TEXT
    )
    ''')

    # Insert data into the database
    cursor.execute('''
    INSERT INTO web_data (title, meta)
    VALUES (%s, %s)
    ''', (data['title'], str(data['meta'])))

    conn.commit()
    cursor.close()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        data = scrape_data(url)
        if data:
            save_to_db(data)
            print(data)
            return f"Data from {url} has been saved to the database."
        else:
            return f"Failed to scrape data from {url}."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)