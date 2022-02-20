from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "葛罗芬戴尔.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "葛罗芬戴尔"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 12  # 英雄的初始威胁值
        self.willpower = 3  # 英雄的意志力
        self.attack_force = 3  # 英雄的攻击力
        self.defense_force = 1  # 英雄的防御力
        self.health_point = 5  # 英雄的生命值
        self.resource_symbol = "学识"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("贵族", "诺多精灵", "战士")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("行动",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：从葛罗芬戴尔的资源池中支付1枚资源标记，以治疗任一角色的1点伤害。（每个回合限制1次）"

        # 剧情描述的斜体文字
        self.describe_text = "你看到的就是他身处幽界的形体：万物嫡传之子的真身。 ——甘道夫，《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.round_mark = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.round_mark is not None and self.round_mark != self.main_game.threat_area.round_number:
            if "行动后" in self.active_condition:
                self.active_condition.pop("行动后")
                self.update_mask()
            self.round_mark = None
        elif self.round_mark is not None and "行动后" not in self.active_condition:
            self.active_condition["行动后"] = None
            self.update_mask()
            self.main_game.button_option.reset()

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "行动" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if hasattr(self, "select_card"):
                    del self.select_card
                if self.active_resource > 0:
                    self.round_mark = self.main_game.threat_area.round_number
                    self.active_condition["行动后"] = None
                    self.active_resource -= 1
                    self.update_mask()
                    card_group = []
                    for card in self.main_game.role_area.card_group:
                        if (card.card_type == "英雄" or card.card_type == "盟友") and card.active_health_point < card.health_point and "免疫" not in card.rule_mark:
                            card_group.append(card)
                    for card in self.main_game.clash_area.card_group:
                        if (card.card_type == "英雄" or card.card_type == "盟友") and card.active_health_point < card.health_point and "免疫" not in card.rule_mark:
                            card_group.append(card)
                    for card in self.main_game.scenario_area.card_group:
                        if (card.card_type == "英雄" or card.card_type == "盟友") and card.active_health_point < card.health_point and "免疫" not in card.rule_mark:
                            card_group.append(card)
                    for card in self.main_game.hand_area.card_group:
                        if (card.card_type == "英雄" or card.card_type == "盟友") and card.active_health_point < card.health_point and "免疫" not in card.rule_mark:
                            card_group.append(card)
                    if card_group:
                        self.select_card = self.main_game.card_select(card_group)
                        self.main_game.information = [0, "英雄卡牌将要治疗", self, self.select_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if hasattr(self, "select_card"):
                    self.select_card.active_health_point += 1
                    if self.select_card.active_health_point > self.select_card.health_point:
                        self.select_card.active_health_point = self.select_card.health_point
                    self.select_card.update_mask()
                    self.main_game.information = [0, "英雄卡牌治疗后", self, self.select_card]
                    del self.select_card
                self.card_order = [None, 0, 0, None, 0, 0]
