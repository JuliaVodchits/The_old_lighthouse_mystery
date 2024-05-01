import pygame
import sys
from pygame.locals import *
import webbrowser

SCREEN_WIDTH = 1024  # размеры окна выбрал такими, потому что картинки 1024 х 512,
SCREEN_HEIGHT = 512  # можно обрезать картинки (или заново сгенерить) если нужен другой размер

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.menu_items = ["Начать новую игру", "Продолжить игру", "Сохранить игру", "Загрузить игру", "Настройки", "Выход"]
        self.selected_item = 0
        self.settings = None  # Инициализация настроек будет выполнена при первом входе
        self.active = False
        self.background = pygame.image.load("Start_menu/menu.jpg").convert() # Загрузка фоновой картинки
        pygame.mixer.music.load("Start_menu/sound.mp3") # Загрузка и воспроизведение фоновой музыки
        pygame.mixer.music.play(-1)  # Повторение вечно

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))  # Используем изображение в качестве фона
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 255) if i == self.selected_item else (150, 200, 250)
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 30))
            self.screen.blit(text, text_rect)

    def move_selection(self, direction):
        self.selected_item = (self.selected_item + direction) % len(self.menu_items)

    def toggle_menu(self):
        self.active = not self.active
        if self.active:
            self.selected_item = 0

    def run_menu(self):
        self.active = True
        # перед запуском меню нужно будет сохранить текущую игру, чтобы можно было вернуться к ней
        # функция save_game()  (pass  - пока не прописана)
        while self.active:
            self.draw_menu()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_selection(-1)
                    elif event.key == pygame.K_DOWN:
                        self.move_selection(1)
                    elif event.key == pygame.K_RETURN:
                        self.handle_menu_selection()

    def handle_menu_selection(self):
        if self.selected_item == 5:  # Выход
            pygame.quit()
            sys.exit()
        elif self.selected_item == 0:  # Новая игра
            loc01.run()  # перехода к игре, к локации loc01
        elif self.selected_item == 1:  # Продолжить игру
            self.save_game()  # Перед переходом в меню нужно сохранить игру, затем загрузить ее
        elif self.selected_item == 2:  # Сохранить игру
            self.load_game() # Перед переходом в меню нужно сохранить игру, затем загрузить ее
        elif self.selected_item == 3:  # Загрузить игру
            self.load_game()
        elif self.selected_item == 4:  # Настройки
            if self.settings is None:
                self.settings = Settings(self.screen, self.background)
            self.settings.handle_input()
        self.active = False

