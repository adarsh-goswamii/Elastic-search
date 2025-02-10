from pprint import pprint
from elasticsearch import Elasticsearch

# Init elastic search
es = Elasticsearch("http://localhost:9200/")
info = es.info()

book_index = "books"

# deleting an index
es.indices.delete(index=book_index, ignore_unavailable=True)

# Creating an index
es.indices.create(index=book_index, settings={
    "index": {
        "number_of_shards": 2,
        "number_of_replicas": 2
    }
})

document = {
    "title": "Hello world!",
    "author": "Adarsh",
    "created_on": "2025-01-01",
    "rating": 4.5
}

# Adding document to an index
es.index(index=book_index, body=document)

# default mapping
mapping = es.indices.get_mapping(index=book_index)
pprint(mapping)

# Adding manual mapping - must be done before adding any document to the index
manual_mapping = {
    "properties": {
        "created_on": {"type": "date"},
        "title": {"type": "text"}
    }
}
# way 1 to add manual mapping
es.indices.create(index="books_2", mappings=manual_mapping)
# way 2 to add manual mapping
es.indices.create(index="books_3")
es.indices.put_mapping(index="book_3", body=manual_mapping)

# Object field
es.indices.create(index="object_index", mappings={
    "properties": {
        "author": {
            "properties": {
                "first_name": {"type": "text"},
                "last_name": {"type": "text"},
            }
        }
    }
})

# Object field - flattened type
es.indices.create(index="nested_object_index", mappings={
    "properties": {
        "author": {
            "type": "flattened"
        }
    }
})

# Object field - nested type
es.indices.create(index="nested_object_index", mappings={
    "properties": {
        "author": {
            "type": "nested"
        }
    }
})
