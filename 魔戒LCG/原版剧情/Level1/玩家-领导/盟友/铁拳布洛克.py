from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "铁拳布洛克.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "铁拳布洛克"  # 卡牌的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 6  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "领导"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.willpower = 2  # 卡牌的意志力
        self.attack_force = 2  # 卡牌的攻击力
        self.defense_force = 1  # 卡牌的防御力
        self.health_point = 4  # 卡牌的生命值
        self.card_attribute = ("矮人", "战士")  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("响应",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "盟友"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "响应：在你控制的一名矮人英雄离场后，将铁拳布洛克从你的手牌中放置进场。"

        # 剧情描述的斜体文字
        self.describe_text = "...为了复仇和争取属于自己的利益，矮人们一向不惜一切代价。 ——《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.main_game.information and self.main_game.information[
            1] == "英雄卡牌离场后" and "矮人" in self.main_game.information[
            2].card_attribute and "响应后" not in self.active_condition and self in self.main_game.hand_area.card_group:
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
                self.main_game.button_option.import_button(str(self), (
                    ("响应-" + self.card_name, None), ("不响应-" + self.card_name, None)))
                if self.main_game.button_option.option // 100000 == 1:
                    self.main_game.button_option.reset()
                    self.card_order[1] += 1
                elif self.main_game.button_option.option // 100000 == 2:
                    self.main_game.button_option.reset()
                    self.card_order[1] += 3
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if self in self.main_game.hand_area.card_group and not self.main_game.unique_detection(self):
                    self.main_game.information = [0, self.card_type + "卡牌将要放置进场", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if self in self.main_game.hand_area.card_group and not self.main_game.unique_detection(self):
                    self.main_game.role_area.card_group[self] = self.main_game.hand_area.card_group.pop(self)
                    self.main_game.information = [0, self.card_type + "卡牌放置进场后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
