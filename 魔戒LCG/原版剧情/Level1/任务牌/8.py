from main import *


class Task(Task_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "8.jpg"  # 任务卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 任务卡牌的原始图像
        self.card_number = 8  # 任务序号，本数字决定游戏开始时，任务牌组中卡牌的放置顺序。
        self.card_name = "比翁之路"  # 本卡牌的名称。剧情中每个连续的场景都具有各自的独有名称
        self.plot_name = "穿越幽暗密林"  # 这个任务所属的剧情的名称
        self.plot_finish = True  # 剧情结束标志符，True表示这张卡完成后会通关此剧情。
        self.encounter_symbol = ("树", "蜘蛛", "半兽人")  # 遭遇信息，表明在该剧情中哪些遭遇牌应洗入遭遇牌组
        self.task_point = 10  # 任务点，表示要到达剧情的下一个场景，需要在本卡牌上放置的进度标记数量(None表示任务牌的A面没有任务点)
        self.rule_mark = ("永久",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "任务"  # 卡牌类型

        # 规则文字，布置说明、特殊效果以及在剧情中本场景产生的状态
        self.rule_text = "当昂哥立安的子嗣在场时，玩家不能通过本场景。如果玩家顺利通过本场景，玩家赢得游戏胜利。"

        # 剧情描述的斜体文字
        self.describe_text = "你试图沿着一条秘密的隐匿小径来躲避敌人..."

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        if not self.active_task_point:
            for card in self.main_game.scenario_area.card_group:
                if card.card_name == "昂哥立安的子嗣":
                    return
            for card in self.main_game.clash_area.card_group:
                if card.card_name == "昂哥立安的子嗣":
                    return
            self.active_task_point = -1
            self.main_game.game_victory()
