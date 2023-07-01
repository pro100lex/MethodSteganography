from stegano import lsb
from stegano import exifHeader
from steganocryptopy.steganography import Steganography
import os


def encrypt_to_png(path_img, message_text):
    """Функция шифрования сообщения в файл png"""
    normalized_path = path_img.replace('"', '').replace('\\', '/')
    img_with_secret = lsb.hide(normalized_path, message_text)

    if not os.path.exists('images'):
        os.mkdir('images')

    saved_path = f'images/{normalized_path[normalized_path.rfind("/") + 1:normalized_path.rfind(".")]}_with_secret.png'
    img_with_secret.save(saved_path)

    return f'Сообщение зашифровано в файл: {saved_path}'


def decrypt_from_png(path_img):
    """Функция дешифрования сообщения из файла png"""
    normalized_path = path_img.replace('"', '').replace('\\', '/')
    img_decrypt_message = lsb.reveal(normalized_path)

    return f'Результат дешифровки: {img_decrypt_message}'


def encrypt_to_jpg(path_img, message_text):
    """Функция шифрования сообщения в файл jpg"""
    normalized_path = path_img.replace('"', '').replace('\\', '/')

    if not os.path.exists('images'):
        os.mkdir('images')

    saved_path = f'images/{normalized_path[normalized_path.rfind("/") + 1:normalized_path.rfind(".")]}_with_secret.jpg'

    img_with_secret = exifHeader.hide(path_img, saved_path, message_text)

    return f'Сообщение зашифровано в файл: {saved_path}'


def decrypt_from_jpg(path_img):
    """Функция дешифрования сообщения из файла jpg"""
    normalized_path = path_img.replace('"', '').replace('\\', '/')
    img_decrypt_message = exifHeader.reveal(normalized_path).decode()

    return f'Результат дешифровки: {img_decrypt_message}'


def encrypt_with_key_png(path_img, path_message):
    """Функция шифрования сообщения в файл png при помощи ключа"""
    normalized_path_img = path_img.replace('"', '').replace('\\', '/')
    normalized_path_message = path_message.replace('"', '').replace('\\', '/')

    if not os.path.exists('images'):
        os.mkdir('images')

    if not os.path.exists('secret_keys'):
        os.mkdir('secret_keys')

    saved_path_img = f'images/{normalized_path_img[normalized_path_img.rfind("/") + 1:normalized_path_img.rfind(".")]}_with_secret.png'
    saved_path_key = f'secret_keys/{normalized_path_img[normalized_path_img.rfind("/") + 1:normalized_path_img.rfind(".")]}_key.key'

    Steganography.generate_key(saved_path_key)
    img_with_secret = Steganography.encrypt(f'secret_keys/{normalized_path_img[normalized_path_img.rfind("/") + 1:normalized_path_img.rfind(".")]}_key.key', normalized_path_img, normalized_path_message)
    img_with_secret.save(saved_path_img)

    return f'Сообщение зашифровано в файл: {saved_path_img}\n' \
           f'Ключ в файле: {saved_path_key}'


def decrypt_with_key_png(path_img, path_key):
    """Функция дешифрования сообщения из файла png при помощи ключа"""
    normalized_path_img = path_img.replace('"', '').replace('\\', '/')
    normalized_path_key = path_key.replace('"', '').replace('\\', '/')

    img_decrypt_message = Steganography.decrypt(normalized_path_key, normalized_path_img)

    return f'Результат дешифровки: {img_decrypt_message}'


def main():
    variants_operations = {1: 'Написать текст и зашифровать (png)', 2: 'Расшифровать текст (png)', 3: 'Написать текст и зашифровать (jpg)', 4: 'Расшифровать текст (jpg)', 5: 'Зашифровать текст через дополнительную защиту - ключ (png)', 6: 'Расшифровать текст с ключом (png)'}

    for key, value in variants_operations.items():
        print(f'{key} => {value}')

    preferred_action = int(input('Выберите предпочитаемое действие: '))

    if preferred_action == 1:
        path_img = input('Путь до изображения в которое нужно спрятать сообщение: ')
        message_text = input('Текст который нужно зашифровать: ')
        print(encrypt_to_png(path_img=path_img, message_text=message_text))

    elif preferred_action == 2:
        path_img = input('Путь до изображения которое нужно дешифровать: ')
        print(decrypt_from_png(path_img=path_img))

    elif preferred_action == 3:
        path_img = input('Путь до изображения в которое нужно спрятать сообщение: ')
        message_text = input('Текст который нужно зашифровать: ')
        print(encrypt_to_jpg(path_img=path_img, message_text=message_text))

    elif preferred_action == 4:
        path_img = input('Путь до изображения которое нужно дешифровать: ')
        print(decrypt_from_jpg(path_img=path_img))

    elif preferred_action == 5:
        path_img = input('Путь до изображения в которое нужно спрятать сообщение: ')
        path_message = input('Путь до текста который нужно зашифровать: ')
        print(encrypt_with_key_png(path_img=path_img, path_message=path_message))

    elif preferred_action == 6:
        path_img = input('Путь до изображения которое нужно дешифровать: ')
        path_key = input('Путь до ключа дешифровки: ')
        print(decrypt_with_key_png(path_img=path_img, path_key=path_key))


if __name__ == '__main__':
    main()