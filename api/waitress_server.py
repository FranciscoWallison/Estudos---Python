from waitress import serve
import __init__
print("localhost:8080")
serve(__init__.create_app(), listen='0.0.0.0:8080', url_scheme='https')
