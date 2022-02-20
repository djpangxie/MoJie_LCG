from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "法拉墨.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "法拉墨"  # 卡牌的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 4  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "领导"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.willpower = 2  # 卡牌的意志力
        self.attack_force = 1  # 卡牌的攻击力
        self.defense_force = 2  # 卡牌的防御力
        self.health_point = 3  # 卡牌的生命值
        self.card_attribute = ("刚铎", "贵族", "游侠")  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "盟友"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：横置法拉墨，以选择一位玩家。该玩家控制的每名角色获得+1意志力直到本阶段结束。"

        # 剧情描述的斜体文字
        self.describe_text = "这段时间他经常自愿执行最危险的任务。不过，他的命运似乎受到上天的眷顾，再不然就是他的时候还未到。 ——马伯龙，《双城奇谋》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if "目标卡牌" in self.active_condition:
            for card in self.main_game.role_area.card_group:
                if card not in self.active_condition["目标卡牌"] and (
                        card.card_type == "英雄" or card.card_type == "盟友") and "免疫" not in card.rule_mark:
                    self.active_condition["目标卡牌"].append(card)
                    card.active_willpower += 1
                    card.update_mask()
            for card in self.main_game.clash_area.card_group:
                if card not in self.active_condition["目标卡牌"] and (
                        card.card_type == "英雄" or card.card_type == "盟友") and "免疫" not in card.rule_mark:
                    self.active_condition["目标卡牌"].append(card)
                    card.active_willpower += 1
                    card.update_mask()
            for card in self.main_game.scenario_area.card_group:
                if card not in self.active_condition["目标卡牌"] and (
                        card.card_type == "英雄" or card.card_type == "盟友") and "免疫" not in card.rule_mark:
                    self.active_condition["目标卡牌"].append(card)
                    card.active_willpower += 1
                    card.update_mask()
            for card in self.active_condition["目标卡牌"].copy():
                if not self.main_game.on_spot(card):
                    self.active_condition["目标卡牌"].remove(card)
        if "目标卡牌" in self.active_condition and self.phase_mark is not None and (self.main_game.threat_area.current_phase != self.phase_mark or self.main_game.information and self.main_game.information[1] == "盟友卡牌将要离场" and self.main_game.information[2] == self):
            for card in self.active_condition["目标卡牌"]:
                card.active_willpower -= 1
                if card.active_willpower < 0:
                    card.active_willpower = 0
                card.update_mask()
            self.active_condition.pop("目标卡牌")
            self.active_condition.pop("行动后")
            self.update_mask()
            self.main_game.button_option.reset()
            self.phase_mark = None

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "行动" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.active_condition["已横置"] = None
                self.update_mask()
                self.main_game.information = [0, "盟友卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.phase_mark = self.main_game.threat_area.current_phase
                self.active_condition["目标卡牌"] = []
                self.active_condition["行动后"] = None
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
