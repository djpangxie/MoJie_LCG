from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "陷入绝望.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "陷入绝望"  # 这张卡的名称
        self.encounter_symbol = "爪印"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("展示后", "暗影")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "阴谋"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "展示后：从当前任务牌上移除4枚进度标记。（如果任务牌上少于4枚进度标记，则将其全部移除。）"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = "暗影：防御角色不计算其防御力。"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._threat_increment = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self._threat_increment is not None:
            for role in self._threat_increment.copy():
                if not self.main_game.on_spot(role):
                    self._threat_increment.pop(role)
        if self.main_game.information and self.main_game.information[1][-5:] == "卡牌展示后" and self.main_game.information[
            3] == self and str(self) not in self.main_game.information:
            if self.main_game.information[2] != "order":
                self.pause_card = self.main_game.information[2]
                self.pause_card_order = self.main_game.information[2].card_order
                self.main_game.information[2].card_order = [None, -1, 0, None, -1, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["展示后", 0, 0, False, 0, 0]
        elif self._threat_increment is not None and "暗影牌" in self.active_condition and "攻击中" not in \
                self.active_condition["暗影牌"][0].active_condition:
            for role in self._threat_increment:
                role.active_defense_force += self._threat_increment[role]
                role.update_mask()
            self._threat_increment = None
        elif self._threat_increment is not None and "暗影牌" in self.active_condition and self.active_condition["暗影牌"][
            0] in self.main_game.clash_area.card_group and "分配暗影" in self.active_condition["暗影牌"][
            0].active_condition and self in self.active_condition["暗影牌"][0].active_condition["分配暗影"] and "攻击中" in \
                self.active_condition["暗影牌"][0].active_condition:
            for role in self.active_condition["暗影牌"][0].active_condition["攻击中"]:
                if "宣告防御" in role.active_condition and self.active_condition["暗影牌"][0] in role.active_condition[
                    "宣告防御"] and self.main_game.on_spot(role) and role.active_defense_force:
                    if role in self._threat_increment:
                        self._threat_increment[role] += role.active_defense_force
                    else:
                        self._threat_increment[role] = role.active_defense_force
                    role.active_defense_force = 0
                    role.update_mask()

    # 执行这张卡片的展示后效果
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
                if self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point and \
                        self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point > 0:
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point += 4
                    if self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point > \
                            self.main_game.task_area.task_deck[self.main_game.task_area.task_number].task_point:
                        self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point = \
                            self.main_game.task_area.task_deck[self.main_game.task_area.task_number].task_point
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number].update_mask()
                self.main_game.information = [0, "阴谋卡牌展示后效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and not self.main_game.response_conflict:
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
                self.main_game.information = [0, "阴谋卡牌将要执行暗影效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "结算暗影" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self._threat_increment = {}
                self.main_game.information = [0, "阴谋卡牌暗影效果结算后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "弃除暗影" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self._threat_increment = None
                self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]].remove(self)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]
