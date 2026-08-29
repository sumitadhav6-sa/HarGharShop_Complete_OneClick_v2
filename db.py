import sqlite3
from config import Config
from werkzeug.security import generate_password_hash

def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn=get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL DEFAULT 'customer');
    CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,category TEXT NOT NULL,subcategory TEXT NOT NULL,price REAL NOT NULL,old_price REAL DEFAULT 0,rating REAL DEFAULT 4.0,stock INTEGER DEFAULT 10,image TEXT,description TEXT);
    CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,customer_name TEXT NOT NULL,mobile TEXT NOT NULL,address TEXT NOT NULL,payment TEXT NOT NULL,total REAL NOT NULL,status TEXT DEFAULT 'Placed');
    CREATE TABLE IF NOT EXISTS order_items(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER,product_id INTEGER,name TEXT NOT NULL,price REAL NOT NULL,qty INTEGER NOT NULL);
    """)
    conn.commit(); conn.close()

def seed_data():
    conn=get_db()
    if not conn.execute("SELECT id FROM users WHERE email=?",(Config.ADMIN_EMAIL,)).fetchone():
        conn.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                     ("Sumit Adhav",Config.ADMIN_EMAIL,generate_password_hash(Config.ADMIN_PASSWORD),"admin"))
    if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]==0:
        def u(q): return "https://images.unsplash.com/photo-"+q+"?auto=format&fit=crop&w=700&q=80"
        P=[
        ("Samsung Galaxy S25","mobiles","smartphones",74999,82999,4.8,25,u("1598327105666-5b89351aff97"),"Premium Android smartphone with flagship performance."),
        ("iPhone 16","mobiles","smartphones",69999,79999,4.9,20,u("1591337676887-a217a6970a8a"),"Apple smartphone with advanced camera and performance."),
        ("OnePlus 13R","mobiles","smartphones",42999,49999,4.7,18,u("1511707171634-5f897ff02aa9"),"Fast, smooth smartphone with a large display."),
        ("Redmi Note 14 Pro","mobiles","smartphones",26999,31999,4.5,32,u("1511707171634-5f897ff02aa9"),"Feature-packed everyday smartphone."),
        ("Realme Narzo 70","mobiles","smartphones",15999,18999,4.4,30,u("1511707171634-5f897ff02aa9"),"Value smartphone for everyday use."),
        ("Nokia 105","mobiles","feature-phones",1899,2199,4.2,50,u("1523275335684-37898b6baf30"),"Simple and reliable feature phone."),
        ("USB-C Fast Charger 33W","mobiles","mobile-accessories",799,1299,4.5,80,u("1609592424841-74c0c0f6e7f8"),"Compact fast charger with USB-C support."),
        ("Wireless Power Bank 10000mAh","mobiles","mobile-accessories",1499,2499,4.4,65,u("1609592424841-74c0c0f6e7f8"),"Portable power bank for phones and gadgets."),
        ("HP 15 Laptop","electronics","laptops",54999,64999,4.5,15,u("1496181133206-80ce9b88a853"),"Everyday productivity laptop."),
        ("Dell Inspiron 14","electronics","laptops",62999,72999,4.6,12,u("1517336714739-489689fd1ca8"),"Powerful laptop for work and study."),
        ("Lenovo IdeaPad Slim 3","electronics","laptops",51999,60999,4.5,17,u("1496181133206-80ce9b88a853"),"Slim laptop for students and professionals."),
        ("boAt Rockerz Headphones","electronics","audio",1499,3999,4.4,50,u("1505740420928-5e560c06d30e"),"Wireless Bluetooth headphones."),
        ("Sony Wireless Headphones","electronics","audio",4999,6999,4.7,25,u("1505740420928-5e560c06d30e"),"Immersive wireless audio."),
        ("JBL Bluetooth Speaker","electronics","audio",2999,4499,4.6,35,u("1608043152269-423dbba4e7c1"),"Portable speaker with powerful sound."),
        ("Smart LED TV 43 Inch","electronics","televisions",24999,38999,4.7,10,u("1593359677879-a4bb92f829d1"),"4K smart television."),
        ("55 Inch 4K Smart TV","electronics","televisions",39999,54999,4.6,8,u("1593359677879-a4bb92f829d1"),"Large 4K television for home entertainment."),
        ("Smart Fitness Watch","electronics","smartwatches",1999,4999,4.4,35,u("1575311373937-040b8e1fd5b6"),"Fitness tracking smartwatch."),
        ("Premium AMOLED Smartwatch","electronics","smartwatches",4999,7999,4.6,22,u("1575311373937-040b8e1fd5b6"),"AMOLED smartwatch with health and fitness tracking."),
        ("Mirrorless Camera","electronics","cameras",54999,64999,4.7,7,u("1516035069371-29a1b244cc32"),"Compact camera for creators."),
        ("Digital Action Camera","electronics","cameras",7999,10999,4.3,14,u("1516035069371-29a1b244cc32"),"Action camera for travel and outdoor videos."),
        ("Men Cotton Shirt","fashion","mens-fashion",699,1499,4.4,60,u("1596755094514-f87e34085b2c"),"Comfortable cotton shirt."),
        ("Men Slim Fit Jeans","fashion","mens-fashion",1199,2299,4.5,40,u("1542272604-787c3835535d"),"Classic slim-fit denim."),
        ("Men Casual T-Shirt","fashion","mens-fashion",499,999,4.3,75,u("1521572163474-6864f9cf17ab"),"Soft everyday casual t-shirt."),
        ("Women's Kurti Set","fashion","womens-fashion",899,1999,4.6,45,u("1610030469983-98e550d6193c"),"Traditional kurti set."),
        ("Women's Saree","fashion","womens-fashion",1299,2499,4.5,35,u("1610030469983-98e550d6193c"),"Elegant saree for festive occasions."),
        ("Women's Handbag","fashion","womens-fashion",999,1999,4.4,30,u("1584917865442-de89df76afd3"),"Stylish everyday handbag."),
        ("Kids Printed T-Shirt","fashion","kids-fashion",399,799,4.5,55,u("1503919545889-aef636e10ad4"),"Comfortable printed kids t-shirt."),
        ("Kids Casual Dress","fashion","kids-fashion",699,1299,4.4,35,u("1518831959640-1c0f6f3e4b3a"),"Comfortable casual kids dress."),
        ("Nike Running Shoes","footwear","sports-shoes",3299,5999,4.8,40,u("1542291026-7eec264c27ff"),"Lightweight running shoes."),
        ("Adidas Sports Shoes","footwear","sports-shoes",3799,6499,4.7,32,u("1542291026-7eec264c27ff"),"Performance shoes for training."),
        ("Men Casual Sneakers","footwear","casual-shoes",1499,2499,4.4,45,u("1525966222134-fcfa99b8ae77"),"Everyday casual sneakers."),
        ("Women's Casual Shoes","footwear","casual-shoes",1299,2299,4.5,38,u("1543163521-1bf539c55dd2"),"Comfortable casual shoes."),
        ("Women's Flat Sandals","footwear","sandals",699,1299,4.3,50,u("1543163521-1bf539c55dd2"),"Comfortable daily sandals."),
        ("Men Comfort Sandals","footwear","sandals",599,999,4.2,45,u("1542291026-7eec264c27ff"),"Lightweight comfort sandals."),
        ("Non-Stick Cookware Set","home","kitchen",1899,3499,4.3,25,u("1584990347449-399066607212"),"Kitchen cookware set."),
        ("Mixer Grinder 750W","home","kitchen",2499,3999,4.5,20,u("1556911220-bff31c812dba"),"Powerful mixer grinder for home."),
        ("Electric Kettle 1.5L","home","kitchen",899,1599,4.4,40,u("1594212699903-ec8a3eca50f5"),"Fast boiling electric kettle."),
        ("Decorative Wall Clock","home","home-decor",799,1499,4.4,30,u("1563861826100-9cb868fdbe1c"),"Modern wall clock for home decor."),
        ("LED Table Lamp","home","home-decor",599,999,4.5,45,u("1507473885765-e6ed057f782c"),"Warm LED table lamp."),
        ("Air Purifier","home","appliances",6999,9999,4.5,12,u("1585771724684-383e3b2f1f1d"),"Compact air purifier for rooms."),
        ("Room Heater","home","appliances",1999,2999,4.3,18,u("1484704849700-f032a568e944"),"Compact room heater."),
        ("Skin Moisturizer","beauty","skincare",349,599,4.4,70,u("1556228578-0d85b1a4d571"),"Daily moisturizing skincare."),
        ("Vitamin C Face Serum","beauty","skincare",499,899,4.5,55,u("1620916566398-39f1143c2b5d"),"Lightweight vitamin C serum."),
        ("Matte Lipstick","beauty","makeup",399,699,4.5,60,u("1586495777744-4413f21062fa"),"Long-lasting matte lipstick."),
        ("Compact Makeup Kit","beauty","makeup",899,1499,4.4,35,u("1596462502278-27bfdc403348"),"Everyday makeup essentials."),
        ("Herbal Shampoo","beauty","hair-care",299,499,4.3,65,u("1556228720-195a672e8a03"),"Gentle shampoo for regular use."),
        ("Hair Serum","beauty","hair-care",349,599,4.4,50,u("1522337360788-8b13dee7a37e"),"Smoothing hair serum."),
        ("Basmati Rice 5kg","groceries","staples",499,599,4.6,100,u("1586201375761-83865001e31c"),"Premium basmati rice."),
        ("Wheat Atta 5kg","groceries","staples",299,349,4.5,100,u("1509440159596-0249088772ff"),"Fresh whole wheat flour."),
        ("Toor Dal 1kg","groceries","staples",159,199,4.5,100,u("1585996903551-7c6f7b4e5d55"),"Everyday protein-rich dal."),
        ("Namkeen Family Pack","groceries","snacks",149,199,4.3,80,u("1621939514649-89b2f0d1f2e8"),"Crunchy family snack pack."),
        ("Chocolate Cookies","groceries","snacks",99,129,4.4,90,u("1499636136210-6f4f4b1f6f9f"),"Crispy chocolate cookies."),
        ("Green Tea 100 Bags","groceries","beverages",249,349,4.5,60,u("1594631252845-6b4d7c6f8a9d"),"Refreshing green tea."),
        ("Instant Coffee 200g","groceries","beverages",299,399,4.4,65,u("1512568400610-62da28bce7a0"),"Rich instant coffee."),
        ]
        conn.executemany("""INSERT INTO products(name,category,subcategory,price,old_price,rating,stock,image,description) VALUES(?,?,?,?,?,?,?,?,?)""",P)
    conn.commit(); conn.close()
