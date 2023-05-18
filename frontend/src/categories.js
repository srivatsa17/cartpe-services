// To be removed after testing
const categories = [
  {
    "id": 1,
    "name": "Men",
    "slug": "men",
    "description": "Clothing related to men.",
    "level": 0,
    "parent": null,
    "children": [
        {
            "id": 2,
            "name": "Topwear",
            "slug": "topwear",
            "description": "Topwear related to men.",
            "level": 1,
            "parent": "Men",
            "children": [
                {
                    "id": 3,
                    "name": "T-shirts",
                    "slug": "t-shirts",
                    "description": "T-shirts related to men.",
                    "level": 2,
                    "parent": "Topwear",
                    "children": [],
                    "products": [],
                    "created_at": "2023-04-29T20:37:43.381375+05:30",
                    "updated_at": "2023-04-29T20:37:43.381427+05:30"
                }
            ],
            "products": [],
            "created_at": "2023-04-29T20:10:26.116594+05:30",
            "updated_at": "2023-04-29T22:11:57.331130+05:30"
        }
    ],
    "products": [],
    "created_at": "2023-04-29T20:07:35.829305+05:30",
    "updated_at": "2023-04-29T20:07:35.829343+05:30"
},
{
    "id": 16,
    "name": "Women",
    "slug": "women",
    "description": "Topwear related to women.",
    "level": 0,
    "parent": null,
    "children": [],
    "products": [],
    "created_at": "2023-04-30T15:24:07.057139+05:30",
    "updated_at": "2023-04-30T15:24:07.057162+05:30"
},
{
    "id": 18,
    "name": "Electronics",
    "slug": "electronics",
    "description": "Electronic items",
    "level": 0,
    "parent": null,
    "children": [
        {
            "id": 19,
            "name": "Cameras",
            "slug": "cameras",
            "description": "Camera items",
            "level": 1,
            "parent": "Electronics",
            "children": [
                {
                    "id": 20,
                    "name": "DSLR Cameras",
                    "slug": "dslr-cameras",
                    "description": "DSLR Camera items",
                    "level": 2,
                    "parent": "Cameras",
                    "children": [],
                    "products": [
                        {
                            "id": 1,
                            "sku": "4e3e918c-b7b6-47cd-b6b7-643909f3e2f7",
                            "name": "Cannon EOS 80D DSLR Camera",
                            "slug": "cannon-eos-80d-dslr-camera",
                            "description": "Characterized by versatile imaging specs, the Canon EOS 80D further clarifies itself using a pair of robust focusing systems and an intuitive design",
                            "price": 929.99,
                            "brand": "Cannon",
                            "stock_count": 5,
                            "discount": 10,
                            "discounted_price": 93.0,
                            "selling_price": 836.99,
                            "category": "DSLR Cameras",
                            "attributes": [
                                {
                                    "id": 3,
                                    "name": "color",
                                    "attribute_values": [
                                        {
                                            "id": 5,
                                            "value": "blue"
                                        },
                                        {
                                            "id": 6,
                                            "value": "green"
                                        }
                                    ]
                                },
                                {
                                    "id": 4,
                                    "name": "size",
                                    "attribute_values": [
                                        {
                                            "id": 7,
                                            "value": "18"
                                        }
                                    ]
                                }
                            ],
                            "product_images": [
                                {
                                    "id": 6,
                                    "image": "/cartpe-website-favicon-white.png",
                                    "is_featured": false,
                                    "product": 1,
                                    "created_at": "2023-05-02T13:09:05.706047+05:30",
                                    "updated_at": "2023-05-02T13:09:05.706083+05:30"
                                },
                                {
                                    "id": 1,
                                    "image": "/cartpe-high-resolution-color-logo.png",
                                    "is_featured": true,
                                    "product": 1,
                                    "created_at": "2023-05-01T22:46:59.630186+05:30",
                                    "updated_at": "2023-05-03T01:00:59.864985+05:30"
                                }
                            ],
                            "created_at": "2023-04-30T20:27:47.847482+05:30",
                            "updated_at": "2023-05-12T00:25:52.029714+05:30"
                        }
                    ],
                    "created_at": "2023-04-30T20:26:25.373341+05:30",
                    "updated_at": "2023-04-30T20:26:25.373365+05:30"
                }
            ],
            "products": [],
            "created_at": "2023-04-30T20:26:01.577467+05:30",
            "updated_at": "2023-04-30T20:26:01.577875+05:30"
        }
    ],
    "products": [],
    "created_at": "2023-04-30T20:25:23.690362+05:30",
    "updated_at": "2023-04-30T20:25:23.690435+05:30"
  }
]

export default categories;