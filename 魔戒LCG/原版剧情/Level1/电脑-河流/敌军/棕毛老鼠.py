from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "棕毛老鼠.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 0, 3)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "棕毛老鼠"  # 这张卡的名称
        self.clash_value = 1  # 这张卡的交锋值
        self.threat_force = 1  # 这张卡的威胁力
        self.attack_force = 1  # 这张卡的攻击力
        self.defense_force = 1  # 这张卡的防御力
        self.health_point = main_game.settings.health_point_ceiling  # 这张卡的生命值
        self.encounter_symbol = "河流"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("生物", "老鼠")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("永久", "强制", "暗影")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "棕毛老鼠不能被伤害。\n强制：如果玩家在场景3中并且所有剩余的敌军均具有印刷的老鼠属性，从场中弃除棕毛老鼠。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：攻击的敌军本回合不能被伤害。"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._throwing = False
        self._shield_card = None

    # 重置卡牌
    def reset_card(self):
        super().reset_card()
        self._throwing = False
        self._shield_card = None

    # 卡牌侦听
    def card_listening(self):
        if self.active_health_point != self.health_point:
            self.active_health_point = self.health_point
            self.update_mask()
        super().card_listening()
        if self.main_game.information and "卡牌将要攻击" in self.main_game.information[1] and self.main_game.information[
            3] == self:
            if "战斗阶段" in self.main_game.information[1]:
                if self.main_game.threat_area.order[3]:
                    self.main_game.threat_area.order[5] = 1
                else:
                    self.main_game.threat_area.order[2] = 1
            else:
                if self.main_game.information[2].card_order[3]:
                    self.main_game.information[2].card_order[5] = 1
                else:
                    self.main_game.information[2].card_order[2] = 1
            self.main_game.information = None
        elif self._shield_card and self.main_game.information and "卡牌将要攻击" in self.main_game.information[1] and \
                self.main_game.information[3] == self._shield_card:
            if "战斗阶段" in self.main_game.information[1]:
                if self.main_game.threat_area.order[3]:
                    self.main_game.threat_area.order[5] = 1
                else:
                    self.main_game.threat_area.order[2] = 1
            else:
                if self.main_game.information[2].card_order[3]:
                    self.main_game.information[2].card_order[5] = 1
                else:
                    self.main_game.information[2].card_order[2] = 1
            self.main_game.information = None
        elif 4 < self.main_game.task_area.task_deck[
            self.main_game.task_area.task_number].card_number < 7 and not self._throwing and self.main_game.card_estimate(
            self) is not None:
            can_throw = False
            for card in self.main_game.scenario_area.card_group:
                if card.card_type == "敌军" and "老鼠" in card.card_attribute:
                    can_throw = True
                elif card.card_type == "敌军" and "老鼠" not in card.card_attribute:
                    return
            for card in self.main_game.clash_area.card_group:
                if card.card_type == "敌军" and "老鼠" in card.card_attribute:
                    can_throw = True
                elif card.card_type == "敌军" and "老鼠" not in card.card_attribute:
                    return
            if can_throw:
                self._throwing = True
                self.card_order = ["强制", 0, 0, False, 0, 0]

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "强制" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要执行强制效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 1:
            if self.card_order[2]:
                self._throwing = False
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌强制效果结算后", self]
                self.card_order = ["被弃除", 0, 0, False, 0, 0]
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
                self._shield_card = self.active_condition["暗影牌"][0]
                self.main_game.information = [0, "敌军卡牌暗影效果结算后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "弃除暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self._shield_card = None
                self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]].remove(
                    self)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]
