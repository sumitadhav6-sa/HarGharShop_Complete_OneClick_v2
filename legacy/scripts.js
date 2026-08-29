// HarGharShop Available Products List
const products = [
    {
        id: 1,
        title: "Boat Rockerz 450 Bluetooth Wireless Headphones",
        category: "electronics",
        price: 1499,
        oldPrice: 3990,
        rating: "★★★★☆ (4.5)",
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"
    },
    {
        id: 2,
        title: "Men's Premium Cotton Slim Fit Casual Shirt",
        category: "fashion",
        price: 699,
        oldPrice: 1499,
        rating: "★★★★★ (4.8)",
        image: "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500"
    },
    {
        id: 3,
        title: "Smart Android 4K UHD LED TV (43 Inch)",
        category: "electronics",
        price: 24999,
        oldPrice: 38990,
        rating: "★★★★☆ (4.7)",
        image: "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500"
    },
    {
        id: 4,
        title: "Stainless Steel Vacuum Insulated Water Flask",
        category: "home",
        price: 499,
        oldPrice: 999,
        rating: "★★★★☆ (4.3)",
        image: "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"
    },
    {
        id: 5,
        title: "Nike Air Lightweight Running & Gym Shoes",
        category: "footwear",
        price: 3299,
        oldPrice: 5999,
        rating: "★★★★★ (4.9)",
        image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"
    },
    {
        id: 6,
        title: "Modern Non-Stick 3-Piece Cookware Set",
        category: "home",
        price: 1899,
        oldPrice: 3499,
        rating: "★★★★☆ (4.2)",
        image: "https://images.unsplash.com/photo-1584990347449-399066607212?w=500"
    },
    {
        id: 7,
        title: "Women's Embroidered Traditional Kurti Set",
        category: "fashion",
        price: 899,
        oldPrice: 1999,
        rating: "★★★★☆ (4.6)",
        image: "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500"
    },
    {
        id: 8,
        title: "Smart Fitness Watch with Heart Rate Sensor",
        category: "electronics",
        price: 1999,
        oldPrice: 4999,
        rating: "★★★★☆ (4.4)",
        image: "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500"
    }
];

let cart = [];

// Render All Available Products to Screen
function renderProducts(items) {
    const grid = document.getElementById("productGrid");
    if (!grid) return;
    
    grid.innerHTML = "";

    items.forEach(product => {
        const card = document.createElement("div");
        card.classList.add("product-card");
        card.innerHTML = `
            <img src="${product.image}" alt="${product.title}">
            <span class="stock-status">✔ AVAILABLE (IN STOCK)</span>
            <h4>${product.title}</h4>
            <div class="product-rating">${product.rating}</div>
            <div class="price-row">
                <span class="price">₹${product.price.toLocaleString('en-IN')}</span>
                <span class="old-price">₹${product.oldPrice.toLocaleString('en-IN')}</span>
            </div>
            <button class="add-btn" onclick="addToCart(${product.id})">
                <i class="fa-solid fa-cart-plus"></i> Add to Cart
            </button>
        `;
        grid.appendChild(card);
    });
}

// Category Filter
function filterCategory(categoryName, element) {
    const buttons = document.querySelectorAll('.cat-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    if (element) element.classList.add('active');

    const heading = document.getElementById('categoryHeading');
    heading.innerText = categoryName === 'all' ? 'All Available Products' : categoryName.toUpperCase() + ' (Available)';

    if (categoryName === 'all') {
        renderProducts(products);
    } else {
        const filtered = products.filter(p => p.category === categoryName);
        renderProducts(filtered);
    }
}

// Add Item To Cart
function addToCart(productId) {
    const item = products.find(p => p.id === productId);
    const existing = cart.find(c => c.id === productId);

    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({ ...item, qty: 1 });
    }
    updateCartUI();
}

// Remove Item
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartUI();
}

// Update Cart Display
function updateCartUI() {
    const cartItems = document.getElementById("cartItems");
    const cartCount = document.getElementById("cartCount");
    const cartTotal = document.getElementById("cartTotal");

    const totalCount = cart.reduce((sum, item) => sum + item.qty, 0);
    cartCount.innerText = totalCount;

    const total = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
    cartTotal.innerText = total.toLocaleString('en-IN');

    if (cart.length === 0) {
        cartItems.innerHTML = '<p style="text-align:center; color:#94a3b8; margin-top:20px;">Aapka cart khali hai.</p>';
        return;
    }

    cartItems.innerHTML = "";
    cart.forEach(item => {
        const itemDiv = document.createElement("div");
        itemDiv.classList.add("cart-item");
        itemDiv.innerHTML = `
            <div class="cart-item-details">
                <h5>${item.title}</h5>
                <p>₹${item.price.toLocaleString('en-IN')} × ${item.qty}</p>
            </div>
            <button class="del-btn" onclick="removeFromCart(${item.id})">
                <i class="fa-solid fa-trash"></i>
            </button>
        `;
        cartItems.appendChild(itemDiv);
    });
}

// Toggle Cart Sidebar
function toggleCart() {
    document.getElementById("cartDrawer").classList.toggle("open");
}

// Search
function searchProducts() {
    const term = document.getElementById("searchInput").value.toLowerCase();
    const filtered = products.filter(p => p.title.toLowerCase().includes(term));
    renderProducts(filtered);
}

// Order Checkout
function checkoutOrder() {
    if (cart.length === 0) {
        alert("Pehle cart mein items add karein!");
        return;
    }
    alert("🎉 Dhanyawad! Aapka order HarGharShop par book ho gaya hai.\nPlatform created by Sumit Adhav.");
    cart = [];
    updateCartUI();
    toggleCart();
}

// Turant sabhi products screen par load karein
renderProducts(products);