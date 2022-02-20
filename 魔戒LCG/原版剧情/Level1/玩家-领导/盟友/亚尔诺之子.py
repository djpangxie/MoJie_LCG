from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "亚尔诺之子.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "亚尔诺之子"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 3  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "领导"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.willpower = 0  # 卡牌的意志力
        self.attack_force = 2  # 卡牌的攻击力
        self.defense_force = 0  # 卡牌的防御力
        self.health_point = 2  # 卡牌的生命值
        self.card_attribute = ("登丹人",)  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("响应",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "盟友"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "响应：在亚尔诺之子进场后，选择一张在场景区中或当前与另一位玩家交锋的敌军牌。与该敌军交锋。"

        # 剧情描述的斜体文字
        self.describe_text = "...他们在亚尔诺创建了北方王国，在安度因河口的刚铎创建了南方王国。 ——《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.main_game.information and "卡牌放置进场后" in self.main_game.information[1] and self.main_game.information[3] == self and "响应后" not in self.active_condition:
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
                    cards = []
                    for card in self.main_game.scenario_area.card_group:
                        if card.card_type == "敌军" and "免疫" not in card.rule_mark:
                            cards.append(card)
                    if cards:
                        self.main_game.card_select(cards).card_order = ["交锋", 0, 0, False, 0, 0]
                    self.card_order[1] += 1
                    self.main_game.button_option.reset()
                elif self.main_game.button_option.option // 100000 == 2:
                    self.card_order[1] += 1
                    self.main_game.button_option.reset()
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
