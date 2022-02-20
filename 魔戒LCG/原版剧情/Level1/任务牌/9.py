from main import *


class Task(Task_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "9.jpg"  # 任务卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 任务卡牌的原始图像
        self.card_number = 1  # 任务序号，本数字决定游戏开始时，任务牌组中卡牌的放置顺序。
        self.card_name = "来到河岸边..."  # 本卡牌的名称。剧情中每个连续的场景都具有各自的独有名称
        self.plot_name = "安度因河之旅"  # 这个任务所属的剧情的名称
        self.plot_finish = False  # 剧情结束标志符，True表示这张卡完成后会通关此剧情。
        self.encounter_symbol = ("河流", "眼球", "爪印", "半兽人")  # 遭遇信息，表明在该剧情中哪些遭遇牌应洗入遭遇牌组
        self.task_point = None  # 任务点，表示要到达剧情的下一个场景，需要在本卡牌上放置的进度标记数量(None表示任务牌的A面没有任务点)
        self.rule_mark = ("布置",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "任务"  # 卡牌类型

        # 规则文字，布置说明、特殊效果以及在剧情中本场景产生的状态
        self.rule_text = "布置：每位玩家从遭遇牌组顶端展示一张卡牌，并将其加入场景区中。"

        # 剧情描述的斜体文字
        self.describe_text = "携带着捎给凯兰崔尔女皇的紧急信件走出了幽暗密林，现在你必须沿着安度因河一路向南，前往罗瑞安森林。虽然幽暗密林已经在你身后，但依然意识到某种东西对你紧追不舍，因此你加快了步伐..."

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.troll_enemy = []

    # 噩梦难度下使巨魔敌军不受附属并且在遭遇牌组耗尽的时候将遭遇弃牌堆洗回遭遇牌组
    def reject_affiliated(self):
        if self.main_game.xuanxiang % 10 == 3:
            if self.main_game.information and "卡牌将要附属" in self.main_game.information[1] and self.main_game.information[
                3] in self.troll_enemy and "不受附属" in self.main_game.information[3].rule_mark:
                if self.main_game.information[2] == "order":
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
            for enemy in self.troll_enemy:
                if self.main_game.card_estimate(
                        enemy) is not None and "不受附属" in enemy.rule_mark and "被附属" in enemy.active_condition:
                    for affiliated in enemy.active_condition["被附属"]:
                        if not affiliated.card_order[0]:
                            affiliated.card_order = ["弃除附属", 0, 0, False, 0, 0]
            if not self.main_game.encounter_area.encounter_deck and self.main_game.encounterdiscard_area.encounterdiscard_deck:
                self.main_game.encounter_area.encounter_deck = self.main_game.encounterdiscard_area.encounterdiscard_deck
                self.main_game.encounterdiscard_area.encounterdiscard_deck = []
                for card in self.main_game.encounter_area.encounter_deck:
                    card.reset_card()
                    card.update_mask()
                random.shuffle(self.main_game.encounter_area.encounter_deck)

    # 卡牌侦听
    def card_listening(self):
        self.reject_affiliated()
        if self.main_game.information and "任务卡牌展示后" in self.main_game.information[1] and self.main_game.information[
            2] == "order" and self.main_game.information[3] == self:
            if self.main_game.xuanxiang % 10 == 3:
                card = Print_Card(self.main_game)
                card.card_image = pygame.image.load(os.path.join(self.card_dir, "Nightmare2.jpg")).convert()
                card.card_type = "噩梦难度"
                card.rule_text = "你正在进行噩梦模式。\n所有的巨魔敌军获得规则文字：“不受附属。”\n如果遭遇牌组耗尽(任何时候)，将遭遇弃牌堆洗回遭遇牌组。"
                self.main_game.card_exhibition(card, self.main_game.settings.card_exhibition_time)
                self.main_game.encounter_area.nightmare_remove(
                    {"邪恶的暴风雪": 3, "暗藏危险的迷雾": 2, "安度因河岸": 2, "多尔哥多兽人": 3, "魔法溪流": 2, "陷入绝望": 2, "迷雾山脉地精": 3,
                     "死灵法师的关隘": 2})
            self.card_order = ["布置", 0, 0, False, 0, 0]
            self.main_game.information = None

    # 执行这张卡片的布置效果
    def run_card_order(self):
        if self.card_order[0] == "布置" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.xuanxiang % 10 == 3:
                    for card in self.main_game.encounter_area.encounter_deck:
                        if card.card_type == "敌军" and "巨魔" in card.card_attribute and "不受附属" not in card.rule_mark:
                            card.rule_mark = list(card.rule_mark)
                            card.rule_mark.append("不受附属")
                            card.rule_mark = tuple(card.rule_mark)
                            card.rule_text = "不受附属。\n" + card.rule_text
                            self.troll_enemy.append(card)
                self.main_game.information = [0, "任务卡牌将要执行布置效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.information = [0, "遭遇卡牌将要展示", self, self.main_game.encounter_area.encounter_deck[0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 2:
            if self.card_order[2]:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.encounter_area.encounter_deck[0].reset_card()
                    self.main_game.encounter_area.encounter_deck[0].update_mask()
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    self.encounter_card = self.main_game.encounter_area.encounter_deck.pop(0)
                    self.main_game.card_exhibition(self.encounter_card, self.main_game.settings.card_exhibition_time)
                    self.main_game.scenario_area.card_group[self.encounter_card] = None
                    self.main_game.information = [0, "遭遇卡牌展示后", self, self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌将要放置进场", self,
                                                  self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 4:
            if self.card_order[2]:
                if hasattr(self, "encounter_card"):
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
                if hasattr(self, "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌放置进场后", self,
                                                  self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 5:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "encounter_card"):
                    del self.encounter_card
                self.main_game.information = [0, "任务卡牌布置效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 6:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌将要展示", self, self.main_game.task_area.task_deck[
                    self.main_game.task_area.task_number + 1]]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 7:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.card_exhibition(
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number + 1],
                    self.main_game.settings.card_exhibition_time)
                self.main_game.information = [0, "任务卡牌展示后", self, self.main_game.task_area.task_deck[self.main_game.task_area.task_number + 1]]
                self.main_game.task_area.task_number += 1
                self.main_game.task_area.task_deck[self.main_game.task_area.task_number].card_order = ["展示后", 0, 0, False, 0, 0]
                self.card_order = [None, 0, 0, None, 0, 0]
