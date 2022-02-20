from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "安度因巨魔幼崽.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 0, 3)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "安度因巨魔幼崽"  # 这张卡的名称
        self.clash_value = 26  # 这张卡的交锋值
        self.threat_force = 2  # 这张卡的威胁力
        self.attack_force = 4  # 这张卡的攻击力
        self.defense_force = 3  # 这张卡的防御力
        self.health_point = 5  # 这张卡的生命值
        self.encounter_symbol = "河流"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("巨魔",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("永久", "强制")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "如果山丘巨魔不在场中，安度因巨魔幼崽获得“涌现”。\n强制：在战斗阶段开始时，安度因巨魔幼崽与一位已与山丘巨魔交锋的玩家交锋。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = ""

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._successful = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if ("关键词+" not in self.active_condition or "涌现" not in self.active_condition[
            "关键词+"]) and "暗影牌" not in self.active_condition:
            on_spot = False
            for card in self.main_game.scenario_area.card_group:
                if card.card_name == "山丘巨魔":
                    on_spot = True
                    break
            else:
                for card in self.main_game.clash_area.card_group:
                    if card.card_name == "山丘巨魔":
                        on_spot = True
                        break
            if not on_spot:
                if "关键词+" in self.active_condition:
                    self.active_condition["关键词+"].append("涌现")
                else:
                    self.active_condition["关键词+"] = ["涌现"]
                    self.update_mask()
        if self.active_health_point > 0 and "关键词+" in self.active_condition and "涌现" in self.active_condition[
            "关键词+"] and self.main_game.information and self.main_game.information[1][-5:] == "卡牌展示后" and \
                self.main_game.information[3] == self and str(self) not in self.main_game.information:
            if self.main_game.information[2] != "order":
                self.pause_card = self.main_game.information[2]
                self.pause_card_order = self.main_game.information[2].card_order
                self.main_game.information[2].card_order = [None, -1, 0, None, -1, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["展示后", 0, 0, False, 0, 0]
        elif self.active_health_point > 0 and self in self.main_game.scenario_area.card_group and self.main_game.information and \
                self.main_game.information[1] == "进入战斗阶段后" and self.main_game.information[2] == "order" and str(
            self) not in self.main_game.information:
            for card in self.main_game.clash_area.card_group:
                if card.card_name == "山丘巨魔":
                    self.copy_information = self.main_game.information
                    self.main_game.information = None
                    self.card_order = ["强制", 0, 0, False, 0, 0]
                    break

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "展示后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition[
                    "关键词+"] and self.main_game.encounter_area.encounter_deck:
                    self.main_game.information = [0, "遭遇卡牌将要展示", self, self.main_game.encounter_area.encounter_deck[0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 1:
            if self.card_order[2]:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.encounter_area.encounter_deck[0].reset_card()
                    self.main_game.encounter_area.encounter_deck[0].update_mask()
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition[
                    "关键词+"] and self.main_game.encounter_area.encounter_deck:
                    self.encounter_card = self.main_game.encounter_area.encounter_deck.pop(0)
                    self.main_game.card_exhibition(self.encounter_card, self.main_game.settings.card_exhibition_time)
                    self.main_game.scenario_area.card_group[self.encounter_card] = None
                    self.main_game.information = [0, "遭遇卡牌展示后", self, self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition["关键词+"] and hasattr(self,
                                                                                                         "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌将要放置进场", self,
                                                  self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 3:
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
        elif self.card_order[0] == "展示后" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and not self.main_game.response_conflict:
                if hasattr(self, "encounter_card"):
                    del self.encounter_card
                if self.pause_card:
                    self.pause_card.card_order = self.pause_card_order
                    self.pause_card = None
                    self.pause_card_order = None
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "强制" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要执行强制效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.active_health_point > 0 and self in self.main_game.scenario_area.card_group:
                    self._successful = True
                self.main_game.information = [0, "敌军卡牌强制效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                if self._successful:
                    self.card_order = ["交锋", 0, 0, False, 0, 0]
                else:
                    self.card_order = [None, 0, 0, None, 0, 0]
                self._successful = None
