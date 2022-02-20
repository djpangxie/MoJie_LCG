from main import *


class Task(Task_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "16.jpg"  # 任务卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 任务卡牌的原始图像
        self.card_number = 2  # 任务序号，本数字决定游戏开始时，任务牌组中卡牌的放置顺序。
        self.card_name = "死灵法师之塔"  # 本卡牌的名称。剧情中每个连续的场景都具有各自的独有名称
        self.plot_name = "逃离多尔哥多"  # 这个任务所属的剧情的名称
        self.plot_finish = False  # 剧情结束标志符，True表示这张卡完成后会通关此剧情。
        self.encounter_symbol = ("塔楼", "蜘蛛", "半兽人")  # 遭遇信息，表明在该剧情中哪些遭遇牌应洗入遭遇牌组
        self.task_point = 9  # 任务点，表示要到达剧情的下一个场景，需要在本卡牌上放置的进度标记数量(-1表示任务牌的A面没有任务点)
        self.rule_mark = ("展示后", "永久")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "任务"  # 卡牌类型

        # 规则文字，布置说明、特殊效果以及在剧情中本场景产生的状态
        self.rule_text = "展示后：随机选择一张英雄牌（由玩家将所有英雄收集在一起）并面朝下放置。该英雄目前被视为“囚犯”，不能被使用、伤害，以及收集资源，直到在本剧情后续中被“解救”（卡牌效果所示）。\n所有玩家共为一组，每回合中不能打出超过一张的盟友牌。\n玩家不能前往本剧情的下一个场景，除非他们已经至少获取了一张目标牌。"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.target_group = None
        self.round_mark = None

    # 卡牌侦听
    def card_listening(self):
        if self.round_mark is None and self.main_game.information and self.main_game.information[1] == "玩家成功打出卡牌后" and \
                self.main_game.information[2].card_type == "盟友":
            self.round_mark = self.main_game.threat_area.round_number
        elif self.round_mark is not None and self.main_game.information and self.main_game.information[
            1] == "玩家将要打出卡牌" and self.main_game.information[2].card_type == "盟友":
            self.main_game.information[2].card_order = [None, 0, 0, False, 0, 0]
            del self.main_game.information[2].deduction_heros
            self.main_game.information = None
        elif self.round_mark is not None and self.main_game.threat_area.round_number != self.round_mark:
            self.round_mark = None
        if not self.active_task_point:
            for affiliated in self.target_group:
                if "附属到" in affiliated.active_condition:
                    for card in affiliated.active_condition["附属到"]:
                        if self.main_game.player_control(card):
                            self.active_task_point = -1
                            self.card_order = ["已完成", 0, 0, False, 0, 0]
                            return

    # 执行这张卡片的完成效果
    def run_card_order(self):
        if self.card_order[0] == "展示后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "任务卡牌将要执行展示后效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "展示后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                hero = random.choice(self.main_game.role_area.hero_group)
                if hero.card_order[0]:
                    return
                else:
                    hero.card_order = ["离场", 0, 0, False, 0, 0, "遭遇附属区"]
                self.main_game.information = [0, "任务卡牌展示后效果结算后", self]
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
                self.round_mark = None
                self.main_game.card_exhibition(
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number + 1],
                    self.main_game.settings.card_exhibition_time)
                self.main_game.information = [0, "任务卡牌展示后", self,
                                              self.main_game.task_area.task_deck[
                                                  self.main_game.task_area.task_number + 1]]
                self.main_game.task_area.task_number += 1
                self.main_game.task_area.task_deck[self.main_game.task_area.task_number].target_group = self.target_group
                self.main_game.task_area.task_deck[self.main_game.task_area.task_number].card_order = ["展示后", 0, 0,
                                                                                                       False, 0, 0]
                self.card_order = [None, 0, 0, None, 0, 0]
