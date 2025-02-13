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
book_response = es.index(index=book_index, body=document)

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

# Text search type - text
es.indices.create("text_index", mappings={
    "properties": {
        "email_body": {"type": "text"}
    }
})

email = "this is an email body"
es.index(index="text_index", body={"email_body": email})

# Text search type - completion
es.indices.create("completion_index", mappings={
    "properties": {
        "city": {"type": "completion"}
    }
})
city_options = ["Lucknow", "Agra", "Kanpur"]
es.index(index="completion_index", body={"city": { "input": city_options }})

# delete document
es.delete(index=book_index, id='1') # Note if id is not present in the index it will throw error.

# Get document
es.get(index=book_index, id='1')

# Count document
es.count(index=book_index, query="user:adarsh")

# Exists - index
es.indices.exists(index=book_index)

# Exists - document
es.exists(index=book_index, id='1')

# Update document - existing field
response = es.update(index=book_index, id=book_response.get('_id', ""),
          script={"source": "ctx._source.title = params.title", "params": {"title": "Updated Book Title"}})

# Update document - updating a document using doc (patch operation)
response = es.update(index=book_index, id=book_response.get('_id', ""),
          doc={ "title": "Learn elasticsearch" })

# Update document - adding a new field
response = es.update(index=book_index, id=book_response.get('_id', ""),
          script={"source": "ctx._source.description = params.desc", "params": {"desc": "Book description"}})

# Update document - removing a field
response = es.update(index=book_index, id=book_response.get('_id', ""),
          script={"source": "ctx._source.remove('description')"})

# Update document - add document if no such id is found
response = es.update(index=book_index, id="wrong_id",
          doc={ "title": "Learn elasticsearch" }, doc_as_upsert=True)

print(es.get(index=book_index, id=response.get('_id')))
