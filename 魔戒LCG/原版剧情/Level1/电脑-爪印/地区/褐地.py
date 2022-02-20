from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "褐地.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (2, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "褐地"  # 这张卡的名称
        self.threat_force = 5  # 这张卡的威胁力
        self.task_point = 1  # 任务点，表示探索完该地区需要的进度标记数量
        self.encounter_symbol = "爪印"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("荒原",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("强制",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "地区"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "强制：在玩家探索到褐地后，放置1枚进度标记到本地区上。"

        # 剧情描述的斜体文字
        self.describe_text = "他们已经来到了介于南幽暗密林和艾明穆尔之间，被称作“褐地”的广大荒地，连亚拉冈也不知道是什么样的疫病、战争或是魔王的伎俩，才把此地变得如此恐怖。 ——《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._successful = False

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_task_point > 0 and self.main_game.information and self.main_game.information[1] == "地区卡牌激活后" and \
                self.main_game.information[2] == self and str(self) not in self.main_game.information:
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["强制", 0, 0, False, 0, 0]

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "强制" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "地区卡牌将要执行强制效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self._successful = True
                self.main_game.information = [0, "地区卡牌强制效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if self._successful:
                    self.active_task_point -= 1
                    if self.active_task_point < 0:
                        self.active_task_point = 0
                    self.update_mask()
                self._successful = False
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.card_order = [None, 0, 0, None, 0, 0]
