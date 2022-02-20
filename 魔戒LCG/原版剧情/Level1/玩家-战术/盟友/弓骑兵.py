from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "弓骑兵.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "弓骑兵"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 3  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "战术"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.willpower = 0  # 卡牌的意志力
        self.attack_force = 2  # 卡牌的攻击力
        self.defense_force = 1  # 卡牌的防御力
        self.health_point = 2  # 卡牌的生命值
        self.card_attribute = ("洛汗", "弓箭手")  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ("远攻",)  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ()  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "盟友"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "远攻."

        # 剧情描述的斜体文字
        self.describe_text = "马队中似乎有几名弓箭手，十分擅长在急驰的马背上射击。 ——《双城奇谋》"

        super().__init__()  # 初始化基类中的各种属性位置信息
