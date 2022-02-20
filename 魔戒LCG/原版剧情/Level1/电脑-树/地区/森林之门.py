from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "森林之门.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (2, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "森林之门"  # 这张卡的名称
        self.threat_force = 2  # 这张卡的威胁力
        self.task_point = 4  # 任务点，表示探索完该地区需要的进度标记数量
        self.encounter_symbol = "树"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("森林",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("响应",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "地区"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "响应：在你探索到森林之门后，起始玩家可以补两张卡牌。"

        # 剧情描述的斜体文字
        self.describe_text = "这条道路十分狭窄，在树木之间蜿蜒前进。很快，入口的亮光看起来就成了远处的余光，四周的一片死寂让他们的脚步声成了沉重的鼓声，所有的树木似乎都饶有兴味地侧耳倾听着。 ——《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_task_point > 0 and self.main_game.information and self.main_game.information[1] == "地区卡牌激活后" and \
                self.main_game.information[2] == self and "响应后" not in self.active_condition:
            self.main_game.response_conflict = True
            self.card_order = ["响应", 0, 0, False, 0, 0]
            self.active_condition["响应后"] = None

    # 执行这张卡片的响应效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "响应" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif self.main_game.response_pause != True:
                self.main_game.response_pause = True
                self.main_game.button_option.import_button(str(self), (
                    ("响应-" + self.card_name, None), ("不响应-" + self.card_name, None)))
                if self.main_game.button_option.option // 100000 == 1:
                    self.card_order[3] = True
                    self.card_order[4] = 0
                    self.card_order[5] = 0
                    self.card_order[1] += 1
                    self.main_game.button_option.reset()
                elif self.main_game.button_option.option // 100000 == 2:
                    self.card_order[1] += 2
                    self.main_game.button_option.reset()
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information and self.card_order[3]:
                if self.card_order[5]:
                    self.card_order[4] += 1
                    self.card_order[5] -= 1
                elif self.card_order[4] % 2:
                    if self.main_game.playerdeck_area.player_deck:
                        card = self.main_game.playerdeck_area.player_deck.pop(0)
                        self.main_game.hand_area.card_group[card] = None
                        self.main_game.information = [0, "玩家补卡后", self, card]
                    self.card_order[4] += 1
                else:
                    if self.card_order[4] < 3 and self.main_game.playerdeck_area.player_deck:
                        self.main_game.information = [0, "玩家将要补卡", self]
                        self.card_order[4] += 1
                    else:
                        self.card_order[3] = False
                        self.card_order[4] = 0
                        self.card_order[5] = 0
                        self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
