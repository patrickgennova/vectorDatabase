
products_data = [
    {
        "name": "Relaxed Fit Tee",
        "section": "MEN",
        "family": "T-SHIRTS",
        "fit": "Non-stretch, Relaxed fit",
        "composition": "100% cotton. Jersey. Crewneck, Short sleeves",
        "color": "Red"
    },
    {
        "name": "Relaxed Fit Tee",
        "section": "MEN",
        "family": "T-SHIRTS",
        "fit": "Non-stretch, Relaxed fit",
        "composition": "100% cotton. Jersey. Crewneck, Short sleeves",
        "color": "Green"
    },
    {
        "name": "TRUCKER JACKET",
        "section": "MEN",
        "family": "JACKETS",
        "fit": "Standard fit",
        "composition": "100% cotton, Denim, Point collar, Long sleeves",
        "color": "Gray"
    },
    {
        "name": "SLIM WELT POCKET JEANS",
        "section": "WOMEN",
        "family": "JEANS",
        "fit": "Mid rise: 8 3/4'', Inseam: 30'', Leg opening: 13''",
        "composition": "62% cotton, 28% viscose (ECOVERO™), 8% elastomultiester, 2% elastane, Denim, Stretch, Zip fly, 5-pocket styling",
        "color": "Black"
    },
    {
        "name": "BAGGY DAD UTILITY PANTS",
        "section": "WOMEN",
        "family": "JEANS",
        "fit": "Mid rise, Straight leg",
        "composition": "95% cotton, 5% recycled cotton, Denim, No Stretch",
        "color": "Green"
    },
    {
        "name": "THE PERFECT TEE",
        "section": "WOMEN",
        "family": "T-SHIRTS",
        "fit": "Standard fit, Model wears a size small",
        "composition": "100% cotton, Crewneck, Short sleeves",
        "color": "White"
    },
    {
        "name": "LELOU SHRUNKEN MOTO JACKET",
        "section": "WOMEN",
        "family": "JACKETS",
        "fit": "Slim fit",
        "composition": "100% polyurethane - releases plastic microfibers into the environment during washing, Long sleeves",
        "color": "Black"
    }
]


import weaviate
import weaviate.classes as wvc


def init():
    # Connect with default parameters
    client = weaviate.connect_to_local()

    # Check if the connection was successful
    try:
        client.is_ready()
        print("Successfully connected to Weaviate.")
        products_collection = client.collections.create(
                name="Products",
                vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_transformers(
                    vectorize_collection_name=True
                    )
                )

        products_objs = list()
        for i,d in enumerate(products_data):
            products_objs.append({
                "name": d["name"],
                "section": d["section"],
                "family" : d["family"],
                "fit": d["fit"],
                "composition": d["composition"],
                "color": d["color"],
            })

        products_collection.data.insert_many(products_objs)

    finally:
        client.close()

def read():
    # Connect with default parameters
    client = weaviate.connect_to_local()

    # Check if the connection was successful
    try:
        client.is_ready()
        print("Successfully connected to Weaviate.")

        products = client.collections.get("Products")

        response = products.query.near_text(
            query="women's jeans with cotton pocket black",
            return_metadata=wvc.query.MetadataQuery(distance=True),
            limit=2,
            return_properties=["name", "family", "color", "fit"]
        )

        for o in response.objects:
            print(o.properties)
            print(o.metadata.distance)
    finally:
        client.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read()