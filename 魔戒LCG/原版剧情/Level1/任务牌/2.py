from main import *


class Task(Task_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "2.jpg"  # 任务卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 任务卡牌的原始图像
        self.card_number = 2  # 任务序号，本数字决定游戏开始时，任务牌组中卡牌的放置顺序。
        self.card_name = "苍蝇与蜘蛛"  # 本卡牌的名称。剧情中每个连续的场景都具有各自的独有名称
        self.plot_name = "穿越幽暗密林"  # 这个任务所属的剧情的名称
        self.plot_finish = False  # 剧情结束标志符，True表示这张卡完成后会通关此剧情。
        self.encounter_symbol = ("树", "蜘蛛", "半兽人")  # 遭遇信息，表明在该剧情中哪些遭遇牌应洗入遭遇牌组
        self.task_point = 8  # 任务点，表示要到达剧情的下一个场景，需要在本卡牌上放置的进度标记数量(-1表示任务牌的A面没有任务点)
        self.rule_mark = ()  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "任务"  # 卡牌类型

        # 规则文字，布置说明、特殊效果以及在剧情中本场景产生的状态
        self.rule_text = ""

        # 剧情描述的斜体文字
        self.describe_text = "他们所看见最恶心的东西就是蜘蛛网：这些浓密黑暗的网子拥有特别粗硬的蛛丝，往往会从一棵树延伸到另一棵树，或是缠挂在道路两边的树枝上。不过，倒是没有任何的蛛网挂在道路中央，不知道这是由于某种魔法将它们清除，还是有某种他们想不出来的原因。——《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        if not self.active_task_point:
            self.active_task_point = -1
            self.card_order = ["已完成", 0, 0, False, 0, 0]

    # 执行这张卡片的完成效果
    def run_card_order(self):
        if self.card_order[0] == "已完成" and self.card_order[1] == 0:
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
