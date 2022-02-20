from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "伊欧玟.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "伊欧玟"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 9  # 英雄的初始威胁值
        self.willpower = 4  # 英雄的意志力
        self.attack_force = 1  # 英雄的攻击力
        self.defense_force = 1  # 英雄的防御力
        self.health_point = 3  # 英雄的生命值
        self.resource_symbol = "精神"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("贵族", "洛汗")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("行动",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：从你的手牌中弃除一张卡牌，以使伊欧玟获得+1意志力直到本阶段结束。每回合每位玩家可以触发一次本效果。"

        # 剧情描述的斜体文字
        self.describe_text = "瘦高的身躯穿着一袭白袍，系着银色的腰带；她看来英气勃发，让人可以感受到一种钢铁般的坚毅，果然是拥有王族血统的女子。 ——《双城奇谋》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.round_mark = None
        self.phase_mark = None
        self._increment = 0

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.phase_mark is not None and self.main_game.threat_area.current_phase != self.phase_mark:
            if "行动后" in self.active_condition:
                self.active_willpower -= self._increment
                if self.active_willpower < 0:
                    self.active_willpower = 0
                self.update_mask()
            self._increment = 0
            self.phase_mark = None
        elif self.round_mark is not None and self.round_mark != self.main_game.threat_area.round_number:
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
                if self.main_game.hand_area.card_group:
                    cards = []
                    for card in self.main_game.hand_area.card_group:
                        if "免疫" not in card.rule_mark:
                            cards.append(card)
                    if cards:
                        card = self.main_game.card_select(cards)
                        card.card_order = ["被弃除", 0, 0, False, 0, 0]
                        self.phase_mark = self.main_game.threat_area.current_phase
                        self.round_mark = self.main_game.threat_area.round_number
                        self.active_condition["行动后"] = None
                        self.active_willpower += 1
                        self._increment += 1
                        self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
