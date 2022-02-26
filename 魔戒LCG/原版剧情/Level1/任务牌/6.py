from main import *


class Task(Task_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "6.jpg"  # 任务卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 任务卡牌的原始图像
        self.card_number = 6  # 任务序号，本数字决定游戏开始时，任务牌组中卡牌的放置顺序。
        self.card_name = "“不要离开小径！”"  # 本卡牌的名称。剧情中每个连续的场景都具有各自的独有名称
        self.plot_name = "穿越幽暗密林"  # 这个任务所属的剧情的名称
        self.plot_finish = True  # 剧情结束标志符，True表示这张卡完成后会通关此剧情。
        self.encounter_symbol = ("树", "蜘蛛", "半兽人")  # 遭遇信息，表明在该剧情中哪些遭遇牌应洗入遭遇牌组
        self.task_point = 0  # 任务点，表示要到达剧情的下一个场景，需要在本卡牌上放置的进度标记数量(None表示任务牌的A面没有任务点)
        self.rule_mark = ("展示后",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "任务"  # 卡牌类型

        # 规则文字，布置说明、特殊效果以及在剧情中本场景产生的状态
        self.rule_text = "展示后：每位玩家必须从遭遇牌组和遭遇弃牌堆中搜寻一张由自己选择的蜘蛛卡牌，并将其加入场景区中。\n玩家必须找到并消灭昂哥立安的子嗣才能赢得本次游戏的胜利。"

        # 剧情描述的斜体文字
        self.describe_text = "阴影愈发地黑暗，你意识到一个邪恶的物体正打算将你拖离小径。你必须消灭它才能通过这里。"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        if self.main_game.information and self.main_game.information[1] == "敌军卡牌被消灭后" and self.main_game.information[
            2].card_name == "昂哥立安的子嗣":
            self.main_game.information = None
            self.main_game.game_victory()

    # 执行这张卡片的展示后效果
    def run_card_order(self):
        if self.card_order[0] == "展示后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌将要执行展示后效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                spider_cards = []
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    for card in self.main_game.encounterdiscard_area.encounterdiscard_deck:
                        if card.card_type == "敌军" and "蜘蛛" in card.card_attribute:
                            spider_cards.append(card)
                if self.main_game.encounter_area.encounter_deck:
                    for card in self.main_game.encounter_area.encounter_deck:
                        if card.card_type == "敌军" and "蜘蛛" in card.card_attribute:
                            spider_cards.append(card)
                if spider_cards:
                    self.select_card = self.main_game.card_select(spider_cards)
                    self.main_game.information = [0, self.select_card.card_type + "卡牌将要放置进场", self, self.select_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if hasattr(self, "select_card"):
                    if self.main_game.encounterdiscard_area.encounterdiscard_deck and self.select_card in self.main_game.encounterdiscard_area.encounterdiscard_deck:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck.remove(self.select_card)
                        self.select_card.reset_card()
                        self.select_card.update_mask()
                        self.main_game.scenario_area.card_group[self.select_card] = None
                        self.main_game.information = [0, self.select_card.card_type + "卡牌放置进场后", self, self.select_card]
                    elif self.main_game.encounter_area.encounter_deck and self.select_card in self.main_game.encounter_area.encounter_deck:
                        self.main_game.encounter_area.encounter_deck.remove(self.select_card)
                        self.main_game.scenario_area.card_group[self.select_card] = None
                        self.main_game.information = [0, self.select_card.card_type + "卡牌放置进场后", self, self.select_card]
                    del self.select_card
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌展示后效果结算后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
