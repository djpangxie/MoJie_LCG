from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "保持警惕.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "保持警惕"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 1  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "领导"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "事件"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：选择并重置一张盟友牌。"

        # 剧情描述的斜体文字
        self.describe_text = "...不管是这条路或是任何其他的道路，都已经不再绝对安全了。要刚强胆壮！ ——《王者再临》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "打出事件后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                allys = []
                for card in self.main_game.hand_area.card_group:
                    if card.card_type == "盟友" and "已横置" in card.active_condition and "免疫" not in card.rule_mark:
                        allys.append(card)
                for card in self.main_game.role_area.card_group:
                    if card.card_type == "盟友" and "已横置" in card.active_condition and "免疫" not in card.rule_mark:
                        allys.append(card)
                for card in self.main_game.clash_area.card_group:
                    if card.card_type == "盟友" and "已横置" in card.active_condition and "免疫" not in card.rule_mark:
                        allys.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "盟友" and "已横置" in card.active_condition and "免疫" not in card.rule_mark:
                        allys.append(card)
                if allys:
                    self.select_ally = self.main_game.card_select(allys)
                    self.main_game.information = [0, "盟友卡牌将要重置", self, self.select_ally]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "select_ally") and "已横置" in self.select_ally.active_condition:
                    self.select_ally.active_condition.pop("已横置")
                    self.select_ally.update_mask()
                    self.main_game.information = [0, "盟友卡牌重置后", self, self.select_ally]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if hasattr(self, "select_ally"):
                    del self.select_ally
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
