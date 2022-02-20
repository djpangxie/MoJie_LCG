"""游戏的组牌器"""
from main import *


class Button_Area:
    """按钮区"""

    def __init__(self, set_card):
        main_game = set_card.main_game
        self.set_card = set_card
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = (
                             main_game.settings.screen_width - 4 * main_game.settings.screen_width / main_game.settings.area_width_spacing - self.height *
                             main_game.settings.original_card_size[0] / main_game.settings.original_card_size[
                                 1]) // 2
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (main_game.settings.screen_width // main_game.settings.area_width_spacing,
                             main_game.settings.screen_height // main_game.settings.area_height_spacing)
        self.button_group = (self._type_choice(), self._faction_choice())  # 初始化所有按钮

    def set_card_group(self):
        """根据当前按钮区设置来设置当前卡牌选择区提供的卡牌"""
        cards = []
        if self.button_group[0].card_name == "英雄":
            cards = self.set_card.hero_group.copy()
        elif self.button_group[0].card_name == "盟友":
            cards = self.set_card.ally_group.copy()
        elif self.button_group[0].card_name == "附属":
            cards = self.set_card.affiliated_group.copy()
        elif self.button_group[0].card_name == "事件":
            cards = self.set_card.action_group.copy()
        if self.button_group[1].card_name != "派系":
            for card in cards.copy():
                if hasattr(card, "resource_symbol") and card.resource_symbol != self.button_group[
                    1].card_name or hasattr(card, "faction_symbol") and card.faction_symbol != self.button_group[
                    1].card_name:
                    cards.remove(card)
        return cards

    def display_draw(self):
        cards_len = len(self.button_group)
        cards = self.button_group
        card_width = self.height * self.main_game.settings.original_card_size[0] // \
                     self.main_game.settings.original_card_size[1]
        hover_card_image = None  # 如果鼠标当前悬停在按钮上，记录其图像留到最后再画
        hover_card_rect = None  # 如果鼠标当前悬停在按钮上，记录其rect留到最后再画
        num = 0
        while cards_len and num <= cards_len:
            if num:
                hand_card_image_1 = hand_card_image_2
                hand_card_image_rect_1 = hand_card_image_rect_2
            if num != cards_len:
                hand_card_image_2 = cards[num].card_image
                hand_card_image_rect_2 = hand_card_image_2.get_rect(centery=self.rect.centery)
                hand_card_image_rect_2.centerx = (self.width - card_width) * (2 * num + 1) // (
                        cards_len * 2) + self.rect.x + card_width // 2
            if num:
                # 设置卡牌的可选区域
                if num != cards_len and hand_card_image_rect_2.x - hand_card_image_rect_1.x < card_width:
                    hand_card_image_rect_1.width = hand_card_image_rect_2.x - hand_card_image_rect_1.x
                # 如果鼠标单击或右击了这个按钮，则触发其选项
                if self.set_card.mouse_click and hand_card_image_rect_1.collidepoint(
                        self.set_card.mouse_click) or self.set_card.mouse_rightclick and hand_card_image_rect_1.collidepoint(
                    self.set_card.mouse_rightclick):
                    self.set_card.mouse_click = None
                    self.set_card.mouse_rightclick = None
                    buttons = []
                    from main import Print_Card
                    for number in range(len(cards[num - 1].card_target)):
                        card = Print_Card(self.main_game)
                        card.card_name = cards[num - 1].card_target[number]
                        card.card_image = pygame.Surface((self.height * self.main_game.settings.original_card_size[0] //
                                                          self.main_game.settings.original_card_size[1], self.height))
                        card.card_image.fill(self.main_game.settings.font_color_background)
                        card_rect = card.card_image.get_rect()
                        font = pygame.font.Font(
                            os.path.join(self.main_game.main_path, self.main_game.settings.font_file), card_rect.h // 3)
                        font_image = font.render(card.card_name, True, self.main_game.settings.font_color)
                        font_image_rect = font_image.get_rect(center=card_rect.center)
                        card.card_image.blit(font_image, font_image_rect)
                        buttons.append(card)
                    cards[num - 1].card_name = self.main_game.card_select(buttons).card_name
                    cards[num - 1].card_image.fill((128, 128, 128))
                    card_rect = cards[num - 1].card_image.get_rect()
                    font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                            card_rect.h // 3)
                    font_image = font.render(cards[num - 1].card_name, True, self.main_game.settings.font_color,
                                             self.main_game.settings.font_color_background)
                    font_image_rect = font_image.get_rect(center=card_rect.center)
                    cards[num - 1].card_image.blit(font_image, font_image_rect)
                    self.set_card.area_group[3].update_card_group()
                    return
                # 鼠标悬停可选区域上时让按钮最后再画，否则当下就画出来
                if hand_card_image_rect_1.collidepoint(self.set_card.mouse_pos) and hover_card_image is None:
                    hover_card_image = hand_card_image_1
                    hover_card_rect = hand_card_image_rect_1
                else:
                    self.main_game.screen.blit(hand_card_image_1, hand_card_image_rect_1)
                # END
            num += 1
        # 最后画鼠标悬停其上的按钮以使其处于所有按钮上方
        if hover_card_image:
            self.main_game.screen.fill(self.main_game.settings.font_color_background, hover_card_rect)
            self.main_game.screen.blit(hover_card_image, hover_card_rect)

    def _type_choice(self):
        """创建卡牌类型选择按钮"""
        from main import Print_Card
        card = Print_Card(self.main_game)
        card.card_name = "英雄"
        card.card_target = ("英雄", "盟友", "附属", "事件")
        card.card_image = pygame.Surface((self.height * self.main_game.settings.original_card_size[0] //
                                          self.main_game.settings.original_card_size[1], self.height))
        card.card_image.fill((128, 128, 128))
        card.card_image.set_colorkey((128, 128, 128))
        card_rect = card.card_image.get_rect()
        font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                card_rect.h // 3)
        font_image = font.render(card.card_name, True, self.main_game.settings.font_color,
                                 self.main_game.settings.font_color_background)
        font_image_rect = font_image.get_rect(center=card_rect.center)
        card.card_image.blit(font_image, font_image_rect)
        return card

    def _faction_choice(self):
        """创建派系选择按钮"""
        from main import Print_Card
        card = Print_Card(self.main_game)
        card.card_name = "派系"
        card.card_target = ["派系"]
        card.card_image = pygame.Surface((self.height * self.main_game.settings.original_card_size[0] //
                                          self.main_game.settings.original_card_size[1], self.height))
        card.card_image.fill((128, 128, 128))
        card.card_image.set_colorkey((128, 128, 128))
        card_rect = card.card_image.get_rect()
        font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                card_rect.h // 3)
        font_image = font.render(card.card_name, True, self.main_game.settings.font_color,
                                 self.main_game.settings.font_color_background)
        font_image_rect = font_image.get_rect(center=card_rect.center)
        card.card_image.blit(font_image, font_image_rect)
        return card


class Player_Hero:
    """玩家英雄卡牌区"""

    def __init__(self, set_card):
        main_game = set_card.main_game
        self.set_card = set_card
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = (
                             main_game.settings.screen_width - 4 * main_game.settings.screen_width / main_game.settings.area_width_spacing - self.height *
                             main_game.settings.original_card_size[0] / main_game.settings.original_card_size[
                                 1]) // 2
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topright = (round(
            main_game.settings.screen_width - self.height * main_game.settings.original_card_size[0] /
            main_game.settings.original_card_size[
                1] - 2 * main_game.settings.screen_width / main_game.settings.area_width_spacing),
                              main_game.settings.screen_height // main_game.settings.area_height_spacing)

    def display_draw(self):
        cards_len = len(self.set_card.player_hero)
        cards = self.set_card.player_hero.copy()
        card_width = self.height * self.main_game.settings.original_card_size[0] // \
                     self.main_game.settings.original_card_size[1]
        hover_card_image = None  # 如果鼠标当前悬停在卡牌上，记录其图像留到最后再画
        hover_card_rect = None  # 如果鼠标当前悬停在卡牌上，记录其rect留到最后再画
        num = 0
        while cards_len and num <= cards_len:
            if num:
                hand_card_image_1 = hand_card_image_2
                hand_card_image_rect_1 = hand_card_image_rect_2
            if num != cards_len:
                hand_card_image_2 = pygame.transform.scale(cards[num].card_image, (card_width, self.height))
                hand_card_image_rect_2 = hand_card_image_2.get_rect(centery=self.rect.centery)
                hand_card_image_rect_2.centerx = (self.width - card_width) * (2 * num + 1) // (
                        cards_len * 2) + self.rect.x + card_width // 2
            if num:
                # 设置卡牌的可选区域
                if num != cards_len and hand_card_image_rect_2.x - hand_card_image_rect_1.x < card_width:
                    hand_card_image_rect_1.width = hand_card_image_rect_2.x - hand_card_image_rect_1.x
                # 如果鼠标单击了这张卡牌，将其从英雄卡牌区去除
                if self.set_card.mouse_click and hand_card_image_rect_1.collidepoint(self.set_card.mouse_click):
                    self.set_card.player_hero.pop(num - 1)
                    self.set_card.mouse_click = None
                # 如果鼠标右击了这张卡牌，将此卡牌载入卡牌展示器展示
                if self.set_card.mouse_rightclick and hand_card_image_rect_1.collidepoint(
                        self.set_card.mouse_rightclick):
                    self.main_game.card_exhibition(cards[num - 1])
                    self.set_card.mouse_rightclick = None
                # 鼠标悬停可选区域上时让卡牌最后再画，否则当下就画出来
                if hand_card_image_rect_1.collidepoint(self.set_card.mouse_pos) and hover_card_image is None:
                    hover_card_image = hand_card_image_1
                    hover_card_rect = hand_card_image_rect_1
                else:
                    self.main_game.screen.blit(hand_card_image_1, hand_card_image_rect_1)
                # END
            num += 1
        # 最后画鼠标悬停其上的卡以使其处于所有卡牌上方
        if hover_card_image:
            self.main_game.screen.blit(hover_card_image, hover_card_rect)


class Player_Deck:
    """玩家牌组区"""

    def __init__(self, set_card):
        main_game = set_card.main_game
        self.set_card = set_card
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = round(
            self.height * main_game.settings.original_card_size[0] / main_game.settings.original_card_size[1])
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topright = (
            main_game.settings.screen_width - main_game.settings.screen_width // main_game.settings.area_width_spacing,
            main_game.settings.screen_height // main_game.settings.area_height_spacing)
        self.number_font = pygame.font.Font(os.path.join(main_game.main_path, self.main_game.settings.font_file),
                                            self.height // 3)

    def display_draw(self):
        self.main_game.screen.fill(self.main_game.settings.font_color_background, self.rect)
        number_image = self.number_font.render(str(len(self.set_card.player_deck)), True,
                                               self.main_game.settings.font_color, (128, 128, 128)).convert()
        number_image.set_colorkey((128, 128, 128))
        number_image_rect = number_image.get_rect(center=self.rect.center)
        self.main_game.screen.blit(number_image, number_image_rect)
        if self.set_card.player_deck and self.set_card.mouse_click and self.rect.collidepoint(
                self.set_card.mouse_click):
            # 如果鼠标单击了这个区域，则开启卡组删除器
            self.set_card.mouse_click = None
            self.cards_delete()
        elif self.set_card.mouse_rightclick and self.rect.collidepoint(self.set_card.mouse_rightclick):
            # 如果鼠标右击了这个区域，则清空玩家卡组
            self.set_card.mouse_rightclick = None
            self.set_card.player_deck.clear()

    def cards_delete(self):
        card_height = (
                              self.main_game.settings.screen_height - self.main_game.settings.screen_height * 2 * self.main_game.settings.card_select_hnumber / self.main_game.settings.area_height_spacing) / self.main_game.settings.card_select_hnumber
        card_width = int(
            card_height * self.main_game.settings.original_card_size[0] / self.main_game.settings.original_card_size[1])
        card_height = int(card_height)
        card_select_wnumber = int(self.main_game.settings.area_width_spacing * self.main_game.settings.screen_width / (
                self.main_game.settings.area_width_spacing * card_width + 2 * self.main_game.settings.screen_width))
        cards = self.set_card.player_deck
        index = 0
        while cards:
            num = 0
            cards_list = []
            while card_select_wnumber and num < len(cards):
                card = []
                for number in range(card_select_wnumber):
                    if num < len(cards):
                        card.append(cards[num])
                        num += 1
                cards_list.append(card)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.set_card.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.set_card.mouse_rightclick = None
                        self.set_card.mouse_click = event.pos
                    elif event.button == 3:
                        self.set_card.mouse_click = None
                        self.set_card.mouse_rightclick = event.pos
                    elif event.button == 4:
                        if index > 0:
                            index -= 1
                    elif event.button == 5:
                        if index < len(cards_list) - self.main_game.settings.card_select_hnumber:
                            index += 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if index > 0:
                            index -= 1
                    elif event.key == pygame.K_DOWN:
                        if index < len(cards_list) - self.main_game.settings.card_select_hnumber:
                            index += 1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_PAGEUP:
                        while index > 0:
                            index -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_PAGEDOWN:
                        while index < len(cards_list) - self.main_game.settings.card_select_hnumber:
                            index += 1
                    else:
                        self.set_card.mouse_click = None
                        self.set_card.mouse_rightclick = None
                        return
            self.main_game.screen.fill(self.main_game.settings.screen_background)
            for num in range(self.main_game.settings.card_select_hnumber):
                if index + num < len(cards_list):
                    for number in range(card_select_wnumber):
                        if number < len(cards_list[index + num]):
                            card_image = pygame.transform.scale(cards_list[index + num][number].card_image,
                                                                (card_width, card_height))
                            card_image_rect = card_image.get_rect(center=(
                                self.main_game.settings.screen_width * (number * 2 + 1) / 2 / card_select_wnumber,
                                self.main_game.settings.screen_height * (
                                        num * 2 + 1) / 2 / self.main_game.settings.card_select_hnumber))
                            # 如果鼠标单击了这张卡牌，则从卡组中删除它
                            if self.set_card.mouse_click and card_image_rect.collidepoint(self.set_card.mouse_click):
                                cards.remove(cards_list[index + num][number])
                                self.set_card.mouse_click = None
                            # 如果鼠标右击了这张卡牌，将此卡牌载入卡牌展示器展示
                            if self.set_card.mouse_rightclick and card_image_rect.collidepoint(
                                    self.set_card.mouse_rightclick):
                                self.main_game.card_exhibition(cards_list[index + num][number])
                                self.set_card.mouse_rightclick = None
                            # 鼠标悬停可选区域上时让卡牌提高显示
                            if card_image_rect.collidepoint(self.set_card.mouse_pos):
                                card_image_rect.y -= card_image_rect.h // self.main_game.settings.card_enhance_scale
                            self.main_game.screen.blit(card_image, card_image_rect)
            pygame.display.flip()

    def cards_sorting(self):
        """给卡组按盟友、附属、事件、...并且按费用大小的顺序排好序"""
        card_group = [[], [], []]
        for card in self.set_card.player_deck:
            if card.card_type == "盟友":
                card_group[0].append(card)
            elif card.card_type == "附属":
                card_group[1].append(card)
            elif card.card_type == "事件":
                card_group[2].append(card)
        self.set_card.player_deck.clear()
        for cards in card_group:
            kapai = []
            for card in cards:
                num = 0
                while num < len(kapai):
                    if type(kapai[num].card_cost) != int:
                        break
                    if type(card.card_cost) == int and card.card_cost < kapai[num].card_cost:
                        break
                    num += 1
                kapai.insert(num, card)
            self.set_card.player_deck.extend(kapai)


class Card_Area:
    """卡牌选择区"""

    def __init__(self, set_card):
        main_game = set_card.main_game
        self.set_card = set_card
        self.main_game = main_game
        self.height = round(
            main_game.settings.screen_height - 3 * main_game.settings.screen_height / main_game.settings.area_height_spacing - main_game.settings.screen_height * (
                    main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = round(
            main_game.settings.screen_width - 2 * main_game.settings.screen_width / main_game.settings.area_width_spacing)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottomleft = (main_game.settings.screen_width // main_game.settings.area_width_spacing,
                                main_game.settings.screen_height - main_game.settings.screen_height // main_game.settings.area_height_spacing)
        self.card_height = (
                                   self.height - self.height * 2 * main_game.settings.card_select_hnumber / main_game.settings.area_height_spacing) / main_game.settings.card_select_hnumber
        self.card_width = int(
            self.card_height * main_game.settings.original_card_size[0] / main_game.settings.original_card_size[1])
        self.card_height = int(self.card_height)
        self.card_select_wnumber = int(main_game.settings.area_width_spacing * self.width / (
                main_game.settings.area_width_spacing * self.card_width + 2 * self.width))
        self.card_group = None  # 当前卡牌选择区提供的卡牌
        self.cards_list = None  # 显示在屏幕上的卡牌表
        self.index = None  # 屏幕上卡牌表的当前页数

    def update_card_group(self):
        self.card_group = self.set_card.area_group[0].set_card_group()
        num = 0
        self.cards_list = []
        while self.card_group and self.card_select_wnumber and num < len(self.card_group):
            card = []
            for number in range(self.card_select_wnumber):
                if num < len(self.card_group):
                    card.append(self.card_group[num])
                    num += 1
            self.cards_list.append(card)
        self.index = 0

    def display_draw(self):
        if self.card_group:
            for num in range(self.main_game.settings.card_select_hnumber):
                if self.index + num < len(self.cards_list):
                    for number in range(self.card_select_wnumber):
                        if number < len(self.cards_list[self.index + num]):
                            card_image = pygame.transform.scale(self.cards_list[self.index + num][number].card_image,
                                                                (self.card_width, self.card_height))
                            card_image_rect = card_image.get_rect(center=(self.width * (
                                    number * 2 + 1) / 2 / self.card_select_wnumber + self.main_game.settings.screen_width // self.main_game.settings.area_width_spacing,
                                                                          self.height * (
                                                                                  num * 2 + 1) / 2 / self.main_game.settings.card_select_hnumber + self.rect.top))
                            # 如果鼠标单击了这张卡牌，则将其加入英雄池或者牌组
                            if self.set_card.mouse_click and card_image_rect.collidepoint(self.set_card.mouse_click):
                                self.set_card.mouse_click = None
                                if self.cards_list[self.index + num][number].card_type == "英雄":
                                    if len(self.set_card.player_hero) < 9:
                                        self.set_card.player_hero.append(self.cards_list[self.index + num][number])
                                elif len(self.set_card.player_deck) < 300:
                                    xuhao = -1
                                    for (xuhao, card) in enumerate(self.set_card.player_deck):
                                        if card.card_name == self.cards_list[self.index + num][number].card_name:
                                            break
                                    self.set_card.player_deck.insert(xuhao + 1,
                                                                     self.cards_list[self.index + num][number])
                                    self.set_card.area_group[2].cards_sorting()
                            # 如果鼠标右击了这张卡牌，将此卡牌载入卡牌展示器展示
                            if self.set_card.mouse_rightclick and card_image_rect.collidepoint(
                                    self.set_card.mouse_rightclick):
                                self.main_game.card_exhibition(self.cards_list[self.index + num][number])
                                self.set_card.mouse_rightclick = None
                            # 鼠标悬停卡牌上时，高亮卡牌边框
                            if card_image_rect.collidepoint(self.set_card.mouse_pos):
                                self.main_game.screen.fill(self.main_game.settings.font_color_background,
                                                           card_image_rect.inflate(
                                                               self.main_game.settings.screen_height // self.main_game.settings.area_height_spacing,
                                                               self.main_game.settings.screen_height // self.main_game.settings.area_height_spacing))
                            self.main_game.screen.blit(card_image, card_image_rect)


class Set_Card:
    """组牌器"""

    def __init__(self, main_game):
        self.main_game = main_game
        self.mouse_pos = (0, 0)  # 用于保存当前鼠标位置
        self.mouse_click = None  # 用于保存当前鼠标单击位置
        self.mouse_rightclick = None  # 用于保存当前鼠标右击位置
        self.hero_group = []  # 所有英雄卡
        self.ally_group = []  # 所有盟友卡
        self.affiliated_group = []  # 所有附属卡
        self.action_group = []  # 所有事件卡
        self.player_hero = None  # 玩家英雄卡
        self.player_deck = None  # 玩家牌组
        self.area_group = (Button_Area(self), Player_Hero(self), Player_Deck(self), Card_Area(self))  # 初始化几个区域的实例
        # 加载卡牌
        main_game.screen.fill(main_game.settings.screen_background)
        font = pygame.font.Font(None, main_game.settings.screen_height // 5)
        font_image = font.render("cards loading...", True, main_game.settings.font_color)
        font_rect = font_image.get_rect(
            center=(main_game.settings.screen_width // 2, main_game.settings.screen_height // 2))
        main_game.screen.blit(font_image, font_rect)
        pygame.display.flip()
        self._load_all_card()
        self.player_hero, self.player_deck = main_game._load_player_deck()
        # END
        self.area_group[2].cards_sorting()
        self.area_group[3].update_card_group()

    def run_set_card(self):
        while True:
            # 输入侦测区
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_rightclick = None
                        self.mouse_click = event.pos
                    elif event.button == 3:
                        self.mouse_click = None
                        self.mouse_rightclick = event.pos
                    elif event.button == 4 and self.area_group[3].rect.collidepoint(event.pos):
                        if self.area_group[3].index > 0:
                            self.area_group[3].index -= 1
                    elif event.button == 5 and self.area_group[3].rect.collidepoint(event.pos):
                        if self.area_group[3].index < len(
                                self.area_group[3].cards_list) - self.main_game.settings.card_select_hnumber:
                            self.area_group[3].index += 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.area_group[3].index > 0:
                            self.area_group[3].index -= 1
                    elif event.key == pygame.K_DOWN:
                        if self.area_group[3].index < len(
                                self.area_group[3].cards_list) - self.main_game.settings.card_select_hnumber:
                            self.area_group[3].index += 1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_PAGEUP:
                        while self.area_group[3].index > 0:
                            self.area_group[3].index -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_PAGEDOWN:
                        while self.area_group[3].index < len(
                                self.area_group[3].cards_list) - self.main_game.settings.card_select_hnumber:
                            self.area_group[3].index += 1
                    elif event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_RETURN:
                        with open("玩家牌组", "w") as file:
                            for card in self.player_hero:
                                head, tail = os.path.split(card.card_dir)
                                text = [tail + "."]
                                while head and head != self.main_game.main_path:
                                    head, tail = os.path.split(head)
                                    text.insert(0, tail + ".")
                                file.writelines(text)
                                file.write(os.path.splitext(card.card_file)[0] + "\n")
                            for card in self.player_deck:
                                head, tail = os.path.split(card.card_dir)
                                text = [tail + "."]
                                while head and head != self.main_game.main_path:
                                    head, tail = os.path.split(head)
                                    text.insert(0, tail + ".")
                                file.writelines(text)
                                file.write(os.path.splitext(card.card_file)[0] + "\n")
                        return
            # END
            # 屏幕显示区
            self.main_game.screen.fill(self.main_game.settings.screen_background)
            for area in self.area_group:
                area.display_draw()
            pygame.display.flip()
            # END

    # 这个函数将在组牌器打开时载入所有玩家卡牌库里的卡牌
    def _load_all_card(self):
        with open(os.path.join(self.main_game.main_path, "卡牌库")) as file:
            all_card_paths = file.readlines()
        for module_path in all_card_paths:
            if len(module_path) > 4:
                module_name = import_module(module_path.strip('\n'))
                try:
                    if callable(module_name.Hero):
                        self.hero_group.append(module_name.Hero(self.main_game))
                        if self.hero_group[-1].resource_symbol not in self.area_group[0].button_group[1].card_target:
                            self.area_group[0].button_group[1].card_target.append(self.hero_group[-1].resource_symbol)
                except AttributeError:
                    try:
                        if callable(module_name.Player):
                            card = module_name.Player(self.main_game)
                            if card.card_type == "盟友":
                                self.ally_group.append(card)
                                if self.ally_group[-1].faction_symbol not in self.area_group[0].button_group[
                                    1].card_target:
                                    self.area_group[0].button_group[1].card_target.append(
                                        self.ally_group[-1].faction_symbol)
                            elif card.card_type == "附属":
                                self.affiliated_group.append(card)
                                if self.affiliated_group[-1].faction_symbol not in self.area_group[0].button_group[
                                    1].card_target:
                                    self.area_group[0].button_group[1].card_target.append(
                                        self.affiliated_group[-1].faction_symbol)
                            elif card.card_type == "事件":
                                self.action_group.append(card)
                                if self.action_group[-1].faction_symbol not in self.area_group[0].button_group[
                                    1].card_target:
                                    self.area_group[0].button_group[1].card_target.append(
                                        self.action_group[-1].faction_symbol)
                    except AttributeError:
                        raise
