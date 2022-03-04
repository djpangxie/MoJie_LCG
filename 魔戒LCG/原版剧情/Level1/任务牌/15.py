from main import *


class Task(Task_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "15.jpg"  # 任务卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 任务卡牌的原始图像
        self.card_number = 1  # 任务序号，本数字决定游戏开始时，任务牌组中卡牌的放置顺序。
        self.card_name = "死灵法师之塔"  # 本卡牌的名称。剧情中每个连续的场景都具有各自的独有名称
        self.plot_name = "逃离多尔哥多"  # 这个任务所属的剧情的名称
        self.plot_finish = False  # 剧情结束标志符，True表示这张卡完成后会通关此剧情。
        self.encounter_symbol = ("塔楼", "蜘蛛", "半兽人")  # 遭遇信息，表明在该剧情中哪些遭遇牌应洗入遭遇牌组
        self.task_point = None  # 任务点，表示要到达剧情的下一个场景，需要在本卡牌上放置的进度标记数量(None表示任务牌的A面没有任务点)
        self.rule_mark = ("布置",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "任务"  # 卡牌类型

        # 规则文字，布置说明、特殊效果以及在剧情中本场景产生的状态
        self.rule_text = "布置：从遭遇牌组中搜寻三张目标牌，将它们展示并放置进场景区中。同时，将多尔哥多戒灵面朝上放置在任务牌组旁（但不作为在场）。然后，将遭遇牌组洗牌，为每张目标牌展示一张遭遇牌，并将目标牌附属到对应的遭遇牌上。"

        # 剧情描述的斜体文字
        self.describe_text = "凯兰崔尔女皇命你前往多尔哥多附近调查。调查期间，你的一位盟友被暗中埋伏的半兽人抓获，目前正被关押在地牢的监狱中..."

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.target_group = []

    # 卡牌侦听
    def card_listening(self):
        if self.main_game.information and "任务卡牌展示后" in self.main_game.information[1] and self.main_game.information[
            2] == "order" and self.main_game.information[3] == self:
            if self.main_game.xuanxiang % 10 == 3:
                card = Print_Card(self.main_game)
                card.card_image = pygame.image.load(os.path.join(self.card_dir, "Nightmare3.jpg")).convert()
                card.card_type = "噩梦难度"
                card.rule_text = "你正在进行噩梦模式。\n强制：当场景1B展示后，根据游戏中玩家的数量决定随机抓捕的英雄数量：1-2位玩家=1名英雄被捕。3位玩家=2名英雄被捕，4位玩家=3名英雄被捕。所有被捕的英雄面朝下放置并被视为“囚犯”，不能被使用、伤害，以及收集资源，直到他们被解救。（一位玩家不能被本效果抓捕一名以上的英雄。）"
                self.main_game.card_exhibition(card, self.main_game.settings.card_exhibition_time)
                self.main_game.encounter_area.nightmare_remove(
                    {"多尔哥多兽人": 2, "魔法溪流": 2, "密布蛛网的森林": 1, "幽暗密林山区": 3, "身陷蛛网": 2, "死灵法师之触": 1, "死灵法师的关隘": 1, "暗影笼罩": 2,
                     "塔楼前门": 2, "铁手铐": 1})
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
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                card = None
                if self.main_game.encounter_area.encounter_deck:
                    for card in self.main_game.encounter_area.encounter_deck:
                        if card.card_name == "多尔哥多戒灵":
                            break
                if card is not None and card.card_name == "多尔哥多戒灵":
                    self.main_game.encounter_area.encounter_deck.remove(card)
                    if self.main_game.encounter_area.encounter_affiliated:
                        self.main_game.encounter_area.encounter_affiliated.append(card)
                    else:
                        self.main_game.encounter_area.encounter_affiliated = [card]
                random.shuffle(self.main_game.encounter_area.encounter_deck)
                self.card_order[3] = True
                self.card_order[4] = 0
                self.card_order[5] = 0
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[3] = False
            elif not self.main_game.information and self.card_order[3]:
                if self.card_order[5]:
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
                    self.card_order[3] = False
                    self.card_order[4] = 0
                    self.card_order[5] = 0
                    self.card_order[1] += 1
                elif self.card_order[4] % 4 == 0:
                    card = None
                    if self.main_game.encounter_area.encounter_deck:
                        for card in self.main_game.encounter_area.encounter_deck:
                            if card.card_type == "目标":
                                break
                    if card is not None and card.card_type == "目标":
                        self.main_game.information = [0, "目标卡牌将要展示", self, card]
                        self.card_order[4] += 1
                    else:
                        self.card_order[3] = False
                        self.card_order[4] = 0
                        self.card_order[5] = 0
                        self.card_order[1] += 1
                elif self.card_order[4] % 4 == 1:
                    card = None
                    if self.main_game.encounter_area.encounter_deck:
                        for card in self.main_game.encounter_area.encounter_deck:
                            if card.card_type == "目标":
                                break
                    if card is not None and card.card_type == "目标":
                        self.encounter_card = card
                        self.main_game.encounter_area.encounter_deck.remove(card)
                        self.main_game.card_exhibition(self.encounter_card,
                                                       self.main_game.settings.card_exhibition_time)
                        self.main_game.scenario_area.card_group[self.encounter_card] = None
                        self.main_game.information = [0, "目标卡牌展示后", self, self.encounter_card]
                    self.card_order[4] += 1
                elif self.card_order[4] % 4 == 2:
                    if hasattr(self, "encounter_card"):
                        self.main_game.information = [0, "目标卡牌将要放置进场", self, self.encounter_card]
                    self.card_order[4] += 1
                elif self.card_order[4] % 4 == 3:
                    if hasattr(self, "encounter_card"):
                        self.main_game.information = [0, "目标卡牌放置进场后", self, self.encounter_card]
                        self.target_group.append(self.encounter_card)
                        del self.encounter_card
                    self.card_order[4] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌布置效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌将要展示", self, self.main_game.task_area.task_deck[
                    self.main_game.task_area.task_number + 1]]
                self.card_order[1] += 1
        elif self.card_order[0] == "布置" and self.card_order[1] == 5:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.card_exhibition(
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number + 1],
                    self.main_game.settings.card_exhibition_time)
                self.main_game.information = [0, "任务卡牌展示后", self, self.main_game.task_area.task_deck[
                    self.main_game.task_area.task_number + 1]]
                self.main_game.task_area.task_number += 1
                self.main_game.task_area.task_deck[
                    self.main_game.task_area.task_number].target_group = self.target_group
                self.main_game.task_area.task_deck[self.main_game.task_area.task_number].card_order = ["展示后", 0, 0,
                                                                                                       False, 0, 0]
                self.card_order = [None, 0, 0, None, 0, 0]
