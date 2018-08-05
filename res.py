import pygame


def load(image):
    img = pygame.image.load(image)
    dim = img.get_size()
    dim = (dim[0]*2, dim[1]*2)
    img = pygame.transform.scale(img, dim)
    return img


walk1 = load("pig/walk1.png")
walk2 = load("pig/walk2.png")
walk3 = load("pig/walk3.png")
spike = load("spike.png")
walk = walk1, walk2, walk3

