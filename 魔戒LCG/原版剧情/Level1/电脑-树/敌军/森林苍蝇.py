from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "森林苍蝇.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 0, 3)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "森林苍蝇"  # 这张卡的名称
        self.clash_value = 27  # 这张卡的交锋值
        self.threat_force = 4  # 这张卡的威胁力
        self.attack_force = 1  # 这张卡的攻击力
        self.defense_force = 0  # 这张卡的防御力
        self.health_point = 3  # 这张卡的生命值
        self.encounter_symbol = "树"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("生物", "昆虫")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("强制", "暗影")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "强制：在你与森林苍蝇交锋后，对你的每名已横置角色造成1点伤害。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：如果攻击的敌军是昆虫，额外分配两张暗影牌。"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.main_game.information and self.main_game.information[
            1] == "敌军卡牌交锋后" and self.main_game.information[2] == self and str(self) not in self.main_game.information:
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["强制", 0, 0, False, 0, 0]

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "强制" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.roles = []
                for card in self.main_game.role_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" in card.active_condition:
                        self.roles.append(card)
                for card in self.main_game.clash_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" in card.active_condition:
                        self.roles.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" in card.active_condition:
                        self.roles.append(card)
                self.main_game.information = [0, "敌军卡牌将要执行强制效果", self]
                self.card_order[3] = True
                self.card_order[4] = 0
                self.card_order[5] = 0
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information and self.card_order[3]:
                if self.card_order[5]:
                    if hasattr(self, "roles") and self.roles:
                        self.roles.pop(0)
                    self.card_order[4] += 1
                    self.card_order[5] -= 1
                elif self.card_order[4] % 2:
                    if self.roles:
                        self.roles[0].active_health_point -= 1
                        if self.roles[0].active_health_point < 0:
                            self.roles[0].active_health_point = 0
                        self.roles[0].update_mask()
                        self.main_game.information = [0, "敌军卡牌攻击后", self, self.roles.pop(0)]
                    self.card_order[4] += 1
                else:
                    if hasattr(self, "roles") and self.roles:
                        self.main_game.information = [0, "敌军卡牌将要攻击", self, self.roles[0]]
                        self.card_order[4] += 1
                    elif hasattr(self, "roles"):
                        del self.roles
                        self.card_order[3] = False
                        self.card_order[4] = 0
                        self.card_order[5] = 0
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
                if self.main_game.encounter_area.encounter_deck and (
                        "昆虫" in self.active_condition["暗影牌"][0].card_attribute or "属性+" in self.active_condition["暗影牌"][
                    0].active_condition and "昆虫" in self.active_condition["暗影牌"][0].active_condition["属性+"]):
                    self.main_game.information = [0, "将要分配暗影牌", self, self.active_condition["暗影牌"][0]]
                    self.card_order[1] += 1
                else:
                    self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    shadow_card = self.main_game.encounter_area.encounter_deck.pop(0)
                    shadow_card.active_condition["暗影牌"] = [self.active_condition["暗影牌"][0]]
                    shadow_card.update_mask()
                    if "分配暗影" in self.active_condition["暗影牌"][0].active_condition:
                        self.active_condition["暗影牌"][0].active_condition["分配暗影"].append(shadow_card)
                    else:
                        self.active_condition["暗影牌"][0].active_condition["分配暗影"] = [shadow_card]
                        self.active_condition["暗影牌"][0].update_mask()
                    if self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]]:
                        self.main_game.card_estimate(self.active_condition["暗影牌"][0])[
                            self.active_condition["暗影牌"][0]].append(shadow_card)
                    else:
                        self.main_game.card_estimate(self.active_condition["暗影牌"][0])[
                            self.active_condition["暗影牌"][0]] = [shadow_card]
                    if "暗影" in shadow_card.rule_mark:
                        self.main_game.card_exhibition(shadow_card, self.main_game.settings.card_exhibition_time)
                        shadow_card.card_order = ["结算暗影", 0, 0, False, 0, 0]
                    self.main_game.information = [0, "分配暗影牌后", self, self.active_condition["暗影牌"][0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.information = [0, "将要分配暗影牌", self, self.active_condition["暗影牌"][0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    shadow_card = self.main_game.encounter_area.encounter_deck.pop(0)
                    shadow_card.active_condition["暗影牌"] = [self.active_condition["暗影牌"][0]]
                    shadow_card.update_mask()
                    if "分配暗影" in self.active_condition["暗影牌"][0].active_condition:
                        self.active_condition["暗影牌"][0].active_condition["分配暗影"].append(shadow_card)
                    else:
                        self.active_condition["暗影牌"][0].active_condition["分配暗影"] = [shadow_card]
                        self.active_condition["暗影牌"][0].update_mask()
                    if self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]]:
                        self.main_game.card_estimate(self.active_condition["暗影牌"][0])[
                            self.active_condition["暗影牌"][0]].append(shadow_card)
                    else:
                        self.main_game.card_estimate(self.active_condition["暗影牌"][0])[
                            self.active_condition["暗影牌"][0]] = [shadow_card]
                    if "暗影" in shadow_card.rule_mark:
                        self.main_game.card_exhibition(shadow_card, self.main_game.settings.card_exhibition_time)
                        shadow_card.card_order = ["结算暗影", 0, 0, False, 0, 0]
                    self.main_game.information = [0, "分配暗影牌后", self, self.active_condition["暗影牌"][0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 5:
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
