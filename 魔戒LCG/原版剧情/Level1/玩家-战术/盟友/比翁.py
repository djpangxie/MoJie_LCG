from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "比翁.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "比翁"  # 卡牌的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 6  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "战术"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.willpower = 1  # 卡牌的意志力
        self.attack_force = 3  # 卡牌的攻击力
        self.defense_force = 3  # 卡牌的防御力
        self.health_point = 6  # 卡牌的生命值
        self.card_attribute = ("比翁一族", "战士")  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "盟友"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：比翁获得+5攻击力直到本阶段结束。在你触发本效果的阶段结束时，将比翁洗回你的牌组。（每个回合限制1次）"

        # 剧情描述的斜体文字
        self.describe_text = "我不需要差遣你们，不用客气了，但我想你们会需要我的帮助的。 ——《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None
        self.round_mark = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.phase_mark is not None and self.main_game.threat_area.current_phase != self.phase_mark:
            if "行动后" in self.active_condition and self.main_game.card_estimate(self) is not None:
                self.card_order = ["离场", 0, 0, False, 0, 0, "牌组"]
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
                self.phase_mark = self.main_game.threat_area.current_phase
                self.round_mark = self.main_game.threat_area.round_number
                self.active_condition["行动后"] = None
                self.active_attack_force += 5
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
