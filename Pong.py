from superwires import games, color

import random

games.init(screen_width=640, screen_height=480, fps=60)


class Pizza(games.Sprite):
    pizza = games.load_image("pizza.bmp")
    speed = 4

    def __init__(self):
        super(Pizza, self).__init__(image=Pizza.pizza,
                                    x=random.randrange(0, games.screen.width),
                                    y=random.randrange(0, games.screen.height / 5),
                                    dy=Pizza.speed,
                                    dx=Pizza.speed)

    def update(self):
        if self.right > games.screen.width or self.left < 0:
            self.dx = -self.dx
        if self.top < 0:
            self.dy = -self.dy
        if self.bottom > games.screen.height:
            self.end_game()

    def handle_cought(self):
        self.dy = -self.dy

    def end_game(self):
        end_message = games.Message(value="Koniec gry",
                                    size=90,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    lifetime=5 * games.screen.fps,
                                    after_death=games.screen.quit)
        games.screen.add(end_message)


class Pan(games.Sprite):
    image = games.load_image("patelnia.bmp")

    def __init__(self):
        super(Pan, self).__init__(image=Pan.image,
                                  x=games.mouse.x,
                                  y=games.screen.height)

    """patelnia """

    def update(self):
        self.x = games.mouse.x

        if self.left < 0:
            self.left = 0

        if self.right > games.screen.width:
            self.right = games.screen.width

        self.check_catch()

    def check_catch(self):
        """sprawdz czy nie doszlo do kolizji z pizza"""
        for pizza in self.overlapping_sprites:
            pizza.handle_cought()


def main():
    the_pan = Pan()
    games.screen.add(the_pan)

    the_pizza = Pizza()
    games.screen.add(the_pizza)

    games.mouse.is_visible = False
    games.screen.event_grab = True
    games.screen.mainloop()


main()
