from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "暗影驱使.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (1, 1, 1)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "暗影驱使"  # 这张卡的名称
        self.encounter_symbol = "半兽人"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("展示后", "暗影")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "阴谋"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "展示后：当前在场景区中的每个敌军和地区获得+1威胁力直到本阶段结束。如果场景区中没有卡牌，暗影驱使获得”涌现“。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：从防御角色上选择并弃除一张附属牌。(如果本次攻击无人防御，则以弃除你控制的所有附属牌代替。)"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if hasattr(self, "card_group"):
            for card in self.card_group.copy():
                if not self.main_game.on_spot(card):
                    self.card_group.remove(card)
        if self.main_game.information and self.main_game.information[1][-5:] == "卡牌展示后" and self.main_game.information[
            3] == self and str(self) not in self.main_game.information:
            if self.main_game.information[2] != "order":
                self.pause_card = self.main_game.information[2]
                self.pause_card_order = self.main_game.information[2].card_order
                self.main_game.information[2].card_order = [None, -1, 0, None, -1, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["展示后", 0, 0, False, 0, 0]
        elif self.phase_mark != None and self.main_game.threat_area.current_phase != self.phase_mark:
            for card in self.card_group:
                card.active_threat_force -= 1
                if card.active_threat_force < 0:
                    card.active_threat_force = 0
                card.update_mask()
            self.main_game.scenario_area.card_group.pop(self)
            if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
            else:
                self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
            self.phase_mark = None
            del self.card_group

    # 执行这张卡片的效果
    def run_card_order(self):
        if self.card_order[0] == "展示后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "阴谋卡牌将要执行展示后效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.card_group = []
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "敌军" or card.card_type == "地区":
                        card.active_threat_force += 1
                        card.update_mask()
                        self.card_group.append(card)
                if self.card_group:
                    self.phase_mark = self.main_game.threat_area.current_phase
                else:
                    if "关键词+" in self.active_condition:
                        self.active_condition["关键词+"].append("涌现")
                    else:
                        self.active_condition["关键词+"] = ["涌现"]
                        self.update_mask()
                    del self.card_group
                self.main_game.information = [0, "阴谋卡牌展示后效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition["关键词+"] and self.main_game.encounter_area.encounter_deck:
                    self.main_game.information = [0, "遭遇卡牌将要展示", self, self.main_game.encounter_area.encounter_deck[0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 3:
            if self.card_order[2]:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.encounter_area.encounter_deck[0].reset_card()
                    self.main_game.encounter_area.encounter_deck[0].update_mask()
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition["关键词+"] and self.main_game.encounter_area.encounter_deck:
                    self.encounter_card = self.main_game.encounter_area.encounter_deck.pop(0)
                    self.main_game.card_exhibition(self.encounter_card, self.main_game.settings.card_exhibition_time)
                    self.main_game.scenario_area.card_group[self.encounter_card] = None
                    self.main_game.information = [0, "遭遇卡牌展示后", self, self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition["关键词+"] and hasattr(self,
                                                                                                         "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌将要放置进场", self,
                                                  self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 5:
            if self.card_order[2]:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition["关键词+"] and hasattr(self,
                                                                                                         "encounter_card"):
                    self.main_game.scenario_area.card_group.pop(self.encounter_card)
                    self.encounter_card.reset_card()
                    self.encounter_card.update_mask()
                    if self.main_game.encounter_area.encounter_deck:
                        self.main_game.encounter_area.encounter_deck.insert(0, self.encounter_card)
                        random.shuffle(self.main_game.encounter_area.encounter_deck)
                    else:
                        self.main_game.encounter_area.encounter_deck = [self.encounter_card]
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition["关键词+"] and hasattr(self,
                                                                                                         "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌放置进场后", self,
                                                  self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 6:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and not self.main_game.response_conflict:
                if hasattr(self, "encounter_card"):
                    del self.encounter_card
                if self.phase_mark == None:
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
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "阴谋卡牌将要执行暗影效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.active_condition["暗影牌"][0].active_condition["攻击中"]:
                    affiliateds = []
                    for defender in self.active_condition["暗影牌"][0].active_condition["攻击中"]:
                        if "被附属" in defender.active_condition:
                            for affiliated in defender.active_condition["被附属"]:
                                affiliateds.append(affiliated)
                    affiliated = self.main_game.card_select(affiliateds)
                    if affiliated:
                        affiliated.card_order = ["弃除附属", 0, 0, False, 0, 0]
                else:
                    for card in self.main_game.hand_area.card_group:
                        if "被附属" in card.active_condition:
                            for affiliated in card.active_condition["被附属"]:
                                if self.main_game.player_control(affiliated):
                                    affiliated.card_order = ["弃除附属", 0, 0, False, 0, 0]
                    for card in self.main_game.role_area.card_group:
                        if "被附属" in card.active_condition:
                            for affiliated in card.active_condition["被附属"]:
                                if self.main_game.player_control(affiliated):
                                    affiliated.card_order = ["弃除附属", 0, 0, False, 0, 0]
                    for card in self.main_game.clash_area.card_group:
                        if "被附属" in card.active_condition:
                            for affiliated in card.active_condition["被附属"]:
                                if self.main_game.player_control(affiliated):
                                    affiliated.card_order = ["弃除附属", 0, 0, False, 0, 0]
                    for card in self.main_game.scenario_area.card_group:
                        if "被附属" in card.active_condition:
                            for affiliated in card.active_condition["被附属"]:
                                if self.main_game.player_control(affiliated):
                                    affiliated.card_order = ["弃除附属", 0, 0, False, 0, 0]
                    for card in self.main_game.task_area.region_card:
                        if "被附属" in card.active_condition:
                            for affiliated in card.active_condition["被附属"]:
                                if self.main_game.player_control(affiliated):
                                    affiliated.card_order = ["弃除附属", 0, 0, False, 0, 0]
                self.main_game.information = [0, "阴谋卡牌暗影效果结算后", self]
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
