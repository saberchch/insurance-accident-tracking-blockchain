import json
from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

class Block:
    def __init__(self, index, year, month, num_accidents, previous_block=None):
        self.index = index
        self.year = year
        self.month = month
        self.num_accidents = num_accidents
        self.previous_block = previous_block
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.year) + str(self.month) + str(self.num_accidents) + str(self.previous_block.hash if self.previous_block else "")
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_block(self, block, num_accidents):
        if self.chain:
            previous_block = self.chain[-1]
        else:
            previous_block = None
        new_block = Block(len(self.chain), block.year, block.month, num_accidents, previous_block)
        self.chain.append(new_block)
        self.update_json()  # Update JSON file after adding a block

    def update_json(self):
        data = {"chain": []}
        for block in self.chain:
            block_data = {
                "index": block.index,
                "year": block.year,
                "month": block.month,
                "num_accidents": block.num_accidents,
                "previous_block_hash": block.previous_block.hash if block.previous_block else None,
                "hash": block.hash
            }
            data["chain"].append(block_data)

        with open("data/accidents.json", "w") as file:
            json.dump(data, file, indent=4)

    def to_dict(self):
        data = {"chain": []}
        for block in self.chain:
            block_data = {
                "index": block.index,
                "year": block.year,
                "month": block.month,
                "num_accidents": block.num_accidents,
                "previous_block_hash": block.previous_block.hash if block.previous_block else None,
                "hash": block.hash
            }
            data["chain"].append(block_data)
        return data

    @classmethod
    def from_dict(cls, blockchain_dict):
        blockchain = cls()
        for block_data in blockchain_dict["chain"]:
            previous_block = None
            if block_data["previous_block_hash"]:
                previous_block = blockchain.chain[-1]
            block = Block(
                block_data["index"],
                block_data["year"],
                block_data["month"],
                block_data["num_accidents"],
                previous_block
            )
            blockchain.chain.append(block)
        return blockchain

def is_accidents_json_empty():
    return os.stat("data/accidents.json").st_size == 0

@app.route("/")
def index():
    return render_template("index.html")
    

@app.route("/blockchain_warning")
def blockchain_warning():
    return render_template("blockchain_warning.html")

@app.route("/create_genesis_block", methods=["GET", "POST"])
def create_genesis_block():
    if request.method == "POST":
        initial_year = int(request.form["initial_year"])
        initial_month = int(request.form["initial_month"])
        num_accidents = int(request.form["num_accidents"])

        genesis_block = Block(0, initial_year, initial_month, num_accidents)
        blockchain = Blockchain()
        blockchain.add_block(genesis_block, num_accidents)
        session["blockchain"] = blockchain.to_dict()
        return redirect(url_for("index"))

    if is_accidents_json_empty():
        return render_template("create_genesis_block.html")
    else:
        return redirect(url_for("blockchain_warning"))

@app.route("/create_genesis_block_confirm", methods=["POST"])
def create_genesis_block_confirm():
    blockchain_dict = session.get("blockchain")
    if blockchain_dict:
        # If blockchain already exists, redirect to index route
        return redirect(url_for("add_accidents"))

    return redirect(url_for("create_genesis_block"))

@app.route("/add_accidents", methods=["GET", "POST"])
def add_accidents():
    if is_accidents_json_empty():
        return redirect(url_for("create_genesis_block"))
    
    blockchain_dict = session.get("blockchain")
    #if not blockchain_dict:
        #return redirect(url_for("create_genesis_block"))

    blockchain = Blockchain.from_dict(blockchain_dict)

    previous_block = blockchain.chain[-1] if blockchain.chain else None
    previous_year = previous_block.year if previous_block else None
    previous_month = previous_block.month if previous_block else None
    
    if request.method == "POST":
        year = int(request.form["year"])
        month = int(request.form["month"])
        num_accidents = int(request.form["num_accidents"])

        # Add the new block first to update the blockchain data
        blockchain.add_block(Block(len(blockchain.chain), year, month, num_accidents, previous_block), num_accidents)
        session["blockchain"] = blockchain.to_dict()

        # Calculate next month and year after processing user input
        next_month = month + 1
        next_year = year
        if next_month > 12:
            next_month = 1
            next_year += 1

        return redirect(url_for("index"))

    # Calculate next month and year for rendering the form
    next_month = previous_month + 1 if previous_month else 1
    next_year = previous_year
    if next_month > 12:
        next_month = 1
        if next_year is not None:  # Increment year only if it's not None
            next_year += 1

    return render_template("add_accidents.html", next_year=next_year, next_month=next_month)


if __name__ == "__main__":
    app.run(debug=True)
