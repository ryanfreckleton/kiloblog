import os

def should_be_less_than_1024_bytes():
    size = os.path.getsize('kiloblog.py')
    assert 1024 >= size
