from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "奋起战斗.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "奋起战斗"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = "X"  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "精神"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "事件"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：在任一玩家的弃牌堆中选择一名印刷费用为X的盟友。将该盟友放置进场并由你控制。（所选盟友可隶属任意影响力派系。）"

        # 剧情描述的斜体文字
        self.describe_text = "“...放心地继续战斗。” ——波罗莫，《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.select_card = None
        self.temporary_card_cost = None

    # 执行这张卡片的运行效果
    def run_card_order(self):
        if self.card_order[0] == "选定X费" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                point = 0
                heros = []
                for hero in self.main_game.role_area.hero_group:
                    if self.faction_symbol == hero.resource_symbol or "资源符+" in hero.active_condition and self.faction_symbol in \
                            hero.active_condition["资源符+"]:
                        heros.append(hero)
                for hero in heros:
                    point += hero.active_resource
                if len(self.active_card_cost) > 2 and self.active_card_cost[1] == "-":
                    point += int(self.active_card_cost[2:])
                elif len(self.active_card_cost) > 2 and self.active_card_cost[1] == "+":
                    point -= int(self.active_card_cost[2:])
                allys = []
                if heros and self.main_game.playerdiscard_area.playerdiscard_deck:
                    for ally in self.main_game.playerdiscard_area.playerdiscard_deck:
                        if ally.card_type == "盟友" and not self.main_game.unique_detection(ally) and hasattr(ally,
                                                                                                            "faction_symbol") and ally.faction_symbol != "中立" and (
                                type(ally.active_card_cost) != int or point >= ally.active_card_cost):
                            allys.append(ally)
                if allys:
                    self.select_card = self.main_game.card_select(allys)
                    num = self.select_card.card_cost
                    if len(self.active_card_cost) > 2 and self.active_card_cost[1] == "-":
                        num -= int(self.active_card_cost[2:])
                        if num < 0:
                            num = 0
                    elif len(self.active_card_cost) > 2 and self.active_card_cost[1] == "+":
                        num += int(self.active_card_cost[2:])
                    self.temporary_card_cost = self.active_card_cost
                    self.active_card_cost = num
                    self.update_mask()
                    self.card_order = ["打出", 0, 0, False, 0, 0]
                else:
                    self.card_order[0] = None
        elif self.card_order[0] != "选定X费":
            super().run_card_order()
        if self.card_order[0] == "打出事件后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if self.select_card and self.select_card in self.main_game.playerdiscard_area.playerdiscard_deck and not self.main_game.unique_detection(
                        self.select_card):
                    self.main_game.information = [0, "盟友卡牌将要放置进场", self, self.select_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.select_card and self.select_card in self.main_game.playerdiscard_area.playerdiscard_deck and not self.main_game.unique_detection(
                        self.select_card):
                    self.select_card.reset_card()
                    self.select_card.update_mask()
                    self.main_game.role_area.card_group[self.select_card] = None
                    self.main_game.playerdiscard_area.playerdiscard_deck.remove(self.select_card)
                    self.main_game.information = [0, "盟友卡牌放置进场后", self, self.select_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if self.temporary_card_cost:
                    self.active_card_cost = self.temporary_card_cost
                    self.temporary_card_cost = None
                    self.update_mask()
                self.select_card = None
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
