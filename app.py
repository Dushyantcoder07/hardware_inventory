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

@app.route("/dashboard")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    # Total Products
    cursor.execute("SELECT COUNT(*) FROM Products")
    total_products = cursor.fetchone()[0]

    # Total Stock
    cursor.execute("SELECT SUM(Quantity) FROM Products")
    total_stock = cursor.fetchone()[0]

    # Total Brands
    cursor.execute("SELECT COUNT(*) FROM Brands")
    total_brands = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_stock=total_stock,
        total_brands=total_brands
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

@app.route("/analytics")
def analytics():

    #importing pandas
    import pandas as pd 
    conn = get_connection()
    query = """SELECT Category,
                COUNT(*) AS ProductCount
                FROM Products
                GROUP BY Category"""
    
    df = pd.read_sql(query,conn)

    conn.close()
    
    #importing matplot for graph
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,5))

    plt.bar(
    df["Category"],
    df["ProductCount"]
    )

    plt.title("Products by Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Products")

    plt.savefig("static/category_graph.png")

    plt.tight_layout()

    plt.close()
    return render_template("analytics.html")


if __name__ == "__main__":
    app.run(debug=True)