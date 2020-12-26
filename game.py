import sys
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_status import Game_status

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        #window mode
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #FullScreen
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien invasion')
        self.bg_color = self.settings.bg_color

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.stats = Game_status(self)


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_down_events(event)
            elif event.type == pygame.KEYUP:
                self._check_up_events(event)

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitem()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()


    def _check_down_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_rigth = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()



    def _check_up_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_rigth = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_q:
            sys.exit()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()


    def _create_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2* alien_width)

        ship_height = self.ship.rect.height
        avaolable_space_y = self.settings.screen_height  - 3*alien_height - ship_height
        number_rows = avaolable_space_y // (2 * alien_height)

        for row in range(number_rows):
            for i in range(number_aliens_x):
                self._create_alien(i,row)





    def _create_alien(self,number,rows):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 *alien.rect.height*rows
        self.aliens.add(alien)

    def _update_alien(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            print("ship hit!!!!")
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_dicrection()
                break
    def _change_fleet_dicrection(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
           self.stats.game_active = False

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def run_game(self):
        while True:
            if self.stats.game_active:
                self._check_events()
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_alien()
            self._update_screen()




if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()