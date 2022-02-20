from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "幽暗密林的蜘蛛.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 0, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "幽暗密林的蜘蛛"  # 这张卡的名称
        self.clash_value = 18  # 这张卡的交锋值
        self.threat_force = 3  # 这张卡的威胁力
        self.attack_force = 2  # 这张卡的攻击力
        self.defense_force = 2  # 这张卡的防御力
        self.health_point = 4  # 这张卡的生命值
        self.encounter_symbol = "树"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("生物", "蜘蛛")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("暗影",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "当幽暗密林的蜘蛛与你交锋时，你每控制一名已横置的角色，其获得+1攻击力。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：选择并横置一名你控制的角色。如果本次攻击无人防御，同时对其造成2点伤害。"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.transverse_number = 0

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self in self.main_game.clash_area.card_group:
            role_number = 0
            for card in self.main_game.role_area.card_group:
                if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" in card.active_condition:
                    role_number += 1
            if role_number != self.transverse_number:
                self.active_attack_force += role_number - self.transverse_number
                if self.active_attack_force < 0:
                    self.active_attack_force = 0
                self.update_mask()
                self.transverse_number = role_number
        elif self.transverse_number:
            self.active_attack_force -= self.transverse_number
            if self.active_attack_force < 0:
                self.active_attack_force = 0
            self.update_mask()
            self.transverse_number = 0

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "结算暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要执行暗影效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if hasattr(self, "select_role"):
                    del self.select_role
                roles = []
                for card in self.main_game.role_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" not in card.active_condition:
                        roles.append(card)
                for card in self.main_game.clash_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" not in card.active_condition:
                        roles.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" not in card.active_condition:
                        roles.append(card)
                if roles:
                    self.select_role = self.main_game.card_select(roles)
                    self.main_game.information = [0, self.select_role.card_type + "卡牌将要横置", self, self.select_role]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 2:
            if self.card_order[2]:
                if hasattr(self, "select_role"):
                    del self.select_role
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if hasattr(self, "select_role") and "已横置" not in self.select_role.active_condition:
                    if not self.active_condition["暗影牌"][0].active_condition["攻击中"]:
                        self.select_role.active_health_point -= 2
                        if self.select_role.active_health_point < 0:
                            self.select_role.active_health_point = 0
                    self.select_role.active_condition["已横置"] = None
                    self.select_role.update_mask()
                    self.main_game.information = [0, self.select_role.card_type + "卡牌横置后", self, self.select_role]
                    del self.select_role
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
