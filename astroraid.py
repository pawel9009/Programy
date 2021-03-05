from superwires import games,color
import random,math
games.init(screen_width=640, screen_height=480 , fps = 60)

class Wrapper(games.Sprite):
    def update(self):
        if self.top > games.screen.height:
            self.bottom=0
        if self.bottom <0:
            self.top=games.screen.height
        if self.left>games.screen.width:
            self.right=0
        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        self.destroy()

class Colider(Wrapper):
    def update(self):
        super(Colider, self).update()
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        new_explosion = Explosion(self.x,self.y)
        games.screen.add(new_explosion)
        self.destroy()

class Asteroid(Wrapper):
    """ astreoida na ekranie"""
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    SPAWN = 2
    POINTS = 30
    total = 0

    images = {SMALL:games.load_image("reszta/asteroida_mala.bmp"),
              MEDIUM: games.load_image("reszta/asteroida_sred.bmp"),
              LARGE: games.load_image("reszta/asteroida_duza.bmp")}

    SPEED = 2

    def __init__(self,game,x,y,size):
        super(Asteroid, self).__init__(
            image= Asteroid.images[size],
            x=x,
            y=y,
            dx=random.choice([-1,1])* Asteroid.SPEED*random.random()/size,
            dy=random.choice([-1, 1]) * Asteroid.SPEED * random.random() / size)
        self.game = game
        Asteroid.total+=1
        self.size =size


    def die(self):
        Asteroid.total-=1
        self.game.score.value +=int(Asteroid.POINTS/self.size)
        self.game.score.right = games.screen.width-10
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(game = self.game,
                                        x=self.x,
                                        y = self.y,
                                        size= self.size-1)
                games.screen.add(new_asteroid)
        if Asteroid.total == 0:
            self.game.advance()
        super(Asteroid, self).die()


class Ship(Colider):
    the_ship  = games.load_image("reszta/statek.bmp")
    ROTATION_STEP = 3
    VELOCITY_STEP = 0.3
    sound = games.load_sound("reszta/przyspieszenie.wav")
    MISSILE_DELAY = 25
    VELOCITY_MAX =3

    def __init__(self,game,x,y):
        super(Ship, self).__init__(
            image=Ship.the_ship,
            x = x,
            y=y)
        self.missile_wait =0
        self.game = game

    def update(self):
        super(Ship, self).update()

        if self.missile_wait>0:
            self.missile_wait-=1

        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle-=self.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle+=self.ROTATION_STEP

        if games.keyboard.is_pressed(games.K_UP):
            Ship.sound.play()
            angle = self.angle*math.pi / 180 #radiany
            self.dx +=Ship.VELOCITY_STEP*math.sin(angle)
            self.dy +=Ship.VELOCITY_STEP*-math.cos(angle)

            self.dx = min(max(self.dx, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
            self.dy = min(max(self.dy, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)


        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait==0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY

    def die(self):
        self.game.end()
        super(Ship, self).die()

class Game(object):

    def __init__(self):
        self.lvl = 0

        self.sound = games.load_sound("reszta/poziom.wav")

        self.score = games.Text(value=0,
                                size=50,
                                color = color.red,
                                top=games.screen.height-460,
                                right=games.screen.width-10,
                                is_collideable=False)
        games.screen.add(self.score)

        self.ship = Ship(game =self,
                         x = games.screen.width/2,
                         y = games.screen.height/2)
        games.screen.add(self.ship)

    def play(self):
        games.music.load("reszta/temat.mid")
        games.music.play(-1)

        nebula = games.load_image("reszta/mglawica.jpg")
        games.screen.background = nebula
        self.advance()

        games.screen.mainloop()

    def advance(self):

        self.lvl+=1
        BUFFER = 150
        for i in range(self.lvl):
            x_min = random.randrange(BUFFER)
            y_min = BUFFER-x_min

            x_distance = random.randrange(x_min,games.screen.width-x_min)
            y_distance = random.randrange(y_min,games.screen.height-y_min)

            x = self.ship.x + x_distance
            y = self.ship.y + y_distance

            x %=games.screen.width
            y %=games.screen.height

            new_asteroid = Asteroid(game = self,
                                    x = x,
                                    y = y,
                                    size=Asteroid.LARGE)
            games.screen.add(new_asteroid)

        lvl_message = games.Message(value="Poziom "+ str(self.lvl),
                                    size=40,
                                    color= color.yellow,
                                    x = games.screen.width/2,
                                    y = games.screen.height/10,
                                    lifetime=3* games.screen.fps,
                                    is_collideable=False)
        games.screen.add(lvl_message)

        if self.lvl>1:
            self.sound.play()

    def end(self):
        end_message = games.Message(value="Koniec gry",
                                    size=90,
                                    color=color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime=5*games.screen.fps,
                                    after_death= games.screen.quit,
                                    is_collideable=False)
        games.screen.add(end_message)

class Explosion(games.Animation):
    sound = games.load_sound("reszta/eksplozja.wav")
    images = ["reszta/eksplozja1.bmp",
              "reszta/eksplozja2.bmp",
              "reszta/eksplozja3.bmp",
              "reszta/eksplozja4.bmp",
              "reszta/eksplozja5.bmp",
              "reszta/eksplozja6.bmp",
              "reszta/eksplozja7.bmp",
              "reszta/eksplozja8.bmp",
              "reszta/eksplozja9.bmp"]
    def __init__(self,x,y):
        super(Explosion, self).__init__(images=Explosion.images,
                                        x=x,
                                        y=y,
                                        repeat_interval= 4,
                                        n_repeats=1,
                                        is_collideable=False)
        Explosion.sound.play()

class Missile(Colider):
    image = games.load_image("reszta/pocisk.bmp")
    sound = games.load_sound("reszta/pocisk.wav")
    BUFFER = 40
    VELOCITY = 7
    LIFETIME = 40

    def __init__(self,x,y, angle):
        Missile.sound.play()
        angle = angle *math.pi/180
        buffer_x =Missile.BUFFER * math.sin(angle)
        buffer_y =Missile.BUFFER * -math.cos(angle)
        x= x+buffer_x
        y= y + buffer_y

        dx = Missile.VELOCITY * math.sin(angle)
        dy = Missile.VELOCITY * -math.cos(angle)
        super(Missile, self).__init__(image=Missile.image,
                                      x = x,
                                      y=y,
                                      dx=dx, dy=dy)
        self.lifetime = Missile.LIFETIME

    def update(self):
        super(Missile, self).update()
        self.lifetime-=1
        if self.lifetime == 0:
            self.destroy()


def main():
    astrocrash = Game()
    astrocrash.play()

main()