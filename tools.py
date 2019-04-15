def get_hash(filepath):
    import hashlib

    buf_size = 65536

    sha1 = hashlib.sha1()

    with open(filepath, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break

            sha1.update(data)

    return sha1.hexdigest().upper()
