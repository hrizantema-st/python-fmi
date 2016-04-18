def transpose(matrix):
    return [list(i) for i in zip(*matrix)]


def grayscale_pixel(pixel):
    tmp = int(0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2])
    return (tmp, tmp, tmp)


def grayscale_image(image):
    return [[grayscale_pixel(pixel) for pixel in row] for row in image]


def grayscale(function):
    def decorator(*args, **kwargs):
        current_image = function(*args, **kwargs)
        return grayscale_image(current_image)
    return decorator


@grayscale
def rotate_left(image):
    transposed_image = transpose(image)
    return transposed_image[::-1]


@grayscale
def rotate_right(image):
    reversed_image = image[::-1]
    return transpose(reversed_image)


def invert_pixel(pixel):
    return (255 - pixel[0], 255 - pixel[1], 255 - pixel[2])


def invert_row(row):
    return list(map(invert_pixel, row))


@grayscale
def invert(image):
    return list(map(invert_row, image))


def lighten_pixel(pixel, number):
    red = pixel[0] + number * (255 - pixel[0])
    green = pixel[1] + number * (255 - pixel[1])
    blue = pixel[2] + number * (255 - pixel[2])
    return (int(red), int(green), int(blue))


@grayscale
def lighten(image, number):
    new_image = []
    for row in image:
        current_row = list(map(lambda x: lighten_pixel(x, number), row))
        new_image.append(current_row)
    return new_image
    #return [list(map(lambda x: lighten_pxl(x, number), row)) for row in image]


def darken_pixel(pixel, number):
    red = pixel[0] - number * pixel[0]
    green = pixel[1] - number * pixel[1]
    blue = pixel[2] - number * pixel[2]
    return (int(red), int(green), int(blue))


@grayscale
def darken(image, number):
    new_image = []
    for row in image:
        current_row = list(map(lambda x: darken_pixel(x, number), row))
        new_image.append(current_row)
    return new_image
