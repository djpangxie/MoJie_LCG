from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "死灵法师的关隘.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (1, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "死灵法师的关隘"  # 这张卡的名称
        self.threat_force = 3  # 这张卡的威胁力
        self.task_point = 2  # 任务点，表示探索完该地区需要的进度标记数量
        self.encounter_symbol = "半兽人"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("要寨", "多尔哥多")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("探索",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "地区"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "探索：起始玩家必须从他的手牌中随机弃除两张卡牌，以探索本地区。"

        # 剧情描述的斜体文字
        self.describe_text = "它是个长满了黑暗枞树的地方，那里的树一株紧接着一株生长，也一起腐烂、枯萎。在其中一处岩石高地中央是多尔哥多，也就是魔王许久以前蛰伏的地方。 ——哈尔达，《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._successful = False

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_task_point > 0 and self.main_game.information and self.main_game.information[1] == "地区卡牌将要激活" and \
                self.main_game.information[2] == self and str(self) not in self.main_game.information:
            self.pause_card = self
            self.pause_card_order = self.card_order
            self.card_order = ["激活", 0, 0, False, 0, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None

    # 执行这张卡片的响应效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "激活" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if len(self.main_game.hand_area.card_group) > 1:
                    card1 = random.choice(tuple(self.main_game.hand_area.card_group.keys()))
                    card1.card_order = ["被弃除", 0, 0, False, 0, 0]
                    card2 = card1
                    while card1 == card2:
                        card2 = random.choice(tuple(self.main_game.hand_area.card_group.keys()))
                    card2.card_order = ["被弃除", 0, 0, False, 0, 0]
                    self._successful = True
                self.card_order[1] += 1
        elif self.card_order[0] == "激活" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if self._successful:
                    self.pause_card.card_order = self.pause_card_order
                    self.pause_card_order = None
                    self.pause_card = None
                    self.main_game.information = self.copy_information
                    self.main_game.information.append(str(self))
                    self.main_game.information[0] = 0
                    self.copy_information = None
                else:
                    self.pause_card = None
                    self.pause_card_order = None
                    self.copy_information = None
                    self.card_order = [None, 0, 0, None, 0, 0]
                self._successful = False
