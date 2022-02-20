from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "多尔哥多戒灵.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (1, 1, 1)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "多尔哥多戒灵"  # 这张卡的名称
        self.clash_value = 40  # 这张卡的交锋值
        self.threat_force = 5  # 这张卡的威胁力
        self.attack_force = 4  # 这张卡的攻击力
        self.defense_force = 3  # 这张卡的防御力
        self.health_point = 9  # 这张卡的生命值
        self.encounter_symbol = "塔楼"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("戒灵",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("不受附属", "强制", "强制")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "不能打出附属牌到多尔哥多戒灵上。\n强制：当囚犯被“解救”时，将多尔哥多戒灵移至场景区。\n强制：在分配给多尔哥多戒灵的暗影效果结算后，与其交锋的玩家必须选择并弃除一名他控制的角色。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = ""

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息
