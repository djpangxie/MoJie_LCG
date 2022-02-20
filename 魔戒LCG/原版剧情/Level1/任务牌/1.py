from main import *


class Task(Task_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "1.jpg"  # 任务卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 任务卡牌的原始图像
        self.card_number = 1  # 任务序号，本数字决定游戏开始时，任务牌组中卡牌的放置顺序。
        self.card_name = "苍蝇与蜘蛛"  # 本卡牌的名称。剧情中每个连续的场景都具有各自的独有名称
        self.plot_name = "穿越幽暗密林"  # 这个任务所属的剧情的名称
        self.plot_finish = False  # 剧情结束标志符，True表示这张卡完成后会通关此剧情。
        self.encounter_symbol = ("树", "蜘蛛", "半兽人")  # 遭遇信息，表明在该剧情中哪些遭遇牌应洗入遭遇牌组
        self.task_point = None  # 任务点，表示要到达剧情的下一个场景，需要在本卡牌上放置的进度标记数量(None表示任务牌的A面没有任务点)
        self.rule_mark = ("布置",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "任务"  # 卡牌类型

        # 规则文字，布置说明、特殊效果以及在剧情中本场景产生的状态
        self.rule_text = "布置：从遭遇牌组中搜寻一张森林蜘蛛和一张老林路，并加入场景区中。然后，将遭遇牌组洗牌。"

        # 剧情描述的斜体文字
        self.describe_text = "你正在穿越幽暗密林，携带着一封来自瑟兰督伊王的紧急信件前往罗瑞安，亲手交给凯兰崔尔女皇。当你沿着黑暗的小径前行时，周围的蜘蛛也正在逐渐向你逼近..."

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        if self.main_game.information and "任务卡牌展示后" in self.main_game.information[1] and self.main_game.information[
            2] == "order" and self.main_game.information[3] == self:
            if self.main_game.xuanxiang % 10 == 3:
                card = Print_Card(self.main_game)
                card.card_image = pygame.image.load(os.path.join(self.card_dir, "Nightmare1.jpg")).convert()
                card.card_type = "噩梦难度"
                card.rule_text = "你正在进行噩梦模式。\n强制：在布置时，每位玩家从遭遇牌组展示一张卡牌并将其加入场景区中。"
                self.main_game.card_exhibition(card, self.main_game.settings.card_exhibition_time)
                self.main_game.encounter_area.nightmare_remove(
                    {"昂哥立安的子嗣": 1, "黑森林蝙蝠": 1, "森林蜘蛛": 3, "多尔哥多兽人": 3, "老林路": 1, "森林之门": 2, "幽暗密林山区": 3, "身陷蛛网": 2})
            self.card_order = ["布置", 0, 0, False, 0, 0]
            self.main_game.information = None

    # 执行这张卡片的布置效果
    def run_card_order(self):
        if self.card_order[0] == "布置" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌将要执行布置效果", self]
                self.card_order[3] = True
                self.card_order[4] = 0
                self.card_order[5] = 0
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[3] = False
            elif not self.main_game.information:
                if self.card_order[3] and self.card_order[4] == 0:
                    if self.card_order[5]:
                        self.card_order[4] += 1
                    else:
                        card = None
                        if self.main_game.encounter_area.encounter_deck:
                            for card in self.main_game.encounter_area.encounter_deck:
                                if card.card_name == "森林蜘蛛":
                                    break
                        if card is not None and card.card_name == "森林蜘蛛":
                            self.main_game.information = [0, card.card_type + "卡牌将要放置进场", self, card]
                            self.card_order[4] += 1
                        else:
                            self.card_order[4] += 2
                elif self.card_order[3] and self.card_order[4] == 1:
                    if self.card_order[5]:
                        self.card_order[4] += 1
                        self.card_order[5] -= 1
                    else:
                        card = None
                        if self.main_game.encounter_area.encounter_deck:
                            for card in self.main_game.encounter_area.encounter_deck:
                                if card.card_name == "森林蜘蛛":
                                    break
                        if card is not None and card.card_name == "森林蜘蛛":
                            self.main_game.encounter_area.encounter_deck.remove(card)
                            self.main_game.scenario_area.card_group[card] = None
                            self.main_game.information = [0, card.card_type + "卡牌放置进场后", self, card]
                        self.card_order[4] += 1
                elif self.card_order[3] and self.card_order[4] == 2:
                    if self.card_order[5]:
                        self.card_order[4] += 1
                    else:
                        card = None
                        if self.main_game.encounter_area.encounter_deck:
                            for card in self.main_game.encounter_area.encounter_deck:
                                if card.card_name == "老林路":
                                    break
                        if card is not None and card.card_name == "老林路":
                            self.main_game.information = [0, card.card_type + "卡牌将要放置进场", self, card]
                            self.card_order[4] += 1
                        else:
                            self.card_order[4] += 2
                elif self.card_order[3] and self.card_order[4] == 3:
                    if self.card_order[5]:
                        self.card_order[4] += 1
                        self.card_order[5] -= 1
                    else:
                        card = None
                        if self.main_game.encounter_area.encounter_deck:
                            for card in self.main_game.encounter_area.encounter_deck:
                                if card.card_name == "老林路":
                                    break
                        if card is not None and card.card_name == "老林路":
                            self.main_game.encounter_area.encounter_deck.remove(card)
                            self.main_game.scenario_area.card_group[card] = None
                            self.main_game.information = [0, card.card_type + "卡牌放置进场后", self, card]
                        self.card_order[4] += 1
                elif self.card_order[3] and self.card_order[4] == 4:
                    if self.card_order[5]:
                        self.card_order[5] = 0
                    else:
                        random.shuffle(self.main_game.encounter_area.encounter_deck)
                        self.card_order[3] = False
                        self.card_order[4] = 0
                        self.card_order[5] = 0
                        self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌布置效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if self.main_game.xuanxiang % 10 == 3:
                    self.main_game.information = [0, "任务卡牌将要执行强制效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if self.main_game.xuanxiang % 10 == 3 and self.main_game.encounter_area.encounter_deck:
                    self.main_game.information = [0, "遭遇卡牌将要展示", self, self.main_game.encounter_area.encounter_deck[0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 5:
            if self.card_order[2]:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.encounter_area.encounter_deck[0].reset_card()
                    self.main_game.encounter_area.encounter_deck[0].update_mask()
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.xuanxiang % 10 == 3 and self.main_game.encounter_area.encounter_deck:
                    self.encounter_card = self.main_game.encounter_area.encounter_deck.pop(0)
                    self.main_game.card_exhibition(self.encounter_card, self.main_game.settings.card_exhibition_time)
                    self.main_game.scenario_area.card_group[self.encounter_card] = None
                    self.main_game.information = [0, "遭遇卡牌展示后", self, self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 6:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.xuanxiang % 10 == 3 and hasattr(self,
                                                                  "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌将要放置进场", self,
                                                  self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 7:
            if self.card_order[2]:
                if self.main_game.xuanxiang % 10 == 3 and hasattr(self, "encounter_card"):
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
                if self.main_game.xuanxiang % 10 == 3 and hasattr(self,
                                                                  "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌放置进场后", self,
                                                  self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 8:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "encounter_card"):
                    del self.encounter_card
                if self.main_game.xuanxiang % 10 == 3:
                    self.main_game.information = [0, "任务卡牌强制效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 9:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌将要展示", self, self.main_game.task_area.task_deck[
                    self.main_game.task_area.task_number + 1]]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 10:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.card_exhibition(
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number + 1],
                    self.main_game.settings.card_exhibition_time)
                self.main_game.information = [0, "任务卡牌展示后", self,
                                              self.main_game.task_area.task_deck[
                                                  self.main_game.task_area.task_number + 1]]
                self.main_game.task_area.task_number += 1
                self.card_order = [None, 0, 0, None, 0, 0]
