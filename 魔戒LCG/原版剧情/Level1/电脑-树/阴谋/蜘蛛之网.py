from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "蜘蛛之网.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 0, 3)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "蜘蛛之网"  # 这张卡的名称
        self.encounter_symbol = "树"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("展示后",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "阴谋"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "展示后：具有最高威胁等级的玩家横置他控制的所有英雄。然后，将本卡牌附属到该玩家的一名英雄上。(视为一张状态附属牌，规则文字：“每当所附属的英雄横置时，对其造成1点伤害。”)"

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
        elif self.main_game.information and "卡牌横置后" in self.main_game.information[
            1] and "附属到" in self.active_condition and self.main_game.information[3] == self.active_condition["附属到"][
            0] and str(self) not in self.main_game.information:
            if self.main_game.information[2] != "order":
                self.pause_card = self.main_game.information[2]
                self.pause_card_order = self.main_game.information[2].card_order
                self.main_game.information[2].card_order = [None, -1, 0, None, -1, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["状态附属效果", 0, 0, False, 0, 0]

    # 执行这张卡片的展示后效果
    def run_card_order(self):
        if self.card_order[0] == "展示后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.heros = []
                for card in self.main_game.role_area.card_group:
                    if card.card_type == "英雄" and "已横置" not in card.active_condition:
                        self.heros.append(card)
                for card in self.main_game.clash_area.card_group:
                    if card.card_type == "英雄" and "已横置" not in card.active_condition:
                        self.heros.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "英雄" and "已横置" not in card.active_condition:
                        self.heros.append(card)
                self.main_game.information = [0, "阴谋卡牌将要执行展示后效果", self]
                self.card_order[3] = True
                self.card_order[4] = 0
                self.card_order[5] = 0
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information and self.card_order[3]:
                if self.card_order[5]:
                    if hasattr(self, "heros") and self.heros:
                        self.heros.pop(0)
                    self.card_order[4] += 1
                    self.card_order[5] -= 1
                elif self.card_order[4] % 2:
                    if self.heros and "已横置" not in self.heros[0].active_condition:
                        self.heros[0].active_condition["已横置"] = None
                        self.heros[0].update_mask()
                        self.main_game.information = [0, self.heros[0].card_type + "卡牌横置后", self, self.heros[0]]
                        self.heros.pop(0)
                    self.card_order[4] += 1
                else:
                    if hasattr(self, "heros") and self.heros:
                        self.main_game.information = [0, self.heros[0].card_type + "卡牌将要横置", self, self.heros[0]]
                        self.card_order[4] += 1
                    elif hasattr(self, "heros"):
                        del self.heros
                        self.card_order[3] = False
                        self.card_order[4] = 0
                        self.card_order[5] = 0
                        self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                heros = []
                for hero in self.main_game.role_area.hero_group:
                    if "免疫" not in hero.rule_mark:
                        heros.append(hero)
                if heros:
                    self.select_hero = self.main_game.card_select(heros)
                    self.main_game.information = [0, "阴谋卡牌将要附属", self, self.select_hero]
                else:
                    self.card_order[2] = 1
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if self.main_game.card_estimate(self.select_hero)[self.select_hero]:
                    self.main_game.card_estimate(self.select_hero)[self.select_hero].append(self)
                else:
                    self.main_game.card_estimate(self.select_hero)[self.select_hero] = [self]
                if "被附属" not in self.select_hero.active_condition or not self.select_hero.active_condition["被附属"]:
                    self.select_hero.active_condition["被附属"] = [self]
                else:
                    self.select_hero.active_condition["被附属"].append(self)
                self.active_condition["附属到"] = [self.select_hero]
                if "属性+" in self.active_condition:
                    self.active_condition["属性+"].append("状态")
                else:
                    self.active_condition["属性+"] = ["状态"]
                if "类型+" in self.active_condition:
                    self.active_condition["类型+"].append("附属")
                else:
                    self.active_condition["类型+"] = ["附属"]
                self.update_mask()
                self.select_hero.update_mask()
                self.main_game.information = [0, "阴谋卡牌附属后", self, self.select_hero]
                self.main_game.scenario_area.card_group.pop(self)
                del self.select_hero
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "阴谋卡牌展示后效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 5:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and not self.main_game.response_conflict:
                if hasattr(self, "select_hero"):
                    del self.select_hero
                if self in self.main_game.scenario_area.card_group:
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
        elif self.card_order[0] == "弃除附属" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "阴谋卡牌将要被弃除", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "弃除附属" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                for hero in self.active_condition["附属到"]:
                    hero.active_condition["被附属"].remove(self)
                    if not hero.active_condition["被附属"]:
                        hero.active_condition.pop("被附属")
                    self.main_game.card_estimate(hero)[hero].remove(self)
                    hero.update_mask()
                self.active_condition.pop("附属到")
                self.active_condition.pop("属性+")
                self.active_condition.pop("类型+")
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.update_mask()
                self.main_game.information = [0, "阴谋卡牌被弃除后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "状态附属效果" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "阴谋卡牌将要攻击", self, self.active_condition["附属到"][0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "状态附属效果" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.active_condition["附属到"][0].active_health_point -= 1
                if self.active_condition["附属到"][0].active_health_point < 0:
                    self.active_condition["附属到"][0].active_health_point = 0
                self.active_condition["附属到"][0].update_mask()
                self.main_game.information = [0, "阴谋卡牌攻击后", self, self.active_condition["附属到"][0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "状态附属效果" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and not self.main_game.response_conflict:
                if self.pause_card and (
                        self.pause_card != self.active_condition["附属到"][0] or self.active_condition["附属到"][
                    0].active_health_point > 0):
                    self.pause_card.card_order = self.pause_card_order
                    self.pause_card = None
                    self.pause_card_order = None
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.card_order = [None, 0, 0, None, 0, 0]
