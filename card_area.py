"""游戏桌面的10个区域"""
from main import *


# 场景区、交锋区、玩家牌放置区、玩家手牌区的卡牌绘制函数(包括了选中卡牌+卡牌选择器+卡牌展示器)
def area_draw(card_group, width, height, rect, main_game):
    cards_len = len(card_group)
    cards = tuple(card_group.keys())
    card_width = height * main_game.settings.original_card_size[0] // main_game.settings.original_card_size[1]
    select_card_rect = None  # 如果当前选中卡牌在这个区域里，记录其rect留到最后再画
    num = 0
    while cards_len and num <= cards_len:
        if num:
            hand_card_image_1 = hand_card_image_2
            hand_card_image_rect_1 = hand_card_image_rect_2
        if num != cards_len:
            hand_card_image_2 = pygame.transform.scale(cards[num].card_image, (card_width, height))
            hand_card_image_rect_2 = hand_card_image_2.get_rect(centery=rect.centery)
            hand_card_image_rect_2.centerx = (width - card_width) * (2 * num + 1) // (
                    cards_len * 2) + rect.x + card_width // 2
        if num:
            # 设置卡牌的可选区域
            if num != cards_len and hand_card_image_rect_2.x - hand_card_image_rect_1.x < card_width:
                hand_card_image_rect_1.width = hand_card_image_rect_2.x - hand_card_image_rect_1.x
            # 如果鼠标单击了这张卡牌，设置其为选中卡牌
            if main_game.mouse_click and hand_card_image_rect_1.collidepoint(main_game.mouse_click):
                main_game.select_card = cards[num - 1]
                main_game.mouse_click = None
            # 如果鼠标右击了这张卡牌，将此卡牌载入卡牌展示器展示
            if main_game.mouse_rightclick and hand_card_image_rect_1.collidepoint(main_game.mouse_rightclick):
                main_game.card_exhibition(cards[num - 1])
                main_game.mouse_rightclick = None
            # 鼠标悬停可选区域上时让卡牌提高显示
            if hand_card_image_rect_1.collidepoint(main_game.mouse_pos) and cards[num - 1] != main_game.select_card:
                hand_card_image_rect_1.y -= height // main_game.settings.card_enhance_scale

            # 绘制附属卡牌
            if card_group[cards[num - 1]]:
                cards_affiliated_len = len(card_group[cards[num - 1]])
                cards_affiliated = card_group[cards[num - 1]]
                number = 0
                while number <= cards_affiliated_len:
                    if number:
                        hand_card_affiliated_image_1 = hand_card_affiliated_image_2
                        hand_card_affiliated_image_rect_1 = hand_card_affiliated_image_rect_2
                    if number != cards_affiliated_len:
                        hand_card_affiliated_image_2 = pygame.transform.scale(cards_affiliated[number].card_image,
                                                                              (card_width, height))
                        hand_card_affiliated_image_rect_2 = hand_card_affiliated_image_2.get_rect(
                            x=hand_card_image_rect_1.x)
                        hand_card_affiliated_image_rect_2.y = hand_card_image_rect_1.y - (
                                cards_affiliated_len - number) * height // main_game.settings.card_enhance_scale
                    if number:
                        # 设置附属牌的可选区域
                        if number != cards_affiliated_len:
                            hand_card_affiliated_image_rect_1.height = hand_card_affiliated_image_rect_2.y - hand_card_affiliated_image_rect_1.y
                        else:
                            hand_card_affiliated_image_rect_1.height = hand_card_image_rect_1.y - hand_card_affiliated_image_rect_1.y

                        if num != cards_len and card_group[
                            cards[num]] and hand_card_image_rect_2.x - hand_card_affiliated_image_rect_1.x < card_width:
                            if len(card_group[cards[num]]) > cards_affiliated_len - number:
                                hand_card_affiliated_image_rect_1.width = hand_card_image_rect_2.x - hand_card_affiliated_image_rect_1.x
                        # 如果鼠标单击了这张卡牌，设置其为选中卡牌
                        if main_game.mouse_click and hand_card_affiliated_image_rect_1.collidepoint(
                                main_game.mouse_click):
                            main_game.select_card = cards_affiliated[number - 1]
                            main_game.mouse_click = None
                        # 如果鼠标右击了这张卡牌，将此卡牌载入卡牌展示器展示
                        if main_game.mouse_rightclick and hand_card_affiliated_image_rect_1.collidepoint(
                                main_game.mouse_rightclick):
                            main_game.card_exhibition(cards_affiliated[number - 1])
                            main_game.mouse_rightclick = None
                        # 鼠标悬停可选区域上时让附属牌提高显示
                        if hand_card_affiliated_image_rect_1.collidepoint(main_game.mouse_pos) and cards_affiliated[
                            number - 1] != main_game.select_card:
                            hand_card_affiliated_image_rect_1.y -= height // main_game.settings.card_enhance_scale

                        # 绘制附属牌图像和其数值蒙板
                        if cards_affiliated[number - 1] != main_game.select_card:
                            main_game.screen.blit(hand_card_affiliated_image_1, hand_card_affiliated_image_rect_1)
                            hand_card_affiliated_image_mask = pygame.transform.scale(
                                cards_affiliated[number - 1].card_image_mask, (card_width, height))
                            main_game.screen.blit(hand_card_affiliated_image_mask, hand_card_affiliated_image_rect_1)
                        else:
                            select_card_rect = hand_card_affiliated_image_rect_1
                    number += 1
            # END

            # 绘制卡牌图像和其数值蒙板
            if cards[num - 1] != main_game.select_card:
                main_game.screen.blit(hand_card_image_1, hand_card_image_rect_1)
                hand_card_image_mask = pygame.transform.scale(cards[num - 1].card_image_mask, (card_width, height))
                main_game.screen.blit(hand_card_image_mask, hand_card_image_rect_1)
            else:
                select_card_rect = hand_card_image_rect_1
            # END

        num += 1
    # 最后画选中卡以使其处于所有卡牌上方
    if select_card_rect:
        select_card_image = pygame.transform.scale(main_game.select_card.card_image, (card_width, height))
        main_game.screen.blit(select_card_image, select_card_rect)
        select_card_image_mask = pygame.transform.scale(main_game.select_card.card_image_mask, (card_width, height))
        main_game.screen.blit(select_card_image_mask, select_card_rect)


