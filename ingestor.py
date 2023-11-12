import pandas as pd
import PyPDF2
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["bot_db"]
collection = db["bot_data"]


# Function to insert data into MongoDB
def insert_into_mongodb(data):
    collection.insert_one(data)


# Read CSV file and insert into MongoDB
csv_data = pd.read_csv("sample.csv")
for _, row in csv_data.iterrows():
    data = {"content": row["content"]}
    insert_into_mongodb(data)


# Read PDF file and insert into MongoDB
def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text


pdf_text = extract_text_from_pdf("sample.pdf")
data = {"content": pdf_text}
insert_into_mongodb(data)
