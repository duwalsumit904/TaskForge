import sys
import uuid

print("Python version:", sys.version)
print("UUID module:", uuid.__file__)
print("UUIDv7 available:", hasattr(uuid, "uuid7"))

if hasattr(uuid, "uuid7"):
    print("Generated UUIDv7:", uuid.uuid7())
else:
    print("UUIDv7 is missing from this Python installation.")
