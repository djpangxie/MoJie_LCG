from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "地精射手.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (2, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "地精射手"  # 这张卡的名称
        self.clash_value = 48  # 这张卡的交锋值
        self.threat_force = 2  # 这张卡的威胁力
        self.attack_force = 2  # 这张卡的攻击力
        self.defense_force = 0  # 这张卡的防御力
        self.health_point = 2  # 这张卡的生命值
        self.encounter_symbol = "爪印"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("地精", "半兽人")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("永久", "强制")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "在遭遇阶段中，如果场景区中有其它敌军，玩家不能主动与地精射手交锋。\n强制：在战斗阶段结束时，如果地精射手在场景区中，对每位玩家控制的一名角色造成1点伤害。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = ""

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌被选中时，导入卡牌按钮树
    def import_button(self):
        super().import_button()
        if ("交锋", None) in self.main_game.button_option.buttons:
            for card in self.main_game.scenario_area.card_group:
                if card.card_type == "敌军" and card != self:
                    self.main_game.button_option.buttons.remove(("交锋", None))
                    self.main_game.button_option._set_current_button()
                    break

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self in self.main_game.scenario_area.card_group and self.main_game.information and \
                self.main_game.information[1] == "将要进入恢复阶段" and self.main_game.information[2] == "order" and str(
            self) not in self.main_game.information:
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["强制", 0, 0, False, 0, 0]

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "强制" and self.card_order[1] == 0:
            if self.card_order[2]:
                if hasattr(self, "select_role"):
                    del self.select_role
                self.card_order[1] += 1
            elif not self.main_game.information:
                if hasattr(self, "select_role"):
                    del self.select_role
                self.main_game.information = [0, "敌军卡牌将要执行强制效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                roles = []
                for card in self.main_game.role_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and card.active_health_point > 0:
                        roles.append(card)
                for card in self.main_game.clash_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and card.active_health_point > 0:
                        roles.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and card.active_health_point > 0:
                        roles.append(card)
                if roles:
                    self.select_role = self.main_game.card_select(roles)
                    self.main_game.information = [0, "敌军卡牌将要攻击", self, self.select_role]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "select_role"):
                    self.select_role.active_health_point -= 1
                    if self.select_role.active_health_point < 0:
                        self.select_role.active_health_point = 0
                    self.select_role.update_mask()
                    self.main_game.information = [0, "敌军卡牌攻击后", self, self.select_role]
                    self.select_role = "OK"
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "select_role") and self.select_role == "OK":
                    self.main_game.information = [0, "敌军卡牌强制效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if hasattr(self, "select_role"):
                    del self.select_role
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.card_order = [None, 0, 0, None, 0, 0]
