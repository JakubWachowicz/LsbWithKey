from PIL import Image




#Funkcja konwertująca string na 8 bitowy ciąg
def convert_to_binary(string):
    binary = ''.join(format(ord(char), '08b') for char in string)
    return binary


#Funkcja kodująca ciąg znaków w obrazie formatu PNG
def encodeLsbWithSecretkey(path, message, secretKey,path_to_save):

    #zainicjalizowanie ograzu
    image = Image.open(path)

    #podział obrazu na kanały
    red_channel, green_channel, blue_channel = image.split()

    #umieszczenie wartości kanałów do odowiednich list
    red_pixels = list(red_channel.getdata())
    green_pixels = list(green_channel.getdata())
    blue_pixels = list(blue_channel.getdata())


    #Oblicznie maksymalnej ilosci znaków jakie mogą zmieścić sie w obrazie
    if(len(message)> len(red_pixels)/8):
        print("Podana wiadomość jest za długa")
        return False


    #Przekonwertowanie klucza i wiadomości na 8bitowy ciąg
    binKey = convert_to_binary(secretKey)
    binMessage = convert_to_binary(message)

    keyLen = len(binKey)
    currentIndex = 0

    #Zakodowanie wiadomości w obrazie

    for i in range(len(red_pixels)):

        #Wykonanie operacji XOR na ostatnim bitcie wartości z czerwonego kanału i bitcie na pozycji [i % keyLen] z klucza
        temp = ord(binKey[i % keyLen]) ^ ord(convert_to_binary(str(red_pixels[i]))[-1])


        #Jeżeli temp = 1 to zmodyfikuj ostatni bit wartości z zielonego kanału
        if temp == 1:

            green_pixels[i] = green_pixels[i] & 0xFE | int(binMessage[currentIndex])
            currentIndex += 1
        #W przeciwnym wypadku zmodyfikuj ostatni bit wartości z niebieskiego kanału
        else:

            blue_pixels[i] = blue_pixels[i] & 0xFE | int(binMessage[currentIndex])
            currentIndex += 1
        #Jeżeli index jest równy długości zakodowanej binarnie wiadomości to przerwij
        if currentIndex == len(binMessage):
            break

    print(red_pixels)

    #Utworzenie i zapisanie nowo powstałego obrazu
    encoded_image = Image.new('RGB', image.size)
    encoded_image.putdata(list(zip(red_pixels, green_pixels, blue_pixels)))

    encoded_image.save(path_to_save)
    return True





#Funkcja do dekodowanie wiadomości z obrazu

def decodeLsbWithSecretkey(path, secretKey):
    # zainicjalizowanie ograzu
    image = Image.open(path)
    # podział obrazu na kanały
    red_channel, green_channel, blue_channel = image.split()


    # umieszczenie wartości kanałów do odowiednich list
    red_pixels = list(red_channel.getdata())
    green_pixels = list(green_channel.getdata())
    blue_pixels = list(blue_channel.getdata())

    #Przekonwertowanie klucza na 8bitowy ciąg
    binKey = convert_to_binary(secretKey)
    keyLen = len(binKey)
    currentIndex = 0
    secret_msg = ''
    decoded_message = ""

    #Odkodowanie wiadomości
    for i in range(len(green_pixels)):
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
            decoded_char = chr(int(decoded_message, 2))
            # Znacznik końca wiadomości
            if decoded_char == '\x00':
                break
            # W przeciwnym wypadku zmodyfikuj ostatni bit wartości z niebieskiego kanału
            else:
                secret_msg+= decoded_char
                print(decoded_char, end="")
            decoded_message = ""
    #Zwrócenie odczytanej wiadomości


    return secret_msg