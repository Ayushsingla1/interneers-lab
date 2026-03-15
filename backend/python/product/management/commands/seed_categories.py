from django.core.management.base import BaseCommand
from product.infrastructure.models import CategoryDocument


class Command(BaseCommand):
    help = "Seed categories with upsert functionality"

    def handle(self, *args, **options):
        """Seed categories with upsert functionality"""

        categories_data = [
            {
                "title": "Pantry Essentials",
                "description": "Basic pantry staples and cooking essentials",
            },
            {
                "title": "Beverages",
                "description": "Drinks, teas, coffees, and other beverages",
            },
            {
                "title": "Snacks & Confectionery",
                "description": "Snacks, chocolates, candies, and sweet treats",
            },
            {
                "title": "Health & Wellness",
                "description": "Organic, natural, and health-focused products",
            },
            {
                "title": "Baking & Cooking",
                "description": "Ingredients and supplies for baking and cooking",
            },
            {
                "title": "Breakfast Foods",
                "description": "Cereals, spreads, and breakfast essentials",
            },
            {
                "title": "International Foods",
                "description": "Specialty foods from around the world",
            },
            {
                "title": "Condiments & Spices",
                "description": "Sauces, spices, and flavor enhancers",
            },
        ]

        self.stdout.write("Starting category seeding...")

        for category_data in categories_data:
            try:

                result = CategoryDocument.objects(
                    title=category_data["title"]
                ).update_one(set__description=category_data["description"], upsert=True)

                if result == 1:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Created category: {category_data['title']}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠ No changes for category: {category_data['title']}"
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Error processing category '{category_data['title']}': {str(e)}"
                    )
                )

        self.stdout.write(self.style.SUCCESS(f"\nSeeding completed!"))
