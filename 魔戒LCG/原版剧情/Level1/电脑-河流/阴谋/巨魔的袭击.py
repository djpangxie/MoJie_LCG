from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "巨魔的袭击.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 0, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "巨魔的袭击"  # 这张卡的名称
        self.encounter_symbol = "河流"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("展示后", "暗影")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "阴谋"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "展示后：所有交锋中的巨魔敌军进行攻击。如果没有巨魔敌军被交锋，巨魔的袭击获得“涌现”。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：如果攻击的敌军是巨魔，本次攻击对每位玩家进行结算。（未与本敌军交锋的每位玩家均为无人防御。）"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.bonus_attack = None

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
        elif self.bonus_attack is False and self.main_game.information and (
                self.main_game.information[1] == "将要离开资源阶段" or self.main_game.information[1] == "将要离开计划阶段" or
                self.main_game.information[1] == "将要离开任务阶段" or self.main_game.information[1] == "将要离开探索阶段" or
                self.main_game.information[1] == "将要离开遭遇阶段" or self.main_game.information[1] == "将要离开战斗阶段" or
                self.main_game.information[1] == "将要离开恢复阶段") and self.main_game.information[2] == "order":
            troll_enemy = []
            for enemy in self.main_game.clash_area.card_group:
                if enemy.card_type == "敌军" and (
                        "巨魔" in enemy.card_attribute or "属性+" in enemy.active_condition and "巨魔" in
                        enemy.active_condition["属性+"]):
                    troll_enemy.append(enemy)
            if troll_enemy:
                enemys = []
                for enemy in self.main_game.scenario_area.card_group:
                    if enemy.card_type == "敌军":
                        enemy.active_condition["已攻击"] = None
                        enemy.update_mask()
                    if "分配暗影" in enemy.active_condition:
                        enemys.append(enemy)
                for enemy in self.main_game.clash_area.card_group:
                    if enemy.card_type == "敌军":
                        enemy.active_condition["已攻击"] = None
                        enemy.update_mask()
                    if "分配暗影" in enemy.active_condition:
                        enemys.append(enemy)
                for enemy in enemys:
                    for shadow_card in enemy.active_condition["分配暗影"]:
                        if shadow_card.card_type == "暗影牌":
                            if shadow_card.card_target:
                                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0,
                                                                                                      shadow_card.card_target)
                                else:
                                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [
                                        shadow_card.card_target]
                            self.main_game.card_estimate(enemy)[enemy].remove(shadow_card)
                        else:
                            if "暗影" in shadow_card.rule_mark:
                                shadow_card.card_order = ["弃除暗影", 0, 0, False, 0, 0]
                            else:
                                self.main_game.card_estimate(enemy)[enemy].remove(shadow_card)
                                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, shadow_card)
                                else:
                                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [shadow_card]
                    enemy.active_condition.pop("分配暗影")
                    enemy.update_mask()
                for enemy in troll_enemy:
                    enemy.active_condition.pop("已攻击")
                    enemy.update_mask()
                self.pause_card = "order"
                self.pause_card_order = self.main_game.threat_area.order
                self.main_game.threat_area.order = [True, 52, 0, True, 0, 0]
                self.main_game.threat_area.current_phase = 5
                self.copy_information = self.main_game.information
                self.main_game.information = None
                self.bonus_attack = True
            else:
                self.main_game.scenario_area.card_group.pop(self)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.bonus_attack = None
        elif self.bonus_attack is True and self.main_game.threat_area.order[1] == 55 and not self.main_game.information:
            enemys = []
            for enemy in self.main_game.scenario_area.card_group:
                if "已攻击" in enemy.active_condition:
                    enemy.active_condition.pop("已攻击")
                    enemy.update_mask()
                if "分配暗影" in enemy.active_condition:
                    enemys.append(enemy)
            for enemy in self.main_game.clash_area.card_group:
                if "已攻击" in enemy.active_condition:
                    enemy.active_condition.pop("已攻击")
                    enemy.update_mask()
                if "分配暗影" in enemy.active_condition:
                    enemys.append(enemy)
            for enemy in enemys:
                for shadow_card in enemy.active_condition["分配暗影"]:
                    if shadow_card.card_type == "暗影牌":
                        if shadow_card.card_target:
                            if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                                self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0,
                                                                                                  shadow_card.card_target)
                            else:
                                self.main_game.encounterdiscard_area.encounterdiscard_deck = [shadow_card.card_target]
                        self.main_game.card_estimate(enemy)[enemy].remove(shadow_card)
                    else:
                        if "暗影" in shadow_card.rule_mark:
                            shadow_card.card_order = ["弃除暗影", 0, 0, False, 0, 0]
                        else:
                            self.main_game.card_estimate(enemy)[enemy].remove(shadow_card)
                            if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                                self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, shadow_card)
                            else:
                                self.main_game.encounterdiscard_area.encounterdiscard_deck = [shadow_card]
                enemy.active_condition.pop("分配暗影")
                enemy.update_mask()
            self.main_game.threat_area.order = self.pause_card_order
            self.pause_card = None
            self.pause_card_order = None
            self.main_game.information = self.copy_information
            self.main_game.information[0] = 0
            self.copy_information = None
            self.main_game.scenario_area.card_group.pop(self)
            if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
            else:
                self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
            self.bonus_attack = None

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
                on_clash = False
                for enemy in self.main_game.clash_area.card_group:
                    if enemy.card_type == "敌军" and (
                            "巨魔" in enemy.card_attribute or "属性+" in enemy.active_condition and "巨魔" in
                            enemy.active_condition["属性+"]):
                        on_clash = True
                        break
                if on_clash:
                    self.bonus_attack = False
                else:
                    if "关键词+" in self.active_condition:
                        self.active_condition["关键词+"].append("涌现")
                    else:
                        self.active_condition["关键词+"] = ["涌现"]
                        self.update_mask()
                self.main_game.information = [0, "阴谋卡牌展示后效果结算后", self]
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
                if self.bonus_attack is None:
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
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "弃除暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]].remove(
                    self)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]
