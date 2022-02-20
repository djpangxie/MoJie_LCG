from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "东口巡逻队.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (1, 1, 1)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "东口巡逻队"  # 这张卡的名称
        self.clash_value = 5  # 这张卡的交锋值
        self.threat_force = 3  # 这张卡的威胁力
        self.attack_force = 3  # 这张卡的攻击力
        self.defense_force = 1  # 这张卡的防御力
        self.health_point = 2  # 这张卡的生命值
        self.encounter_symbol = "树"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("地精", "半兽人")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("暗影",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = ""

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：攻击的敌军获得+1攻击力。(如果本次攻击无人防御，你的威胁等级再上升3点。)"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._increment = 0

    # 重置卡牌
    def reset_card(self):
        super().reset_card()
        self._increment = 0

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
                self.active_condition["暗影牌"][0].active_attack_force += 1
                self.active_condition["暗影牌"][0].update_mask()
                self._increment += 1
                if not self.active_condition["暗影牌"][0].active_condition["攻击中"]:
                    self.main_game.information = [0, "玩家将要上升威胁等级", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if not self.active_condition["暗影牌"][0].active_condition["攻击中"]:
                    self.main_game.threat_area.threat_value += 3
                    self.main_game.information = [0, "玩家上升威胁等级后", self]
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
                self.active_condition["暗影牌"][0].active_attack_force -= self._increment
                if self.active_condition["暗影牌"][0].active_attack_force < 0:
                    self.active_condition["暗影牌"][0].active_attack_force = 0
                self.active_condition["暗影牌"][0].update_mask()
                self._increment = 0
                self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]].remove(self)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]
