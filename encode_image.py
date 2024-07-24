from PIL import Image
import os
import math

from encode_message import convert_to_binary


def combine_pixels(red_pixels, green_pixels, blue_pixels):
    combined_pixels = []

    for i in range(len(red_pixels)):
        red = red_pixels[i]
        green = green_pixels[i]
        blue = blue_pixels[i]

        combined_pixels.append(red)
        combined_pixels.append(green)
        combined_pixels.append(blue)

    return combined_pixels


def resize_image(image_path, max_bits):
    try:
        # Inicjalizacja obrazu
        image = Image.open(image_path)

        # Podzielenie obrazu na kanały
        red_channel_h, green_channel_h, blue_channel_h = image.split()
        red_pixels_h = list(red_channel_h.getdata())

        # Sprawdzenie ilosci bitów potrzemnych na zapis obrazu
        current_bits = len(red_pixels_h) * 8 * 3

        # Sprawdzenie czy obeaz mieści się w podanej licznie bitów
        if current_bits <= max_bits:
            # Obraz jest odpowiedniej wielkości
            return image

        # Oblicznie współczynnika zmniejszia
        reduction_factor = math.sqrt(max_bits / current_bits)

        # Zredukowanie wymiarów obrazu
        new_width = math.floor(image.size[0] * reduction_factor)
        new_height = math.floor(image.size[1] * reduction_factor)
        resized_image = image.resize((new_width, new_height))

        return resized_image
    except Exception as e:
        print("An error occurred while resizing the image:", str(e))
        return None


# Funkcja kodująca obraz w obrazie
def encodeLsbWithSecretkeyImage(path, path_to_hidden_image, secretKey, path_to_save):
    image = Image.open(path)

    # Podział obrazu na kanały
    red_channel, green_channel, blue_channel = image.split()

    red_pixels = list(red_channel.getdata())
    green_pixels = list(green_channel.getdata())
    blue_pixels = list(blue_channel.getdata())

    # zamiana klucza na 8bitowy ciąg
    binKey = convert_to_binary(secretKey)
    max_bits = (len(red_pixels)) - 88

    image_to_hide = Image.open(path_to_hidden_image)
    file_stats = os.stat(path_to_hidden_image)

    # Oblicznie czy obraz zmieści się w obrazie
    if (max_bits < file_stats.st_size * 8):

        # Zmiejszenie obrazu
        print("Zdjęcie do ukrycia jest za duże")

        resized_image = resize_image(path_to_hidden_image, max_bits)
        if resized_image is not None:
            image_to_hide = resized_image

    # Przypisanie nowych wymiarów obrazu
    image_to_hide_size = image_to_hide.size

    # Podziała obrazu do ukrycia na kanały
    red_channel_h, green_channel_h, blue_channel_h = image_to_hide.split()
    red_pixels_h = list(red_channel_h.getdata())
    green_pixels_h = list(green_channel_h.getdata())
    blue_pixels_h = list(blue_channel_h.getdata())

    pixel_list = combine_pixels(red_pixels_h, green_pixels_h, blue_pixels_h)
    index = 0

    # Zamienie liczby bitów na kanał i wielkości obrazka do ukrycia format numberOfBits@(width,height)@
    binMessage = convert_to_binary(str(len(red_pixels_h) * 8 * 3) + '@' + str(image_to_hide_size) + '@')

    keyLen = len(binKey)

    # Zakodowanie wiadomości w obrazie
    for i in range(len(binMessage)):
        temp = ord(binKey[i % keyLen]) ^ ord(convert_to_binary(str(red_pixels[index]))[-1])
        if temp == 1:
            green_pixels[index] = green_pixels[index] & 0xFE | int(binMessage[i])
            index += 1
        else:
            blue_pixels[index] = blue_pixels[index] & 0xFE | int(binMessage[i])
            index += 1

        if index == len(binMessage):
            break

    # Zakodowanie obrazu w obrazie
    # Kolejności kodowanie: wartości kanału R =>wartości kanału G => wartości kanału B

    for i in range(0, len(pixel_list)):

        bits = f'{pixel_list[i]:08b}'

        for i in range(0, 8):
            temp = ord(binKey[index % keyLen]) ^ ord(convert_to_binary(str(red_pixels[index]))[-1])
            if temp == 1:
                green_pixels[index] = green_pixels[index] & 0xFE | int(bits[i])
            else:
                blue_pixels[index] = blue_pixels[index] & 0xFE | int(bits[i])
            index += 1

    # Zapisanie nowo otrzymanego obrazu
    encoded_image = Image.new('RGB', image.size)
    encoded_image.putdata(list(zip(red_pixels, green_pixels, blue_pixels)))

    encoded_image.save(path_to_save)


