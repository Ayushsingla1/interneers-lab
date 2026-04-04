from django.core.management.base import BaseCommand
from product.infrastructure.models import ProductDocument, CategoryDocument
import datetime


class Command(BaseCommand):
    help = "Seed products with upsert functionality"

    def handle(self, *args, **options):
        products_data = [
            {
                "name": "Tata Salt",
                "description": "Iodized vacuum evaporated salt, fine grain quality for everyday cooking",
                "brand": "Tata",
                "price": 25,
                "quantity": 500,
                "category": "Pantry Essentials",
            },
            {
                "name": "Fortune Sunflower Oil",
                "description": "Refined sunflower oil rich in Vitamin E, ideal for frying and cooking",
                "brand": "Fortune",
                "price": 180,
                "quantity": 200,
                "category": "Pantry Essentials",
            },
            {
                "name": "India Gate Basmati Rice",
                "description": "Premium aged basmati rice with long grains and rich aroma",
                "brand": "India Gate",
                "price": 320,
                "quantity": 150,
                "category": "Pantry Essentials",
            },
            {
                "name": "Aashirvaad Atta",
                "description": "Whole wheat flour made from selected grains for soft rotis",
                "brand": "Aashirvaad",
                "price": 290,
                "quantity": 180,
                "category": "Pantry Essentials",
            },
            {
                "name": "Tata Tea Gold",
                "description": "Premium blend of long leaf and dust tea for a rich, flavourful cup",
                "brand": "Tata Tea",
                "price": 220,
                "quantity": 300,
                "category": "Beverages",
            },
            {
                "name": "Nescafe Classic",
                "description": "Pure instant coffee with rich aroma and bold taste",
                "brand": "Nescafe",
                "price": 350,
                "quantity": 250,
                "category": "Beverages",
            },
            {
                "name": "Real Fruit Juice Orange",
                "description": "100% real fruit juice with no added preservatives or colours",
                "brand": "Dabur Real",
                "price": 99,
                "quantity": 400,
                "category": "Beverages",
            },
            {
                "name": "Bisleri Mineral Water 1L",
                "description": "Pure and safe drinking water from a trusted brand",
                "brand": "Bisleri",
                "price": 20,
                "quantity": 1000,
                "category": "Beverages",
            },
            {
                "name": "Lay's Classic Salted Chips",
                "description": "Crispy potato chips with a classic salted flavour, perfect for snacking",
                "brand": "Lay's",
                "price": 20,
                "quantity": 600,
                "category": "Snacks & Confectionery",
            },
            {
                "name": "Cadbury Dairy Milk",
                "description": "Smooth and creamy milk chocolate made with rich cocoa",
                "brand": "Cadbury",
                "price": 50,
                "quantity": 500,
                "category": "Snacks & Confectionery",
            },
            {
                "name": "Haldiram's Aloo Bhujia",
                "description": "Crunchy and spicy potato snack, a classic Indian namkeen",
                "brand": "Haldiram's",
                "price": 65,
                "quantity": 450,
                "category": "Snacks & Confectionery",
            },
            {
                "name": "Oreo Chocolate Sandwich Cookies",
                "description": "Chocolate biscuit with a sweet cream filling, a timeless favourite",
                "brand": "Oreo",
                "price": 40,
                "quantity": 550,
                "category": "Snacks & Confectionery",
            },
            {
                "name": "Organic India Tulsi Green Tea",
                "description": "Certified organic tulsi and green tea blend for immunity and calm",
                "brand": "Organic India",
                "price": 250,
                "quantity": 200,
                "category": "Health & Wellness",
            },
            {
                "name": "Saffola Gold Oats",
                "description": "100% natural rolled oats, high in fibre and great for heart health",
                "brand": "Saffola",
                "price": 160,
                "quantity": 300,
                "category": "Health & Wellness",
            },
            {
                "name": "Patanjali Aloe Vera Juice",
                "description": "Natural aloe vera juice for digestion, skin, and overall wellness",
                "brand": "Patanjali",
                "price": 120,
                "quantity": 250,
                "category": "Health & Wellness",
            },
            {
                "name": "True Elements Mixed Seeds",
                "description": "Roasted mix of pumpkin, sunflower, and flax seeds for a healthy snack",
                "brand": "True Elements",
                "price": 299,
                "quantity": 180,
                "category": "Health & Wellness",
            },
            {
                "name": "Pillsbury Maida",
                "description": "Fine refined flour perfect for baking cakes, pastries, and bread",
                "brand": "Pillsbury",
                "price": 75,
                "quantity": 350,
                "category": "Baking & Cooking",
            },
            {
                "name": "Dr. Oetker Baking Powder",
                "description": "Reliable leavening agent for perfectly risen cakes and baked goods",
                "brand": "Dr. Oetker",
                "price": 85,
                "quantity": 400,
                "category": "Baking & Cooking",
            },
            {
                "name": "Weikfield Cocoa Powder",
                "description": "Rich unsweetened cocoa powder for baking and making hot chocolate",
                "brand": "Weikfield",
                "price": 130,
                "quantity": 300,
                "category": "Baking & Cooking",
            },
            {
                "name": "Milkmaid Condensed Milk",
                "description": "Sweetened condensed milk ideal for desserts, baking, and beverages",
                "brand": "Nestle",
                "price": 110,
                "quantity": 450,
                "category": "Baking & Cooking",
            },
            {
                "name": "Kellogg's Corn Flakes",
                "description": "Classic toasted corn flakes, a crispy and nutritious breakfast choice",
                "brand": "Kellogg's",
                "price": 175,
                "quantity": 400,
                "category": "Breakfast Foods",
            },
            {
                "name": "Amul Butter",
                "description": "Pasteurised butter made from fresh cream, perfect for spreading",
                "brand": "Amul",
                "price": 55,
                "quantity": 600,
                "category": "Breakfast Foods",
            },
            {
                "name": "Kissan Mixed Fruit Jam",
                "description": "Fruity and sweet jam made from real mixed fruits, great on toast",
                "brand": "Kissan",
                "price": 115,
                "quantity": 500,
                "category": "Breakfast Foods",
            },
            {
                "name": "Quaker Oats",
                "description": "Whole grain rolled oats for a wholesome and filling breakfast",
                "brand": "Quaker",
                "price": 140,
                "quantity": 350,
                "category": "Breakfast Foods",
            },
            {
                "name": "Barilla Spaghetti",
                "description": "Premium Italian durum wheat spaghetti for authentic pasta dishes",
                "brand": "Barilla",
                "price": 220,
                "quantity": 250,
                "category": "International Foods",
            },
            {
                "name": "Kikkoman Soy Sauce",
                "description": "Naturally brewed Japanese soy sauce for marinades and stir-fries",
                "brand": "Kikkoman",
                "price": 310,
                "quantity": 200,
                "category": "International Foods",
            },
            {
                "name": "Knorr Chicken Noodle Soup",
                "description": "Ready-to-cook noodle soup mix with chicken flavour from Knorr",
                "brand": "Knorr",
                "price": 60,
                "quantity": 400,
                "category": "International Foods",
            },
            {
                "name": "Del Monte Sweet Corn",
                "description": "Tender and sweet golden corn kernels in brine, ready to use",
                "brand": "Del Monte",
                "price": 95,
                "quantity": 350,
                "category": "International Foods",
            },
            # Condiments & Spices
            {
                "name": "MDH Garam Masala",
                "description": "Aromatic blend of whole spices ground to perfection for rich curries",
                "brand": "MDH",
                "price": 80,
                "quantity": 500,
                "category": "Condiments & Spices",
            },
            {
                "name": "Maggi Hot & Sweet Sauce",
                "description": "Tangy tomato-chilli sauce perfect as a dip or cooking ingredient",
                "brand": "Maggi",
                "price": 90,
                "quantity": 450,
                "category": "Condiments & Spices",
            },
            {
                "name": "Everest Turmeric Powder",
                "description": "Pure and vibrant turmeric powder with high curcumin content",
                "brand": "Everest",
                "price": 55,
                "quantity": 600,
                "category": "Condiments & Spices",
            },
            {
                "name": "Heinz Tomato Ketchup",
                "description": "Classic thick and rich tomato ketchup, a household favourite worldwide",
                "brand": "Heinz",
                "price": 160,
                "quantity": 400,
                "category": "Condiments & Spices",
            },
        ]

        self.stdout.write("Starting product seeding...")

        category_cache = {}

        for product_data in products_data:
            try:
                category_title = product_data["category"]

                if category_title not in category_cache:
                    category = CategoryDocument.objects(title=category_title).first()
                    if not category:
                        self.stdout.write(
                            self.style.ERROR(
                                f"✗ Category '{category_title}' not found. Run seed_categories first."
                            )
                        )
                        continue
                    category_cache[category_title] = category

                category_doc = category_cache[category_title]

                result = ProductDocument.objects(name=product_data["name"]).update_one(
                    set__description=product_data["description"],
                    set__brand=product_data["brand"],
                    set__price=product_data["price"],
                    set__quantity=product_data["quantity"],
                    set__category=category_doc,
                    set__created_at=datetime.datetime.now(),
                    set__updated_at=datetime.datetime.now(),
                    upsert=True,
                )

                if result == 1:
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Created product: {product_data['name']}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Updated product: {product_data['name']}")
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error processing product '{product_data['name']}': {str(e)}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("\nProduct seeding completed!"))
