from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "贝拉沃.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "贝拉沃"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 10  # 英雄的初始威胁值
        self.willpower = 2  # 英雄的意志力
        self.attack_force = 2  # 英雄的攻击力
        self.defense_force = 2  # 英雄的防御力
        self.health_point = 4  # 英雄的生命值
        self.resource_symbol = "学识"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("登丹人", "游侠")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("行动",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：横置贝拉沃，以选择一位玩家。该玩家补两张卡牌。每个回合限制1次。"

        # 剧情描述的斜体文字
        self.describe_text = "不过，在布理之外的荒野中有许多神秘的旅者，布理人称他们为游侠，对他们的来历一无所知。 ——《魔戒现身》"

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
                self.main_game.information = [0, "英雄卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.round_mark = self.main_game.threat_area.round_number
                self.active_condition["已横置"] = None
                self.active_condition["行动后"] = None
                self.update_mask()
                self.main_game.information = [0, "英雄卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "玩家将要补卡", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.playerdeck_area.player_deck:
                    card = self.main_game.playerdeck_area.player_deck.pop(0)
                    self.main_game.hand_area.card_group[card] = None
                    self.main_game.information = [0, "玩家补卡后", self, card]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "玩家将要补卡", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 5:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.main_game.playerdeck_area.player_deck:
                    card = self.main_game.playerdeck_area.player_deck.pop(0)
                    self.main_game.hand_area.card_group[card] = None
                    self.main_game.information = [0, "玩家补卡后", self, card]
                self.card_order = [None, 0, 0, None, 0, 0]