# 威胁、阶段、步骤...数值区
class Threat_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = self.height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = main_game.settings.screen_width // main_game.settings.area_width_spacing
        self.rect.y = main_game.settings.screen_height // main_game.settings.area_height_spacing

        self.game_phase = ("资源", "计划", "任务", "探索", "遭遇", "战斗", "恢复")  # 游戏的七个阶段
        # 游戏的任务、遭遇和战斗阶段对应的步骤
        self.game_step = (
            ("指派角色", "集结", "任务结算"), ("主动交锋", "交锋检定"),
            ("选择敌军", "宣告防御者", "结算暗影效果", "决定敌军伤害", "宣告攻击目标", "决定攻击力", "决定战斗伤害"))
        self.threat_failure = 0  # 当前游戏失败所需达到的威胁值
        self.threat_value = 0  # 游戏的威胁数值
        self.round_number = 0  # 游戏的回合数
        self.victory_point_deck = None  # 游戏的胜利点牌堆
        self.current_phase = -1  # game_phase序列的游戏当前阶段索引，-1表示游戏未开始或者阶段结束
        self.current_step = -1  # game_step序列的游戏当前步骤索引，-1表示当前阶段没有步骤
        self.action_window = False  # 表明游戏是否处于行动窗口
        self.order = [False, 0, 0, False, 0, 0]  # 程序真正循环游戏的步骤，在run_game()中每次只执行一步

    # 初始化游戏的威胁数值
    def initialize_threat(self):
        if self.main_game.xuanxiang // 1000 == 111:
            self.threat_failure = 50
        for hero in self.main_game.role_area.hero_group:
            self.threat_value += hero.initial_threat

    # 游戏失败的判定
    def test_game_over(self):
        if self.threat_value >= self.threat_failure or not self.main_game.role_area.hero_group:
            self.main_game.screen.fill(self.main_game.settings.screen_background)
            font = pygame.font.Font(None, self.main_game.settings.screen_height // 4)
            font_image = font.render("Game Over", True, self.main_game.settings.font_color)
            font_rect = font_image.get_rect(
                center=(self.main_game.settings.screen_width // 2, self.main_game.settings.screen_height // 2))
            self.main_game.screen.blit(font_image, font_rect)
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and (
                            event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN):
                        sys.exit()

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        threat_area_image = pygame.Surface((self.width, self.height)).convert()
        threat_area_image.fill(self.main_game.settings.threat_area_background)
        font_size = self.height // 5
        while font_size > 1:
            display_font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                            font_size)
            if display_font.size("威胁：" + str(self.threat_value))[0] > self.width or \
                    display_font.size("回合：" + str(self.round_number))[0] > self.width:
                font_size -= 1
            elif self.current_phase >= 0 and self.current_phase < 7 and \
                    display_font.size("阶段：" + self.game_phase[self.current_phase])[0] > self.width:
                font_size -= 1
            elif self.current_phase == 2 and self.current_step >= 0 and self.current_step < 3 and \
                    display_font.size("步骤：" + self.game_step[0][self.current_step])[
                        0] > self.width or self.current_phase == 4 and self.current_step >= 0 and self.current_step < 2 and \
                    display_font.size("步骤：" + self.game_step[1][self.current_step])[
                        0] > self.width or self.current_phase == 5 and self.current_step >= 0 and self.current_step < 7 and \
                    display_font.size("步骤：" + self.game_step[2][self.current_step])[0] > self.width:
                font_size -= 1
            else:
                break

        # 绘制威胁值
        threat_value_image = display_font.render("威胁：" + str(self.threat_value), True,
                                                 self.main_game.settings.font_color,
                                                 self.main_game.settings.threat_area_background).convert()
        threat_value_image_rect = threat_value_image.get_rect()
        threat_value_image_rect.center = (self.width // 2, self.height // 5)

        # 绘制回合数
        round_number_image = display_font.render("回合：" + str(self.round_number), True,
                                                 self.main_game.settings.font_color,
                                                 self.main_game.settings.threat_area_background).convert()
        round_number_image_rect = round_number_image.get_rect()
        round_number_image_rect.center = (self.width // 2, 2 * self.height // 5)

        # 绘制当前阶段
        if self.current_phase >= 0 and self.current_phase < 7:
            current_phase_image = display_font.render("阶段：" + self.game_phase[self.current_phase], True,
                                                      self.main_game.settings.font_color,
                                                      self.main_game.settings.threat_area_background).convert()
        else:
            current_phase_image = display_font.render("阶段：", True, self.main_game.settings.font_color,
                                                      self.main_game.settings.threat_area_background).convert()
        current_phase_image_rect = current_phase_image.get_rect()
        current_phase_image_rect.center = (self.width // 2, 3 * self.height // 5)

        # 绘制当前步骤
        if self.current_phase == 2 and self.current_step >= 0 and self.current_step < 3:
            current_step_image = display_font.render("步骤：" + self.game_step[0][self.current_step], True,
                                                     self.main_game.settings.font_color,
                                                     self.main_game.settings.threat_area_background).convert()
        elif self.current_phase == 4 and self.current_step >= 0 and self.current_step < 2:
            current_step_image = display_font.render("步骤：" + self.game_step[1][self.current_step], True,
                                                     self.main_game.settings.font_color,
                                                     self.main_game.settings.threat_area_background).convert()
        elif self.current_phase == 5 and self.current_step >= 0 and self.current_step < 7:
            current_step_image = display_font.render("步骤：" + self.game_step[2][self.current_step], True,
                                                     self.main_game.settings.font_color,
                                                     self.main_game.settings.threat_area_background).convert()
        else:
            current_step_image = display_font.render("步骤：", True, self.main_game.settings.font_color,
                                                     self.main_game.settings.threat_area_background).convert()
        current_step_image_rect = current_step_image.get_rect()
        current_step_image_rect.center = (self.width // 2, 4 * self.height // 5)

        threat_area_image.blits(((threat_value_image, threat_value_image_rect),
                                 (round_number_image, round_number_image_rect),
                                 (current_phase_image, current_phase_image_rect),
                                 (current_step_image, current_step_image_rect)), False)
        self.main_game.screen.blit(threat_area_image, self.rect)

    # 侦听行动窗口按钮的动作
    def listening_action_window(self):
        if self.main_game.information and self.main_game.information[1] == "将要进入行动窗口":
            self.action_window = True
            if self.order[3]:
                self.order[3] = False
            else:
                self.order[0] = False
            self.main_game.information = None
        if self.action_window:
            button = []
            action_cards = []
            for card in self.main_game.role_area.card_group:
                if "行动" in card.rule_mark and "已横置" not in card.active_condition and "行动后" not in card.active_condition and "暗影牌" not in card.active_condition and card.card_type != "目标" and not \
                        card.card_order[0]:
                    button.append(("行动-" + card.card_name, None))
                    action_cards.append(card)
                if self.main_game.role_area.card_group[card]:
                    for card_affiliated in self.main_game.role_area.card_group[card]:
                        if "行动" in card_affiliated.rule_mark and "已横置" not in card_affiliated.active_condition and "行动后" not in card_affiliated.active_condition and "暗影牌" not in card_affiliated.active_condition and card_affiliated.card_type != "目标" and not \
                                card_affiliated.card_order[0]:
                            button.append(("行动-" + card_affiliated.card_name, None))
                            action_cards.append(card_affiliated)
            for card in self.main_game.clash_area.card_group:
                if "行动" in card.rule_mark and "已横置" not in card.active_condition and "行动后" not in card.active_condition and "暗影牌" not in card.active_condition and card.card_type != "目标" and not \
                        card.card_order[0]:
                    button.append(("行动-" + card.card_name, None))
                    action_cards.append(card)
                if self.main_game.clash_area.card_group[card]:
                    for card_affiliated in self.main_game.clash_area.card_group[card]:
                        if "行动" in card_affiliated.rule_mark and "已横置" not in card_affiliated.active_condition and "行动后" not in card_affiliated.active_condition and "暗影牌" not in card_affiliated.active_condition and card_affiliated.card_type != "目标" and not \
                                card_affiliated.card_order[0]:
                            button.append(("行动-" + card_affiliated.card_name, None))
                            action_cards.append(card_affiliated)
            for card in self.main_game.scenario_area.card_group:
                if "行动" in card.rule_mark and "已横置" not in card.active_condition and "行动后" not in card.active_condition and "暗影牌" not in card.active_condition and card.card_type != "目标" and not \
                        card.card_order[0]:
                    button.append(("行动-" + card.card_name, None))
                    action_cards.append(card)
                if self.main_game.scenario_area.card_group[card]:
                    for card_affiliated in self.main_game.scenario_area.card_group[card]:
                        if "行动" in card_affiliated.rule_mark and "已横置" not in card_affiliated.active_condition and "行动后" not in card_affiliated.active_condition and "暗影牌" not in card_affiliated.active_condition and card_affiliated.card_type != "目标" and not \
                                card_affiliated.card_order[0]:
                            button.append(("行动-" + card_affiliated.card_name, None))
                            action_cards.append(card_affiliated)
            for card in self.main_game.task_area.region_card:
                if self.main_game.task_area.region_card[card]:
                    for card_affiliated in self.main_game.task_area.region_card[card]:
                        if "行动" in card_affiliated.rule_mark and "已横置" not in card_affiliated.active_condition and "行动后" not in card_affiliated.active_condition and "暗影牌" not in card_affiliated.active_condition and card_affiliated.card_type != "目标" and not \
                                card_affiliated.card_order[0]:
                            button.append(("行动-" + card_affiliated.card_name, None))
                            action_cards.append(card_affiliated)
            if button:
                self.main_game.button_option.import_button("action_window", button)
            else:
                self.main_game.button_option.import_button("action_window", (("事件行动窗口", None),))
            if self.main_game.button_option.option // 100000 and button:
                action_cards[self.main_game.button_option.option // 100000 - 1].card_order = ["行动", 0, 0, False, 0,
                                                                                              0]
                self.main_game.button_option.reset()
            elif self.main_game.next_step:
                self.main_game.button_option.reset()
                self.main_game.next_step = 0
                self.action_window = False
                if self.order[0]:
                    self.order[3] = True
                else:
                    self.order[0] = True

    # 在此处运行游戏的7阶段循环
    def run_order(self):
        if self.order[0] and self.order[1] == 0:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.round_number += 1
                self.current_phase = 0
                self.main_game.information = [0, "游戏开始任务卡牌将要展示", "order",
                                              self.main_game.task_area.task_deck[self.main_game.task_area.task_number]]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 1:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.card_exhibition(self.main_game.task_area.task_deck[self.main_game.task_area.task_number],
                                               self.main_game.settings.card_exhibition_time)
                self.main_game.information = [0, "游戏开始任务卡牌展示后", "order",
                                              self.main_game.task_area.task_deck[self.main_game.task_area.task_number]]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 2:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "将要进入资源阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 3:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = 0
                self.main_game.information = [0, "进入资源阶段后", "order"]
                self.resource_target = self.main_game.role_area.hero_group.copy()
                self.order[3] = True
                self.order[4] = 0
                self.order[5] = 0
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 4:
            if self.order[2]:
                if hasattr(self, "resource_target"):
                    del self.resource_target
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information and self.order[3]:
                if self.order[5]:
                    if hasattr(self, "resource_target") and self.resource_target:
                        self.resource_target.pop(0)
                    self.order[4] += 1
                    self.order[5] -= 1
                elif self.order[4] % 2:
                    if self.resource_target:
                        self.resource_target[0].active_resource += 1
                        self.resource_target[0].update_mask()
                        self.main_game.information = [0, "资源阶段英雄卡牌增加资源后", "order", self.resource_target.pop(0)]
                    self.order[4] += 1
                else:
                    if hasattr(self, "resource_target") and self.resource_target:
                        self.main_game.information = [0, "资源阶段英雄卡牌将要增加资源", "order", self.resource_target[0]]
                        self.order[4] += 1
                    elif hasattr(self, "resource_target"):
                        del self.resource_target
                        self.order[3] = False
                        self.order[4] = 0
                        self.order[5] = 0
                        self.order[1] += 1
        elif self.order[0] and self.order[1] == 5:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.playerdeck_area.player_deck:
                    self.main_game.information = [0, "资源阶段玩家将要补卡", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 6:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.playerdeck_area.player_deck:
                    card = self.main_game.playerdeck_area.player_deck.pop(0)
                    self.main_game.hand_area.card_group[card] = None
                    self.main_game.information = [0, "资源阶段玩家补卡后", "order", card]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 7:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "将要离开资源阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 8:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = -1
                self.main_game.information = [0, "将要进入计划阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 9:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = 1
                self.main_game.information = [0, "进入计划阶段后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 10:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.next_step:
                    self.main_game.next_step = 0
                    self.main_game.information = [0, "将要离开计划阶段", "order"]
                    self.order[1] += 1
        elif self.order[0] and self.order[1] == 11:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = -1
                self.main_game.information = [0, "将要进入任务阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 12:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = 2
                self.main_game.information = [0, "进入任务阶段后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 13:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "将要进入指派角色步骤", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 14:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = 0
                self.main_game.information = [0, "进入指派角色步骤后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 15:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.select_card = None
                self.main_game.information = [0, "将要进入行动窗口", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 16:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.next_step:
                    self.main_game.next_step = 0
                    self.main_game.information = [0, "将要离开指派角色步骤", "order"]
                    self.order[1] += 1
        elif self.order[0] and self.order[1] == 17:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.select_card = None
                self.main_game.information = [0, "将要进入行动窗口", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 18:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = -1
                self.main_game.information = [0, "将要进入集结步骤", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 19:
            if self.order[2]:
                self.order[1] += 8
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = 1
                self.main_game.information = [0, "进入集结步骤后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 20:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.select_card = None
                self.main_game.information = [0, "将要进入行动窗口", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 21:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if not self.main_game.encounter_area.encounter_deck and self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounter_area.encounter_deck = self.main_game.encounterdiscard_area.encounterdiscard_deck
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = []
                    for card in self.main_game.encounter_area.encounter_deck:
                        card.reset_card()
                        card.update_mask()
                    random.shuffle(self.main_game.encounter_area.encounter_deck)
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.information = [0, "遭遇卡牌将要展示", "order",
                                                  self.main_game.encounter_area.encounter_deck[0]]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 22:
            if self.order[2]:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.encounter_area.encounter_deck[0].reset_card()
                    self.main_game.encounter_area.encounter_deck[0].update_mask()
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    self.encounter_card = self.main_game.encounter_area.encounter_deck.pop(0)
                    self.main_game.card_exhibition(self.encounter_card, self.main_game.settings.card_exhibition_time)
                    self.main_game.scenario_area.card_group[self.encounter_card] = None
                    self.main_game.information = [0, "遭遇卡牌展示后", "order", self.encounter_card]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 23:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌将要放置进场", "order",
                                                  self.encounter_card]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 24:
            if self.order[2]:
                if hasattr(self, "encounter_card"):
                    self.main_game.card_estimate(self.encounter_card).pop(self.encounter_card)
                    self.encounter_card.reset_card()
                    self.encounter_card.update_mask()
                    if self.main_game.encounter_area.encounter_deck:
                        self.main_game.encounter_area.encounter_deck.insert(0, self.encounter_card)
                        random.shuffle(self.main_game.encounter_area.encounter_deck)
                    else:
                        self.main_game.encounter_area.encounter_deck = [self.encounter_card]
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌放置进场后", "order",
                                                  self.encounter_card]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 25:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "encounter_card"):
                    del self.encounter_card
                if not self.main_game.encounter_area.encounter_deck and self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounter_area.encounter_deck = self.main_game.encounterdiscard_area.encounterdiscard_deck
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = []
                    for card in self.main_game.encounter_area.encounter_deck:
                        card.reset_card()
                        card.update_mask()
                    random.shuffle(self.main_game.encounter_area.encounter_deck)
                self.main_game.information = [0, "将要离开集结步骤", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 26:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.select_card = None
                self.main_game.information = [0, "将要进入行动窗口", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 27:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = -1
                self.main_game.information = [0, "将要进入任务结算步骤", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 28:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = 2
                self.main_game.information = [0, "进入任务结算步骤后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 29:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.select_card = None
                self.main_game.information = [0, "将要进入行动窗口", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 30:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                willpower = 0
                threat = 0
                for card in self.main_game.role_area.card_group:
                    if "任务中" in card.active_condition:
                        willpower += card.active_willpower
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "敌军" or card.card_type == "地区":
                        threat += card.active_threat_force
                self.main_game.information = [0, "将要结算任务", "order", willpower - threat]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 31:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                willpower = 0
                threat = 0
                for card in self.main_game.role_area.card_group:
                    if "任务中" in card.active_condition:
                        willpower += card.active_willpower
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "敌军" or card.card_type == "地区":
                        threat += card.active_threat_force
                if willpower > threat:
                    if self.main_game.task_area.region_card:
                        if len(self.main_game.task_area.region_card) > 1:
                            region = self.main_game.card_select(tuple(self.main_game.task_area.region_card.keys()))
                        else:
                            region = tuple(self.main_game.task_area.region_card.keys())[0]
                        region.active_task_point -= willpower - threat
                        if region.active_task_point < 0:
                            region.active_task_point = 0
                        region.update_mask()
                    else:
                        self.main_game.task_area.task_deck[
                            self.main_game.task_area.task_number].active_task_point -= willpower - threat
                        if self.main_game.task_area.task_deck[
                            self.main_game.task_area.task_number].active_task_point < 0:
                            self.main_game.task_area.task_deck[
                                self.main_game.task_area.task_number].active_task_point = 0
                        self.main_game.task_area.task_deck[self.main_game.task_area.task_number].update_mask()
                elif willpower < threat:
                    self.threat_value += threat - willpower
                self.main_game.information = [0, "将要离开任务结算步骤", "order", willpower - threat]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 32:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.select_card = None
                self.main_game.information = [0, "将要进入行动窗口", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 33:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = -1
                self.main_game.information = [0, "将要离开任务阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 34:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                for card in self.main_game.role_area.card_group:
                    if "任务中" in card.active_condition:
                        card.active_condition.pop("任务中")
                        card.update_mask()
                self.current_phase = -1
                self.main_game.information = [0, "将要进入探索阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 35:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = 3
                self.main_game.information = [0, "进入探索阶段后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 36:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                can_activate = False
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "地区" and not self.main_game.task_area.region_card:
                        can_activate = True
                        break
                if self.main_game.next_step or not can_activate:
                    self.main_game.next_step = 0
                    self.order[1] += 1
        elif self.order[0] and self.order[1] == 37:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "将要离开探索阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 38:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = -1
                self.main_game.information = [0, "将要进入遭遇阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 39:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = 4
                self.main_game.information = [0, "进入遭遇阶段后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 40:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "将要进入主动交锋步骤", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 41:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = 0
                self.main_game.information = [0, "进入主动交锋步骤后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 42:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                can_encounter = False
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "敌军":
                        can_encounter = True
                        break
                if self.main_game.next_step or not can_encounter:
                    self.main_game.next_step = 0
                    self.order[1] += 1
        elif self.order[0] and self.order[1] == 43:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "将要离开主动交锋步骤", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 44:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = -1
                self.main_game.information = [0, "将要进入交锋检定步骤", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 45:
            if self.order[2]:
                self.order[1] += 1
            elif not self.main_game.information:
                self.current_step = 1
                self.main_game.information = [0, "进入交锋检定步骤后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 46:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "敌军" and card.active_clash_value <= self.threat_value:
                        card.card_order = ["交锋", 0, 0, False, 0, 0]
                self.main_game.information = [0, "将要离开交锋检定步骤", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 47:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = -1
                self.main_game.information = [0, "将要离开遭遇阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 48:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = -1
                self.main_game.information = [0, "将要进入战斗阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 49:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = 5
                self.main_game.information = [0, "进入战斗阶段后", "order"]
                self.order[3] = True
                self.order[4] = 0
                self.order[5] = 0
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 50:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information and self.order[3]:
                if self.order[5]:
                    self.order[4] += 1
                    self.order[5] -= 1
                elif self.order[4] % 2:
                    enemy = None
                    num = 0
                    for card in self.main_game.clash_area.card_group:
                        if "分配暗影" not in card.active_condition and "已攻击" not in card.active_condition:
                            if num == 0:
                                enemy = card
                            elif card.active_clash_value > enemy.active_clash_value:
                                enemy = card
                            num += 1
                    if num:
                        shadow_card = Print_Card(self.main_game)
                        if self.main_game.encounter_area.encounter_deck:
                            shadow_card.card_target = self.main_game.encounter_area.encounter_deck.pop(0)
                        shadow_card.card_image = self.main_game.computer_card_image.copy()
                        shadow_card.card_type = "暗影牌"
                        shadow_card.active_condition["暗影牌"] = [enemy]
                        enemy.active_condition["分配暗影"] = [shadow_card]
                        if self.main_game.clash_area.card_group[enemy]:
                            self.main_game.clash_area.card_group[enemy].append(shadow_card)
                        else:
                            self.main_game.clash_area.card_group[enemy] = [shadow_card]
                        enemy.update_mask()
                        self.main_game.information = [0, "分配暗影牌后", "order", enemy]
                    self.order[4] += 1
                else:
                    enemy = None
                    num = 0
                    for card in self.main_game.clash_area.card_group:
                        if "分配暗影" not in card.active_condition and "已攻击" not in card.active_condition:
                            if num == 0:
                                enemy = card
                            elif card.active_clash_value > enemy.active_clash_value:
                                enemy = card
                            num += 1
                    if num:
                        self.main_game.information = [0, "将要分配暗影牌", "order", enemy]
                        self.order[4] += 1
                    else:
                        self.order[3] = True
                        self.order[4] = 0
                        self.order[5] = 0
                        self.order[1] += 1
        elif self.order[0] and self.order[1] == 51:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information and self.order[3]:
                # 应对步骤中出现的攻击和防御者变故
                if hasattr(self, "enemy"):
                    if "攻击中" in self.enemy.active_condition:
                        for role in self.enemy.active_condition["攻击中"].copy():
                            if role not in self.main_game.role_area.card_group:
                                if "宣告防御" in role.active_condition:
                                    role.active_condition.pop("宣告防御")
                                    role.update_mask()
                                self.enemy.active_condition["攻击中"].remove(role)
                    if self.enemy not in self.main_game.clash_area.card_group and self.enemy not in self.main_game.scenario_area.card_group:
                        if "攻击中" in self.enemy.active_condition:
                            for role in self.enemy.active_condition["攻击中"]:
                                if "宣告防御" in role.active_condition:
                                    role.active_condition.pop("宣告防御")
                                    role.update_mask()
                            self.enemy.active_condition.pop("攻击中")
                        else:
                            for role in self.main_game.role_area.card_group:
                                if "宣告防御" in role.active_condition:
                                    role.active_condition.pop("宣告防御")
                                    role.update_mask()
                        self.enemy.update_mask()
                        del self.enemy
                        if hasattr(self, "defender"):
                            del self.defender
                        if hasattr(self, "damage"):
                            del self.damage
                        self.order[4] = 0
                        self.order[5] = 0
                # END
                if self.order[5]:
                    self.order[4] += 1
                    self.order[5] -= 1
                elif self.order[4] % 18 == 0:
                    self.current_step = -1
                    can_attack = False
                    for enemy in self.main_game.clash_area.card_group:
                        if "已攻击" not in enemy.active_condition:
                            can_attack = True
                            break
                    if can_attack:
                        self.main_game.information = [0, "将要进入选择敌军步骤", "order"]
                        self.order[4] += 1
                    else:
                        self.order[3] = True
                        self.order[4] = 0
                        self.order[5] = 0
                        self.order[1] += 1
                elif self.order[4] % 18 == 1:
                    self.current_step = 0
                    self.main_game.information = [0, "进入选择敌军步骤后", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 2:
                    enemys = []
                    for enemy in self.main_game.clash_area.card_group:
                        if "已攻击" not in enemy.active_condition:
                            enemys.append(enemy)
                    self.enemy = self.main_game.card_select(enemys)
                    self.enemy.active_condition["攻击中"] = []
                    self.enemy.update_mask()
                    self.main_game.information = [0, "将要离开选择敌军步骤", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 3:
                    self.main_game.select_card = None
                    self.main_game.information = [0, "将要进入行动窗口", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 4:
                    self.current_step = -1
                    self.main_game.information = [0, "将要进入宣告防御者步骤", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 5:
                    self.current_step = 1
                    self.main_game.information = [0, "进入宣告防御者步骤后", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 6:
                    if self.main_game.next_step or not self.main_game.multiple_defender and self.enemy.active_condition[
                        "攻击中"]:
                        self.main_game.next_step = 0
                        self.main_game.information = [0, "将要离开宣告防御者步骤", "order"]
                        self.order[4] += 1
                elif self.order[4] % 18 == 7:
                    self.main_game.select_card = None
                    self.main_game.information = [0, "将要进入行动窗口", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 8:
                    self.current_step = -1
                    self.main_game.information = [0, "将要进入结算暗影效果步骤", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 9:
                    self.current_step = 2
                    self.main_game.information = [0, "进入结算暗影效果步骤后", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 10:
                    if "分配暗影" in self.enemy.active_condition:
                        num = 0
                        for shadow_card in self.enemy.active_condition["分配暗影"].copy():
                            if shadow_card.card_type == "暗影牌":
                                if shadow_card.card_target:
                                    self.enemy.active_condition["分配暗影"][num] = shadow_card.card_target
                                    self.main_game.clash_area.card_group[self.enemy][
                                        self.main_game.clash_area.card_group[self.enemy].index(
                                            shadow_card)] = shadow_card.card_target
                                    shadow_card.card_target.active_condition.update(shadow_card.active_condition)
                                    shadow_card.card_target.update_mask()
                                    if "暗影" in shadow_card.card_target.rule_mark:
                                        self.main_game.card_exhibition(shadow_card.card_target,
                                                                       self.main_game.settings.card_exhibition_time)
                                        shadow_card.card_target.card_order = ["结算暗影", 0, 0, False, 0, 0]
                                    num += 1
                                else:
                                    self.enemy.active_condition["分配暗影"].pop(num)
                                    self.main_game.clash_area.card_group[self.enemy].remove(shadow_card)
                            else:
                                num += 1
                    self.main_game.information = [0, "将要离开结算暗影效果步骤", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 11:
                    self.main_game.select_card = None
                    self.main_game.information = [0, "将要进入行动窗口", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 12:
                    self.current_step = -1
                    self.main_game.information = [0, "将要进入决定敌军伤害步骤", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 13:
                    self.current_step = 3
                    self.main_game.information = [0, "进入决定敌军伤害步骤后", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 14:
                    if self.enemy.active_condition["攻击中"]:
                        defense_force = 0
                        for card in self.enemy.active_condition["攻击中"]:
                            defense_force += card.active_defense_force
                            card.active_condition.pop("宣告防御")
                            card.update_mask()
                        if len(self.enemy.active_condition["攻击中"]) > 1:
                            self.defender = self.main_game.card_select(self.enemy.active_condition["攻击中"])
                        else:
                            self.defender = self.enemy.active_condition["攻击中"][0]
                        if self.enemy.active_attack_force > defense_force:
                            self.damage = self.enemy.active_attack_force - defense_force
                        else:
                            self.damage = 0
                    else:  # 无人防御
                        self.defender = self.main_game.card_select(self.main_game.role_area.hero_group)
                        self.damage = self.enemy.active_attack_force
                    self.enemy.active_condition.pop("攻击中")
                    self.enemy.active_condition["已攻击"] = None
                    self.enemy.update_mask()
                    self.main_game.information = [0, "战斗阶段敌军卡牌将要攻击", self.enemy, self.defender]
                    self.order[4] += 1
                elif self.order[4] % 18 == 15:
                    if hasattr(self, "defender") or hasattr(self, "damage"):
                        self.defender.active_health_point -= self.damage
                        if self.defender.active_health_point < 0:
                            self.defender.active_health_point = 0
                        self.defender.update_mask()
                        self.main_game.information = [0, "战斗阶段敌军卡牌攻击后", self.enemy, self.defender]
                        del self.defender
                        del self.damage
                    self.order[4] += 1
                elif self.order[4] % 18 == 16:
                    if "攻击中" in self.enemy.active_condition:
                        self.enemy.active_condition.pop("攻击中")
                        self.enemy.active_condition["已攻击"] = None
                        self.enemy.update_mask()
                    del self.enemy
                    if hasattr(self, "defender") or hasattr(self, "damage"):
                        del self.defender
                        del self.damage
                    self.main_game.information = [0, "将要离开决定敌军伤害步骤", "order"]
                    self.order[4] += 1
                elif self.order[4] % 18 == 17:
                    self.main_game.select_card = None
                    self.main_game.information = [0, "将要进入行动窗口", "order"]
                    self.order[4] += 1
        elif self.order[0] and self.order[1] == 52:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information and self.order[3]:
                # 应对步骤中出现的攻击和防御者变故
                if hasattr(self, "enemy"):
                    biaozhi = False
                    if "防御中" in self.enemy.active_condition:
                        for role in self.enemy.active_condition["防御中"].copy():
                            if role not in self.main_game.role_area.card_group:
                                if "宣告攻击" in role.active_condition:
                                    role.active_condition.pop("宣告攻击")
                                    role.update_mask()
                                if hasattr(self, "attacker") and role == self.attacker:
                                    del self.attacker
                                elif hasattr(self, "defenders") and role in self.defenders:
                                    self.defenders.remove(role)
                                self.enemy.active_condition["防御中"].remove(role)
                                if not self.enemy.active_condition["防御中"]:
                                    biaozhi = True
                    if self.enemy not in self.main_game.clash_area.card_group and self.enemy not in self.main_game.scenario_area.card_group or biaozhi:
                        if "防御中" in self.enemy.active_condition:
                            for role in self.enemy.active_condition["防御中"]:
                                if "宣告攻击" in role.active_condition:
                                    role.active_condition.pop("宣告攻击")
                                    role.update_mask()
                            self.enemy.active_condition.pop("防御中")
                        else:
                            for role in self.main_game.role_area.card_group:
                                if "宣告攻击" in role.active_condition:
                                    role.active_condition.pop("宣告攻击")
                                    role.update_mask()
                        self.enemy.update_mask()
                        del self.enemy
                        if hasattr(self, "attacker"):
                            del self.attacker
                        if hasattr(self, "attack_force"):
                            del self.attack_force
                        if hasattr(self, "defenders"):
                            del self.defenders
                        self.order[4] = 0
                        self.order[5] = 0
                # END
                if self.order[5]:
                    if hasattr(self, "attacker"):
                        del self.attacker
                    else:
                        self.order[4] += 1
                    self.order[5] -= 1
                elif self.order[4] % 12 == 0:
                    self.current_step = -1
                    can_attack = False
                    for enemy in self.main_game.clash_area.card_group:
                        if enemy.card_type == "敌军" and "防御中" not in enemy.active_condition and "已防御" not in enemy.active_condition:
                            can_attack = True
                            break
                    for role in self.main_game.role_area.card_group:
                        if "攻击场景区" in role.rule_mark and "宣告攻击" not in role.active_condition and "已横置" not in role.active_condition:
                            for enemy in self.main_game.scenario_area.card_group:
                                if enemy.card_type == "敌军" and "防御中" not in enemy.active_condition and "已防御" not in enemy.active_condition:
                                    can_attack = True
                                    break
                            break
                    if can_attack:
                        self.main_game.information = [0, "将要进入宣告攻击目标步骤", "order"]
                        self.order[4] += 1
                    else:
                        self.order[3] = False
                        self.order[4] = 0
                        self.order[5] = 0
                        self.order[1] += 1
                elif self.order[4] % 12 == 1:
                    self.current_step = 4
                    self.main_game.information = [0, "进入宣告攻击目标步骤后", "order"]
                    self.order[4] += 1
                elif self.order[4] % 12 == 2:
                    if self.main_game.next_step:
                        self.main_game.next_step = 0
                        self.order[3] = False
                        self.order[4] = 0
                        self.order[5] = 0
                        self.order[1] += 1
                elif self.order[4] % 12 == 3:
                    self.main_game.select_card = None
                    self.main_game.information = [0, "将要进入行动窗口", "order"]
                    self.order[4] += 1
                elif self.order[4] % 12 == 4:
                    self.current_step = -1
                    self.main_game.information = [0, "将要进入决定攻击力步骤", "order"]
                    self.order[4] += 1
                elif self.order[4] % 12 == 5:
                    self.current_step = 5
                    self.main_game.information = [0, "进入决定攻击力步骤后", "order"]
                    if hasattr(self, "attacker"):
                        del self.attacker
                    self.attack_force = 0
                    self.defenders = self.enemy.active_condition["防御中"].copy()
                    self.order[4] += 1
                elif self.order[4] % 12 == 6:
                    if hasattr(self, "attacker"):
                        self.attack_force += self.attacker.active_attack_force
                        self.main_game.information = [0, "战斗阶段" + self.attacker.card_type + "卡牌攻击后", self.attacker,
                                                      self.enemy]
                        del self.attacker
                    elif self.defenders:
                        self.attacker = self.defenders.pop(0)
                        self.main_game.information = [0, "战斗阶段" + self.attacker.card_type + "卡牌将要攻击", self.attacker,
                                                      self.enemy]
                    else:
                        del self.defenders
                        self.main_game.information = [0, "将要离开决定攻击力步骤", "order"]
                        self.order[4] += 1
                elif self.order[4] % 12 == 7:
                    self.main_game.select_card = None
                    self.main_game.information = [0, "将要进入行动窗口", "order"]
                    self.order[4] += 1
                elif self.order[4] % 12 == 8:
                    self.current_step = -1
                    self.main_game.information = [0, "将要进入决定战斗伤害步骤", "order"]
                    self.order[4] += 1
                elif self.order[4] % 12 == 9:
                    self.current_step = 6
                    self.main_game.information = [0, "进入决定战斗伤害步骤后", "order"]
                    self.order[4] += 1
                elif self.order[4] % 12 == 10:
                    if self.attack_force > self.enemy.active_defense_force:
                        self.enemy.active_health_point -= self.attack_force - self.enemy.active_defense_force
                    if self.enemy.active_health_point < 0:
                        self.enemy.active_health_point = 0
                    for attacker in self.enemy.active_condition["防御中"]:
                        attacker.active_condition.pop("宣告攻击")
                        attacker.update_mask()
                    self.enemy.active_condition.pop("防御中")
                    self.enemy.active_condition["已防御"] = None
                    self.enemy.update_mask()
                    del self.attack_force
                    del self.enemy
                    self.main_game.information = [0, "将要离开决定战斗伤害步骤", "order"]
                    self.order[4] += 1
                elif self.order[4] % 12 == 11:
                    self.main_game.select_card = None
                    self.main_game.information = [0, "将要进入行动窗口", "order"]
                    self.order[4] += 1
        elif self.order[0] and self.order[1] == 53:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_step = -1
                self.main_game.information = [0, "将要离开战斗阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 54:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                enemys = []
                if self.main_game.scenario_area.card_group:
                    enemys.extend(self.main_game.scenario_area.card_group)
                if self.main_game.clash_area.card_group:
                    enemys.extend(self.main_game.clash_area.card_group)
                for enemy in enemys:
                    if "分配暗影" in enemy.active_condition:
                        for shadow_card in enemy.active_condition["分配暗影"]:
                            if "暗影" in shadow_card.rule_mark:
                                shadow_card.card_order = ["弃除暗影", 0, 0, False, 0, 0]
                            else:
                                self.main_game.card_estimate(enemy)[enemy].remove(shadow_card)
                                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, shadow_card)
                                else:
                                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [shadow_card]
                        enemy.active_condition.pop("分配暗影")
                        enemy.update_mask()
                self.current_phase = -1
                self.main_game.information = [0, "将要进入恢复阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 55:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.current_phase = 6
                self.main_game.information = [0, "进入恢复阶段后", "order"]
                self.reset_cards = []
                for card in self.main_game.hand_area.card_group:
                    if "已横置" in card.active_condition:
                        self.reset_cards.append(card)
                    if self.main_game.hand_area.card_group[card]:
                        for affiliated in self.main_game.hand_area.card_group[card]:
                            if "已横置" in affiliated.active_condition:
                                self.reset_cards.append(affiliated)
                for card in self.main_game.role_area.card_group:
                    if "已横置" in card.active_condition:
                        self.reset_cards.append(card)
                    if self.main_game.role_area.card_group[card]:
                        for affiliated in self.main_game.role_area.card_group[card]:
                            if "已横置" in affiliated.active_condition:
                                self.reset_cards.append(affiliated)
                for card in self.main_game.clash_area.card_group:
                    if "已横置" in card.active_condition:
                        self.reset_cards.append(card)
                    if self.main_game.clash_area.card_group[card]:
                        for affiliated in self.main_game.clash_area.card_group[card]:
                            if "已横置" in affiliated.active_condition:
                                self.reset_cards.append(affiliated)
                for card in self.main_game.scenario_area.card_group:
                    if "已横置" in card.active_condition:
                        self.reset_cards.append(card)
                    if self.main_game.scenario_area.card_group[card]:
                        for affiliated in self.main_game.scenario_area.card_group[card]:
                            if "已横置" in affiliated.active_condition:
                                self.reset_cards.append(affiliated)
                for card in self.main_game.task_area.region_card:
                    if "已横置" in card.active_condition:
                        self.reset_cards.append(card)
                    if self.main_game.task_area.region_card[card]:
                        for affiliated in self.main_game.task_area.region_card[card]:
                            if "已横置" in affiliated.active_condition:
                                self.reset_cards.append(affiliated)
                self.order[3] = True
                self.order[4] = 0
                self.order[5] = 0
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 56:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information and self.order[3]:
                if self.order[5]:
                    if hasattr(self, "reset_cards") and self.reset_cards:
                        self.reset_cards.pop(0)
                    self.order[4] += 1
                    self.order[5] -= 1
                elif self.order[4] % 2:
                    if hasattr(self, "reset_cards") and self.reset_cards:
                        if "已横置" in self.reset_cards[0].active_condition:
                            self.reset_cards[0].active_condition.pop("已横置")
                            self.reset_cards[0].update_mask()
                            self.main_game.information = [0, self.reset_cards[0].card_type + "卡牌重置后", "order",
                                                          self.reset_cards[0]]
                        self.reset_cards.pop(0)
                    self.order[4] += 1
                else:
                    if hasattr(self, "reset_cards"):
                        if self.reset_cards:
                            self.main_game.information = [0, self.reset_cards[0].card_type + "卡牌将要重置", "order",
                                                          self.reset_cards[0]]
                            self.order[4] += 1
                            return
                    self.order[3] = False
                    self.order[4] = 0
                    self.order[5] = 0
                    self.order[1] += 1
        elif self.order[0] and self.order[1] == 57:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "reset_cards"):
                    del self.reset_cards
                self.main_game.information = [0, "玩家将要上升威胁等级", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 58:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                self.threat_value += 1
                self.main_game.information = [0, "玩家上升威胁等级后", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 59:
            if self.order[2]:
                self.order[1] += 1
                self.order[2] -= 1
            elif not self.main_game.information:
                for card in self.main_game.clash_area.card_group:
                    if "已攻击" in card.active_condition:
                        card.active_condition.pop("已攻击")
                    if "已防御" in card.active_condition:
                        card.active_condition.pop("已防御")
                    card.update_mask()
                for card in self.main_game.scenario_area.card_group:
                    if "已攻击" in card.active_condition:
                        card.active_condition.pop("已攻击")
                    if "已防御" in card.active_condition:
                        card.active_condition.pop("已防御")
                    card.update_mask()
                self.main_game.information = [0, "将要离开恢复阶段", "order"]
                self.order[1] += 1
        elif self.order[0] and self.order[1] == 60:
            if self.order[2]:
                self.order[1] = 3
                self.order[2] -= 1
                self.round_number += 1
            elif not self.main_game.information:
                self.round_number += 1
                self.current_phase = -1
                self.main_game.information = [0, "将要进入资源阶段", "order"]
                self.order[1] = 3


# 任务卡牌区
class Task_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = self.height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topright = (
            main_game.settings.screen_width - main_game.settings.screen_width // main_game.settings.area_width_spacing,
            main_game.settings.screen_height // main_game.settings.area_height_spacing)

        self.task_deck = None  # 引用任务卡牌区按顺序摆放的所有任务卡
        self.task_number = None  # 当前任务卡在task_deck的索引，[0]为第一个任务，[1]为第二个任务，以此类推...
        self.region_card = {}  # 当前激活的地区卡牌(其上可能有附属卡所以用字典储存)

    # 初始化当前任务索引
    def initialize_task_index(self):
        task_index = []
        for (num, task) in enumerate(self.task_deck):
            if task.card_number == 1:
                task_index.append(num)
        self.task_number = task_index[self.main_game.xuanxiang // 10 % 10 - 1]

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        if self.task_deck:
            # 绘制任务卡牌图像
            task_card_image = pygame.transform.scale(self.task_deck[self.task_number].card_image, (self.width,
                                                                                                   self.width *
                                                                                                   self.main_game.settings.original_card_size[
                                                                                                       0] //
                                                                                                   self.main_game.settings.original_card_size[
                                                                                                       1]))
            task_card_image_rect = task_card_image.get_rect(center=self.rect.center)
            self.main_game.screen.blit(task_card_image, task_card_image_rect)
            # 绘制任务卡牌数值蒙板
            task_card_image_mask = pygame.transform.scale(self.task_deck[self.task_number].card_image_mask, (self.width,
                                                                                                             self.width *
                                                                                                             self.main_game.settings.original_card_size[
                                                                                                                 0] //
                                                                                                             self.main_game.settings.original_card_size[
                                                                                                                 1]))
            self.main_game.screen.blit(task_card_image_mask, task_card_image_rect)
            # 如果鼠标右击了任务牌，将其载入卡牌展示器展示
            if self.main_game.mouse_rightclick and task_card_image_rect.collidepoint(self.main_game.mouse_rightclick):
                self.main_game.card_exhibition(self.task_deck[self.task_number])
                self.main_game.mouse_rightclick = None
            # 绘制激活的地区卡
            area_draw(self.region_card, self.width, self.height, self.rect, self.main_game)

    # 运行每张卡牌的card_listening
    def cards_listening(self):
        self.task_deck[self.task_number].card_listening()
        for card in self.region_card.copy():
            card.card_listening()
            if card in self.region_card and self.region_card[card]:
                for card_affiliated in self.region_card[card].copy():
                    card_affiliated.card_listening()

    # 运行每张卡牌的run_card_order
    def run_cards_order(self):
        if self.task_deck[self.task_number].card_order[0] and not self.task_deck[self.task_number].order_exception:
            self.main_game.run_order = False
        self.task_deck[self.task_number].run_card_order()
        for card in self.region_card.copy():
            if card.card_order[0] and not card.order_exception:
                self.main_game.run_order = False
            card.run_card_order()
            if card in self.region_card and self.region_card[card]:
                for card_affiliated in self.region_card[card].copy():
                    if card_affiliated.card_order[0] and not card_affiliated.order_exception:
                        self.main_game.run_order = False
                    card_affiliated.run_card_order()


# 遭遇牌组区
class Encounter_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = self.height * main_game.settings.original_card_size[0] // \
                     main_game.settings.original_card_size[1]
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topright = (
            main_game.settings.screen_width - main_game.settings.screen_width // main_game.settings.area_width_spacing,
            3 * main_game.settings.screen_height // main_game.settings.area_height_spacing + self.height)

        self.number_font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                            self.height // 3)  # 遭遇卡背上显示剩余卡牌数的字体
        self.encounter_deck = None  # 遭遇牌组
        self.encounter_affiliated = None  # 遭遇牌组的附属牌

    # 噩梦模式下移除标准遭遇中不需要的卡牌
    def nightmare_remove(self, yichu):
        for name in yichu:
            for num in range(yichu[name]):
                for card in self.encounter_deck.copy():
                    if card.card_name == name and (card.card_amount[0] or card.card_amount[1]):
                        self.encounter_deck.remove(card)
                        break

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        select_card_rect = None  # 如果当前选中卡牌在这个附属牌区域里，记录其rect留到最后再画
        # 绘制遭遇牌组的附属牌
        if self.encounter_affiliated:
            cards_affiliated_len = len(self.encounter_affiliated)
            cards_affiliated = self.encounter_affiliated
            number = 0
            while number <= cards_affiliated_len:
                if number:
                    hand_card_affiliated_image_1 = hand_card_affiliated_image_2
                    hand_card_affiliated_image_rect_1 = hand_card_affiliated_image_rect_2
                if number != cards_affiliated_len:
                    hand_card_affiliated_image_2 = pygame.transform.scale(cards_affiliated[number].card_image,
                                                                          self.rect.size)
                    hand_card_affiliated_image_rect_2 = hand_card_affiliated_image_2.get_rect(x=self.rect.x)
                    hand_card_affiliated_image_rect_2.y = self.rect.y - (
                            cards_affiliated_len - number) * self.height // self.main_game.settings.card_enhance_scale
                if number:
                    # 设置附属牌的可选区域
                    if number != cards_affiliated_len:
                        hand_card_affiliated_image_rect_1.height = hand_card_affiliated_image_rect_2.y - hand_card_affiliated_image_rect_1.y
                    else:
                        hand_card_affiliated_image_rect_1.height = self.rect.y - hand_card_affiliated_image_rect_1.y
                    # 如果鼠标单击了这张卡牌，设置其为选中卡牌
                    if self.main_game.mouse_click and hand_card_affiliated_image_rect_1.collidepoint(
                            self.main_game.mouse_click):
                        self.main_game.select_card = cards_affiliated[number - 1]
                        self.main_game.mouse_click = None
                    # 如果鼠标右击了这张卡牌，将此卡牌载入卡牌展示器展示
                    if self.main_game.mouse_rightclick and hand_card_affiliated_image_rect_1.collidepoint(
                            self.main_game.mouse_rightclick):
                        self.main_game.card_exhibition(cards_affiliated[number - 1])
                        self.main_game.mouse_rightclick = None
                    # 鼠标悬停可选区域上时让附属牌提高显示
                    if hand_card_affiliated_image_rect_1.collidepoint(self.main_game.mouse_pos) and cards_affiliated[
                        number - 1] != self.main_game.select_card:
                        hand_card_affiliated_image_rect_1.y -= self.height // self.main_game.settings.card_enhance_scale

                    # 绘制附属牌图像和其数值蒙板
                    if cards_affiliated[number - 1] != self.main_game.select_card:
                        self.main_game.screen.blit(hand_card_affiliated_image_1, hand_card_affiliated_image_rect_1)
                        hand_card_affiliated_image_mask = pygame.transform.scale(
                            cards_affiliated[number - 1].card_image_mask, self.rect.size)
                        self.main_game.screen.blit(hand_card_affiliated_image_mask, hand_card_affiliated_image_rect_1)
                    else:
                        select_card_rect = hand_card_affiliated_image_rect_1
                number += 1
        # END
        # 画遭遇卡组的背景图案和剩余卡牌数
        if self.encounter_deck:
            encounter_card_image = pygame.transform.scale(self.main_game.computer_card_image, self.rect.size)
            encounter_card_image_rect = encounter_card_image.get_rect(center=self.rect.center)
            self.main_game.screen.blit(encounter_card_image, encounter_card_image_rect)
            number_image = self.number_font.render(str(len(self.encounter_deck)), True,
                                                   self.main_game.settings.card_mask_font_color3,
                                                   (128, 128, 128)).convert()
            number_image.set_colorkey((128, 128, 128))
            number_image_rect = number_image.get_rect(center=self.rect.center)
            self.main_game.screen.blit(number_image, number_image_rect)
        # END
        # 最后画选中卡以使其处于所有卡牌上方
        if select_card_rect:
            select_card_image = pygame.transform.scale(self.main_game.select_card.card_image, self.rect.size)
            self.main_game.screen.blit(select_card_image, select_card_rect)
            select_card_image_mask = pygame.transform.scale(self.main_game.select_card.card_image_mask, self.rect.size)
            self.main_game.screen.blit(select_card_image_mask, select_card_rect)

    # 运行每张卡牌的card_listening
    def cards_listening(self):
        if self.encounter_affiliated:
            for card in self.encounter_affiliated.copy():
                card.card_listening()

    # 运行每张卡牌的run_card_order
    def run_cards_order(self):
        if self.encounter_affiliated:
            for card in self.encounter_affiliated.copy():
                if card.card_order[0] and not card.order_exception:
                    self.main_game.run_order = False
                card.run_card_order()


# 玩家牌组区
class Playerdeck_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = self.height * main_game.settings.original_card_size[0] // \
                     main_game.settings.original_card_size[1]
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottomright = (
            main_game.settings.screen_width - main_game.settings.screen_width // main_game.settings.area_width_spacing,
            main_game.settings.screen_height - main_game.settings.screen_height // main_game.settings.area_height_spacing)

        self.number_font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                            self.height // 3)  # 玩家卡背上显示剩余卡牌数的字体

        self.player_deck = None  # 玩家牌组
        self.player_affiliated = None  # 玩家牌组的附属牌

    # 检查player_deck中是否放入了三张以上的重复卡牌，返回True表示是，False表示没有
    def card_repeat_detection(self):
        for (num, card) in enumerate(self.player_deck):
            number = num + 1
            repeat = 0
            while number < len(self.player_deck):
                if card.card_name == self.player_deck[number].card_name:
                    repeat += 1
                    if repeat > 2:
                        return True
                number += 1
        return False

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        select_card_rect = None  # 如果当前选中卡牌在这个附属牌区域里，记录其rect留到最后再画
        # 绘制遭遇牌组的附属牌
        if self.player_affiliated:
            cards_affiliated_len = len(self.player_affiliated)
            cards_affiliated = self.player_affiliated
            number = 0
            while number <= cards_affiliated_len:
                if number:
                    hand_card_affiliated_image_1 = hand_card_affiliated_image_2
                    hand_card_affiliated_image_rect_1 = hand_card_affiliated_image_rect_2
                if number != cards_affiliated_len:
                    hand_card_affiliated_image_2 = pygame.transform.scale(cards_affiliated[number].card_image,
                                                                          self.rect.size)
                    hand_card_affiliated_image_rect_2 = hand_card_affiliated_image_2.get_rect(x=self.rect.x)
                    hand_card_affiliated_image_rect_2.y = self.rect.y - (
                            cards_affiliated_len - number) * self.height // self.main_game.settings.card_enhance_scale
                if number:
                    # 设置附属牌的可选区域
                    if number != cards_affiliated_len:
                        hand_card_affiliated_image_rect_1.height = hand_card_affiliated_image_rect_2.y - hand_card_affiliated_image_rect_1.y
                    else:
                        hand_card_affiliated_image_rect_1.height = self.rect.y - hand_card_affiliated_image_rect_1.y
                    # 如果鼠标单击了这张卡牌，设置其为选中卡牌
                    if self.main_game.mouse_click and hand_card_affiliated_image_rect_1.collidepoint(
                            self.main_game.mouse_click):
                        self.main_game.select_card = cards_affiliated[number - 1]
                        self.main_game.mouse_click = None
                    # 如果鼠标右击了这张卡牌，将此卡牌载入卡牌展示器展示
                    if self.main_game.mouse_rightclick and hand_card_affiliated_image_rect_1.collidepoint(
                            self.main_game.mouse_rightclick):
                        self.main_game.card_exhibition(cards_affiliated[number - 1])
                        self.main_game.mouse_rightclick = None
                    # 鼠标悬停可选区域上时让附属牌提高显示
                    if hand_card_affiliated_image_rect_1.collidepoint(self.main_game.mouse_pos) and cards_affiliated[
                        number - 1] != self.main_game.select_card:
                        hand_card_affiliated_image_rect_1.y -= self.height // self.main_game.settings.card_enhance_scale

                    # 绘制附属牌图像和其数值蒙板
                    if cards_affiliated[number - 1] != self.main_game.select_card:
                        self.main_game.screen.blit(hand_card_affiliated_image_1, hand_card_affiliated_image_rect_1)
                        hand_card_affiliated_image_mask = pygame.transform.scale(
                            cards_affiliated[number - 1].card_image_mask, self.rect.size)
                        self.main_game.screen.blit(hand_card_affiliated_image_mask, hand_card_affiliated_image_rect_1)
                    else:
                        select_card_rect = hand_card_affiliated_image_rect_1
                number += 1
        # END
        # 画遭遇卡组的背景图案和剩余卡牌数
        if self.player_deck:
            playerdeck_card_image = pygame.transform.scale(self.main_game.player_card_image, self.rect.size)
            playerdeck_card_image_rect = playerdeck_card_image.get_rect(center=self.rect.center)
            self.main_game.screen.blit(playerdeck_card_image, playerdeck_card_image_rect)
            number_image = self.number_font.render(str(len(self.player_deck)), True,
                                                   self.main_game.settings.card_mask_font_color3,
                                                   (128, 128, 128)).convert()
            number_image.set_colorkey((128, 128, 128))
            number_image_rect = number_image.get_rect(center=self.rect.center)
            self.main_game.screen.blit(number_image, number_image_rect)
        # END
        # 最后画选中卡以使其处于所有卡牌上方
        if select_card_rect:
            select_card_image = pygame.transform.scale(self.main_game.select_card.card_image, self.rect.size)
            self.main_game.screen.blit(select_card_image, select_card_rect)
            select_card_image_mask = pygame.transform.scale(self.main_game.select_card.card_image_mask, self.rect.size)
            self.main_game.screen.blit(select_card_image_mask, select_card_rect)

    # 运行每张卡牌的card_listening
    def cards_listening(self):
        if self.player_affiliated:
            for card in self.player_affiliated.copy():
                card.card_listening()

    # 运行每张卡牌的run_card_order
    def run_cards_order(self):
        if self.player_affiliated:
            for card in self.player_affiliated.copy():
                if card.card_order[0] and not card.order_exception:
                    self.main_game.run_order = False
                card.run_card_order()


# 遭遇弃牌堆区
class Encounterdiscard_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = self.height * main_game.settings.original_card_size[0] // \
                     main_game.settings.original_card_size[1]
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (
            main_game.settings.screen_width // main_game.settings.area_width_spacing,
            3 * main_game.settings.screen_height // main_game.settings.area_height_spacing + self.height)

        self.number_font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                            self.height // 3)  # 遭遇弃牌堆上显示有多少张的数字的字体
        self.encounterdiscard_deck = None  # 遭遇弃牌堆

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        if self.encounterdiscard_deck:
            encounterdiscard_deck_image = pygame.transform.scale(self.encounterdiscard_deck[0].card_image,
                                                                 self.rect.size)
            encounterdiscard_deck_image_rect = encounterdiscard_deck_image.get_rect(center=self.rect.center)
            # 如果鼠标右击了最上面一张卡牌，将此卡牌载入卡牌展示器展示
            if self.main_game.mouse_rightclick and encounterdiscard_deck_image_rect.collidepoint(
                    self.main_game.mouse_rightclick):
                self.main_game.card_exhibition(self.encounterdiscard_deck[0])
                self.main_game.mouse_rightclick = None
            self.main_game.screen.blit(encounterdiscard_deck_image, encounterdiscard_deck_image_rect)
            encounterdiscard_deck_image_mask = pygame.transform.scale(self.encounterdiscard_deck[0].card_image_mask,
                                                                      self.rect.size)
            self.main_game.screen.blit(encounterdiscard_deck_image_mask, encounterdiscard_deck_image_rect)
            number_image = self.number_font.render(str(len(self.encounterdiscard_deck)), True,
                                                   self.main_game.settings.card_mask_font_color3,
                                                   (128, 128, 128)).convert()
            number_image.set_colorkey((128, 128, 128))
            number_image_rect = number_image.get_rect(center=self.rect.center)
            self.main_game.screen.blit(number_image, number_image_rect)

    # 运行每张卡牌的card_listening
    def cards_listening(self):
        pass

    # 运行每张卡牌的run_card_order
    def run_cards_order(self):
        pass


# 玩家弃牌堆区
class Playerdiscard_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = self.height * main_game.settings.original_card_size[0] // \
                     main_game.settings.original_card_size[1]
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottomleft = (
            main_game.settings.screen_width // main_game.settings.area_width_spacing,
            main_game.settings.screen_height - main_game.settings.screen_height // main_game.settings.area_height_spacing)

        self.number_font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                            self.height // 3)  # 玩家弃牌堆上显示有多少张的数字的字体
        self.playerdiscard_deck = None  # 玩家弃牌堆

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        if self.playerdiscard_deck:
            playerdiscard_deck_image = pygame.transform.scale(self.playerdiscard_deck[0].card_image,
                                                              self.rect.size)
            playerdiscard_deck_image_rect = playerdiscard_deck_image.get_rect(center=self.rect.center)
            # 如果鼠标右击了最上面一张卡牌，将此卡牌载入卡牌展示器展示
            if self.main_game.mouse_rightclick and playerdiscard_deck_image_rect.collidepoint(
                    self.main_game.mouse_rightclick):
                self.main_game.card_exhibition(self.playerdiscard_deck[0])
                self.main_game.mouse_rightclick = None
            self.main_game.screen.blit(playerdiscard_deck_image, playerdiscard_deck_image_rect)
            playerdiscard_deck_image_mask = pygame.transform.scale(self.playerdiscard_deck[0].card_image_mask,
                                                                   self.rect.size)
            self.main_game.screen.blit(playerdiscard_deck_image_mask, playerdiscard_deck_image_rect)
            number_image = self.number_font.render(str(len(self.playerdiscard_deck)), True,
                                                   self.main_game.settings.card_mask_font_color3,
                                                   (128, 128, 128)).convert()
            number_image.set_colorkey((128, 128, 128))
            number_image_rect = number_image.get_rect(center=self.rect.center)
            self.main_game.screen.blit(number_image, number_image_rect)

    # 运行每张卡牌的card_listening
    def cards_listening(self):
        pass

    # 运行每张卡牌的run_card_order
    def run_cards_order(self):
        pass


# 场景区
class Scenario_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = main_game.settings.screen_width - 2 * self.height - 6 * main_game.settings.screen_width // main_game.settings.area_width_spacing
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midtop = (main_game.settings.screen_width // 2,
                            main_game.settings.screen_height // main_game.settings.area_height_spacing)

        self.card_group = {}  # 用于放置区域中的所有卡牌对象

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        area_draw(self.card_group, self.width, self.height, self.rect, self.main_game)

    # 运行每张卡牌的card_listening
    def cards_listening(self):
        for card in self.card_group.copy():
            card.card_listening()
            if card in self.card_group and self.card_group[card]:
                for card_affiliated in self.card_group[card].copy():
                    card_affiliated.card_listening()

    # 运行每张卡牌的run_card_order
    def run_cards_order(self):
        for card in self.card_group.copy():
            if card.card_order[0] and not card.order_exception:
                self.main_game.run_order = False
            card.run_card_order()
            if card in self.card_group and self.card_group[card]:
                for card_affiliated in self.card_group[card].copy():
                    if card_affiliated.card_order[0] and not card_affiliated.order_exception:
                        self.main_game.run_order = False
                    card_affiliated.run_card_order()


# 交锋区
class Clash_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = main_game.settings.screen_width - 2 * (
                self.height * main_game.settings.original_card_size[0] // main_game.settings.original_card_size[
            1]) - 6 * main_game.settings.screen_width // main_game.settings.area_width_spacing
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midtop = (main_game.settings.screen_width // 2,
                            self.height + 3 * main_game.settings.screen_height // main_game.settings.area_height_spacing)

        self.card_group = {}  # 用于放置区域中的所有卡牌对象

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        area_draw(self.card_group, self.width, self.height, self.rect, self.main_game)

    # 运行每张卡牌的card_listening
    def cards_listening(self):
        for card in self.card_group.copy():
            card.card_listening()
            if card in self.card_group and self.card_group[card]:
                for card_affiliated in self.card_group[card].copy():
                    card_affiliated.card_listening()

    # 运行每张卡牌的run_card_order
    def run_cards_order(self):
        for card in self.card_group.copy():
            if card.card_order[0] and not card.order_exception:
                self.main_game.run_order = False
            card.run_card_order()
            if card in self.card_group and self.card_group[card]:
                for card_affiliated in self.card_group[card].copy():
                    if card_affiliated.card_order[0] and not card_affiliated.order_exception:
                        self.main_game.run_order = False
                    card_affiliated.run_card_order()


# 英雄、盟友、附属、事件牌放置区
class Role_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = main_game.settings.screen_width - 2 * main_game.settings.screen_width // main_game.settings.area_width_spacing
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = (main_game.settings.screen_width // 2,
                               main_game.settings.screen_height - 3 * main_game.settings.screen_height // main_game.settings.area_height_spacing - self.height)

        self.hero_group = None  # 玩家的英雄牌
        self.card_group = {}  # 用于放置区域中的所有卡牌对象

    # 检查hero_group中是否放入了重复的独有英雄，返回True表示有，False表示没有
    def hero_repeat_detection(self):
        for (num, hero) in enumerate(self.hero_group):
            number = num + 1
            while number < len(self.hero_group):
                if hero.unique_symbol and hero.card_name == self.hero_group[number].card_name:
                    return True
                number += 1
        return False

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        area_draw(self.card_group, self.width, self.height, self.rect, self.main_game)

    # 运行每张卡牌的card_listening
    def cards_listening(self):
        for card in self.card_group.copy():
            card.card_listening()
            if card in self.card_group and self.card_group[card]:
                for card_affiliated in self.card_group[card].copy():
                    card_affiliated.card_listening()

    # 运行每张卡牌的run_card_order
    def run_cards_order(self):
        for card in self.card_group.copy():
            if card.card_order[0] and not card.order_exception:
                self.main_game.run_order = False
            card.run_card_order()
            if card in self.card_group and self.card_group[card]:
                for card_affiliated in self.card_group[card].copy():
                    if card_affiliated.card_order[0] and not card_affiliated.order_exception:
                        self.main_game.run_order = False
                    card_affiliated.run_card_order()


# 手牌区
class Hand_Area:
    def __init__(self, main_game):
        self.main_game = main_game
        self.height = round(main_game.settings.screen_height * (
                main_game.settings.area_height_spacing - 8) / 4 / main_game.settings.area_height_spacing)
        self.width = main_game.settings.screen_width - 2 * (
                self.height * main_game.settings.original_card_size[0] // main_game.settings.original_card_size[
            1]) - 6 * main_game.settings.screen_width // main_game.settings.area_width_spacing
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = (main_game.settings.screen_width // 2,
                               main_game.settings.screen_height - main_game.settings.screen_height // main_game.settings.area_height_spacing)

        self.card_group = {}  # 用于放置手牌中的所有卡牌对象

    # 在屏幕窗口对象上逐帧绘制的方法
    def display_draw(self):
        area_draw(self.card_group, self.width, self.height, self.rect, self.main_game)

    # 运行每张卡牌的card_listening
    def cards_listening(self):
        for card in self.card_group.copy():
            card.card_listening()
            if card in self.card_group and self.card_group[card]:
                for card_affiliated in self.card_group[card].copy():
                    card_affiliated.card_listening()

    # 运行每张卡牌的run_card_order
    def run_cards_order(self):
        for card in self.card_group.copy():
            if card.card_order[0] and not card.order_exception:
                self.main_game.run_order = False
            card.run_card_order()
            if card in self.card_group and self.card_group[card]:
                for card_affiliated in self.card_group[card].copy():
                    if card_affiliated.card_order[0] and not card_affiliated.order_exception:
                        self.main_game.run_order = False
                    card_affiliated.run_card_order()
