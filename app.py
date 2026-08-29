from flask import Flask, jsonify, request, session, send_from_directory
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from db import get_db, init_db, seed_data

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)

FRONTEND_DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))

init_db()
seed_data()

CATEGORIES = {
    "all":["all"],
    "mobiles":["smartphones","feature-phones","mobile-accessories"],
    "electronics":["laptops","audio","televisions","smartwatches","cameras"],
    "fashion":["mens-fashion","womens-fashion","kids-fashion"],
    "footwear":["sports-shoes","casual-shoes","sandals"],
    "home":["kitchen","home-decor","appliances"],
    "beauty":["skincare","makeup","hair-care"],
    "groceries":["staples","snacks","beverages"]
}

@app.get("/api/health")
def health():
    return jsonify({"status":"ok","app":"HarGharShop"})

@app.get("/api/categories")
def categories():
    return jsonify(CATEGORIES)

@app.get("/api/products")
def products():
    category=request.args.get("category","all")
    subcategory=request.args.get("subcategory","")
    search=request.args.get("search","").strip()
    conn=get_db()
    query="SELECT * FROM products WHERE 1=1"
    params=[]
    if category!="all":
        query+=" AND category=?"; params.append(category)
    if subcategory:
        query+=" AND subcategory=?"; params.append(subcategory)
    if search:
        query+=" AND (name LIKE ? OR category LIKE ? OR subcategory LIKE ?)"
        term=f"%{search}%"; params += [term,term,term]
    query+=" ORDER BY id DESC"
    rows=conn.execute(query,params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.post("/api/register")
def register():
    d=request.get_json() or {}
    name=d.get("name","").strip(); email=d.get("email","").strip().lower(); password=d.get("password","")
    if not name or not email or len(password)<6:
        return jsonify({"error":"Name, valid email and 6+ character password required"}),400
    conn=get_db()
    try:
        conn.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                     (name,email,generate_password_hash(password),"customer"))
        conn.commit()
    except Exception:
        conn.close(); return jsonify({"error":"Email already registered"}),409
    conn.close()
    return jsonify({"message":"Registration successful"}),201

@app.post("/api/login")
def login():
    d=request.get_json() or {}
    email=d.get("email","").strip().lower(); password=d.get("password","")
    conn=get_db(); user=conn.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone(); conn.close()
    if not user: return jsonify({"error":"Invalid email or password"}),401
    valid=(user["role"]=="admin" and password==Config.ADMIN_PASSWORD) or check_password_hash(user["password"],password)
    if not valid: return jsonify({"error":"Invalid email or password"}),401
    session["user_id"]=user["id"]; session["role"]=user["role"]; session["name"]=user["name"]
    return jsonify({"message":"Login successful","user":{"name":user["name"],"role":user["role"]}})

@app.post("/api/logout")
def logout():
    session.clear(); return jsonify({"message":"Logged out"})

@app.get("/api/me")
def me():
    if "user_id" not in session: return jsonify({"loggedIn":False})
    return jsonify({"loggedIn":True,"name":session.get("name"),"role":session.get("role")})

def admin_required():
    return session.get("role")=="admin"

@app.post("/api/admin/products")
def add_product():
    if not admin_required(): return jsonify({"error":"Admin login required"}),403
    d=request.get_json() or {}
    if any(not d.get(k) for k in ["name","category","subcategory","price"]):
        return jsonify({"error":"name, category, subcategory and price are required"}),400
    conn=get_db()
    cur=conn.execute("""INSERT INTO products
    (name,category,subcategory,price,old_price,rating,stock,image,description)
    VALUES(?,?,?,?,?,?,?,?,?)""",
    (d["name"],d["category"],d["subcategory"],float(d["price"]),float(d.get("old_price",0)),
     float(d.get("rating",4)),int(d.get("stock",10)),d.get("image",""),d.get("description","")))
    conn.commit(); row=conn.execute("SELECT * FROM products WHERE id=?",(cur.lastrowid,)).fetchone(); conn.close()
    return jsonify(dict(row)),201

@app.delete("/api/admin/products/<int:product_id>")
def delete_product(product_id):
    if not admin_required(): return jsonify({"error":"Admin login required"}),403
    conn=get_db(); conn.execute("DELETE FROM products WHERE id=?",(product_id,)); conn.commit(); conn.close()
    return jsonify({"message":"Product deleted"})

@app.post("/api/orders")
def order():
    if "user_id" not in session: return jsonify({"error":"Please login before placing an order"}),401
    d=request.get_json() or {}
    required=["customer_name","mobile","address","payment","total","items"]
    if any(k not in d or not d[k] for k in required): return jsonify({"error":"All checkout fields are required"}),400
    if not str(d["mobile"]).isdigit() or len(str(d["mobile"]))!=10: return jsonify({"error":"Mobile number must be exactly 10 digits"}),400
    items=d["items"]
    if not isinstance(items,list) or not items: return jsonify({"error":"Cart is empty"}),400
    conn=get_db()
    cur=conn.execute("INSERT INTO orders(user_id,customer_name,mobile,address,payment,total) VALUES(?,?,?,?,?,?)",
        (session["user_id"],d["customer_name"],d["mobile"],d["address"],d["payment"],float(d["total"])))
    oid=cur.lastrowid
    for x in items:
        conn.execute("INSERT INTO order_items(order_id,product_id,name,price,qty) VALUES(?,?,?,?,?)",
                     (oid,int(x["id"]),x["name"],float(x["price"]),int(x["qty"])))
    conn.commit(); conn.close()
    return jsonify({"message":"Order placed successfully","orderId":oid}),201

@app.get("/api/orders")
def my_orders():
    if "user_id" not in session: return jsonify({"error":"Login required"}),401
    conn=get_db()
    rows=conn.execute("SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",(session["user_id"],)).fetchall()
    out=[]
    for r in rows:
        d=dict(r); d["items"]=[dict(x) for x in conn.execute("SELECT * FROM order_items WHERE order_id=?",(r["id"],)).fetchall()]; out.append(d)
    conn.close(); return jsonify(out)

@app.get("/api/admin/orders")
def admin_orders():
    if not admin_required(): return jsonify({"error":"Admin login required"}),403
    conn=get_db(); rows=conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall(); conn.close()
    return jsonify([dict(r) for r in rows])


@app.put("/api/admin/orders/<int:order_id>")
def update_order(order_id):
    if not admin_required(): return jsonify({"error":"Admin login required"}),403
    status=(request.get_json() or {}).get("status","Placed")
    allowed={"Placed","Packed","Shipped","Delivered","Cancelled"}
    if status not in allowed: return jsonify({"error":"Invalid status"}),400
    conn=get_db(); conn.execute("UPDATE orders SET status=? WHERE id=?",(status,order_id)); conn.commit(); conn.close()
    return jsonify({"message":"Order status updated"})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path.startswith("api/"):
        return jsonify({"error": "API endpoint not found"}), 404
    if os.path.isdir(FRONTEND_DIST):
        requested = os.path.join(FRONTEND_DIST, path)
        if path and os.path.isfile(requested):
            return send_from_directory(FRONTEND_DIST, path)
        return send_from_directory(FRONTEND_DIST, "index.html")
    return jsonify({"message": "Frontend is not built. Run START_ONE_SERVER.bat or npm run build."}), 503

if __name__=="__main__":
    app.run(debug=False,port=5000)
