from flask import Flask, render_template_string, request
import json
import os

app = Flask(__name__)

# -----------------------------------------
# Load inventory from metadata
# -----------------------------------------

def load_inventory():
    inventory = []
    folder = "reports_store/metadata"

    if not os.path.exists(folder):
        return inventory

    for file in os.listdir(folder):
        if file.endswith("latest.json"):
            try:
                with open(os.path.join(folder, file), encoding="utf-8") as f:
                    data = json.load(f)
                    inventory.append(data)
            except:
                continue

    return inventory


# -----------------------------------------
# Main Store Page
# -----------------------------------------

@app.route("/")
def store():
    inventory = load_inventory()

    city = request.args.get("city")
    property_type = request.args.get("property")

    # filtering
    if city:
        inventory = [i for i in inventory if i.get("city") == city]

    if property_type:
        inventory = [i for i in inventory if i.get("property_type") == property_type]

    return render_template_string(TEMPLATE, items=inventory)


# -----------------------------------------
# UI Template (Cute + Premium)
# -----------------------------------------

TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>Warda Store</title>
<style>
body {
    font-family: 'Arial';
    background: #f7f7fb;
    margin: 0;
}

.header {
    text-align: center;
    padding: 30px;
    background: linear-gradient(90deg, #ff7eb3, #ff758c);
    color: white;
    font-size: 28px;
    font-weight: bold;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    padding: 30px;
}

.card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

.title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}

.meta {
    color: #777;
    font-size: 14px;
    margin-bottom: 10px;
}

.price {
    font-size: 20px;
    color: #ff4d6d;
    font-weight: bold;
}

.button {
    margin-top: 10px;
    display: block;
    text-align: center;
    background: #ff758c;
    color: white;
    padding: 10px;
    border-radius: 10px;
    text-decoration: none;
}

.button:hover {
    background: #ff4d6d;
}

</style>
</head>

<body>

<div class="header">
💎 متجر التقارير الذكية | Warda Intelligence
</div>

<div class="grid">

{% for item in items %}

<div class="card">
    <div class="title">
        {{item.product_title}} - {{item.district}}
    </div>

    <div class="meta">
        📍 {{item.city}} | 🏠 {{item.property_type}}
    </div>

    <div class="price">
        ${{item.price}}
    </div>

    <a class="button" href="#">
        عرض التقرير
    </a>
</div>

{% endfor %}

</div>

</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
