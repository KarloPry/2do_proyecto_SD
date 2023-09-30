class Encryption:
    def __init__(self, path):
        self.file_path = path

    def encrypt_image(self, key):
        with open(f"{self.file_path}", mode="rb") as image:
            image_content = image.read()
            image_content = bytearray(image_content)
            for index, value in enumerate(image_content):
                image_content[index] = value ^ key
        with open(f"{self.file_path}_encrypted.png", mode="wb") as encrypted_image:
            encrypted_image.write(image_content)
        print("Encryption done")
        return f"{self.file_path}_encrypted.png"
