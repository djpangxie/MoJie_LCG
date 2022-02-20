from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "东口.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (2, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "东口"  # 这张卡的名称
        self.threat_force = 1  # 这张卡的威胁力
        self.task_point = 6  # 任务点，表示探索完该地区需要的进度标记数量
        self.encounter_symbol = "爪印"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("荒原",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("永久",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "地区"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "当决定是否探索地区时，如果没有激活的地区，玩家必须探索东口。"

        # 剧情描述的斜体文字
        self.describe_text = "“...东方的大地一片荒芜，布满了索伦的爪牙...” ——哈尔达，《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if not self.main_game.task_area.region_card and self.main_game.information and self.main_game.information[
            1] == "进入探索阶段后" and self.main_game.information[2] == "order" and str(
            self) not in self.main_game.information and self in self.main_game.scenario_area.card_group:
            self.main_game.information.append(str(self))
            self.card_order = ["探索", 0, 0, False, 0, 0]
