from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "血雨腥风.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 0, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "血雨腥风"  # 这张卡的名称
        self.encounter_symbol = "河流"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("展示后", "暗影")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "阴谋"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "展示后：移除所有敌军上的所有伤害标记。然后，每位玩家的威胁等级上升与他交锋敌军上刚移除的伤害标记数量相等的点数。如果没有伤害标记因本效果移除，血雨腥风获得“涌现”。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：将本敌军上的所有伤害标记移至防御角色上。（如果无人防御，则将伤害标记移至承受本次攻击的英雄上。）"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._increment = 0

    # 重置卡牌
    def reset_card(self):
        super().reset_card()
        self._increment = 0

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
        elif "暗影牌" in self.active_condition and self._increment and self.main_game.information and "战斗阶段敌军卡牌将要攻击" in \
                self.main_game.information[1] and self.main_game.information[2] == self.active_condition["暗影牌"][0]:
            self.main_game.threat_area.damage += self._increment
            self._increment = 0

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
                self.card_order[1] += 2
            elif not self.main_game.information:
                damage_mark = False
                for enemy in self.main_game.scenario_area.card_group:
                    if enemy.card_type == "敌军" and 0 < enemy.active_health_point < enemy.health_point:
                        damage_mark = True
                        enemy.active_health_point = enemy.health_point
                        enemy.update_mask()
                for enemy in self.main_game.clash_area.card_group:
                    if enemy.card_type == "敌军" and 0 < enemy.active_health_point < enemy.health_point:
                        self._increment += enemy.health_point - enemy.active_health_point
                        enemy.active_health_point = enemy.health_point
                        enemy.update_mask()
                if self._increment:
                    self.main_game.information = [0, "玩家将要上升威胁等级", self]
                    self.card_order[1] -= 1
                elif not damage_mark:
                    if "关键词+" in self.active_condition:
                        self.active_condition["关键词+"].append("涌现")
                    else:
                        self.active_condition["关键词+"] = ["涌现"]
                        self.update_mask()
                self.card_order[1] += 2
        elif self.card_order[0] == "展示后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self._increment:
                    self.main_game.threat_area.threat_value += self._increment
                    self.main_game.information = [0, "玩家上升威胁等级后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "阴谋卡牌展示后效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition[
                    "关键词+"] and self.main_game.encounter_area.encounter_deck:
                    self.main_game.information = [0, "遭遇卡牌将要展示", self, self.main_game.encounter_area.encounter_deck[0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 5:
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
        elif self.card_order[0] == "展示后" and self.card_order[1] == 6:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if "关键词+" in self.active_condition and "涌现" in self.active_condition["关键词+"] and hasattr(self,
                                                                                                         "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌将要放置进场", self,
                                                  self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 7:
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
        elif self.card_order[0] == "展示后" and self.card_order[1] == 8:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and not self.main_game.response_conflict:
                if hasattr(self, "encounter_card"):
                    del self.encounter_card
                self._increment = 0
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
                self._increment = 0
                self.main_game.information = [0, "阴谋卡牌将要执行暗影效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if 0 < self.active_condition["暗影牌"][0].active_health_point < self.active_condition["暗影牌"][0].health_point:
                    self._increment = self.active_condition["暗影牌"][0].health_point - self.active_condition["暗影牌"][0].active_health_point
                    self.active_condition["暗影牌"][0].active_health_point = self.active_condition["暗影牌"][0].health_point
                    self.active_condition["暗影牌"][0].update_mask()
                self.main_game.information = [0, "阴谋卡牌暗影效果结算后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "弃除暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self._increment = 0
                self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]].remove(self)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]
