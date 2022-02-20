from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "暗藏危险的迷雾.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (2, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "暗藏危险的迷雾"  # 这张卡的名称
        self.encounter_symbol = "眼球"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("展示后",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "阴谋"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "展示后：在场景区中的每个地区获得+1威胁力直到本阶段结束。然后，每位威胁等级等于或高于35的玩家从他的手牌中选择并弃除一张卡牌。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = ""

        # 剧情描述的斜体文字
        self.describe_text = "“但是，除非稍后雾气稍散，不然我们也很难找到去路。” ——亚拉冈，《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None
        self.card_group = []

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.main_game.information and self.main_game.information[1][-5:] == "卡牌展示后" and self.main_game.information[
            3] == self and str(self) not in self.main_game.information:
            if self.main_game.information[2] != "order":
                self.pause_card = self.main_game.information[2]
                self.pause_card_order = self.main_game.information[2].card_order
                self.main_game.information[2].card_order = [None, -1, 0, None, -1, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["展示后", 0, 0, False, 0, 0]
        elif self.phase_mark is not None and self.main_game.threat_area.current_phase == self.phase_mark:
            for card in self.main_game.scenario_area.card_group:
                if card.card_type == "地区" and card not in self.card_group:
                    card.active_threat_force += 1
                    card.update_mask()
                    self.card_group.append(card)
            for card in self.card_group.copy():
                if card not in self.main_game.scenario_area.card_group:
                    card.active_threat_force -= 1
                    if card.active_threat_force < 0:
                        card.active_threat_force = 0
                    card.update_mask()
                    self.card_group.remove(card)
        elif self.phase_mark is not None and self.main_game.threat_area.current_phase != self.phase_mark:
            for card in self.card_group:
                card.active_threat_force -= 1
                if card.active_threat_force < 0:
                    card.active_threat_force = 0
                card.update_mask()
            if self.main_game.threat_area.threat_value >= 35 and self.main_game.hand_area.card_group:
                self.card_group.clear()
                for card in self.main_game.hand_area.card_group:
                    if not card.card_order[0]:
                        self.card_group.append(card)
                if self.card_group:
                    self.main_game.card_select(self.card_group).card_order = ["被弃除", 0, 0, False, 0, 0]
            self.main_game.scenario_area.card_group.pop(self)
            if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
            else:
                self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
            self.phase_mark = None
            self.card_group.clear()

    # 执行这张卡片的效果
    def run_card_order(self):
        if self.card_order[0] == "展示后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "阴谋卡牌将要执行展示后效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.phase_mark = self.main_game.threat_area.current_phase
                self.main_game.information = [0, "阴谋卡牌展示后效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and not self.main_game.response_conflict:
                if self.phase_mark is None:
                    self.main_game.scenario_area.card_group.pop(self)
                    if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                    else:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                if self.pause_card:
                    self.pause_card.card_order = self.pause_card_order
                    self.pause_card = None
                    self.pause_card_order = None
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.card_order = [None, 0, 0, None, 0, 0]
