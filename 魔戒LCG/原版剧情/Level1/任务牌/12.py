from main import *


class Task(Task_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "12.jpg"  # 任务卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 任务卡牌的原始图像
        self.card_number = 4  # 任务序号，本数字决定游戏开始时，任务牌组中卡牌的放置顺序。
        self.card_name = "安度因河的航程"  # 本卡牌的名称。剧情中每个连续的场景都具有各自的独有名称
        self.plot_name = "安度因河之旅"  # 这个任务所属的剧情的名称
        self.plot_finish = False  # 剧情结束标志符，True表示这张卡完成后会通关此剧情。
        self.encounter_symbol = ("河流", "眼球", "爪印", "半兽人")  # 遭遇信息，表明在该剧情中哪些遭遇牌应洗入遭遇牌组
        self.task_point = 16  # 任务点，表示要到达剧情的下一个场景，需要在本卡牌上放置的进度标记数量(None表示任务牌的A面没有任务点)
        self.rule_mark = ("永久",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "任务"  # 卡牌类型

        # 规则文字，布置说明、特殊效果以及在剧情中本场景产生的状态
        self.rule_text = "每个任务阶段，从遭遇牌组中额外展示一张卡牌。在遭遇阶段中，不进行交锋检定。（每位玩家在每个遭遇阶段中依然可以选择主动交锋一个敌军。）"

        # 剧情描述的斜体文字
        self.describe_text = "由于敌兵的袭击，要保持好平衡并有效地击退他们变得困难重重。"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        self.main_game.task_area.task_deck[
            self.main_game.task_area.task_number - self.card_number + 1].reject_affiliated()
        if self.main_game.information and self.main_game.information[1] == "将要离开集结步骤" and self.main_game.information[
            2] == "order" and str(self) not in self.main_game.information:
            self.main_game.information.append(str(self))
            self.card_order = ["额外遭遇牌", 0, 0, False, 0, 0]
        elif self.main_game.information and self.main_game.information[1] == "将要进入交锋检定步骤" and \
                self.main_game.information[2] == "order":
            self.main_game.threat_area.order[2] = 1
            self.main_game.information = None
        elif not self.active_task_point:
            self.active_task_point = -1
            self.card_order = ["已完成", 0, 0, False, 0, 0]

    # 执行这张卡片的完成效果
    def run_card_order(self):
        if self.card_order[0] == "额外遭遇牌" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.information = [0, "遭遇卡牌将要展示", self, self.main_game.encounter_area.encounter_deck[0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "额外遭遇牌" and self.card_order[1] == 1:
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
        elif self.card_order[0] == "额外遭遇牌" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌将要放置进场", self,
                                                  self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "额外遭遇牌" and self.card_order[1] == 3:
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
                    del self.encounter_card
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if hasattr(self, "encounter_card"):
                    if self.encounter_card.card_type != "阴谋":
                        self.main_game.information = [0, self.encounter_card.card_type + "卡牌放置进场后", self,
                                                      self.encounter_card]
                    del self.encounter_card
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "已完成" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌完成后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "已完成" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌将要展示", self, self.main_game.task_area.task_deck[
                    self.main_game.task_area.task_number + 1]]
                self.card_order[1] += 1
        elif self.card_order[0] == "已完成" and self.card_order[1] == 2:
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
                self.main_game.task_area.task_deck[self.main_game.task_area.task_number].card_order = ["展示后", 0, 0,
                                                                                                       False, 0, 0]
                self.card_order = [None, 0, 0, None, 0, 0]
