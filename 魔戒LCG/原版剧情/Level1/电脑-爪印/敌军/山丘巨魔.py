from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "山丘巨魔.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (1, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "山丘巨魔"  # 这张卡的名称
        self.clash_value = 30  # 这张卡的交锋值
        self.threat_force = 1  # 这张卡的威胁力
        self.attack_force = 6  # 这张卡的攻击力
        self.defense_force = 3  # 这张卡的防御力
        self.health_point = 9  # 这张卡的生命值
        self.encounter_symbol = "爪印"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("巨魔",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("永久",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 4  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "山丘巨魔造成的过量战斗伤害（超过被攻击角色当前生命值的伤害）必须分配到上升你等量的威胁等级上。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = ""

        # 剧情描述的斜体文字
        self.describe_text = "“昨天羊腿、今天羊腿，妈呀，希望明天看起来不像羊腿！” ——食人妖，《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._defender = None
        self._excess = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.main_game.information and "敌军卡牌将要攻击" in self.main_game.information[1] and self.main_game.information[2] == self:
            if "战斗阶段" in self.main_game.information[1]:
                self._defender = self.main_game.information[3]
                self._excess = self.main_game.threat_area.damage - self._defender.active_health_point
        elif self.active_health_point > 0 and self._defender and self.main_game.information and "敌军卡牌攻击后" in \
                self.main_game.information[1] and self.main_game.information[2] == self and self.main_game.information[
            3] == self._defender and self._defender.active_health_point <= 0 and self._excess > 0:
            self.card_order = ["过量伤害", 0, 0, False, 0, 0]
            self._defender = None

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "过量伤害" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "玩家将要上升威胁等级", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "过量伤害" and self.card_order[1] == 1:
            if self.card_order[2]:
                self._excess = None
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.threat_area.threat_value += self._excess
                self.main_game.information = [0, "玩家上升威胁等级后", self]
                self._excess = None
                self.card_order = [None, 0, 0, None, 0, 0]