# Funkcja do odczytu obrazu z obrazu
def decodeLsbWithSecretkeyImage(path, secretKey, path_to_save):
    # Incializacja obrazu
    image = Image.open(path)

    # Podzielenie obrazu na kanały
    red_channel, green_channel, blue_channel = image.split()

    red_pixels = list(red_channel.getdata())
    green_pixels = list(green_channel.getdata())
    blue_pixels = list(blue_channel.getdata())

    # Konwersja klucza na ciąg 8bitowy
    binKey = convert_to_binary(secretKey)
    keyLen = len(binKey)

    decoded_message = ""

    pix_index = 0
    # Tabice zawierająca wartości pixeli
    red = []
    green = []
    blue = []
    # Zmienna zawierająca informacje o statnie odczyty // 0 - odczyt ilości bitów, 1 odczyt wymiaru obrazu, 2 odczyt obrazu
    encodingStage = 0
    number_of_bits = ''
    image_size = ''

    # Odczytanie wiadomości i obrazu
    for i in range(0, len(green_pixels)):
        # Wykonanie operacji XOR na ostatnim bitcie wartości z czerwonego kanału i bitcie na pozycji [i % keyLen] z klucza
        temp = ord(binKey[i % keyLen]) ^ ord(convert_to_binary(str(red_pixels[i]))[-1])

        # Jeżeli temp = 1 toodczytaj ostatni bit wartości z zielonego kanału
        if temp == 1:
            decoded_message += str(green_pixels[i] & 0x01)
        # W przeciwnym wypadku to odczytaj ostatni bit wartości z niebieskiego kanału
        else:
            decoded_message += str(blue_pixels[i] & 0x01)

        # Odkodowanie 8bitowego ciągu
        if len(decoded_message) == 8:
            # Zamiana ciągu na znak ascii
            decoded_char = chr(int(decoded_message, 2))

            if (decoded_char == "@" and encodingStage <= 1):
                encodingStage += 1

            if (encodingStage == 0):
                # Odczytanie ilości_bitów
                number_of_bits += decoded_char

            elif (encodingStage == 1):
                # Odczytanie wielkości obrazu
                image_size += decoded_char

            # Odczytnie wartości pixeli obrazu
            else:
                # Zamiana ciągu na liczbe
                decoded_int = int(decoded_message, 2)
                if pix_index == 0:
                    red.append(decoded_int)
                    pix_index += 1
                elif (pix_index == 1):
                    green.append(decoded_int)
                    pix_index += 1
                elif (pix_index == 2):
                    blue.append(decoded_int)
                    pix_index = 0

            decoded_message = ''
            if encodingStage == 2:
                if i >= int(number_of_bits):
                    break

    # Zdekodowanie wielkości i szerokości obrazu
    a = image_size.split(',')[0]
    h = image_size.split(',')[1]
    w = a[2:]
    h = h[:-1]

    # Sklejenie wartości poszczególnych kanałów
    hidden_image = Image.new('RGB', (int(w), int(h)))
    hidden_image.putdata(list(zip(green, blue, red)))
    hidden_image.save(path_to_save)

    return True