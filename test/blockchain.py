import hashlib
import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Blockchain Classes
class Block:
    def __init__(self, index, year, month, num_accidents, previous_block=None):
        self.index = index
        self.year = year
        self.month = month
        self.num_accidents = num_accidents
        self.previous_block = previous_block
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.year) + str(self.month) + str(self.num_accidents) + (self.previous_block.hash if self.previous_block else "")
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_block(self, year, month, num_accidents):
        previous_block = self.chain[-1] if self.chain else None
        new_block = Block(len(self.chain), year, month, num_accidents, previous_block)
        self.chain.append(new_block)

    def to_dict(self):
        return {"chain": [{"index": block.index,
                           "year": block.year,
                           "month": block.month,
                           "num_accidents": block.num_accidents,
                           "previous_block_hash": block.previous_block.hash if block.previous_block else None,
                           "hash": block.hash} for block in self.chain]}

    @classmethod
    def from_dict(cls, blockchain_dict):
        blockchain = cls()
        for block_data in blockchain_dict["chain"]:
            previous_block = blockchain.chain[-1] if blockchain.chain else None
            block = Block(block_data["index"], block_data["year"], block_data["month"], block_data["num_accidents"], previous_block)
            blockchain.chain.append(block)
        return blockchain

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_genesis_block", methods=["GET", "POST"])
def create_genesis_block():
    if request.method == "POST":
        initial_year = int(request.form["initial_year"])
        initial_month = int(request.form["initial_month"])
        num_accidents = int(request.form["num_accidents"])

        genesis_block = Block(0, initial_year, initial_month, num_accidents)
        blockchain = Blockchain()
        blockchain.add_block(initial_year, initial_month, num_accidents)
        session["blockchain"] = blockchain.to_dict()

        return redirect(url_for("index"))

    return render_template("create_genesis_block.html")

@app.route("/add_accidents", methods=["GET", "POST"])
def add_accidents():
    if "blockchain" not in session:
        return redirect(url_for("create_genesis_block"))

    blockchain = Blockchain.from_dict(session["blockchain"])

    if request.method == "POST":
        year = int(request.form["year"])
        month = int(request.form["month"])
        num_accidents = int(request.form["num_accidents"])

        blockchain.add_block(year, month, num_accidents)
        session["blockchain"] = blockchain.to_dict()

        return redirect(url_for("index"))

    previous_block = blockchain.chain[-1] if blockchain.chain else None
    next_year = previous_block.year if previous_block else None
    next_month = (previous_block.month + 1) if previous_block else 1

    if next_month > 12:
        next_month = 1
        next_year += 1

    return render_template("add_accidents.html", next_year=next_year, next_month=next_month)

if __name__ == "__main__":
    app.run(debug=True)
