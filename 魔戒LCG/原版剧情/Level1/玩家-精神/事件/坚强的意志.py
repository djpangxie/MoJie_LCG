from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "坚强的意志.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "坚强的意志"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 0  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "精神"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("响应",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "事件"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "响应：在你探索到一个地区后，横置一名精神派系的角色，以放置2枚进度标记到该地区上。"

        # 剧情描述的斜体文字
        self.describe_text = "于是，亚拉冈领路，在他那坚强的意志力下，所有的登丹人和坐骑都跟着他一起进入。 ——《王者再临》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.region = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.main_game.information and self.main_game.information[1] == "地区卡牌激活后" and "免疫" not in \
                self.main_game.information[2].rule_mark and "响应后" not in self.active_condition:
            self.region = self.main_game.information[2]
            self.main_game.response_conflict = True
            self.card_order = ["响应", 0, 0, False, 0, 0]
            self.active_condition["响应后"] = None

    # 执行这张卡片的响应效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "响应" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif self.main_game.response_pause != True:
                self.main_game.response_pause = True
                point = 0
                heros = []
                for hero in self.main_game.role_area.hero_group:
                    if self.faction_symbol == hero.resource_symbol or "资源符+" in hero.active_condition and self.faction_symbol in \
                            hero.active_condition["资源符+"]:
                        heros.append(hero)
                for hero in heros:
                    point += hero.active_resource
                if heros and point >= self.active_card_cost and self.main_game.card_estimate(self.region) is not None:
                    self.main_game.button_option.import_button(str(self), (
                        ("响应-" + self.card_name, None), ("不响应-" + self.card_name, None)))
                    if self.main_game.button_option.option // 100000 == 1:
                        self.main_game.button_option.reset()
                        self.card_order = ["打出", 0, 0, False, 0, 0]
                    elif self.main_game.button_option.option // 100000 == 2:
                        self.main_game.button_option.reset()
                        self.card_order[1] += 1
                else:
                    self.main_game.button_option.reset()
                    self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.region = None
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                cards = []
                for card in self.main_game.role_area.card_group:
                    if (card.card_type == "英雄" and (
                            card.resource_symbol == "精神" or "资源符+" in card.active_condition and "精神" in
                            card.active_condition["资源符+"]) or card.card_type == "盟友" and (
                                card.faction_symbol == "精神" or "派系+" in card.active_condition and "精神" in
                                card.active_condition[
                                    "派系+"])) and "已横置" not in card.active_condition and "免疫" not in card.rule_mark:
                        cards.append(card)
                for card in self.main_game.clash_area.card_group:
                    if (card.card_type == "英雄" and (
                            card.resource_symbol == "精神" or "资源符+" in card.active_condition and "精神" in
                            card.active_condition["资源符+"]) or card.card_type == "盟友" and (
                                card.faction_symbol == "精神" or "派系+" in card.active_condition and "精神" in
                                card.active_condition[
                                    "派系+"])) and "已横置" not in card.active_condition and "免疫" not in card.rule_mark:
                        cards.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if (card.card_type == "英雄" and (
                            card.resource_symbol == "精神" or "资源符+" in card.active_condition and "精神" in
                            card.active_condition["资源符+"]) or card.card_type == "盟友" and (
                                card.faction_symbol == "精神" or "派系+" in card.active_condition and "精神" in
                                card.active_condition[
                                    "派系+"])) and "已横置" not in card.active_condition and "免疫" not in card.rule_mark:
                        cards.append(card)
                if cards:
                    self.select_card = self.main_game.card_select(cards)
                    self.main_game.information = [0, self.select_card.card_type + "卡牌将要横置", self, self.select_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "select_card") and "已横置" not in self.select_card.active_condition:
                    self.select_card.active_condition["已横置"] = None
                    self.select_card.update_mask()
                    self.main_game.information = [0, self.select_card.card_type + "卡牌横置后", self, self.select_card]
                    self.region.active_task_point -= 2
                    if self.region.active_task_point < 0:
                        self.region.active_task_point = 0
                    self.region.update_mask()
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if hasattr(self, "select_card"):
                    del self.select_card
                self.region = None
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
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