class Settings:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.font = pygame.font.Font(None, 36)
        self.settings_items = ["Громкость: ", "Яркость: ", "Назад"]
        self.selected_item = 0
        self.volume_level = 5  # Примерная громкость на шкале от 0 до 10
        self.brightness_level = 5  # Примерная яркость на шкале от 0 до 10
        self.active = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for i, item in enumerate(self.settings_items):
            setting_value = ""
            if i == 0:
                setting_value = str(self.volume_level)
            elif i == 1:
                setting_value = str(self.brightness_level)

            text = self.font.render(item + setting_value, True,
                                        (255, 255, 255) if i == self.selected_item else (150, 200, 250))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
            self.screen.blit(text, text_rect)

    def change_setting(self, direction):
        if self.selected_item == 0:  # Громкость
            self.volume_level = max(0, min(10, self.volume_level + direction))
            pygame.mixer.music.set_volume(self.volume_level / 10)
        elif self.selected_item == 1:  # Яркость
            self.brightness_level = max(0, min(10, self.brightness_level + direction))
            # Применение изменения яркости (если возможно)
            # Здесь могла бы быть функция для изменения яркости экрана, если бы это поддерживалось

    def handle_input(self):
        self.active = True
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % len(self.settings_items)
                    elif event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % len(self.settings_items)
                    elif event.key == pygame.K_LEFT:
                        self.change_setting(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.change_setting(1)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_item == 2:  # Назад
                            main()
                            self.active = False
            self.draw()
            pygame.display.flip()


    def save_game(self):
        # Код для сохранения данных игры в SQLite
        pass

    def load_game(self):
        # Код для загрузки данных игры из SQLite
        pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = Menu(screen)
    menu.run_menu()


class Location:    # класс локации, все атрибуты можно хранить и загружать из SQLite
    def __init__(self, background_image_path, music_path, options=None):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load(background_image_path)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Тайна старого маяка")
        self.music_path = music_path
        self.dialog = []
        self.next_locations = []
        self.options = options if options else []
        self.character_images = {}  # словарь для хранения изображений персонажей
        self.voice_clips = {}  # словарь для хранения звуковых файлов диалогов

    def load_character_image(self, character_name, image_path):
        image = pygame.image.load(image_path)
        self.character_images[character_name] = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_voice_clip(self, dialog_id, clip_path):
        self.voice_clips[dialog_id] = pygame.mixer.Sound(clip_path)

    def play_voice_clip(self, dialog_id):
        if dialog_id in self.voice_clips:
            # Приглушение фоновой музыки во время диалога
            pygame.mixer.music.set_volume(0.2)
            self.voice_clips[dialog_id].play()
            # Ожидание окончания воспроизведения звукового файла
            while pygame.mixer.get_busy():
                pygame.time.delay(100)

            # Восстановление громкости фоновой музыки
            pygame.mixer.music.set_volume(1.0)

    def run_dialog(self):  # функция диалогов
        index = 0
        last_index = -1  # переменная для отслеживания последнего воспроизведённого индекса
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()  # выход из игры
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        main()
                    elif event.key == K_SPACE:  # листаем фразы диалога клавишей Пробела
                        if index < len(self.dialog) - 1:
                            index += 1
                        else:
                            running = False  # выход из диалога
                    elif event.key == K_BACKSPACE:
                        pygame.quit()
                        sys.exit()
            self.screen.blit(self.background, (0, 0))
            speaker, text = self.dialog[index]
            if speaker in self.character_images:
                character_image = self.character_images[speaker]
                self.screen.blit(character_image, (0, 0))  # Позиция изображения персонажа
            self.draw_text(f"{speaker}: {text}", (100, 450))  # Рисуем текст поверх изображения персонажа
            pygame.display.update()

            if last_index != index:  # проверяем, изменился ли индекс
                last_index = index  # обновляем последний индекс
                self.play_voice_clip(index)  # воспроизведение звукового файла для текущей реплики по индексу

            self.clock.tick(60)


    def start_music(self):                            # запускает звуковой файл
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(-1,0.0)                   # бесконечное воспроизведение звука

    def draw_text(self, text, position, font_size=24, max_width=850):
        font = pygame.font.Font(None, font_size)  # Создаем шрифт заданного размера
        words = text.split(' ')  # Разбиваем текст на слова
        x, y = position
        space = font.size(' ')[0]  # Ширина пробела
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word, True, (250, 200, 250))
            word_width, word_height = word_surface.get_size()
            if max_width is not None and current_width + word_width >= max_width:
                # Если добавление слова превышает максимальную ширину, выводим текущую строку
                line_surface = font.render(' '.join(current_line), True, (250, 200, 250))
                self.screen.blit(line_surface, (x, y))
                y += word_height  # Перемещаемся на следующую строку
                current_line = [word]  # Начинаем новую строку с текущего слова
                current_width = word_width + space
            else:
                # Добавляем слово в текущую строку
                current_line.append(word)
                current_width += word_width + space

        # Вывод последней строки
        line_surface = font.render(' '.join(current_line), True, (250, 200, 250))
        self.screen.blit(line_surface, (x, y))

    def choose_action(self):  # выбор перехода к следующей локации
        opt = None            # opt - переменная сделанного выбора
        while opt is None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:    # вызов меню
                        main()
                    elif event.key == K_1 and len(self.options) >= 1:    # выбор из двух вариантов
                        opt = 0                                        # можно сделать больше при большом желании,
                    elif event.key == K_2 and len(self.options) >= 2:  # но я думаю нам двух достаточно
                        opt = 1
                    elif event.key == K_3 and len(self.options) >= 3:
                        opt = 2
                    if opt is not None:                                # когда выбор сделан, opt is not None, - остановка воспроизведения звука
                        pygame.mixer.music.stop()
                        if isinstance(self.next_locations[opt], str):  # Проверка на тип объекта - строка
                            webbrowser.open_new_tab(self.next_locations[opt])  # Открытие внешней ссылки
                            main()  # Возврат в меню после открытия ссылки
                        else:
                            self.next_locations[opt].run()  # Переход к следующей локации
                            return None
            self.screen.blit(self.background, (0, 0))
            for i, option in enumerate(self.options):
                self.draw_text(f"{i + 1}. {option}", (100, 400 + 25 * i), font_size=24) # вывод надписей для выбора следующей локации
            pygame.display.update()
            self.clock.tick(60)
        return opt

    def run(self):  # запуск всех методов локации
        self.start_music()
        self.run_dialog()
        opt = self.choose_action()
        if opt is not None and opt < len(self.next_locations):
            next_location = self.next_locations[opt]
            if next_location:
                next_location.run()
            next_action = next_location.choose_action()
            if next_action == "menu":
                return "menu"
        else:
            pygame.quit()



