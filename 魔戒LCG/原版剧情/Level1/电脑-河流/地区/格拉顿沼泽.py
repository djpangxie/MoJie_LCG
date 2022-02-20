from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "格拉顿沼泽.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 0, 3)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "格拉顿沼泽"  # 这张卡的名称
        self.threat_force = 10  # 这张卡的威胁力
        self.task_point = 10  # 任务点，表示探索完该地区需要的进度标记数量
        self.encounter_symbol = "河流"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("沼泽地",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("行动", "暗影")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "地区"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：对你控制的一名英雄造成1点伤害，以使格拉顿沼泽的威胁力减1，直到本阶段结束。任何玩家可以触发本效果。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：与防御玩家交锋的每个敌军获得+1攻击力直到本阶段结束。（如果本次攻击无人防御，则以+2攻击力代替。）"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None
        self._increment = 0
        self.enemy_group = None

    # 重置卡牌
    def reset_card(self):
        super().reset_card()
        self.phase_mark = None
        self._increment = 0
        self.enemy_group = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.phase_mark is not None and self.main_game.threat_area.current_phase != self.phase_mark:
            self.active_threat_force += self._increment
            self.update_mask()
            self._increment = 0
            self.phase_mark = None
        elif self.enemy_group is not None and "暗影牌" in self.active_condition and self.main_game.information and \
                self.main_game.information[1][-6:] == "卡牌将要离场" and self.main_game.information[2] == \
                self.active_condition["暗影牌"][0]:
            for card in self.enemy_group:
                card.active_attack_force -= self._increment
                if card.active_attack_force < 0:
                    card.active_attack_force = 0
                card.update_mask()
            self.enemy_group = None
            self._increment = 0
        elif self.enemy_group is not None:
            for card in self.main_game.clash_area.card_group:
                if card not in self.enemy_group and card.card_type == "敌军":
                    self.enemy_group.append(card)
                    card.active_attack_force += self._increment
                    card.update_mask()
            for card in self.enemy_group.copy():
                if not self.main_game.on_spot(card):
                    self.enemy_group.remove(card)

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "行动" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.select_hero = self.main_game.card_select(self.main_game.role_area.hero_group)
                self.main_game.information = [0, "地区卡牌将要攻击", self, self.select_hero]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 1:
            if self.card_order[2]:
                del self.select_hero
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.select_hero.active_health_point -= 1
                if self.select_hero.active_health_point < 0:
                    self.select_hero.active_health_point = 0
                self.select_hero.update_mask()
                if self.active_threat_force > 0:
                    self.active_threat_force -= 1
                    self._increment += 1
                    self.update_mask()
                    self.phase_mark = self.main_game.threat_area.current_phase
                self.main_game.information = [0, "地区卡牌攻击后", self, self.select_hero]
                del self.select_hero
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "地区卡牌将要执行暗影效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.active_condition["暗影牌"][0].active_condition["攻击中"]:
                    self._increment += 1
                else:
                    self._increment += 2
                self.enemy_group = []
                self.main_game.information = [0, "地区卡牌暗影效果结算后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "弃除暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                for card in self.enemy_group:
                    card.active_attack_force -= self._increment
                    if card.active_attack_force < 0:
                        card.active_attack_force = 0
                    card.update_mask()
                self.enemy_group = None
                self._increment = 0
                self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]].remove(
                    self)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]
