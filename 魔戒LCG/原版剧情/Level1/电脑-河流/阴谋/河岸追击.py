from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "河岸追击.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 0, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "河岸追击"  # 这张卡的名称
        self.encounter_symbol = "河流"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("展示后",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "阴谋"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "展示后：从胜利点计数区和遭遇弃牌堆中搜寻一个具有最高生命值的敌军。将该敌军返回场景区。如果没有敌军因本效果返回，河岸追击获得“涌现”。(不能被取消)"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = ""

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

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

    # 执行这张卡片的效果
    def run_card_order(self):
        if self.card_order[0] == "展示后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.highest_health_card = None
                num = 0
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    for card in self.main_game.encounterdiscard_area.encounterdiscard_deck:
                        if card.card_type == "敌军":
                            if num == 0:
                                self.highest_health_card = card
                            elif self.highest_health_card.health_point < card.health_point < self.main_game.settings.health_point_ceiling:
                                self.highest_health_card = card
                            num += 1
                num = 0
                if self.main_game.threat_area.victory_point_deck:
                    for card in self.main_game.threat_area.victory_point_deck:
                        if card.card_type == "敌军":
                            if num == 0 and self.highest_health_card is None:
                                self.highest_health_card = card
                            elif self.highest_health_card.health_point < card.health_point < self.main_game.settings.health_point_ceiling:
                                self.highest_health_card = card
                            num += 1
                if self.highest_health_card:
                    self.main_game.information = [0, "敌军卡牌将要放置进场", self, self.highest_health_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[2] = 0
                self.highest_health_card = None
            elif not self.main_game.information:
                if self.highest_health_card and self.main_game.encounterdiscard_area.encounterdiscard_deck and self.highest_health_card in self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.remove(self.highest_health_card)
                    self.highest_health_card.reset_card()
                    self.highest_health_card.update_mask()
                    self.main_game.scenario_area.card_group[self.highest_health_card] = None
                    self.main_game.information = [0, "敌军卡牌放置进场后", self, self.highest_health_card]
                elif self.highest_health_card and self.main_game.threat_area.victory_point_deck and self.highest_health_card in self.main_game.threat_area.victory_point_deck:
                    self.main_game.threat_area.victory_point_deck.remove(self.highest_health_card)
                    self.highest_health_card.reset_card()
                    self.highest_health_card.update_mask()
                    self.main_game.scenario_area.card_group[self.highest_health_card] = None
                    self.main_game.information = [0, "敌军卡牌放置进场后", self, self.highest_health_card]
                else:
                    if "关键词+" in self.active_condition:
                        self.active_condition["关键词+"].append("涌现")
                    else:
                        self.active_condition["关键词+"] = ["涌现"]
                        self.update_mask()
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition[
                    "关键词+"] and self.main_game.encounter_area.encounter_deck:
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
                if "关键词+" in self.active_condition and "涌现" in self.active_condition[
                    "关键词+"] and self.main_game.encounter_area.encounter_deck:
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
                del self.highest_health_card
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
