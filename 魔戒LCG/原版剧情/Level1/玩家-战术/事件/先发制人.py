from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "先发制人.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "先发制人"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 1  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "战术"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "事件"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：横置一名你控制的角色，以立即宣告其为攻击者（并结算此次攻击）攻击任一合理的敌军目标。"

        # 剧情描述的斜体文字
        self.describe_text = "...他相信如果自己先发制人，只要伤害够大，或许可以不用发动接下来的攻击。 ——甘道夫，《双城奇谋》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._successful = False

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "打出事件后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                cards = []
                for card in self.main_game.role_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" not in card.active_condition and "免疫" not in card.rule_mark:
                        cards.append(card)
                for card in self.main_game.clash_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" not in card.active_condition and "免疫" not in card.rule_mark:
                        cards.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" not in card.active_condition and "免疫" not in card.rule_mark:
                        cards.append(card)
                if cards:
                    self.select_card = self.main_game.card_select(cards)
                    self.main_game.information = [0, self.select_card.card_type + "卡牌将要横置", self, self.select_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if hasattr(self, "select_card") and "已横置" not in self.select_card.active_condition:
                    self.select_card.active_condition["已横置"] = None
                    self.select_card.update_mask()
                    self.main_game.information = [0, self.select_card.card_type + "卡牌横置后", self, self.select_card]
                    self._successful = True
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if hasattr(self, "select_card") and self._successful:
                    enemys = []
                    for card in self.main_game.role_area.card_group:
                        if card.card_type == "敌军":
                            enemys.append(card)
                    for card in self.main_game.clash_area.card_group:
                        if card.card_type == "敌军":
                            enemys.append(card)
                    for card in self.main_game.scenario_area.card_group:
                        if card.card_type == "敌军":
                            enemys.append(card)
                    if enemys:
                        self.select_enemy = self.main_game.card_select(enemys)
                        self.main_game.information = [0, self.select_card.card_type + "卡牌将要宣告攻击", self.select_card,
                                                      self.select_enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if hasattr(self, "select_card") and self._successful and hasattr(self, "select_enemy"):
                    self.select_card.active_condition["宣告攻击"] = [self.select_enemy]
                    self.select_card.update_mask()
                    self.main_game.information = [0, self.select_card.card_type + "卡牌宣告攻击后", self.select_card,
                                                  self.select_enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if hasattr(self, "select_card") and self._successful and hasattr(self, "select_enemy"):
                    self.main_game.information = [0, self.select_card.card_type + "卡牌将要攻击", self.select_card,
                                                  self.select_enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 5:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "select_card") and self._successful and hasattr(self, "select_enemy"):
                    if self.select_card.active_attack_force > self.select_enemy.active_defense_force:
                        self.select_enemy.active_health_point -= self.select_card.active_attack_force - self.select_enemy.active_defense_force
                    if self.select_enemy.active_health_point < 0:
                        self.select_enemy.active_health_point = 0
                    self.select_card.active_condition.pop("宣告攻击")
                    self.select_card.update_mask()
                    self.select_enemy.update_mask()
                    self.main_game.information = [0, self.select_card.card_type + "卡牌攻击后", self.select_card,
                                                  self.select_enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 6:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if hasattr(self, "select_card"):
                    del self.select_card
                if hasattr(self, "select_enemy"):
                    del self.select_enemy
                self._successful = False
                our_affiliate = []
                enemy_affiliate = []
                if self.main_game.hand_area.card_group[self]:
                    for card in self.main_game.hand_area.card_group[self]:
                        if self.main_game.player_control(card):
                            our_affiliate.append(card)
                        else:
                            enemy_affiliate.append(card)
                self.main_game.hand_area.card_group.pop(self)
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    for card in our_affiliate:
                        self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, card)
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = [self]
                    self.main_game.playerdiscard_area.playerdiscard_deck.extend(our_affiliate)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    for card in enemy_affiliate:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, card)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = enemy_affiliate
                self.card_order = [None, 0, 0, None, 0, 0]
