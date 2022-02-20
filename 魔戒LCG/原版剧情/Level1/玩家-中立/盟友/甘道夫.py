from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "甘道夫.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "甘道夫"  # 卡牌的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 5  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "中立"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.willpower = 4  # 卡牌的意志力
        self.attack_force = 4  # 卡牌的攻击力
        self.defense_force = 4  # 卡牌的防御力
        self.health_point = 4  # 卡牌的生命值
        self.card_attribute = ("巫师",)  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("响应",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "盟友"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "在本回合结束时，从场中弃除甘道夫。\n响应：在甘道夫进场后，(选择其一):补三张卡牌，或对一个在场的敌军造成4点伤害，或你的威胁等级下降5点。"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.round_mark = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.main_game.information and "卡牌放置进场后" in self.main_game.information[
            1] and self.main_game.information[3] == self and "响应后" not in self.active_condition:
            self.main_game.response_conflict = True
            self.card_order = ["响应", 0, 0, False, 0, 0]
            self.active_condition["响应后"] = None
            self.round_mark = self.main_game.threat_area.round_number
        elif self.active_health_point > 0 and not self.main_game.information and self.round_mark is not None and self.main_game.threat_area.round_number != self.round_mark:
            if None is not self.main_game.card_estimate(self) is not self.main_game.hand_area.card_group:
                self.card_order = ["被弃除", 0, 0, False, 0, 0]
            self.round_mark = None

    # 执行这张卡片的响应效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "响应" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif self.main_game.response_pause != True:
                self.main_game.response_pause = True
                self.main_game.button_option.import_button(str(self), (
                    ("响应-" + self.card_name, None), ("不响应-" + self.card_name, None)))
                if self.main_game.button_option.option // 100000 == 1:
                    self.card_order[1] += 1
                    self.main_game.button_option.reset()
                elif self.main_game.button_option.option // 100000 == 2:
                    self.card_order[1] = 7
                    self.main_game.button_option.reset()
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] = 7
            elif self.main_game.response_pause != True:
                self.main_game.response_pause = True
                self.main_game.button_option.import_button(str(self),
                                                           (("补三张卡牌", None), ("对敌军造成4点伤害", None), ("降低5点威胁等级", None)))
                if self.main_game.button_option.option // 100000 == 1:
                    self.card_order[3] = True
                    self.card_order[4] = 0
                    self.card_order[5] = 0
                    self.card_order[1] += 1
                    self.main_game.button_option.reset()
                elif self.main_game.button_option.option // 100000 == 2:
                    enemys = []
                    for card in self.main_game.role_area.card_group:
                        if card.card_type == "敌军" and "免疫" not in card.rule_mark:
                            enemys.append(card)
                    for card in self.main_game.clash_area.card_group:
                        if card.card_type == "敌军" and "免疫" not in card.rule_mark:
                            enemys.append(card)
                    for card in self.main_game.scenario_area.card_group:
                        if card.card_type == "敌军" and "免疫" not in card.rule_mark:
                            enemys.append(card)
                    if enemys:
                        self.select_enemy = self.main_game.card_select(enemys)
                        self.main_game.information = [0, "盟友卡牌将要攻击", self, self.select_enemy]
                        self.card_order[1] = 4
                    else:
                        self.card_order[1] = 7
                    self.main_game.button_option.reset()
                elif self.main_game.button_option.option // 100000 == 3:
                    self.main_game.information = [0, "玩家将要下降威胁等级", self]
                    self.card_order[1] = 6
                    self.main_game.button_option.reset()
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information and self.card_order[3]:
                if self.card_order[5]:
                    self.card_order[4] += 1
                    self.card_order[5] -= 1
                elif self.card_order[4] % 2:
                    if self.main_game.playerdeck_area.player_deck:
                        card = self.main_game.playerdeck_area.player_deck.pop(0)
                        self.main_game.hand_area.card_group[card] = None
                        self.main_game.information = [0, "玩家补卡后", self, card]
                    self.card_order[4] += 1
                else:
                    if self.card_order[4] < 5 and self.main_game.playerdeck_area.player_deck:
                        self.main_game.information = [0, "玩家将要补卡", self]
                        self.card_order[4] += 1
                    else:
                        self.card_order[3] = False
                        self.card_order[4] = 0
                        self.card_order[5] = 0
                        self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 3:
            self.card_order[1] = 7
        elif self.card_order[0] == "响应" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "select_enemy"):
                    self.select_enemy.active_health_point -= 4
                    if self.select_enemy.active_health_point < 0:
                        self.select_enemy.active_health_point = 0
                    self.select_enemy.update_mask()
                    self.main_game.information = [0, "盟友卡牌攻击后", self, self.select_enemy]
                    del self.select_enemy
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 5:
            self.card_order[1] = 7
        elif self.card_order[0] == "响应" and self.card_order[1] == 6:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.threat_area.threat_value -= 5
                if self.main_game.threat_area.threat_value < 0:
                    self.main_game.threat_area.threat_value = 0
                self.main_game.information = [0, "玩家下降威胁等级后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 7:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
