from flask import Flask, render_template,request,redirect
from database import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    
    search = request.args.get("search")

    conn = get_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM Products WHERE ProductName LIKE ?",
            ('%' + search + '%',)
        )
    else:
        cursor.execute(
            "SELECT * FROM Products"
        )

    products = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        products=products,
        total_products=len(products)
    )

@app.route("/add",methods=["GET","POST"])
def add_product():

    if request.method == "POST":
        product_name = request.form["product_name"]
        brand = request.form["brand"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(""" INSERT INTO Products
            (ProductName, Brand, Category, Price, Quantity)
            VALUES (?, ?, ?, ?, ?)""",
            (product_name,brand,category,price,quantity))
        
        conn.commit()
        conn.close()

        return redirect("/")
    
    return render_template("add_product.html")

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit_product(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Products WHERE ProductID = ?",(id,)
    )

    product = cursor.fetchone()

    if request.method == "POST":

        product_name = request.form["product_name"]
        brand = request.form["brand"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                UPDATE Products
                SET ProductName=?,
                Brand=?,
                Category=?,
                Price=?,
                Quantity=?
            WHERE ProductID=?
        """, (
        product_name,
        brand,
        category,
        price,
        quantity,
        id
    ))

        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("edit_product.html", product=product)

@app.route("/delete/<int:id>")
def delete_product(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
                  "DELETE FROM Products WHERE ProductID=?",(id,))
    
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)