if __name__ == '__main__':
    loc01 = Location('Loc01_Prolog/loc01_Pab.jpg', 'Loc01_Prolog/plesk-voln.mp3',
                     ["Расспросить бармена местного паба", "Расспросить посетителей местного паба"])

    loc1_1 = Location('Loc1_dialogs/loc1_1.jpg', 'Loc1_dialogs/loc1_1.mp3', ["Изучить записку",
                    "Расспросить посетителей бара"]) # создание локаций: loc1 - первая локация, _1 - первая сцена
    loc1_2 = Location('Loc1_2_Zapiska/loc1_2.jpg', 'Loc1_2_Zapiska/loc1_2.mp3', ["Дом сторожа маяка",
                    "Расспросить посетителей бара"])                  # локация: loc1_2 - первая локация, вторая сцена
    loc1_3 = Location('Loc1_dialogs/loc1_3.jpg', 'Loc1_dialogs/loc1_3.mp3', ["Дом сторожа маяка",
                    "Изучить записку", "Расспросить бармена"])
    loc2_1 = Location('Loc2_dialogs/loc2_1.jpg', 'Loc2_dialogs/loc2_1.mp3', ["Встреча в прибрежном лесу",
                    "Разорванное письмо"]) # Соседка сторожа
    loc2_2 = Location('Loc2_2_Pismo/loc2_2.jpg', 'Loc2_2_Pismo/loc2_2.mp3', ["Встреча в прибрежном лесу",
                    "Вернуться в бар, изучить записку"]) # разорванное письмо
    loc3_1 = Location('loc3_dialogs/loc3_1.jpg', 'loc3_dialogs/loc3_1.mp3', ["Старый маяк",
                    "Искать странный компас"]) # Встреча со старым рыбаком в прибрежном лесу
    loc3_2 = Location('loc3_2_Kompas/loc3_2.jpg', 'loc3_2_Kompas/loc3_2.mp3', ["Старый маяк",
                    "Вернуться в дом сторожа, изучить разорванное письмо"])  # Странный компас
    loc4_1 = Location('loc4_1.jpg', 'loc4_1.mp3', ["Призрак старого хозяина маяка",
                    "Найти компас"])  # Старый маяк
    loc4_2 = Location('loc4_2.jpg', 'loc4_2.mp3', ["Тайна маяка",
                    "Уйти, не злить призрака"]) # Призрак старого маяка
    loc4_3 = Location('Loc4_3_Table/loc4_3.png', 'Loc4_3_Table/loc4_3.mp3', ["Домой"])
                    # Тайна маяка. Логотипы Зерокодера
    loc5_1 = Location('log5_1.jpg', 'loc5_1.mp3', ["Игра окончена"])
                    # Уплывает. Тайна раскрыта
    loc5_2 = Location('log5_1.jpg', 'loc5_1.mp3', ["Игра окончена"])
                    # Уплывает, но вернется, чтобы раскрыть Тайну

    loc01.next_locations = [loc1_1,loc1_3]
    loc1_1.next_locations = [loc1_2, loc1_3] # Выбор варианта следующей локации: либо loc1_2, либо loc1_3
    loc1_2.next_locations = [loc2_1, loc1_3]
    loc1_3.next_locations = [loc2_1, loc1_2, loc1_1]
    loc2_1.next_locations = [loc3_1, loc2_2]
    loc2_2.next_locations = [loc3_1, loc1_2]
    loc3_1.next_locations = [loc4_1, loc3_2]
    loc3_2.next_locations = [loc4_1, loc2_2]
    loc4_1.next_locations = [loc4_2, loc3_2]
    loc4_2.next_locations = [loc4_3, loc5_2]
    loc4_3.next_locations = [loc5_1]
    loc5_1.next_locations = ["https://university.zerocoder.ru/club-courses-new2"]
    loc5_2.next_locations = []

    loc01.dialog = [("Автор", " Молодой журналист Кирилл приезжает в небольшой прибрежный городок, "
                    "чтобы написать статью о старом маяке, окруженном мрачными легендами и тайнами. "
                    "По прибытии, Кирилл узнает о недавнем исчезновении местного сторожа маяка "
                    "и решает начать собственное расследование.")]

    loc1_1.dialog = [("Кирилл", "Здравствуйте, я Кирилл, новенький здесь."), # диалоги: loc1_1.dialog -
                     ("Бармен", "Приветствую, Кирилл! Что вам налить?"),     # диалог первой локации первой сцены
                     ("Кирилл",
                      "Кофе, пожалуйста! Я слышал, что вы можете рассказать много интересного о старом маяке."),
                     ("Бармен", "Да, маяк... Он уже много лет беспокоит умы местных."),
                     ("Кирилл", "Я весь во внимании, Расскажите."),
                     ("Бармен", " Странности начались, когда последний сторож исчез без вести."),
                     ("Бармен",
                      "А недавно кто-то видел странные огни там. Кстати, вы не первый, кто интересуется маяком."),
                     ("Бармен", "Недавно тут был детектив, оставил записку, но так и не вернулся."),
                     ("Кирилл", "Записка? Можно мне её посмотреть?"),
                     ("Бармен", "Конечно, держите. Надеюсь, она поможет вам больше, чем тому бедняге.")]
    loc1_2.dialog = [("Автор", "Ключ к правдивости легенды лежит в прошлом. Следи за знамениями в Прибрежном лесу."),
                     ("Кирил", "Что это значит? Хм..."),
                     ("Кирилл", "В любом случае,  ключ нужно искать в Прибрежном лесу."),
                     ("Кирилл", "Полученных данных маловато, поэтому нужно сперва поговорить с посетителями бара.")]
    loc1_3.dialog = [("Кирилл", "Приветствую вас, меня зовут Кирилл. А вас?"),
                     ("Посетитель бара", "Приветствую, Кирилл. Что вас интересует?"),
                     ("Кирилл", "Слышал вы можете помочь с подсказкой для разгадки тайн маяка."),
                     ("Посетитель бара", "Всё что я могу - это указать тебе направление, а дальше ты уже сам разберёшься."),
                     ("Посетитель бара", "Найди соседку сторожа, она точно знает то, что не знаем мы.")]
    loc2_1.dialog = [("Кирилл", "Бог в помощь, мадам! Я слышал, что вы можете рассказать много интересного про сторожа старого маяка"), # диалог  второй локации первой сцены
                     ("Соседка сторожа", "Конечно, голубчик. Что тебя интересует?"),
                     ("Кирилл", "Почему все вокруг боятся этого маяка и его сторожа?"),
                     ("Соседка сторожа", "Люди всегда боятся того, что не знают или не могут понять."),
                     ("Кирилл", "Как мне попасть внутрь дома?"),
                     ("Соседка сторожа", "Ключ под ковриком, только не сори там, и приберись за собой.")]
    loc2_2.dialog = [("Автор", "Десть шагов на север от старого чёрного дуба, затем пятнадцать шагов на восток. Внутри огромного пня ты найдёшь то, что поможет тебе раскрыть эту тайну маяка."),
                     ("Кирилл", "Ну вот - а я уже думал, что всё время придётся разгадывать загадки."), # здесь можно поместить мысли Кирилла или его монолог
                     ("Кирилл", "Возьму ка я топор, чтобы не страшно было.")]
    loc3_1.dialog = [("Кирилл", "Здравствуйте. Что вы знаете о маяке и его таинственном обитателе?"),
                     ("Рыбак", "Маяк - место страшное, но помогает он и тем, кто верит. Помни: многие видели Призрака, но мало кто смог разгадать его загадку."),
                     ("Кирилл", "Спасибо за совет. Можете ли вы дать какую-то подсказку, помогающую разгадать тайны местности?"),
                     ("Рыбак", "Запомни: ключ к разгадке таится в словах, которые не сказаны вслух, но слышны в сердце каждого.")]
    loc3_2.dialog = [("Кирилл", "Странный старик. Говорит фразами как магистр Йода из Звёздных войн"),
                     ("Кирилл", "Итак, что мы имеем?. Записка детектива, разорванное письмо и компас"), # здесь тоже можно поместить мысли Кирилла или его монолог
                     ("Кирилл", "А что это тут у нас на обратной стороне написано? Две тысячи двадцать четыре."),
                     ("Кирилл", "Это явно какой-то шифр... или код...")]
    loc4_1.dialog = [("Кирилл", "Вот и маяк. Надо осмотреть окрестности."),
                     ("Кирилл", "Это потайная дверь... и кодовый замок."),
                     ("Кирилл", "Быть может написанный код на компасе и есть тот самый шифр?"),
                     ("Кирилл", "Вводим код... заходим... Хорошо что топор не пригодился.")]
    loc4_2.dialog = [("Призрак", "Зачем ты пришел сюда, живой?"),
                     ("Кирилл", "Я ищу ответы на загадки этого места и на пропажу сторожа маяка."),
                     ("Призрак", "Ты смел, ирод. Но что же ты готов отдать в обмен на правду?"),
                     ("Кирилл", "Все, что у меня есть - знание и любопытство."),
                     ("Призрак", "Знание ценно, но тебе нужно разгадать последнюю загадку. Разгадаешь - будешь жить долго и счастливо! Не разгадаешь - не сносить тебе головы!")]
    loc4_3.dialog = [("Table", "Как то всё на первый взгляд гладко прошло... я думал что будет битва."),
                     ("Table_2", "Что это там лежит на столе?"), # здесь тоже можно поместить мысли Кирилла или его монолог
                     ("QR-code", "Какие-то карточки... а на обратной стороне что?"),
                     ("Final_Artefact", "Это же QR-код. Но куда он меня приведёт?"),
                     ("Courses", "Вот же истину твердили древние цивилизации: сокровище - это не золото и брильянты, а знания!")]
    loc5_1.dialog = [("Кирилл", "Я уплывал. Какая-то светлая грусть прокралась в мое сердце."), # мысли Кирилла
                     ("Кирилл", "Тайна старого маяка раскрыта, но поверит ли мне читатель?")]  # или его монолог
    loc5_2.dialog = [("Кирилл", "Я уплывал, мысли о маяке терзали мое сердце."),  # мысли Кирилла
                     ("Кирилл", "Я вернусь сюда, я обязательно вернусь и докопаюсь до истины.")]  # или его монолог

    loc01.load_voice_clip(0, 'Loc01_Prolog/Prolog.mp3')

    loc1_1.load_voice_clip(0, 'Loc1_dialogs/loc1_1_01.mp3')
    loc1_1.load_voice_clip(1, 'Loc1_dialogs/loc1_1_02b.mp3')
    loc1_1.load_voice_clip(2, 'Loc1_dialogs/loc1_1_03.mp3')
    loc1_1.load_voice_clip(3, 'Loc1_dialogs/loc1_1_04b.mp3')
    loc1_1.load_voice_clip(4, 'Loc1_dialogs/loc1_1_05.mp3')
    loc1_1.load_voice_clip(5, 'Loc1_dialogs/loc1_1_06b.mp3')
    loc1_1.load_voice_clip(6, 'Loc1_dialogs/loc1_1_07b.mp3')
    loc1_1.load_voice_clip(7, 'Loc1_dialogs/loc1_1_08b.mp3')
    loc1_1.load_voice_clip(8, 'Loc1_dialogs/loc1_1_09.mp3')
    loc1_1.load_voice_clip(9, 'Loc1_dialogs/loc1_1_10b.mp3')

    loc1_2.load_voice_clip(0, 'Loc1_2_Zapiska/Zapiska.mp3')
    loc1_2.load_voice_clip(1, 'Loc1_2_Zapiska/loc1_2_01_Kirill.mp3')
    loc1_2.load_voice_clip(2, 'Loc1_2_Zapiska/loc1_2_02_Kirill.mp3')
    loc1_2.load_voice_clip(3, 'Loc1_2_Zapiska/loc1_2_03_Kirill.mp3')

    loc1_3.load_voice_clip(0, 'Loc1_dialogs/loc1_3_01_Kirill.mp3')
    loc1_3.load_voice_clip(1, 'Loc1_dialogs/loc1_3_02_Posetitel.mp3')
    loc1_3.load_voice_clip(2, 'Loc1_dialogs/loc1_3_03_Kirill.mp3')
    loc1_3.load_voice_clip(3, 'Loc1_dialogs/loc1_3_04_Posetitel.mp3')
    loc1_3.load_voice_clip(4, 'Loc1_dialogs/loc1_3_05_Posetitel.mp3')

    loc2_1.load_voice_clip(0, 'Loc2_dialogs/loc2_1_01_Kirill.mp3')
    loc2_1.load_voice_clip(1, 'Loc2_dialogs/loc2_1_02_Sosedka.mp3')
    loc2_1.load_voice_clip(2, 'Loc2_dialogs/loc2_1_03_Kirill.mp3')
    loc2_1.load_voice_clip(3, 'Loc2_dialogs/loc2_1_04_Sosedka.mp3')
    loc2_1.load_voice_clip(4, 'Loc2_dialogs/loc2_1_05_Kirill.mp3')
    loc2_1.load_voice_clip(5, 'Loc2_dialogs/loc2_1_06_Sosedka.mp3')

    loc2_2.load_voice_clip(0, 'Loc2_2_Pismo/Pismo.mp3')
    loc2_2.load_voice_clip(1, 'Loc2_dialogs/loc2_2_01_Kirill.mp3')
    loc2_2.load_voice_clip(2, 'Loc2_dialogs/loc2_2_02_Kirill.mp3')

    loc3_1.load_voice_clip(0, 'Loc3_dialogs/loc3_1_01_Kirill.mp3')
    loc3_1.load_voice_clip(1, 'loc3_dialogs/loc3_1_02_Fisher.mp3')
    loc3_1.load_voice_clip(2, 'loc3_dialogs/loc3_1_03_Kirill.mp3')
    loc3_1.load_voice_clip(3, 'loc3_dialogs/loc3_1_04_Fisher.mp3')

    loc3_2.load_voice_clip(0, 'loc3_2_Kompas/loc3_2_01_Kirill.mp3')
    loc3_2.load_voice_clip(1, 'loc3_2_Kompas/loc3_2_02_Kirill.mp3')
    loc3_2.load_voice_clip(2, 'loc3_2_Kompas/loc3_2_03_Kirill.mp3')
    loc3_2.load_voice_clip(3, 'loc3_2_Kompas/loc3_2_04_Kirill.mp3')

    loc4_1.load_voice_clip(0, 'loc4_1_near_Pharos/loc4_1_01_Kirill.mp3')
    loc4_1.load_voice_clip(1, 'loc4_1_near_Pharos/loc4_1_02_Kirill.mp3')
    loc4_1.load_voice_clip(2, 'loc4_1_near_Pharos/loc4_1_03_Kirill.mp3')
    loc4_1.load_voice_clip(3, 'loc4_1_near_Pharos/loc4_1_04_Kirill.mp3')

    loc4_2.load_voice_clip(0, 'loc4_dialogs/loc4_2_01_Ghost.mp3')
    loc4_2.load_voice_clip(1, 'loc4_dialogs/loc4_2_02_Kirill.mp3')
    loc4_2.load_voice_clip(2, 'loc4_dialogs/loc4_2_03_Ghost.mp3')
    loc4_2.load_voice_clip(3, 'loc4_dialogs/loc4_2_04_Kirill.mp3')
    loc4_2.load_voice_clip(4, 'loc4_dialogs/loc4_2_05_Ghost.mp3')

    loc4_3.load_voice_clip(0, 'loc4_dialogs/loc4_3_01_Kirill.mp3')
    loc4_3.load_voice_clip(1, 'loc4_dialogs/loc4_3_02_Kirill.mp3')
    loc4_3.load_voice_clip(2, 'loc4_dialogs/loc4_3_03_Kirill.mp3')
    loc4_3.load_voice_clip(3, 'loc4_dialogs/loc4_3_04_Kirill.mp3')
    loc4_3.load_voice_clip(4, 'loc4_dialogs/loc4_3_05_Kirill.mp3')

    loc5_1.load_voice_clip(0, 'Loc5_Return_Home/loc5_1_01_Kirill.mp3')
    loc5_1.load_voice_clip(1, 'Loc5_Return_Home/loc5_1_02_Kirill.mp3')

    loc5_2.load_voice_clip(0, 'Loc5_Return_Home/loc5_2_01_Kirill.mp3')
    loc5_2.load_voice_clip(1, 'Loc5_Return_Home/loc5_2_02_Kirill.mp3')

    loc01.character_images['Автор'] = pygame.image.load('Loc01_Prolog/loc01_Pab.jpg')
    loc1_1.character_images['Кирилл'] = pygame.image.load('Loc1_dialogs/Kirill.jpeg')
    loc1_1.character_images['Бармен'] = pygame.image.load('Loc1_dialogs/Barmen.jpeg')
    loc1_3.character_images['Кирилл'] = pygame.image.load('Loc1_dialogs/Kirill.jpeg')
    loc1_3.character_images['Посетитель бара'] = pygame.image.load('Loc1_dialogs/loc1_3.jpg')
    loc2_1.character_images['Кирилл'] = pygame.image.load('Loc1_dialogs/Kirill.jpeg')
    loc2_1.character_images['Соседка сторожа'] = pygame.image.load('Loc2_dialogs/loc2_1.jpg')
    loc3_1.character_images['Кирилл'] = pygame.image.load('Loc1_dialogs/Kirill.jpeg')
    loc3_1.character_images['Рыбак'] = pygame.image.load('loc3_dialogs/loc3_1.jpg')
    loc4_2.character_images['Призрак'] = pygame.image.load('loc4_2.jpg')
    loc4_2.character_images['Кирилл'] = pygame.image.load('Loc1_dialogs/Kirill.jpeg')
    loc4_3.character_images['Table'] = pygame.image.load('Loc4_3_Table/loc4_3.jpg')
    loc4_3.character_images['Table_2'] = pygame.image.load('Loc4_3_Table/loc4_3.png')
    loc4_3.character_images['QR-code'] = pygame.image.load('Loc4_3_Table/qr-code_512x512.png')
    loc4_3.character_images['Final_Artefact'] = pygame.image.load('Loc4_3_Table/Final_Artefact_1024x512.jpg')
    loc4_3.character_images['Courses'] = pygame.image.load('Loc4_3_Table/Courses_1024x512.jpg')



    main()

