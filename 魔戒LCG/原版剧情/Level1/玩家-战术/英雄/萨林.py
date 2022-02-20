from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "萨林.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "萨林"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 9  # 英雄的初始威胁值
        self.willpower = 1  # 英雄的意志力
        self.attack_force = 2  # 英雄的攻击力
        self.defense_force = 2  # 英雄的防御力
        self.health_point = 4  # 英雄的生命值
        self.resource_symbol = "战术"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("矮人", "战士")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("永久",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "当萨林被指派执行任务时，对每个刚从遭遇牌组展示的敌军造成1点伤害。"

        # 剧情描述的斜体文字
        self.describe_text = "铁锤击打铁砧忙，凿刻工匠手艺强；炉火中铸刀，精工来装鞘，矿工挖坑，石匠建造。 ——《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and "任务中" in self.active_condition and self.main_game.information and \
                self.main_game.information[1] == "遭遇卡牌将要展示" and self.main_game.information[
            3].card_type == "敌军" and "免疫" not in self.main_game.information[3].rule_mark and str(
            self) not in self.main_game.information:
            if self.main_game.information[2] != "order":
                self.pause_card = self.main_game.information[2]
                self.pause_card_order = self.main_game.information[2].card_order
                self.main_game.information[2].card_order = [None, -1, 0, None, -1, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["执行卡牌效果", 0, 0, False, 0, 0]

    # 执行这张卡片的展示后效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "执行卡牌效果" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要攻击", self, self.copy_information[3]]
                self.card_order[1] += 1
        elif self.card_order[0] == "执行卡牌效果" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.copy_information[3].active_health_point -= 1
                if self.copy_information[3].active_health_point < 0:
                    self.copy_information[3].active_health_point = 0
                self.copy_information[3].update_mask()
                self.main_game.information = [0, "英雄卡牌攻击后", self, self.copy_information[3]]
                self.card_order[1] += 1
        elif self.card_order[0] == "执行卡牌效果" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and not self.main_game.response_conflict:
                if self.pause_card:
                    self.pause_card.card_order = self.pause_card_order
                    self.pause_card = None
                    self.pause_card_order = None
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.card_order = [None, 0, 0, None, 0, 0]

                if not self.main_game.information[3].active_health_point:
                    self.main_game.encounter_area.encounter_deck.remove(self.main_game.information[3])
                    if self.main_game.information[3].victory_points:
                        if self.main_game.threat_area.victory_point_deck:
                            self.main_game.threat_area.victory_point_deck.insert(0, self.main_game.information[3])
                        else:
                            self.main_game.threat_area.victory_point_deck = [self.main_game.information[3]]
                    else:
                        if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                            self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0,
                                                                                              self.main_game.information[
                                                                                                  3])
                        else:
                            self.main_game.encounterdiscard_area.encounterdiscard_deck = [self.main_game.information[3]]
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
