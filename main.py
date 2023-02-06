import pygame
import sys
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

from settings import *
from sprites_for_myGame import BackGround, Ground, Plane, Obstacle


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(531, 328)
        MainWindow.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 70, 461, 61))
        self.label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 180, 211, 91))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Стартовое окно"))
        self.label.setText(_translate("MainWindow", "Для начала игры нажмите конпку старт"))
        self.pushButton.setText(_translate("MainWindow", "старт"))


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run_game)

    def run_game(self):
        self.close()
        game = Game()
        game.run()


class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Game')
        self.clock = pygame.time.Clock()
        self.active_player = True

        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        bg_height = pygame.image.load('graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        BackGround(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)

        self.timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer, 1400)

        self.score_text = pygame.font.SysFont('arrial', 80)
        self.score = 0
        self.start = 0

        self.ok = pygame.image.load('graphics/ui/menu.png').convert_alpha()
        self.ok_rect = self.ok.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) \
                or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active_player = False
            self.plane.kill()

    def display_score(self):
        if self.active_player:
            self.score = (pygame.time.get_ticks() - self.start) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.ok_rect.height / 1.5)

        score_surf = self.score_text.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        self.screen.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:

            delta = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active_player:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.active_player = True
                        self.start = pygame.time.get_ticks()

                if event.type == self.timer and self.active_player:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

            self.screen.fill('black')
            self.all_sprites.update(delta)
            self.all_sprites.draw(self.screen)
            self.display_score()

            if self.active_player:
                self.collisions()
            else:
                self.screen.blit(self.ok, self.ok_rect)

            pygame.display.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
