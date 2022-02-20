from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "魔法溪流.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (2, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "魔法溪流"  # 这张卡的名称
        self.threat_force = 2  # 这张卡的威胁力
        self.task_point = 2  # 任务点，表示探索完该地区需要的进度标记数量
        self.encounter_symbol = "半兽人"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("森林",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("永久",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "地区"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "当魔法溪流处于激活的地区时，玩家不能补牌。"

        # 剧情描述的斜体文字
        self.describe_text = "我知道森林中有一条河流，强劲的黑水切过你们的道路，你们绝对不可以喝那里的水，也不可以在里面沐浴，因为，我听说河水之中有着强大的魔法，会让人昏昏欲睡，并且忘却一切。 ——比翁，《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self in self.main_game.task_area.region_card and self.main_game.information and "玩家将要补卡" in \
                self.main_game.information[1]:
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
