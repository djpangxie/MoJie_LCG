from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "昂哥立安的子嗣.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (1, 1, 1)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "昂哥立安的子嗣"  # 这张卡的名称
        self.clash_value = 32  # 这张卡的交锋值
        self.threat_force = 3  # 这张卡的威胁力
        self.attack_force = 5  # 这张卡的攻击力
        self.defense_force = 2  # 这张卡的防御力
        self.health_point = 9  # 这张卡的生命值
        self.encounter_symbol = "蜘蛛"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("生物", "蜘蛛")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("展示后", "暗影")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "展示后：当前被指派执行任务的每名角色获得-1意志力直到本阶段结束。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：防御玩家的威胁等级上升4点。(如果本次攻击无人防御，则以上升8点代替。)"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None
        self.role_group = []

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.phase_mark is not None:
            for card in self.role_group.copy():
                if not self.main_game.on_spot(card[0]):
                    self.role_group.remove(card)
        if self.active_health_point > 0 and self.main_game.information and self.main_game.information[1][
                                                                           -5:] == "卡牌展示后" and \
                self.main_game.information[3] == self and str(self) not in self.main_game.information:
            if self.main_game.information[2] != "order":
                self.pause_card = self.main_game.information[2]
                self.pause_card_order = self.main_game.information[2].card_order
                self.main_game.information[2].card_order = [None, -1, 0, None, -1, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["展示后", 0, 0, False, 0, 0]
        elif self.phase_mark is not None and (self.main_game.threat_area.current_phase != self.phase_mark or self.main_game.information and self.main_game.information[1] == "敌军卡牌将要离场" and self.main_game.information[2] == self):
            for card in self.role_group:
                if card[1]:
                    card[0].active_willpower += 1
                    card[0].update_mask()
            self.phase_mark = None
            self.role_group.clear()

    # 执行这张卡片的展示后效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "展示后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要执行展示后效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.phase_mark = self.main_game.threat_area.current_phase
                for card in self.main_game.role_area.card_group:
                    if "任务中" in card.active_condition:
                        card.active_willpower -= 1
                        if card.active_willpower < 0:
                            card.active_willpower = 0
                            self.role_group.append((card, False))
                        else:
                            self.role_group.append((card, True))
                        card.update_mask()
                self.main_game.information = [0, "敌军卡牌展示后效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and not self.main_game.response_conflict:
                if self.pause_card:
                    self.pause_card.card_order = self.pause_card_order
                    self.pause_card = None
                    self.pause_card_order = None
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要执行暗影效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "玩家将要上升威胁等级", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.active_condition["暗影牌"][0].active_condition["攻击中"]:
                    self.main_game.threat_area.threat_value += 4
                else:
                    self.main_game.threat_area.threat_value += 8
                self.main_game.information = [0, "玩家上升威胁等级后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌暗影效果结算后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "弃除暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]].remove(self)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]
